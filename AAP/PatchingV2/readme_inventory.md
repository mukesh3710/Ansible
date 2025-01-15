# Creating and managing inventory for Linux Patching in Ansible Automation Platform with ServiceNow CMDB

## 1. Create a New Organization

1. Log in to the AAP Web UI.
2. Navigate to **Organizations** from the left-side menu.
3. Click **Add** to create a new organization.
4. Fill in the following details:
    * **Name:** (e.g., "Linux Patching Org")
    * **Description:** (e.g., "Organization for managing Linux patching")
5. Click **Save**.

**2. Grant Access to Users**

1. Go to the **Users** section under the **Access** tab of the organization.
2. Click **Add** to assign users to the organization.
3. Select users and assign roles:
    * **Admin:** Full access to the organization.
    * **Member:** Limited access to resources within the organization.
4. Save changes.

**3. Configure the Dynamic Inventory**

1. **Create a New Inventory:**
    * Navigate to **Inventories** in AAP.
    * Click **Add** and select **Inventory**.
    * Fill in the fields:
        * **Name:** (e.g., "Linux Patching Inventory")
        * **Organization:** Select the organization created in Step 1.
        * **Description:** (e.g., "Inventory based on ServiceNow CMDB data")
2. **Add a Dynamic Source:**
    * Go to the **Sources** tab under the inventory.
    * Click **Add Source**.
    * Fill in the following fields:
        * **Name:** (e.g., "ServiceNow Inventory")
        * **Source:** Select **Custom Script**.
        * Upload the dynamic inventory Python script or specify the script path in the **Source Configuration**.
    * Set the **Update Options:**
        * Enable **Overwrite** to replace existing hosts on sync.
        * Enable **Overwrite Vars** to update host variables.
    * Click **Save**.
3. **Test the Inventory Sync:**
    * Go back to the inventory page.
    * Click **Sync** to fetch the inventory from ServiceNow.
    * Verify the results in the **Hosts** tab.

**4. Divide Hosts into Groups**

* The dynamic inventory script organizes hosts into groups (e.g., `pool_1`, `pool_2`, etc.) based on the `u_pool` field.
* **Verify Host Groups:**
    * Navigate to the inventory.
    * Go to the **Groups** tab.
    * You should see groups named like `pool_1`, `pool_2`, etc.
* **Check Group Members:**
    * Click on a group name to view the list of hosts belonging to it.
    * Hosts will be divided automatically by the dynamic inventory script.
* **Use Groups as Limits:**
    * When creating a job template, use these groups as limits to target specific sets of hosts.

**5. Where to Find All Hosts Gathered by the Inventory**

1. Navigate to the **Inventories** section.
2. Select the inventory created in Step 3.
3. Go to the **Hosts** tab to see the full list of hosts fetched from ServiceNow.
4. Use the search bar to filter hosts by name or variables.
5. The `_meta` section in the inventory JSON output contains the host variables.

**6. How to Check the Source of the Inventory**

1. Navigate to the **Inventories** section.
2. Select the inventory created earlier.
3. Go to the **Sources** tab:
    * You’ll see the source (e.g., the name of your ServiceNow dynamic inventory script).
    * Click on the source name to view details such as:
        * Script path or URL.
        * Last sync status.
        * Update options.
4. **Check Last Sync Logs:**
    * Click on the **Activity Stream** tab for the inventory.
    * Review the logs to debug or verify the sync process.

**7. How to Select Hosts by u_pool in Job Templates**

1. **Create a Job Template:**
    * Navigate to **Templates** and click **Add**.
    * Choose **Job Template**.
    * Fill in the following fields:
        * **Name:** (e.g., "Linux Patching - Pool 1")
        * **Inventory:** Select the inventory created in Step 3.
        * **Project:** Select the project containing your playbooks.
        * **Playbook:** Choose the desired playbook.
        * In the **Limit** field, enter the group name (e.g., `pool_1`).
2. **Launch the Job Template:**
    * Run the template to patch hosts in the selected group.

This Markdown file provides a structured and detailed guide to setting up Linux patching in Ansible Automation Platform with ServiceNow CMDB as the data source.
