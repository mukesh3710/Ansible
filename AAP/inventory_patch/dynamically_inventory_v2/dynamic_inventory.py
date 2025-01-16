#!/usr/bin/env python3

import argparse
import json
import os
import requests
import sys

# Fetch credentials from environment variables
def fetch_credentials():
    try:
        snow_api_url = os.environ["SNOW_API_URL"]
        snow_api_id = os.environ["SNOW_API_ID"]
        snow_api_secret = os.environ["SNOW_API_SECRET"]
        snow_api_username = os.environ["SNOW_API_USERNAME"]
        snow_api_password = os.environ["SNOW_API_PASSWORD"]

        # Format the API username and password with "Api_" prefix
        snow_username = f"Api_{snow_api_id}_{snow_api_username}"
        snow_password = f"Api_{snow_api_secret}_{snow_api_password}"

        return snow_api_url, snow_username, snow_password
    except KeyError as e:
        print(f"Error: Missing required environment variable {str(e)}")
        sys.exit(1)

# Fetch data from ServiceNow
def fetch_cmdb_data(api_url, username, password):
    headers = {"Content-Type": "application/json"}
    query_params = {
        "sysparm_fields": "host_name,install_status,u_state,os,u_pool",
        "sysparm_query": "install_status=Installed^u_state=Active^os=Linux"
    }

    try:
        response = requests.get(api_url, auth=(username, password), headers=headers, params=query_params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from ServiceNow: {e}")
        sys.exit(1)

# Generate inventory from fetched data
def generate_inventory(data):
    inventory = {"_meta": {"hostvars": {}}}
    for record in data.get("result", []):
        host_name = record.get("host_name")
        u_pool = record.get("u_pool", "default")
        if host_name:
            # Add host to hostvars
            inventory["_meta"]["hostvars"][host_name] = {
                "u_pool": u_pool,
                "os": record.get("os", "Unknown")
            }
            # Add host to group
            group_name = f"pool_{u_pool}"
            inventory.setdefault(group_name, {"hosts": []})["hosts"].append(host_name)
    return inventory

# Parse and handle arguments
def handle_arguments(inventory):
    parser = argparse.ArgumentParser(description="Dynamic Inventory Script for Patching")
    parser.add_argument("--action", default="--list", help="Action to perform (default: --list)")
    parser.add_argument("--format", default="json", help="Output format (default: json)")
    parser.add_argument("--prefix", help="List hosts with specified prefixes")
    parser.add_argument("--group", help="List all hosts in the specified group")
    parser.add_argument("--host", help="List the group(s) a host belongs to")
    parser.add_argument("--output", help="File to save the full inventory")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    if args.debug:
        print(f"Arguments received: {args}")

    # Handle actions
    if args.action == "--list":
        print(json.dumps(inventory, indent=2))
    elif args.action == "--groups":
        print(json.dumps(list(inventory.keys()), indent=2))
    elif args.action == "--group" and args.group:
        print(json.dumps(inventory.get(args.group, {"hosts": []}), indent=2))
    elif args.action == "--host" and args.host:
        groups = [group for group, data in inventory.items() if args.host in data.get("hosts", [])]
        print(json.dumps(groups, indent=2))
    elif args.action == "--prefix" and args.prefix:
        prefixes = args.prefix.split(",")
        matched_hosts = [host for host in inventory["_meta"]["hostvars"] if any(host.startswith(p) for p in prefixes)]
        print(json.dumps(matched_hosts, indent=2))
    elif args.action == "--generate" and args.output:
        with open(args.output, "w") as f:
            json.dump(inventory, f, indent=2)
        print(f"Full inventory saved to {args.output}")
    else:
        print("Invalid action or missing required arguments")
        sys.exit(1)

# Main function
def main():
    snow_api_url, snow_username, snow_password = fetch_credentials()
    cmdb_data = fetch_cmdb_data(snow_api_url, snow_username, snow_password)
    inventory = generate_inventory(cmdb_data)
    handle_arguments(inventory)

if __name__ == "__main__":
    main()
