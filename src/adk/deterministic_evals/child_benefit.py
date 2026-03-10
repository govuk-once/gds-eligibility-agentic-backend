import json
from pathlib import Path
import sys


def evaluate_test_case(test_case_data: dict, eligibility_agent_tool_call: dict) -> dict:
    """
    Deterministically grades the agent's output and structures a JSON report,
    leaving room for future LLM-based reasoning evaluation.
    """
    case_id = test_case_data["case_id"]
    id_to_name = {
        child["id"]["value"]: child["name"]["value"] 
        for child in test_case_data["facts"]["children"]["value"]
    }
    expected_data = {}
    for result in test_case_data["expected_eligibility"]:
        name = id_to_name[result["child_id"]]
        expected_data[name] = {"eligible": result["eligible"]}

    # Rebuild the expected object structure gracefully
    # because a change in the tool calling has changed the structure
    # so we need to zip it manually if this isn't done
    actual_data = {}
    
    # CASE 1: The payload is from an old run (Function Response) and is already zipped
    if "child_evaluations" in eligibility_agent_tool_call:
        actual_data = {
            eval_obj["child_name"].lower(): eval_obj
            for eval_obj in eligibility_agent_tool_call["child_evaluations"]
        }
        
    # CASE 2: The payload is from a new run (Function Call Arguments) and needs zipping
    elif "child_names" in eligibility_agent_tool_call:
        for name, is_eligible, reasoning in zip(
            eligibility_agent_tool_call.get("child_names", []),
            eligibility_agent_tool_call.get("is_eligible_list", []),
            eligibility_agent_tool_call.get("reasonings", [])
        ):
            actual_data[name.lower()] = {
                "child_name": name,
                "is_eligible": is_eligible,
                "reasoning": reasoning
            }

    case_report = {
        "case_id": case_id,
        "overall_is_correct": True,
        "structural_errors": [],
        "child_evaluations": {},
    }

    expected_keys = {name.lower() for name in expected_data.keys()}
    actual_keys = set(actual_data.keys())

    if expected_keys != actual_keys:
        case_report["overall_is_correct"] = False
        missing, invented = expected_keys - actual_keys, actual_keys - expected_keys
        error_msg = "Child mismatch."
        if missing:
            error_msg += f" Missing: {list(missing)}."
        if invented:
            error_msg += f" Invented: {list(invented)}."
        case_report["structural_errors"].append(error_msg)

    for name, expected in expected_data.items():
        actual = actual_data.get(name.lower())
        if not actual:
            case_report["child_evaluations"][name] = {
                "is_correct": False,
                "error": "Missing",
            }
            continue

        is_correct = expected["eligible"] == actual["is_eligible"]
        if not is_correct:
            case_report["overall_is_correct"] = False

        case_report["child_evaluations"][name] = {
            "expected_eligible": expected["eligible"],
            "actual_eligible": actual["is_eligible"],
            "is_correct": is_correct,
        }

    return case_report


