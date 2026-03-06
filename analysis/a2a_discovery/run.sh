#!/bin/bash
# --- Login to AWS and run this script recursively ---
# We pass "$0" (this script's path) and the internal flag
echo "Launching agents inside aws-vault session..."
aws-vault exec "$ENVIRONMENT" -- docker-compose up
