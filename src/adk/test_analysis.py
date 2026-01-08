#!/usr/bin/env ipython
import re
from pathlib import Path
import subprocess

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns


failure_df = {}
success_df = {}
combined_df = {}
combined_df_raw = {}
success_rates_by_permutation = {}
success_rates_by_permutation_model_size = {}
large_model_improvement_by_permutation = {}
eligibility_df = {}
success_rates_by_eligibility = {}


def invert_mapping(dictionary: dict) -> dict:
    return {elem: k for k, v in dictionary.items() for elem in v}


model_size_commit_mapping = {
    "child_benefit": invert_mapping(
        {
            "small": ["Unknown", "fc922c5", "9493282", "f2dc127"],
            "large": ["575b5e9"],
        }
    ),
    "skilled_worker_visa": invert_mapping(
        {"small": ["Unknown", "db37bc9", "df1795d", "71b1d7c"], "large": ["8ed3c90"]}
    ),
}


def extract_results_for_folder(output_dir, search_character):
    print(output_dir)
    extracted_records = []
    output = subprocess.run(
        ["rg", search_character, "-c", "--hidden"],
        capture_output=True,
        check=False,
        text=True,
        cwd=output_dir,
    )
    for filename in output.stdout.strip().split("\n"):
        if filename:
            if re.match(
                r"(?P<exec_time>[\d:T\.-]+)__RepoCommit=(?P<commit>[a-f0-9]+)/Permutation(?P<permutation>\d+).*",
                filename,
            ):
                extracted_fields = re.search(
                    r"(?P<exec_time>[\d:T\.-]+)__RepoCommit=(?P<commit>[a-f0-9]+)/Permutation(?P<permutation>\d+).*",
                    filename,
                ).groupdict()
            else:
                extracted_fields = re.search(
                    r"(?P<exec_time>[\d:T\.-]+)/Permutation(?P<permutation>\d+).out",
                    filename,
                ).groupdict()
            extracted_fields["permutation"] = int(extracted_fields["permutation"])
            extracted_records.append(extracted_fields)
    return pd.DataFrame.from_records(extracted_records)


def load_and_parse_test_cases(test_cohort: str):
    test_case_file = Path(f"../../prompts/manual/test_cases/{test_cohort}.md")
    with test_case_file.open() as f:
        raw_test_cases = f.readlines()
    test_cases_str = "\n".join(raw_test_cases)
    test_cases = test_cases_str.split(sep="---")
    return test_cases


def extract_test_cases_for_test_cohort(test_cohort):
    test_cases = load_and_parse_test_cases(test_cohort)
    extracted_records = []
    for test_case in test_cases:
        parsed_test_case = list(filter(len, test_case.split("\n")))
        extracted_records.append(dict(
            permutation=extract_permutation_number_from_test_case(parsed_test_case),
            #  "eligible": extract_eligibility_from_test_case(parsed_test_case),
            **extract_eligibility_from_test_case(parsed_test_case)
        ))
    return pd.DataFrame.from_records(extracted_records, index="permutation")


def extract_eligibility_from_test_case(test_case):
    outcome = test_case[-1]
    assert "**Outcome:**" in outcome, outcome
    #  assert outcome.count("Eligible") == 1, outcome

    return {
        "not_eligible": bool(outcome.count("Not Eligible")),
        # If we find the words Eligible outside of the string "Not Eligible" (as the former is a substring of the latter we can just subtract occurrences) then we know the results is partial eligibility
        "eligible": bool(outcome.count("Eligible") - outcome.count("Not Eligible"))
    }


def extract_permutation_number_from_test_case(test_case):
    permutation = test_case[0]
    p_match= re.search(
        r"Permutation (?P<permutation_number>[\d]+):",
        permutation
    )
    assert p_match and len(p_match.groups()) == 1
    return int(p_match.groups()[0])


def get_eligibility_case(row):
    match (row["eligible"], row["not_eligible"]):
        case (True, True): return "Both"
        case (True, False): return "Eligible"
        case (False, True): return "NotEligible"


