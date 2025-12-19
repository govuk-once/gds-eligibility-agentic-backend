#!/usr/bin/env ipython
import re
import pandas as pd
from pathlib import Path
import subprocess


failure_df = {}
success_df = {}
combined_df = {}


def invert_mapping(dictionary: dict) -> dict:
    return {elem: k for k, v in dictionary.items() for elem in v}


model_size_commit_mapping = {
    "child_benefit": invert_mapping({
        "small": [
            "Unknown",
            "fc922c5",
            "9493282",
            "f2dc127"
        ],
        "large": [
            "575b5e9"
        ],
    }),
    "skilled_worker_visa": invert_mapping({
        "small": [
            "Unknown",
            "db37bc9",
            "df1795d",
            "71b1d7c"
        ],
        "large": [
            "8ed3c90"
        ]
    })
}


def extract_results_for_folder(output_dir, search_character):
    print(output_dir)
    extracted_records = []
    output = subprocess.run(["rg", search_character, "-c", "--hidden"], capture_output=True, check=False, text=True, cwd=output_dir)
    for filename in output.stdout.strip().split("\n"):
        if filename:
            if re.match(
                r"(?P<exec_time>[\d:T\.-]+)__RepoCommit=(?P<commit>[a-f0-9]+)/Permutation(?P<permutation>\d+).*",
                filename
            ):
                extracted_fields = re.search(
                    r"(?P<exec_time>[\d:T\.-]+)__RepoCommit=(?P<commit>[a-f0-9]+)/Permutation(?P<permutation>\d+).*",
                    filename
                ).groupdict()
            else:
                extracted_fields = re.search(
                    r"(?P<exec_time>[\d:T\.-]+)/Permutation(?P<permutation>\d+).out",
                    filename
                ).groupdict()
            extracted_records.append(extracted_fields)
    return pd.DataFrame.from_records(extracted_records)


def main():
    for output_dir in Path('.testOutputs').glob('*'):
        test_case= str(output_dir.relative_to(".testOutputs"))

        #  print('failures:')
        failure_df[test_case] = extract_results_for_folder(output_dir, "✗")
        failure_df[test_case]["Passed"] = False
        failure_df[test_case]["commit"].fillna("Unknown", inplace=True)
        failure_df[test_case].set_index(["commit", "exec_time", "permutation"], inplace=True)
        failure_df[test_case]["ModelSize"] = failure_df[test_case].index.get_level_values(0).map(model_size_commit_mapping[test_case])
        #  print(failure_df[test_case].value_counts(["permutation", "ModelSize"]))

        #  print('successes:')
        success_df[test_case] = extract_results_for_folder(output_dir, "✓")
        success_df[test_case]["Passed"] = True
        success_df[test_case]["commit"].fillna("Unknown", inplace=True)
        success_df[test_case].set_index(["commit", "exec_time", "permutation"], inplace=True)
        success_df[test_case]["ModelSize"] = success_df[test_case].index.get_level_values(0).map(model_size_commit_mapping[test_case])
        #  print(success_df[test_case].value_counts(["permutation", "ModelSize"]))

        combined_df[test_case] = pd.concat(
            [
                success_df[test_case],
                failure_df[test_case]
            ],
        )

        combined_df[test_case].set_index(["ModelSize"], inplace=True, append=True)
        print(combined_df[test_case].value_counts(["Passed", "ModelSize"]))
        print(combined_df[test_case].value_counts(["ModelSize", "permutation"], ascending=True))

        success_rates_by_permutation = combined_df[test_case][combined_df[test_case]["Passed"] == True].index.get_level_values(2).value_counts() / combined_df[test_case].index.get_level_values(2).value_counts()
        print(success_rates_by_permutation.nsmallest(n=15))

        success_rates_by_permutation_model_size = combined_df[test_case][combined_df[test_case]["Passed"] == True].index.droplevel(0).droplevel(0).value_counts() / combined_df[test_case].index.droplevel(0).droplevel(0).value_counts()
        print(success_rates_by_permutation_model_size.nsmallest(n=15))


if __name__ == "__main__":
    main()
