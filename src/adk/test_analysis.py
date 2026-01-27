#!/usr/bin/env ipython
from collections import defaultdict
import re
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns


failure_dfs = {}
success_dfs = {}
combined_dfs = {}
combined_dfs_raw = {}
success_rates_by_permutations = {}
success_rates_by_permutation_model_sizes = {}
large_model_improvement_by_permutations = {}
eligibility_dfs = {}
success_rates_by_eligibilitys = {}
success_rates_by_eligibility_model_size = {}


def invert_mapping(dictionary: dict) -> dict:
    return {elem: k for k, v in dictionary.items() for elem in v}

figure_annotations = {
    "child_benefit": {
        "success_rates_by_permutation_model_size.hist": {
            "title": "Accuracy of agent (according to judge) for child benefit",
            "ylabel": "Count",
            "xlabel": "Percentage correctness over all executions"
        },
        "success_rates_by_permutation_model_size.improvement.hist": {
            "title": "Difference in judged accuracy with varying model size for child benefit",
            "ylabel": "Count of permutations",
            "xlabel": "Large model accuracy % minus small model accuracy % for a given permutation",
        },
        "success_rates_by_eligibility.hist": {
            "ylabel": "Count of permutations",
            "xlabel": "Model Accuracy %"
        },
        "success_rates_by_eligibility.modelSize": {
            "ylabel": "Model Size",
            "xlabel": "Eligibility Category",
            "title": "Average judged accuracy for model size and eligibility category",
        },
    },
    "skilled_worker_visa": {
        "success_rates_by_permutation_model_size.hist": {
            "title": "Accuracy of agent (according to judge) for skilled worker visa",
            "ylabel": "Count",
            "xlabel": "Percentage correctness over all executions"
        },
        "success_rates_by_permutation_model_size.improvement.hist": {
            "title": "Difference in judged accuracy with varying model size for skilled worker visa",
            "ylabel": "Count of permutations",
            "xlabel": "Large model accuracy % minus small model accuracy % for a given permutation",
        },
        "success_rates_by_eligibility.hist": {
            "ylabel": "Count of permutations",
            "xlabel": "Model Accuracy %"
        },
        "success_rates_by_eligibility.modelSize": {
            "ylabel": "Model Size",
            "xlabel": "Eligibility Category",
            "title": "Average judged accuracy for model size and eligibility category",
        },
    },
    "child_benefit__stressTestAgent": {
        "success_rates_by_permutation_model_size.hist": {
            "title": "Accuracy of agent (according to judge) for child benefit",
            "ylabel": "Count",
            "xlabel": "Percentage correctness over all executions"
        },
        "success_rates_by_permutation_model_size.improvement.hist": {
            "title": "Difference in judged accuracy with varying model size for child benefit",
            "ylabel": "Count of permutations",
            "xlabel": "Large model accuracy % minus small model accuracy % for a given permutation",
        },
        "success_rates_by_eligibility.hist": {
            "ylabel": "Count of permutations",
            "xlabel": "Model Accuracy %"
        },
        "success_rates_by_eligibility.modelSize": {
            "ylabel": "Model Size",
            "xlabel": "Eligibility Category",
            "title": "Average judged accuracy for model size and eligibility category",
        },
    },
}

model_sizes_hypothesis_mapping = {
    "child_benefit": {"baseline": "gemma4B", "improved": "gemma27B"},
    "skilled_worker_visa": {"baseline": "gemma4B", "improved": "gemma27B"},
    #"child_benefit__stressTestAgent": {"baseline": "gemma27B", "improved": "claude37Sonnet"},
    "child_benefit__stressTestAgent": {"baseline": "claude37Sonnet", "improved": "claude37SonnetOriginalPrompt"},
}

model_size_commit_mapping = {
    "child_benefit": invert_mapping({
        "gemma4B": ["Unknown", "fc922c5", "9493282", "f2dc127"],
        "gemma27B": ["575b5e9"],
    }),
    "skilled_worker_visa": invert_mapping({
        "gemma4B": ["Unknown", "db37bc9", "df1795d", "71b1d7c"], 
        "gemma27B": ["8ed3c90"]
    }),
    "child_benefit__stressTestAgent": invert_mapping({
        "gemma27B": ["1012a61", "976499a", "74e8834"], 
        "claude37Sonnet": ["e680f99"],
        "claude37SonnetOriginalPrompt": ["21506e4"]
    }),
    #defaultdict(lambda: "large"),
}


