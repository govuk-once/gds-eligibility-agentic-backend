import re
import json
from collections.abc import Mapping
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import pandas as pd
from IPython.display import display
from pathlib import Path

# This is where we'll want to add something like "Structured rules"
PROMPT_MAPPING = {
    "Accuracy-ChildBenefit-structuredOutput-v2.md": "Rules via URLs",
    "Accuracy-ChildBenefit-structuredOutput-v2.1_no_links.md": "Training data only",
    "Accuracy-ChildBenefit-structuredOutput-v2.2_no_links_rules_in_prompt.md": "Free text rules",
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


def get_nice_prompt_name(prompt_string: str, prompt_mapping: dict[str, Any]) -> tuple[str, Any]:
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


def apply_presentation_theme(
    fig: plt.Figure,
    *,
    bg_color: str = "#F8F8F8",
    text_color: str = "#111111",
    grid_color: str = "#D0D0D0",
    rounded: bool = True,
    corner_radius: float = 0.03,
    add_panel: bool = True,
    panel_pad: float = 0.008,
    panel_edgecolor: str | None = None,
    panel_linewidth: float = 0.0,
) -> plt.Figure:
    """
    Apply a presentation-style theme to an existing matplotlib figure.

    Parameters
    ----------
    fig
        Existing matplotlib figure.
    bg_color
        Main background colour for the figure and axes.
    text_color
        Colour for titles, labels, ticks, and visible spines.
    grid_color
        Colour for grid lines.
    rounded
        If True, clip axes backgrounds to rounded corners.
    corner_radius
        Rounded corner size in figure coordinates. Values around 0.02-0.04
        usually work well.
    add_panel
        If True, draw a rounded panel behind each axes.
    panel_pad
        Padding around each axes panel in figure coordinates.
    panel_edgecolor
        Optional border colour for the rounded panel.
    panel_linewidth
        Border width for the rounded panel.

    Returns
    -------
    plt.Figure
        The themed figure.
    """
    fig.patch.set_facecolor(bg_color)

    for ax in fig.axes:
        # Base axes styling
        ax.set_facecolor(bg_color)

        ax.title.set_color(text_color)
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)

        ax.tick_params(axis="both", colors=text_color)

        # Spines
        for spine in ax.spines.values():
            spine.set_color(text_color)
            spine.set_linewidth(1.0)

        # Grid
        ax.grid(True, color=grid_color, linewidth=0.8, alpha=0.6)
        ax.set_axisbelow(True)

        # Legend
        legend = ax.get_legend()
        if legend is not None:
            legend.get_frame().set_facecolor(bg_color)
            legend.get_frame().set_edgecolor("none")
            for text in legend.get_texts():
                text.set_color(text_color)

        # Rounded panel behind axes
        if add_panel:
            pos = ax.get_position()
            panel = FancyBboxPatch(
                (pos.x0 - panel_pad, pos.y0 - panel_pad),
                pos.width + 2 * panel_pad,
                pos.height + 2 * panel_pad,
                boxstyle=f"round,pad=0,rounding_size={corner_radius}",
                transform=fig.transFigure,
                facecolor=bg_color,
                edgecolor=panel_edgecolor if panel_edgecolor else "none",
                linewidth=panel_linewidth,
                zorder=-10,
            )
            fig.patches.append(panel)

        # Rounded clipping of the axes area itself
        if rounded:
            rounded_patch = FancyBboxPatch(
                (0, 0),
                1,
                1,
                boxstyle=f"round,pad=0,rounding_size={corner_radius}",
                transform=ax.transAxes,
                facecolor=bg_color,
                edgecolor="none",
            )
            ax.patch = rounded_patch

    return fig


def flatten_run_row_children(row) -> list[dict[str, Any]]:
    """
    Extracts data at the child-level.
    A case with 3 children will return 3 dictionaries.
    """
    run_name = row.run_name
    timestamp_str = run_name.split("__")[0]

    model_string = str(row.model)
    if model_string.lower() == "unknown":
        return []

    results = row.results
    if not isinstance(results, Mapping):
        return []

    output = []

    for case_id, case_data in results.items():
        if case_id == "run_config":
            continue

        duration = case_data.get("duration_seconds")
        if duration is None:
            continue

        # Grab the child_evaluations dictionary (defaulting to an empty dict if missing)
        child_results = case_data.get("child_evaluations", {})

        # Handle if the evaluator stores children as a list of dictionaries
        if isinstance(child_results, list):
            for child in child_results:
                output.append(
                    {
                        "run_name": run_name,
                        "timestamp": pd.to_datetime(timestamp_str),
                        "config_label": row.config_label,
                        "case_id": case_id,
                        "child_id": child.get("child_id", child.get("name", "unknown")),
                        "child_is_correct": int(child.get("is_correct", False)),
                        "duration": float(duration),
                    }
                )

        # Handle if the evaluator stores children as a dictionary {child_id: {data}}
        elif isinstance(child_results, dict):
            for child_id, child_data in child_results.items():
                output.append(
                    {
                        "run_name": run_name,
                        "timestamp": pd.to_datetime(timestamp_str),
                        "config_label": row.config_label,
                        "case_id": case_id,
                        "child_id": child_id,  # e.g., "Alex", "Blake"
                        "child_is_correct": int(child_data.get("is_correct", False)),
                        "duration": float(duration),
                    }
                )

    return output


def flatten_runs_to_children(df_runs: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a DataFrame where every row is an individual child's evaluation.
    """
    flat_data = [
        record
        for row in df_runs.itertuples(index=False)
        for record in flatten_run_row_children(row)
    ]

    return pd.DataFrame(flat_data)
