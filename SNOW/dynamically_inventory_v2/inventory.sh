#!/bin/bash

# Source credentials
CRED_FILE="/path/to/cred_file"
if [[ -f "$CRED_FILE" ]]; then
    source "$CRED_FILE"
else
    echo "Error: Credential file not found at $CRED_FILE"
    exit 1
fi

# Check if required environment variables are set
if [[ -z "$SNOW_API_URL" || -z "$SNOW_API_ID" || -z "$SNOW_API_SECRET" || -z "$SNOW_API_USERNAME" || -z "$SNOW_API_PASSWORD" ]]; then
    echo "Error: Missing required ServiceNow credentials in the credential file"
    exit 1
fi

# Call Python script with passed arguments
python3 /path/to/dynamic_inventory.py "$@"