def extract_results_for_folder(output_dir, search_character) -> pd.DataFrame:
    print(output_dir)
    extracted_records = []
    output = subprocess.run(
        ["rg", search_character, "--hidden"],
        capture_output=True,
        check=False,
        text=True,
        cwd=output_dir,
    )
    for filename in output.stdout.strip().split("\n"):
        if filename:
            with_commit = (
                r"(?P<exec_time>[\d:T\.-]+)__RepoCommit=(?P<commit>[a-f0-9]+)/Permutation(?P<permutation>\d+).*"
                #  + ur":\[evaluation_judge\]: "
                + search_character + r"(?P<reasoning>.*)"
            )
            if re.match(
                with_commit,
                filename,
                re.UNICODE
            ):
                extracted_fields = re.search(
                    with_commit,
                    filename,
                    re.UNICODE
                ).groupdict()
            else:
                without_commit = (
                    r"(?P<exec_time>[\d:T\.-]+)/Permutation(?P<permutation>\d+).out.*"
                    #  + ur":\[evaluation_judge\]: "
                    + search_character + r"(?P<reasoning>.*)"
                )
                extracted_fields = re.search(
                    without_commit,
                    filename,
                    re.UNICODE
                ).groupdict()
            extracted_fields["permutation"] = int(extracted_fields["permutation"])
            extracted_fields["reasoning"] = str(extracted_fields["reasoning"])
            extracted_records.append(extracted_fields)
    return pd.DataFrame.from_records(extracted_records)


def load_and_parse_test_cases(test_cohort: str) -> list[str]:
    test_case_file = Path(f"../../prompts/manual/test_cases/").joinpath(test_cohort.split("__")[0] + ".md")
    with test_case_file.open() as f:
        raw_test_cases = f.readlines()
    test_cases_str = "\n".join(raw_test_cases)
    test_cases = test_cases_str.split(sep="---")
    return test_cases


def extract_test_cases_for_test_cohort(test_cohort) -> pd.DataFrame:
    test_cases = load_and_parse_test_cases(test_cohort)
    extracted_records = []
    for test_case in test_cases:
        parsed_test_case = list(filter(len, test_case.split("\n")))
        extracted_records.append(
            dict(
                permutation=extract_permutation_number_from_test_case(parsed_test_case),
                #  "eligible": extract_eligibility_from_test_case(parsed_test_case),
                **extract_eligibility_from_test_case(parsed_test_case),
            )
        )
    return pd.DataFrame.from_records(extracted_records, index="permutation")


def extract_eligibility_from_test_case(test_case):
    outcome = test_case[-1]
    assert "**Outcome:**" in outcome, outcome
    #  assert outcome.count("Eligible") == 1, outcome

    return {
        "not_eligible": bool(outcome.count("Not Eligible")),
        # If we find the words Eligible outside of the string "Not Eligible" (as the former is a substring of the latter we can just subtract occurrences) then we know the results is partial eligibility
        "eligible": bool(outcome.count("Eligible") - outcome.count("Not Eligible")),
    }


def extract_permutation_number_from_test_case(test_case):
    permutation = test_case[0]
    p_match = re.search(r"Permutation (?P<permutation_number>[\d]+):", permutation)
    assert p_match and len(p_match.groups()) == 1
    return int(p_match.groups()[0])


def get_eligibility_case(row):
    match (row["eligible"], row["not_eligible"]):
        case (True, True):
            return "Both"
        case (True, False):
            return "Eligible"
        case (False, True):
            return "NotEligible"


def load_failure_df(output_dir, test_cohort) -> pd.DataFrame:
    #  print('failures:')
    df = extract_results_for_folder(output_dir, "✗")
    df["Passed"] = False
    if len(df) > 0:
        df["commit"].fillna("Unknown", inplace=True)
    df.set_index(["commit", "exec_time", "permutation"], inplace=True)
    df["ModelSize"] = df.index.get_level_values(0).map(
        model_size_commit_mapping[test_cohort]
    )
    #  print(df.value_counts(["permutation", "ModelSize"]))
    return df


def load_success_df(output_dir, test_cohort) -> pd.DataFrame:
    #  print('successes:')
    df = extract_results_for_folder(output_dir, "✓")
    df["Passed"] = True
    if len(df) > 0:
        df["commit"].fillna("Unknown", inplace=True)
    df.set_index(["commit", "exec_time", "permutation"], inplace=True)
    df["ModelSize"] = df.index.get_level_values(0).map(
        model_size_commit_mapping[test_cohort]
    )
    #  print(df.value_counts(["permutation", "ModelSize"]))
    return df


