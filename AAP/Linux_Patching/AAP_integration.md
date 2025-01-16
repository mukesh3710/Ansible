

## Prerequisites

* **Jump Server Setup:** Ensure the jump server has passwordless SSH access to all Linux client hosts. This is already configured using the shared public key.
* **Dynamic Inventory:** Confirm the dynamic inventory script (from ServiceNow) is already integrated into AAP.
* **Execution Environment:** Build and upload the execution environment with all required dependencies (e.g., ansible.posix, community.general collections).
* **Credential Setup:** Create a credential in AAP for the jump server SSH private key.

## Configure AAP

**Step 1: Add Inventory**

1. Navigate to Inventories in AAP.
2. Add a New Inventory.
3. Choose Dynamic Inventory.
4. Provide the dynamic inventory script for ServiceNow (created earlier).
5. Validate the inventory to ensure it gathers all hosts and groups (e.g., u_pool).

**Step 2: Create Machine Credential**

1. Navigate to Credentials.
2. Add a new credential:
    * Type: Machine
    * Username: root (or the user used for the jump server).
    * Private Key: Upload the SSH private key for the jump server.

**Step 3: Create Projects**

1. Navigate to Projects.
2. Add a project pointing to your Git repository containing the playbooks and roles (e.g., Linux_Patching).
3. Ensure AAP can sync and fetch the playbooks.

**Step 4: Build an Execution Environment**

1. Ensure the execution environment includes:
    * Python dependencies like requests (used for the ServiceNow inventory script).
    * Collections mentioned in collections/requirements.yml (e.g., community.general, ansible.posix).
2. If the execution environment is ready, upload it to AAP.


## Run Job Templates

1. Navigate to the Job Templates in AAP.
2. Launch each job template sequentially:
    * Start with Linux Patching - Precheck.
    * Wait for its completion.
    * Proceed to Linux Patching - Stage.
    * Follow with Linux Patching - Apply.
    * End with Linux Patching - Reboot.

**Tips:**

* Use Surveys to allow dynamic input for the `u_pool` limit when running templates.
* Monitor job execution logs to troubleshoot issues.
