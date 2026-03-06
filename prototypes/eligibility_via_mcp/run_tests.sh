#!/bin/bash

source ./src/runner/script.sh

if [ -z "$1" ]; then
    echo "Error: No AWS profile provided."
    echo "Usage: run_with_env <AWS_PROFILE> <COMMAND>"
    return 1
fi

run_with_aws_profile "$1" pytest -s tests/test_behaviour.py