def get_success_rates_by_permutation(combined_df: pd.DataFrame) -> pd.DataFrame:
    df = (
        100
        * combined_df[combined_df["Passed"] == True]
        .index.get_level_values(2)
        .value_counts()
        / combined_df.index.get_level_values(2).value_counts()
    )
    print(df.nsmallest(n=15))
    return df


def get_success_rates_by_permutation_model_size(combined_df: pd.DataFrame, test_cohort) -> pd.DataFrame:
    df = (
        100
        * combined_df[combined_df["Passed"] == True]
        .index.droplevel(0)
        .droplevel(0)
        .value_counts()
        / combined_df.index.droplevel(0).droplevel(0).value_counts()
    )
    print(df.nsmallest(n=15))
    print(df.reset_index().set_index("permutation").value_counts())

    fig_name = "success_rates_by_permutation_model_size.hist"
    fig = plt.figure(f"hist_{test_cohort}")
    fig.clear()
    ax = sns.histplot(
        df.reset_index(),
        x="count",
        hue="ModelSize",
        multiple="dodge",
        shrink=0.7,
        bins=20,
        common_bins=True,
    )
    ax.set_title(
        figure_annotations[test_cohort][fig_name]["title"]
    )
    ax.set_ylabel(figure_annotations[test_cohort][fig_name]["ylabel"])
    ax.set_xlabel(figure_annotations[test_cohort][fig_name]["xlabel"])
    fig.savefig(f"{fig_name}.{test_cohort}.png")

    return df


def get_large_model_improvements_by_permutation(
    combined_df_raw: pd.DataFrame,
    test_cohort
) -> pd.DataFrame:
    df = (
        combined_df_raw[
            (combined_df_raw["Passed"] == True)
            & (combined_df_raw["ModelSize"] == model_sizes_hypothesis_mapping[test_cohort]["improved"])
        ]
        .index.get_level_values(2)
        .value_counts()
        / combined_df_raw[(combined_df_raw["ModelSize"] == model_sizes_hypothesis_mapping[test_cohort]["improved"])]
        .index.get_level_values(2)
        .value_counts()
    ) - (
        combined_df_raw[
            (combined_df_raw["Passed"] == True)
            & (combined_df_raw["ModelSize"] == model_sizes_hypothesis_mapping[test_cohort]["baseline"])
        ]
        .index.get_level_values(2)
        .value_counts()
        / combined_df_raw[(combined_df_raw["ModelSize"] == model_sizes_hypothesis_mapping[test_cohort]["baseline"])]
        .index.get_level_values(2)
        .value_counts()
    )

    fig_name = "success_rates_by_permutation_model_size.improvement.hist"
    fig = plt.figure(f"improvement_{test_cohort}")
    fig.clear()
    df.hist()
    ax = fig.get_axes()[0]
    ax.set_title(
        figure_annotations[test_cohort][fig_name]["title"]
    )
    ax.set_ylabel(figure_annotations[test_cohort][fig_name]["ylabel"])
    ax.set_xlabel(
        figure_annotations[test_cohort][fig_name]["xlabel"]
    )
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    fig.savefig(
        f"{fig_name}.{test_cohort}.png"
    )
    print(df.value_counts())
    return df


def get_success_rates_by_eligibility(
    success_rates_by_permutation: pd.DataFrame,
    eligibility_df: pd.DataFrame,
    test_cohort,
) -> pd.DataFrame:
    fig_name = "success_rates_by_eligibility.hist"
    fig = plt.figure(f"eligibility_{test_cohort}")
    fig.clear()
    df = eligibility_df.join(success_rates_by_permutation)
    df["eligibility_cat"] = df.apply(get_eligibility_case, axis=1)

    #  df = df.set_index(["eligible", "not_eligible"], append=True)
    #  df.hist()

    ax = sns.histplot(
        df,
        x="count",
        hue="eligibility_cat",
        multiple="dodge",
        shrink=0.7,
        bins=20,
        common_bins=True,
    )
    ax.set_ylabel(figure_annotations[test_cohort][fig_name]["ylabel"])
    ax.set_xlabel(figure_annotations[test_cohort][fig_name]["xlabel"])
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(100.0))

    fig.savefig(f"{fig_name}.{test_cohort}.png")
    return df


