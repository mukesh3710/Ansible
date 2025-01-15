# Linux Patching with AAP

## Linux Patching CMDB Data Management

Ansible Automation Platform for patching utilizes the ServiceNow CMDB as the source of record for patching-related data. 

Within the CMDB, several custom fields are employed to store patching data. The table below identifies the fields and their potential standard values.

| Field Name | Description | Standard Values |
|---|---|---|
| install_status | Official ServiceNow flag identifying the state of the server | Installed (required) |
| u_state | Custom field providing more granularity in server state | Active (required) |
| Os | Operating System name | Linux (required) |
| host_name | Primary identifier of the host in patching | <serverX> |
| u_pool | Custom field used to divide servers into groups | 1-5 |

A dynamic inventory script, written in Python, interacts with ServiceNow to retrieve hostnames and patching-related data. This script then parses the data and organizes servers into Ansible inventory groups based on the values of `u_pool` and `u_state`. These patching group names dictate the execution order during each patching window. Patching is organized by environment and further subdivided into groups within each environment.

## Patching Inventory Script**

The script executes daily within the AAP to maintain an up-to-date inventory. As hosts are added or removed in the CMDB, the inventory reflects these changes. 

This patching script, created using Python, extracts information from ServiceNow. When run without any options, it produces a complete JSON output of the patching inventory, which is then dynamically consumed by AAP to generate the inventory.
