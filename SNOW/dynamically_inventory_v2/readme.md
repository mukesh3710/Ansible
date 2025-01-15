# Dynamic Inventory for Linux Patching

This project provides a dynamic inventory solution for Linux patching using Ansible. It integrates with ServiceNow CMDB to fetch server details and categorizes them into groups for efficient patching. The solution consists of a Python script (`dynamic_inventory.py`) for inventory generation and a Bash script (`generate_inventory.sh`) for execution. Credentials for ServiceNow API are securely managed via an environment-sourced `cred_file`.

## **Project Components**

### **1. Python Script: `dynamic_inventory.py`**
The Python script performs the following tasks:

#### **a. Credential Management**
- Fetches credentials and API details from environment variables.
- Credentials include:
  - ServiceNow API URL (`SNOW_API_URL`)
  - API ID and secret (`SNOW_API_ID`, `SNOW_API_SECRET`)
  - API username and password (`SNOW_API_USERNAME`, `SNOW_API_PASSWORD`)

#### **b. ServiceNow Integration**
- Calls the ServiceNow API to fetch CMDB data.
- Filters servers based on the following criteria:
  - `install_status = Installed`
  - `u_state = Active`
  - `os = Linux`
- Extracts the required fields: `host_name`, `install_status`, `u_state`, `os`, and `u_pool`.

#### **c. Inventory Generation**
- Organizes servers into groups based on their `u_pool` values.
- Generates an inventory structure with host variables and group associations.

#### **d. Command-Line Arguments**
Supports various arguments for flexibility:
- `--list` (default): Outputs the full inventory.
- `--groups`: Lists all available groups.
- `--group [group]`: Lists all hosts in the specified group.
- `--host [host]`: Lists the group(s) a host belongs to.
- `--prefix [prefix]`: Lists all hosts with specified prefixes.
- `--generate`: Saves the full inventory to a file.
- `-d` or `--debug`: Enables debug mode for additional logging.

#### **e. Output Formats**
Supports output formats like JSON, Ansible, and batch run (future implementation).

### **2. Bash Script: `generate_inventory.sh`**
The Bash script:
- Sources credentials from a `cred_file`.
- Verifies the presence of required credentials.
- Invokes the Python script with the provided arguments.

### **3. Credential File: `cred_file`**
Stores ServiceNow API credentials in the following format:

```bash
export SNOW_API_URL="https://your_instance.service-now.com/api/now/table/cmdb_ci_server"
export SNOW_API_ID="your_api_id"
export SNOW_API_SECRET="your_api_secret"
export SNOW_API_USERNAME="your_username"
export SNOW_API_PASSWORD="your_password"
```

Ensure the `cred_file` is protected with appropriate file permissions.

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd <repository-folder>
```

### **2. Configure the Credential File**
Create and populate the `cred_file` with your ServiceNow API credentials:
```bash
nano cred_file
```
Ensure the file has the following format:
```bash
export SNOW_API_URL="<your_snow_api_url>"
export SNOW_API_ID="<your_api_id>"
export SNOW_API_SECRET="<your_api_secret>"
export SNOW_API_USERNAME="<your_username>"
export SNOW_API_PASSWORD="<your_password>"
```

Restrict access to the `cred_file`:
```bash
chmod 600 cred_file
```

### **3. Install Dependencies**
Ensure Python 3 and `requests` library are installed:
```bash
sudo apt install python3
pip install requests
```

### **4. Execute the Bash Script**
Run the script with desired options. Example usage:

#### **Generate and Save Inventory**
```bash
./generate_inventory.sh --action --generate --output /tmp/patching_inventory.json
```

#### **List Full Inventory**
```bash
./generate_inventory.sh --action --list
```

#### **List All Groups**
```bash
./generate_inventory.sh --action --groups
```

#### **List Hosts in a Group**
```bash
./generate_inventory.sh --action --group pool_1
```

#### **List Groups a Host Belongs To**
```bash
./generate_inventory.sh --action --host host_name
```

#### **List Hosts with Specific Prefixes**
```bash
./generate_inventory.sh --action --prefix web,app
```

---

## **Code Explanation**

### **Python Script: `dynamic_inventory.py`**

#### **1. Credential Management**
Fetches ServiceNow API credentials from environment variables. The credentials include API URL, ID, secret, username, and password, formatted as `Api_<ID>_<USERNAME>` and `Api_<SECRET>_<PASSWORD>` for enhanced security.

#### **2. ServiceNow Integration**
- Connects to ServiceNow CMDB using the API.
- Retrieves server data filtered by:
  - `install_status = Installed`
  - `u_state = Active`
  - `os = Linux`

#### **3. Inventory Generation**
Organizes data into:
- Groups based on `u_pool` values (e.g., `pool_1`, `pool_2`).
- Host variables stored in `_meta.hostvars`.

#### **4. Command-Line Arguments**
Uses `argparse` for flexible CLI argument handling:
- Supports full inventory listing, group-specific queries, host-specific queries, and prefix-based filtering.
- Enables saving the inventory to a file.

---

## **Security Considerations**
- Protect the `cred_file` with restricted file permissions (`chmod 600`).
- Avoid hardcoding sensitive credentials directly in the scripts.
- Use environment variables to handle credentials securely.

---

## **Future Enhancements**
- Add support for batch run output format.
- Implement logging for better traceability.
- Introduce unit tests for Python script.

---

## **Contributors**
- [Your Name]
