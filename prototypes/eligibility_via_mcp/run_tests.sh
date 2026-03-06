#!/bin/bash

<<<<<<< HEAD
source ./src/runners/run_script_base.sh
=======
source ./src/runner/script.sh
>>>>>>> 46781da (ELIG-243: complete)

if [ -z "$1" ]; then
    echo "Error: No AWS profile provided."
    echo "Usage: run_with_env <AWS_PROFILE> <COMMAND>"
    return 1
fi

<<<<<<< HEAD
run_with_aws_profile "$1" pytest -s tests/test_universal_credit.py
=======
run_with_aws_profile "$1" pytest -s tests/test_behaviour.py
>>>>>>> 46781da (ELIG-243: complete)
