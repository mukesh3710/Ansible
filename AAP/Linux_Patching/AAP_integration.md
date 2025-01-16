

## Prerequisites

* **Jump Server Setup:** Ensure the jump server has passwordless SSH access to all Linux client hosts. This is already configured using the shared public key.
* **Dynamic Inventory:** Confirm the dynamic inventory script (from ServiceNow) is already integrated into AAP.
* **Execution Environment:** Build and upload the execution environment with all required dependencies (e.g., ansible.posix, community.general collections).
* **Credential Setup:** Create a credential in AAP for the jump server SSH private key.
