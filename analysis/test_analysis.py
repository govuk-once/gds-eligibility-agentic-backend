#!/usr/bin/env ipython

# TODO
# * [ ] Figure out what to do about issues like testOutputs/child_benefit__stressTestAgent/2026-01-28T20:31:36.660804__RepoCommit=10c6f19/Permutation46__rejudgement_2026-01-30T09:44:40.892615
# * [x] Move this file and graphs out into a top level `analysis` folder
# * [ ] Add docstrings
# * [ ] Move to ipython notebook
# * [x] (stretch goal) Move testOutputs out to top level folder, and update transcription and analysis functionality accordingly

from collections import defaultdict
import re
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from matplotlib_venn import venn3, venn2

success_column = "Passed"
#success_column = "RejudgementPassed"
#success_column = "ConsensusPassed"


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
            "title": "Difference in judged accuracy with varying actor prompt for child benefit",
            "ylabel": "Count of permutations",
            "xlabel": "Helpful Actor accuracy % minus Realistic Actor accuracy % for a given permutation",
        },
        "success_rates_by_eligibility.hist": {
            "ylabel": "Count of permutations",
            "xlabel": "Accuracy %"
        },
        "success_rates_by_eligibility.modelSize": {
            "ylabel": "Actor",
            "xlabel": "Eligibility Category",
            "title": "Average judged accuracy for Actor Prompt and Eligibility Category",
        },
    },
}

model_sizes_hypothesis_mapping = {
    "child_benefit": {"baseline": "gemma4B", "improved": "gemma27B"},
    "skilled_worker_visa": {"baseline": "gemma4B", "improved": "gemma27B"},
    #"child_benefit__stressTestAgent": {"baseline": "gemma27B", "improved": "claude37Sonnet"},
    #"child_benefit__stressTestAgent": {"baseline": "claude37Sonnet__Realistic", "improved": "claude37Sonnet__Helpful"},
    #"child_benefit__stressTestAgent": {"baseline": "claude45Sonnet__Realistic", "improved": "claude45Sonnet__Helpful"},
    "child_benefit__stressTestAgent": {"baseline": "Realistic", "improved": "Helpful"},
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
        "claude37SonnetOriginalPrompt": ["21506e4"],
        #"claude45Sonnet__Realistic": ["10c6f19"],
        #"claude45Sonnet__Helpful": ["d6dfd9f"],
        "Realistic": ["10c6f19"],
        "Helpful": ["d6dfd9f"],
    }),
    #defaultdict(lambda: "large"),
}

# TODO extract this from model_sizes_hypothesis mapping and model_sizes_commit_mapping
commits_to_filter = {
    "child_benefit__stressTestAgent": ["10c6f19", "d6dfd9f"],
    #"skilled_worker_visa": ["Unknown", "db37bc9", "df1795d", "71b1d7c", "8ed3c90"],
    #"child_benefit": ["Unknown", "fc922c5", "9493282", "f2dc127", "575b5e9"],
}

