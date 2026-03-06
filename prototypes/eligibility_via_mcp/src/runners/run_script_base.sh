#!/bin/bash

# setup_env.sh

# Function to setup and run commands
run_with_aws_profile() {
    local AWS_PROFILE=$1
    shift # Remove the AWS_PROFILE from the arguments list
    local COMMAND=("$@") # The rest of the arguments are the command to run

    if [ -z "$AWS_PROFILE" ]; then
        echo "Error: No AWS profile provided."
        echo "Usage: run_with_env <AWS_PROFILE> <COMMAND>"
        return 1
    fi

    # 1. Virtual Env Logic
    if [ -d ".venv" ] || [ -f ".venv" ]; then
        if [ -z "$VIRTUAL_ENV" ]; then
            source .venv/bin/activate 2>/dev/null || source .venv
        fi
    fi

    # 2. UV Logic
    if ! command -v uv &> /dev/null; then
        echo "Installing uv..."
        pip install --user uv
    fi
    uv sync

    # 3. Execution
    echo "Launching command inside aws-vault session for $AWS_PROFILE..."
    aws-vault exec "$AWS_PROFILE" -- "${COMMAND[@]}"
}