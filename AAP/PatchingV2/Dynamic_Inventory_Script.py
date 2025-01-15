#!/usr/bin/env python3
import requests
import json
import sys

# ServiceNow API credentials
SNOW_INSTANCE = "your_instance.service-now.com"
SNOW_USERNAME = "your_username"
SNOW_PASSWORD = "your_password"

# API Endpoint and Headers
SNOW_API_URL = f"https://{SNOW_INSTANCE}/api/now/table/cmdb_ci_server"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Query parameters
QUERY_PARAMS = {
    "sysparm_fields": "host_name,install_status,u_state,os,u_pool",
    "sysparm_query": "install_status=Installed^u_state=Active^os=Linux"
}

def fetch_cmdb_data():
    """Fetch data from ServiceNow CMDB."""
    try:
        response = requests.get(SNOW_API_URL, auth=(SNOW_USERNAME, SNOW_PASSWORD), headers=HEADERS, params=QUERY_PARAMS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from ServiceNow: {e}")
        sys.exit(1)

def create_inventory(data):
    """Create dynamic inventory JSON."""
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
            
            # Add host to group based on u_pool
            group_name = f"pool_{u_pool}"
            if group_name not in inventory:
                inventory[group_name] = {"hosts": []}
            inventory[group_name]["hosts"].append(host_name)
    return inventory

def main():
    """Main execution."""
    cmdb_data = fetch_cmdb_data()
    inventory = create_inventory(cmdb_data)
    print(json.dumps(inventory, indent=2))

if __name__ == "__main__":
    main()
