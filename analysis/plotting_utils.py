import re
import pandas as pd
from IPython.display import display
from pathlib import Path
import json

# This is where we'll want to add something like "Structured rules"
PROMPT_MAPPING = {
    "Accuracy-ChildBenefit-structuredOutput-v2.md": "Rules in URLs",
    "Accuracy-ChildBenefit-structuredOutput-v2.1_no_links.md": "Training data only",
    "Accuracy-ChildBenefit-structuredOutput-v2.2_no_links_rules_in_prompt.md": "Rules in prompt",
    "StructuredSpecification-ChildBenefit-v1.md" : "Structured spec"
}


def get_short_model_name(model_string: str) -> str:
    """
    Quick and dirty way to get a human-readable model name with no regex.
    So "bedrock/converse/eu.anthropic.claude-sonnet-4-5-20250929-v1:0" -> "claude-sonnet-4-5"
    """
    base_name = model_string.split("/")[-1].split(".")[-1]
    clean_parts = []

    for part in base_name.split("-"):
        # Stop if we hit an 8-digit date (e.g., 20250929)
        if len(part) == 8 and part.isdigit():
            break

        # Stop if we hit a version tag (starts with 'v' followed by a number, e.g., v1:0)
        if part.startswith("v") and part[1:2].isdigit():
            break

        clean_parts.append(part)
    # Stitch it back together
    return "-".join(clean_parts)

def extract_prompt_version(prompt_name: str) -> str:
    match = re.search(r"v\d+(?:\.\d+)?", str(prompt_name))
    return match.group(0) if match else "v?"

def get_nice_prompt_name(prompt_string: str, prompt_mapping: dict) -> str:
    if not isinstance(prompt_string, str):
        return "Unknown"
    file_name = prompt_string.split("/")[-1]
    return (file_name, prompt_mapping.get(file_name, "Other Prompt"))


def create_df_runs(
    test_cohort: str = "child_benefit", drop_unknown_prompt: bool = True
) -> pd.DataFrame:
    reports_dir = Path(f"testOutputs/{test_cohort}/eval_reports")
    run_data = []
    for run_dir in reports_dir.iterdir():
        if not run_dir.is_dir():
            continue

        summary_path = run_dir / "evaluation_report_summary.json"
        cases_path = run_dir / "evaluation_report_cases.json"

        if summary_path.exists() and cases_path.exists():
            with open(summary_path, "r") as f:
                summary = json.load(f)
            with open(cases_path, "r") as f:
                cases = json.load(f)

            config = summary.get("run_config", {})

            run_data.append(
                {
                    "run_name": run_dir.name,
                    "model": config.get("eligibility_model_string", "unknown"),
                    "prompt": config.get("eligibility_prompt", "unknown"),
                    "url_allowed": config.get("url_tool_call_allowed", True),
                    "commit": config.get("commit", "unknown"),
                    "results": cases.get(
                        "results", cases
                    ),  # Handles nested (old style) or flat cases dict
                }
            )

    df_runs = pd.DataFrame(run_data)

    # From before we recorded the prompt in this way and have different shaped output
    if drop_unknown_prompt:
        df_runs = (df_runs[df_runs["prompt"] != "unknown"]).reset_index()

    # Create some slightly shorter/nicer names for plotting/tables
    df_runs[["prompt_name", "prompt_type"]] = (
        df_runs["prompt"]
        .apply(lambda p: get_nice_prompt_name(p, PROMPT_MAPPING))
        .apply(pd.Series)
    )
    df_runs["model_name"] = df_runs["model"].apply(get_short_model_name)

    df_runs["config_key"] = df_runs.apply(
        lambda x: (x["model_name"], x["prompt_name"], x["url_allowed"]), axis=1
    )

    df_runs["prompt_version"] = df_runs["prompt_name"].apply(extract_prompt_version)

    # Can't plot full prompt name - it breaks the axes
    df_runs["config_label"] = (
        df_runs["model_name"]
        + " | "
        + df_runs["prompt_type"]
       # + " | "
        #+ df_runs["url_allowed"].map({True: "URLs ON", False: "URLs OFF"})
    )
    print("df_runs created and its head looks like this:")
    display(df_runs.head())

    print("Configurations found and their run counts:")
    display(df_runs["config_key"].value_counts().to_frame("Count"))

    return df_runs