def get_success_rates_by_eligibility_model_size(
    success_rates_by_permutation_model_size: pd.DataFrame,
    eligibility_df: pd.DataFrame,
    test_cohort,
) -> pd.DataFrame:
    fig_name = "success_rates_by_eligibility.modelSize"
    fig = plt.figure(f"confusion_{test_cohort}")
    fig.clear()
    df = eligibility_df.join(success_rates_by_permutation_model_size)
    df["eligibility_cat"] = df.apply(get_eligibility_case, axis=1)

    df = df.reset_index().groupby(["eligibility_cat", "ModelSize"], axis=0).mean("count")

    ax = sns.heatmap(
        df.reset_index().pivot(index="ModelSize", columns="eligibility_cat", values="count"),
        annot=True,
        fmt=".1f"
    )

    ax.set_ylabel(figure_annotations[test_cohort][fig_name]["ylabel"])
    ax.set_xlabel(figure_annotations[test_cohort][fig_name]["xlabel"])
    #  ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(100.0))
    ax.set_title(
        figure_annotations[test_cohort][fig_name]["title"]
    )

    fig.savefig(f"{fig_name}.{test_cohort}.png")
    return df


def main(argv):
    if len(argv) > 1:
        output_dir = Path(".testOutputs").joinpath(argv[1])
        assert output_dir.exists()
        analyse_cohort(output_dir)
    else:
        for output_dir in Path(".testOutputs").glob("*"):
            analyse_cohort(output_dir)


def analyse_cohort(output_dir: Path):
    test_cohort = str(output_dir.relative_to(".testOutputs"))
    failure_dfs[test_cohort] = load_failure_df(output_dir, test_cohort)
    success_dfs[test_cohort] = load_success_df(output_dir, test_cohort)
    combined_dfs_raw[test_cohort] = pd.concat(
        [success_dfs[test_cohort], failure_dfs[test_cohort]],
    )
    if output_dir.name.startswith("child_benefit"):
        eligibility_dfs[test_cohort] = extract_test_cases_for_test_cohort(
            test_cohort
        )
        combined_dfs_raw[test_cohort] = combined_dfs_raw[test_cohort].join(
            eligibility_dfs[test_cohort], on="permutation"
        )

    # Assume that we only want to include data from the baseline and improved commit sets, and any other results should be excluded
    combined_dfs_raw[test_cohort] = combined_dfs_raw[test_cohort][
        combined_dfs_raw[test_cohort]["ModelSize"].isin(
            list(model_sizes_hypothesis_mapping[test_cohort].values())
        )
    ]
    combined_dfs[test_cohort] = combined_dfs_raw[test_cohort].set_index(
        ["ModelSize"], append=True
    )
    print(combined_dfs[test_cohort].value_counts(["Passed", "ModelSize"]))
    print(
        combined_dfs[test_cohort].value_counts(
            ["ModelSize", "permutation"], ascending=True
        )
    )
    success_rates_by_permutations[test_cohort] = get_success_rates_by_permutation(
        combined_dfs[test_cohort]
    )
    success_rates_by_permutation_model_sizes[test_cohort] = (
        get_success_rates_by_permutation_model_size(
            combined_dfs[test_cohort], test_cohort
        )
    )
    large_model_improvement_by_permutations[test_cohort] = (
        get_large_model_improvements_by_permutation(
            combined_dfs_raw[test_cohort], test_cohort
        )
    )
    if output_dir.name.startswith("child_benefit"):
        print(
            combined_dfs_raw[test_cohort].value_counts(
                ["Passed", "eligible", "not_eligible"]
            )
        )
        success_rates_by_eligibilitys[test_cohort] = get_success_rates_by_eligibility(
            success_rates_by_permutations[test_cohort],
            eligibility_dfs[test_cohort],
            test_cohort,
        )
        success_rates_by_eligibility_model_size[test_cohort] = get_success_rates_by_eligibility_model_size(
            success_rates_by_permutation_model_sizes[test_cohort],
            eligibility_dfs[test_cohort],
            test_cohort,
        )
        combined_dfs[test_cohort]["correct_outcome"] = combined_dfs[test_cohort]["reasoning"].str.contains(r"The agent (?:\w+ |\w+ the )?correct", regex=True)


if __name__ == "__main__":
    main(sys.argv)
