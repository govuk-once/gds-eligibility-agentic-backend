#!/bin/bash

source ./src/runners/run_script_base.sh

if [ -z "$1" ]; then
    echo "Error: No AWS profile provided."
    echo "Usage: run_with_env <AWS_PROFILE> <COMMAND>"
    return 1
fi

run_with_aws_profile "$1" pytest -s tests/test_pip.py::test_pip_happy_path