def extract_judgement_results_for_folder(output_dir, search_character) -> pd.DataFrame:
    #print(output_dir)
    extracted_records = []
    output = subprocess.run(
        [
            "rg", 
            search_character, 
            Path(os.getcwd()).joinpath(output_dir),
            "--hidden"
        ],
        capture_output=True,
        check=False,
        text=True,
        #cwd=output_dir,
    )
    #print(output.stderr)
    for filename in output.stdout.strip().split("\n"):
        if filename:
            with_commit = (
                r".*(?P<exec_time>[\d:T\.-]+)__RepoCommit=(?P<commit>[a-f0-9]+)/Permutation(?P<permutation>\d+)__rejudgement_(?P<rejudgement_time>[\d:T\.-]+).*"
                #  + ur":\[evaluation_judge\]: "
                + search_character + r"(?P<rejudgement_reasoning>.*)"
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
            extracted_fields["permutation"] = int(extracted_fields["permutation"])
            extracted_fields["rejudgement_reasoning"] = str(extracted_fields["rejudgement_reasoning"])
            extracted_records.append(extracted_fields)
    df = pd.DataFrame.from_records(
        extracted_records,
        columns=["exec_time", "commit", "permutation", "rejudgement_time", "rejudgement_reasoning"]
    )
    if "child_benefit__stressTestAgent" in str(output_dir): 
       df = df[df['commit'].isin(commits_to_filter[output_dir.name])]
    return df


def extract_results_for_folder(output_dir, search_character) -> pd.DataFrame:
    print(output_dir)
    extracted_records = []
    output = subprocess.run(
        [
            "rg", 
            search_character, 
            "--hidden",
            Path(os.getcwd()).joinpath(output_dir),
        ],
        capture_output=True,
        check=False,
        text=True,
        #cwd=output_dir,
    )
    for filename in output.stdout.strip().split("\n"):
        if filename:
            with_commit = (
                r".*(?P<exec_time>[\d:T\.-]+)__RepoCommit=(?P<commit>[a-f0-9]+)/Permutation(?P<permutation>\d+).*"
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
                    r".*(?P<exec_time>[\d:T\.-]+)/Permutation(?P<permutation>\d+).out.*"
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
    df = pd.DataFrame.from_records(
        extracted_records,
        columns=["exec_time", "commit", "permutation", "reasoning"]
    )
    if "child_benefit__stressTestAgent" in str(output_dir): 
       df = df[df['commit'].isin(commits_to_filter[output_dir.name])]
    return df


def load_and_parse_test_cases(test_cohort: str) -> list[str]:
    test_case_file = (
        Path("../") # Repository root
        .joinpath(f"prompts/manual/test_cases/")
        .joinpath(test_cohort.split("__")[0] + ".md")
    )
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

def load_disagree_judgements_df(output_dir, test_cohort) -> pd.DataFrame:
    df = extract_judgement_results_for_folder(output_dir, "☹")
    df["RejudgementAgree"] = False
    df.set_index(["commit", "exec_time", "permutation"], inplace=True)
    return df

def load_agree_judgements_df(output_dir, test_cohort) -> pd.DataFrame:
    df = extract_judgement_results_for_folder(output_dir, "☺")
    df["RejudgementAgree"] = True
    df.set_index(["commit", "exec_time", "permutation"], inplace=True)
    return df

def load_failed_judgements_df(output_dir, test_cohort) -> pd.DataFrame:
    df = extract_judgement_results_for_folder(output_dir, "👎")
    df["RejudgementPassed"] = False
    df.set_index(["commit", "exec_time", "permutation"], inplace=True)
    return df

def load_passed_judgements_df(output_dir, test_cohort) -> pd.DataFrame:
    df = extract_judgement_results_for_folder(output_dir, "👍")
    df["RejudgementPassed"] = True
    df.set_index(["commit", "exec_time", "permutation"], inplace=True)
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
        * combined_df[combined_df[success_column] == True]
        .index.get_level_values(2)
        .value_counts()
        / combined_df.index.get_level_values(2).value_counts()
    )
    print(df.nsmallest(n=15))
    return df


def get_success_rates_by_permutation_model_size(combined_df: pd.DataFrame, test_cohort) -> pd.DataFrame:
    df = (
        100
        * combined_df[combined_df[success_column] == True]
        .index.droplevel(0)
        .droplevel(0)
        .value_counts()
        / combined_df.index.droplevel(0).droplevel(0).value_counts()
    )
    print(df.nsmallest(n=15))
    print(df.reset_index().set_index("permutation").value_counts())

    fig_name = "success_rates_by_permutation_model_size.hist"
    fig = plt.figure(f"{fig_name}_{test_cohort}")
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
    fig.savefig(f"figures/{fig_name}.{test_cohort}.png")

    return df


def get_large_model_improvements_by_permutation(
    combined_df_raw: pd.DataFrame,
    test_cohort
) -> pd.DataFrame:
    df = (
        combined_df_raw[
            (combined_df_raw[success_column] == True)
            & (combined_df_raw["ModelSize"] == model_sizes_hypothesis_mapping[test_cohort]["improved"])
        ]
        .index.get_level_values(2)
        .value_counts()
        / combined_df_raw[(combined_df_raw["ModelSize"] == model_sizes_hypothesis_mapping[test_cohort]["improved"])]
        .index.get_level_values(2)
        .value_counts()
    ) - (
        combined_df_raw[
            (combined_df_raw[success_column] == True)
            & (combined_df_raw["ModelSize"] == model_sizes_hypothesis_mapping[test_cohort]["baseline"])
        ]
        .index.get_level_values(2)
        .value_counts()
        / combined_df_raw[(combined_df_raw["ModelSize"] == model_sizes_hypothesis_mapping[test_cohort]["baseline"])]
        .index.get_level_values(2)
        .value_counts()
    )

    fig_name = "success_rates_by_permutation_model_size.improvement.hist"
    fig = plt.figure(f"{fig_name}_{test_cohort}")
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
        f"figures/{fig_name}.{test_cohort}.png"
    )
    print(df.value_counts())
    return df


def get_success_rates_by_eligibility(
    success_rates_by_permutation: pd.DataFrame,
    eligibility_df: pd.DataFrame,
    test_cohort,
) -> pd.DataFrame:
    fig_name = "success_rates_by_eligibility.hist"
    fig = plt.figure(f"{fig_name}_{test_cohort}")
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

    fig.savefig(f"figures/{fig_name}.{test_cohort}.png")
    return df


