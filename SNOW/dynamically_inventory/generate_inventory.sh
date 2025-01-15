#!/bin/bash

# Configuration
SOURCE_FILE="/path/to/cred_file"
PYTHON_SCRIPT="/path/to/dynamic_inventory.py"
OUTPUT_FILE="/tmp/patching_inventory.json"
DEBUG=0

# Function to display help
function display_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --generate             Generate and save the full inventory as JSON to localhost"
    echo "  --list                 Return the full inventory (default)"
    echo "  --groups               List available groups"
    echo "  --group [group]        List all hosts in the specified group"
    echo "  --host [host]          List the group(s) a host belongs to"
    echo "  --prefix [prefix]      List all hosts with the specified prefixes (comma-separated)"
    echo "  --format [format]      Specify the output format (json, ansible, or batchrun)"
    echo "  -d, --debug            Enable debug mode"
    echo "  -h, --help             Show this help message"
    exit 0
}

# Parse arguments
ACTION="--list"
FORMAT="json"
PREFIX=""
GROUP=""
HOST=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --generate)
            ACTION="--generate"
            shift
            ;;
        --list)
            ACTION="--list"
            shift
            ;;
        --groups)
            ACTION="--groups"
            shift
            ;;
        --group)
            ACTION="--group"
            GROUP="$2"
            shift 2
            ;;
        --host)
            ACTION="--host"
            HOST="$2"
            shift 2
            ;;
        --prefix)
            ACTION="--prefix"
            PREFIX="$2"
            shift 2
            ;;
        --format)
            FORMAT="$2"
            shift 2
            ;;
        -d|--debug)
            DEBUG=1
            shift
            ;;
        -h|--help)
            display_help
            ;;
        *)
            echo "Unknown option: $1"
            display_help
            ;;
    esac
done

# Load credentials
if [[ -f "$SOURCE_FILE" ]]; then
    source "$SOURCE_FILE"
else
    echo "Error: Credential file not found at $SOURCE_FILE"
    exit 1
fi

# Validate required variables
if [[ -z "$SNOW_API_URL" || -z "$SNOW_USERNAME" || -z "$SNOW_PASSWORD" ]]; then
    echo "Error: Missing ServiceNow API credentials in the source file"
    exit 1
fi

# Run the Python script
if [[ $DEBUG -eq 1 ]]; then
    echo "Running Python script with debug enabled..."
fi

python3 "$PYTHON_SCRIPT" \
    --action "$ACTION" \
    --format "$FORMAT" \
    --prefix "$PREFIX" \
    --group "$GROUP" \
    --host "$HOST" \
    --output "$OUTPUT_FILE" \
    --snow-api-url "$SNOW_API_URL" \
    --snow-username "$SNOW_USERNAME" \
    --snow-password "$SNOW_PASSWORD" \
    ${DEBUG:+--debug}

if [[ "$ACTION" == "--generate" ]]; then
    echo "Full inventory saved to $OUTPUT_FILE"
fi