def main():
    for output_dir in Path(".testOutputs").glob("*"):
        if output_dir.name != "child_benefit":
            continue
        test_cohort = str(output_dir.relative_to(".testOutputs"))

        #  print('failures:')
        failure_df[test_cohort] = extract_results_for_folder(output_dir, "✗")
        failure_df[test_cohort]["Passed"] = False
        failure_df[test_cohort]["commit"].fillna("Unknown", inplace=True)
        failure_df[test_cohort].set_index(
            ["commit", "exec_time", "permutation"], inplace=True
        )
        failure_df[test_cohort]["ModelSize"] = (
            failure_df[test_cohort]
            .index.get_level_values(0)
            .map(model_size_commit_mapping[test_cohort])
        )
        #  print(failure_df[test_cohort].value_counts(["permutation", "ModelSize"]))

        #  print('successes:')
        success_df[test_cohort] = extract_results_for_folder(output_dir, "✓")
        success_df[test_cohort]["Passed"] = True
        success_df[test_cohort]["commit"].fillna("Unknown", inplace=True)
        success_df[test_cohort].set_index(
            ["commit", "exec_time", "permutation"], inplace=True
        )
        success_df[test_cohort]["ModelSize"] = (
            success_df[test_cohort]
            .index.get_level_values(0)
            .map(model_size_commit_mapping[test_cohort])
        )
        #  print(success_df[test_cohort].value_counts(["permutation", "ModelSize"]))

        combined_df_raw[test_cohort] = pd.concat(
            [success_df[test_cohort], failure_df[test_cohort]],
        )
        eligibility_df[test_cohort] = extract_test_cases_for_test_cohort(test_cohort)
        combined_df_raw[test_cohort] = combined_df_raw[test_cohort].join(eligibility_df[test_cohort], on="permutation")

        combined_df[test_cohort] = combined_df_raw[test_cohort].set_index(
            ["ModelSize"], append=True
        )
        print(combined_df[test_cohort].value_counts(["Passed", "ModelSize"]))
        print(
            combined_df[test_cohort].value_counts(
                ["ModelSize", "permutation"], ascending=True
            )
        )

        success_rates_by_permutation[test_cohort] = (
            100
            * combined_df[test_cohort][combined_df[test_cohort]["Passed"] == True]
            .index.get_level_values(2)
            .value_counts()
            / combined_df[test_cohort].index.get_level_values(2).value_counts()
        )
        print(success_rates_by_permutation[test_cohort].nsmallest(n=15))

        success_rates_by_permutation_model_size[test_cohort] = (
            100
            * combined_df[test_cohort][combined_df[test_cohort]["Passed"] == True]
            .index.droplevel(0)
            .droplevel(0)
            .value_counts()
            / combined_df[test_cohort].index.droplevel(0).droplevel(0).value_counts()
        )
        print(success_rates_by_permutation_model_size[test_cohort].nsmallest(n=15))
        print(success_rates_by_permutation_model_size[test_cohort].reset_index().set_index("permutation").value_counts())

        fig = plt.figure(f"hist_{test_cohort}")
        fig.clear()
        ax = sns.histplot(
            success_rates_by_permutation_model_size[test_cohort].reset_index(),
            x="count",
            hue="ModelSize",
            multiple="dodge",
            shrink=0.7,
            bins=20,
            common_bins=True,
        )
        ax.set_title(
            "Accuracy of agent (according to judge) for {}".format(
                test_cohort.replace("_", " ")
            )
        )
        ax.set_ylabel("Count")
        ax.set_xlabel("Percentage correctness over all executions")
        fig.savefig(f"success_rates_by_permutation_model_size.hist.{test_cohort}.png")

        large_model_improvement_by_permutation[test_cohort] = (
            combined_df_raw[test_cohort][
                (combined_df_raw[test_cohort]["Passed"] == True)
                & (combined_df_raw[test_cohort]["ModelSize"] == "large")
            ]
            .index.get_level_values(2)
            .value_counts()
            / combined_df_raw[test_cohort][
                (combined_df_raw[test_cohort]["ModelSize"] == "large")
            ]
            .index.get_level_values(2)
            .value_counts()
        ) - (
            combined_df_raw[test_cohort][
                (combined_df_raw[test_cohort]["Passed"] == True)
                & (combined_df_raw[test_cohort]["ModelSize"] == "small")
            ]
            .index.get_level_values(2)
            .value_counts()
            / combined_df_raw[test_cohort][
                (combined_df_raw[test_cohort]["ModelSize"] == "small")
            ]
            .index.get_level_values(2)
            .value_counts()
        )

        fig = plt.figure(f"improvement_{test_cohort}")
        fig.clear()
        large_model_improvement_by_permutation[test_cohort].hist()
        ax = fig.get_axes()[0]
        ax.set_title(
            "Difference in judged accuracy with varying model size for {}".format(
                test_cohort.replace("_", " ")
            )
        )
        ax.set_ylabel("Count of permutations")
        ax.set_xlabel(
            "Large model accuracy % minus small model accuracy % for a given permutation"
        )
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        fig.savefig(
            f"success_rates_by_permutation_model_size.improvement.hist.{test_cohort}.png"
        )
        print(large_model_improvement_by_permutation[test_cohort].value_counts())

        fig = plt.figure(f"eligibility_{test_cohort}")
        fig.clear()
        print(combined_df_raw[test_cohort].value_counts(["Passed", "eligible", "not_eligible"]))
        success_rates_by_eligibility[test_cohort] = eligibility_df[test_cohort].join(success_rates_by_permutation[test_cohort])
        success_rates_by_eligibility[test_cohort]["eligibility_cat"] = success_rates_by_eligibility[test_cohort].apply(get_eligibility_case, axis=1)

        ax = sns.histplot(
            success_rates_by_eligibility[test_cohort],
            x="count",
            hue="eligibility_cat",
            multiple="dodge",
            shrink=0.7,
            bins=20,
            common_bins=True,
        )
        ax.set_ylabel("Count of permutations")
        ax.set_xlabel(
            "Model Accuracy %"
        )
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(100.0))

        fig.savefig(
            f"success_rates_by_eligibility.hist.{test_cohort}.png"
        )


if __name__ == "__main__":
    main()