def main(input_folder_path: str = None):
    """
    Evaluates test outputs. If no path is provided, automatically finds 
    and evaluates the most recent run. Saves summary and detailed JSONs.
    """
    base_dir = Path("../../../analysis/testOutputs/child_benefit/")
    
    # Determine target directory
    if input_folder_path:
        target_dir = Path(base_dir / input_folder_path)
    else:
        if not base_dir.exists():
            print(f"Base directory not found: {base_dir.resolve()}")
            sys.exit(1)
            
        # Get all subdirectories EXCEPT new eval_reports folder
        subdirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name != "eval_reports"]
        
        if not subdirs:
            print(f"No test run directories found in {base_dir.resolve()}")
            sys.exit(1)
            
        # Sort lexicographically and pick the latest
        # as they're all named things like 2026-03-04T08:55:32.859368__RepoCommit=3890395
        subdirs.sort(key=lambda x: x.name)
        target_dir = subdirs[-1]

    if not target_dir.exists():
        print(f"Target directory not found: {target_dir}")
        sys.exit(1)

    print(f"Running deterministic evaluation on: {target_dir.name} ...")

    evaluation_results = {}
    total_cases = 0
    passed_cases = 0

    run_config_metadata = {}

    # Initialize accumulators for our averages
    total_duration_seconds = 0.0
    total_urls_read = 0

    for json_file in target_dir.glob("*.conversation.json"):
        with json_file.open("r") as f:
            data = json.load(f)

        # Safely grab the meta block
        meta_block = data.get("meta", {})
        # I cleaned up the output format. This is only to deal with old formats.
        # If it's an old file, dive into 'conversation'. If it's a new file, just use meta_block.
        meta_content = meta_block.get("conversation", meta_block)
        # Extract the config from the meta dict
        # Everything in same folder has same metadata so we only need to do this once
        if not run_config_metadata:

            run_config_metadata = meta_content.get("run_config", {})            

        
        test_case_data = meta_content["test_case"]
        case_id = test_case_data["case_id"]
        total_cases += 1

        # Extract performance and tool calls
        duration = data.get("performance", {}).get("duration_seconds", 0.0)
        tool_activity = data.get("tool_activity", [])
        
        # Filter out just the web pages it read and grab the URLs
        urls_read = [
            activity.get("arguments", {}).get("url") 
            for activity in tool_activity 
            if activity.get("tool_name") == "read_webpage"
        ]

        # Add to our running totals
        total_duration_seconds += duration
        total_urls_read += len(urls_read)

        # Find the final judgement tool call in the activity log
        judgement_call = next(
            (
                activity 
                for activity in tool_activity 
                if activity.get("tool_name") in ["eligibility_judgement_outcome", "child_benefit_eligibility_agent_payload"]
            ), 
            None
        )

        # Guard against cases where the agent crashed or failed to call the tool
        if not judgement_call or "arguments" not in judgement_call:
            evaluation_results[case_id] = {
                "case_id": case_id,
                "overall_is_correct": False,
                "structural_errors": ["Fatal: No eligibility_judgement_outcome tool call found in transcript."],
                "child_evaluations": {},
                "duration_seconds": duration, # should be None but taking mean later so leave this for now
                "urls_read": urls_read
            }
            continue

        tool_call_payload = judgement_call["arguments"]

        report = evaluate_test_case(test_case_data, tool_call_payload)

        # Inject the metrics into the detailed case report
        report["duration_seconds"] = duration
        report["urls_read"] = urls_read
        report["total_tool_calls"] = len(tool_activity)

        evaluation_results[case_id] = report

        # Track high-level metrics
        if report.get("overall_is_correct", False):
            passed_cases += 1

    detailed_report_data = {
        "run_config": run_config_metadata,
        "results": evaluation_results
    }

    output_dir = base_dir / "eval_reports" / target_dir.name
    output_dir.mkdir(parents=True, exist_ok=True)
    cases_filepath = output_dir / "evaluation_report_cases.json"

    with cases_filepath.open("w") as f:
        json.dump(detailed_report_data, f, indent=4)

    # Calculate averages for the summary
    mean_duration = total_duration_seconds / total_cases if total_cases > 0 else 0
    mean_urls = total_urls_read / total_cases if total_cases > 0 else 0
    accuracy = (passed_cases / total_cases) if total_cases > 0 else 0
    summary_data = {
        "run_name": target_dir.name,
        "run_config": run_config_metadata,
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": total_cases - passed_cases,
        "accuracy": round(accuracy, 4),
        "mean_duration_seconds": round(mean_duration, 2),
        "mean_urls_read": round(mean_urls, 2)  
    }
    
    summary_filepath = output_dir / "evaluation_report_summary.json"
    with summary_filepath.open("w") as f:
        json.dump(summary_data, f, indent=4)

    # Print a concise summary to the console
    print("-" * 50)
    print("EVALUATION COMPLETE")
    print(f"Reports saved to: {output_dir.resolve()}")
    print("-" * 50)
    print(f"Total Cases : {total_cases}")
    print(f"Passed      : {passed_cases}")
    print(f"Failed      : {total_cases - passed_cases}")
    if total_cases > 0:
        print(f"Accuracy    : {accuracy:.4f}%")
        print(f"Avg Duration   : {mean_duration:.2f}s")
        print(f"Avg URLs Read  : {mean_urls:.2f}")

if __name__ == "__main__":
    # If a path is passed use it. Otherwise, default to auto-find latest.
    target_path = sys.argv[1] if len(sys.argv) > 1 else None
    main(target_path)