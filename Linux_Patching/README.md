# Linux Patching Playbook Overview

This document describes the purpose of each playbook in the Linux Patching Automation workflow. The workflow consists of four main steps: **precheck**, **stage**, **apply**, and **reboot**, which work together to streamline patching across Linux environments using Ansible Automation Platform (AAP).

---

## **1. Precheck (`precheck.yml`)**

### **Purpose:**
The precheck playbook validates the environment and ensures that all necessary preconditions are met before patching begins. It collects critical data, verifies system health, and prepares OS-specific settings.

### **Key Actions:**
- Ensures a valid inventory limit is defined in AAP.
- Gathers minimal facts about the target hosts (e.g., OS version and architecture).
- Sets the default Python version and determines OS-specific variables.
- Runs roles to:
  - Fix potential RPM database corruption.
  - Detect and address NFS hangs.

---

## **2. Stage (`stage.yml`)**

### **Purpose:**
The stage playbook prepares the system for patching by downloading and caching the required updates without applying them. This ensures patches are readily available for installation during the apply phase.

### **Key Actions:**
- Ensures a valid inventory limit is defined in AAP.
- Gathers minimal system facts.
- Refreshes subscription manager details.
- Sets OS-specific variables like version and architecture.
- Runs a role to:
  - Download and cache the patches for the system.

---

## **3. Apply (`apply.yml`)**

### **Purpose:**
The apply playbook installs the downloaded patches on the target hosts, ensuring that systems are up to date while minimizing downtime.

### **Key Actions:**
- Ensures a valid inventory limit is defined in AAP.
- Gathers minimal system facts.
- Sets OS-specific variables.
- Runs roles to:
  - Remove older kernels to save space and prevent conflicts.
  - Apply updates from the cached patches.

---

## **4. Reboot (`reboot.yml`)**

### **Purpose:**
The reboot playbook restarts the target systems after patches are applied to ensure all updates take effect and the system operates on the latest kernel and packages.

### **Key Actions:**
- Ensures a valid inventory limit is defined in AAP.
- Executes an unconditional reboot of the target hosts.

---

## **Additional Notes:**
- Each playbook is modular and designed to be executed as an independent template within AAP.
- Dynamic inventory created earlier is used to group hosts by `u_pool`. During execution, specify the `u_pool` as the limit in AAP to target specific groups of servers.
- The roles utilized in these playbooks are part of a pre-configured collection, ensuring reusability and maintainability.

Refer to the primary `README.md` for detailed setup and configuration instructions.