def get_success_rates_by_eligibility_model_size(
    success_rates_by_permutation_model_size: pd.DataFrame,
    eligibility_df: pd.DataFrame,
    test_cohort,
) -> pd.DataFrame:
    fig_name = "success_rates_by_eligibility.modelSize"
    fig = plt.figure(f"{fig_name}_{test_cohort}")
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

    fig.savefig(f"figures/{fig_name}.{test_cohort}.png")
    return df


def main(argv):
    if len(argv) > 0:
        output_dir = Path("testOutputs").joinpath(argv[0])
        assert output_dir.exists()
        analyse_cohort(output_dir)
    else:
        for output_dir in Path("testOutputs").glob("*"):
            analyse_cohort(output_dir)


def deduplicate_rejudgements(df: pd.DataFrame) -> pd.DataFrame:
    if "RejudgementPassed" in df:
        df["RejudgementFailedCount"] = df[df["RejudgementPassed"] == False].groupby(["commit", "exec_time", "permutation"]).agg({
            "RejudgementPassed": 'count'
        })
        df["RejudgementPassedCount"] = df[df["RejudgementPassed"] == True].groupby(["commit", "exec_time", "permutation"]).agg({
            "RejudgementPassed": 'count'
        })
    if "RejudgementAgree" in df:
        df["RejudgementDisagreeCount"] = df[df["RejudgementAgree"] == False].groupby(["commit", "exec_time", "permutation"]).agg({
            "RejudgementAgree": 'count'
        })
        df["RejudgementAgreeCount"] = df[df["RejudgementAgree"] == True].groupby(["commit", "exec_time", "permutation"]).agg({
            "RejudgementAgree": 'count'
        })
    if "rejudgment_time" in df and "rejudgement_reasoning" in df:
        df = df.drop_duplicates(subset=["rejudgement_time", "rejudgement_reasoning"])
    return df


def analyse_cohort(output_dir: Path):
    test_cohort = str(output_dir.relative_to("testOutputs"))
    failure_dfs = load_failure_df(output_dir, test_cohort)
    success_dfs = load_success_df(output_dir, test_cohort)
    combined_dfs_raw = pd.concat(
        [success_dfs, failure_dfs],
    )
    if output_dir.name.startswith("child_benefit"):
        eligibility_dfs = extract_test_cases_for_test_cohort(
            test_cohort
        )
        combined_dfs_raw = combined_dfs_raw.join(
            eligibility_dfs, on="permutation"
        )

    # Assume that we only want to include data from the baseline and improved commit sets, and any other results should be excluded
    combined_dfs_raw = combined_dfs_raw[
        combined_dfs_raw["ModelSize"].isin(
            list(model_sizes_hypothesis_mapping[test_cohort].values())
        )
    ]

    combined_dfs = combined_dfs_raw.set_index(
        ["ModelSize"], append=True
    )
    print(combined_dfs.value_counts([success_column, "ModelSize"]))
    print(
        combined_dfs.value_counts(
            ["ModelSize", "permutation"], ascending=True
        )
    )
    success_rates_by_permutations = get_success_rates_by_permutation(
        combined_dfs
    )
    success_rates_by_permutation_model_sizes = (
        get_success_rates_by_permutation_model_size(
            combined_dfs, test_cohort
        )
    )
    large_model_improvement_by_permutations = (
        get_large_model_improvements_by_permutation(
            combined_dfs_raw, test_cohort
        )
    )
    if output_dir.name.startswith("child_benefit"):
        print(
            combined_dfs_raw.value_counts(
                [success_column, "eligible", "not_eligible"]
            )
        )
        success_rates_by_eligibilitys = get_success_rates_by_eligibility(
            success_rates_by_permutations,
            eligibility_dfs,
            test_cohort,
        )
        success_rates_by_eligibility_model_size = get_success_rates_by_eligibility_model_size(
            success_rates_by_permutation_model_sizes,
            eligibility_dfs,
            test_cohort,
        )

        combined_dfs_raw = load_and_join_rejudgements(output_dir, test_cohort, combined_dfs_raw) 
        combined_dfs_by_run = deduplicate_rejudgements(combined_dfs_raw)
        plot_venn_diagrams(test_cohort, combined_dfs_by_run)
    

