import re
import pandas as pd
from pathlib import Path
import subprocess

output = {}
output_df = {}
for output_dir in Path('.testOutputs').glob('*'):
    print(output_dir)
    extracted_records = []
    output[output_dir] = subprocess.run(["rg", "✗", "-c", "--hidden"], capture_output=True, check=False, text=True, cwd=output_dir)
    for filename in output[output_dir].stdout.strip().split("\n"):
        if filename:
            if re.match(r"(?P<exec_time>[\d:T\.-]+)__RepoCommit=(?P<commit>[a-f0-9]+)/Permutation(?P<permutation>\d+).*", filename):
                extracted_fields = re.search(r"(?P<exec_time>[\d:T\.-]+)__RepoCommit=(?P<commit>[a-f0-9]+)/Permutation(?P<permutation>\d+).*", filename).groupdict()
            else:
                extracted_fields = re.search(r"(?P<exec_time>[\d:T\.-]+)/Permutation(?P<permutation>\d+).out", filename).groupdict()
            extracted_records.append(extracted_fields)
    output_df[output_dir] = pd.DataFrame.from_records(extracted_records)
    print(output_df[output_dir].value_counts("permutation"))