def load_and_join_rejudgements(output_dir, test_cohort, combined_dfs_raw):
    rejudgement_agree_dfs = load_agree_judgements_df(output_dir, test_cohort)
    rejudgement_disagree_dfs = load_disagree_judgements_df(output_dir, test_cohort)
    combined_agree_rejudgement_dfs_raw = pd.concat(
        [rejudgement_agree_dfs, rejudgement_disagree_dfs],
    )
    if len(combined_agree_rejudgement_dfs_raw):
        try:
            combined_dfs_raw = combined_dfs_raw.join(
                combined_agree_rejudgement_dfs_raw,
                rsuffix="__agree",
                ##how="inner",
                #validate="1:1",
                validate="1:m",
            )
        except pd.errors.MergeError as e:
            left = combined_dfs_raw[combined_dfs_raw.index.duplicated()]
            right = combined_agree_rejudgement_dfs_raw[combined_agree_rejudgement_dfs_raw.index.duplicated()]
            import pdb; pdb.set_trace()
            print('LEFT DUPLICATES', left)
            print('RIGHT DUPLCIATES', right)
            raise e

        combined_dfs_raw["ConsensusPassed"] = combined_dfs_raw.apply(
            # To find whether the rejudge believes the case should have passed
            # If the rejudgement agrees with the original judgement, use the original judgement
            # If the rejudgement disagrees with the original judgement use the opposite of the original judgment
            lambda row: row["Passed"] if row["RejudgementAgree"] == True else (not row["Passed"]),
            axis=1
        )
    rejudgement_passed_dfs = load_passed_judgements_df(output_dir, test_cohort)
    rejudgement_failed_dfs = load_failed_judgements_df(output_dir, test_cohort)
    combined_passfail_rejudgement_dfs_raw = pd.concat(
        [rejudgement_passed_dfs, rejudgement_failed_dfs],
    )
    if len(combined_passfail_rejudgement_dfs_raw):
        try:
            combined_dfs_raw = combined_dfs_raw.join(
                combined_passfail_rejudgement_dfs_raw,
                rsuffix="__passfail",
                ##how="inner",
                ##validate="1:1",
                #validate="1:m",
            )
        except pd.errors.MergeError as e:
            left = combined_dfs_raw[combined_dfs_raw.index.duplicated()]
            right = combined_passfail_rejudgement_dfs_raw[combined_passfail_rejudgement_dfs_raw.index.duplicated()]
            import pdb; pdb.set_trace()
            print('LEFT DUPLICATES', left)
            print('RIGHT DUPLCIATES', right)
            raise e
    return combined_dfs_raw


def plot_venn_diagrams(test_cohort, combined_dfs_by_run):
    if "RejudgementPassed" in combined_dfs_by_run and "ConsensusPassed" in combined_dfs_by_run:
        print(combined_dfs_by_run.value_counts(["Passed", "RejudgementPassed", "ConsensusPassed"]))
        fig_name = "venn3_true"
        fig = plt.figure(f"{fig_name}_{test_cohort}")
        fig.clear()
        v = venn3(
            [
                set(combined_dfs_by_run[combined_dfs_by_run["Passed"] == True].index),
                set(combined_dfs_by_run[combined_dfs_by_run["RejudgementPassed"] == True].index),
                set(combined_dfs_by_run[combined_dfs_by_run["ConsensusPassed"] == True].index)
            ],
            ("Passed", "RejudgementPassed", "ConsensusPassed")
        )
        fig.savefig(f"figures/{fig_name}.{test_cohort}.png")
        
        fig_name = "venn3_false"
        fig = plt.figure(f"{fig_name}_{test_cohort}")
        fig.clear()
        v = venn3(
            [
                set(combined_dfs_by_run[combined_dfs_by_run["Passed"] == False].index),
                set(combined_dfs_by_run[combined_dfs_by_run["RejudgementPassed"] == False].index),
                set(combined_dfs_by_run[combined_dfs_by_run["ConsensusPassed"] == False].index)
            ],
            ("Passed", "RejudgementPassed", "ConsensusPassed")
        )
        fig.savefig(f"figures/{fig_name}.{test_cohort}.png")
        #combined_dfs["correct_outcome"] = combined_dfs["reasoning"].str.contains(r"The agent (?:\w+ |\w+ the )?correct", regex=True)
    elif "RejudgementPassed" in combined_dfs_by_run:
        fig_name = "venn2_true"
        fig = plt.figure(f"{fig_name}_{test_cohort}")
        fig.clear()
        v = venn2(
            [
                set(combined_dfs_by_run[combined_dfs_by_run["Passed"] == True].index),
                set(combined_dfs_by_run[combined_dfs_by_run["RejudgementPassed"] == True].index),
            ],
            ("Passed", "RejudgementPassed")
        )
        fig.savefig(f"figures/{fig_name}.{test_cohort}.png")
        
        fig_name = "venn2_false"
        fig = plt.figure(f"{fig_name}_{test_cohort}")
        fig.clear()
        v = venn2(
            [
                set(combined_dfs_by_run[combined_dfs_by_run["Passed"] == False].index),
                set(combined_dfs_by_run[combined_dfs_by_run["RejudgementPassed"] == False].index),
            ],
            ("Passed", "RejudgementPassed")
        )
        fig.savefig(f"figures/{fig_name}.{test_cohort}.png")


if __name__ == "__main__":
    main(sys.argv[1:])