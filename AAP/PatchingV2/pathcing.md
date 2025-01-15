# Linux Patching Automation

This project automates the Linux patching process using Ansible playbooks and roles. The patching workflow includes four key steps: precheck, stage, apply, and reboot. The Ansible Automation Platform (AAP) is used to execute these steps dynamically, leveraging a previously created inventory grouped by `u_pool` names.

## **Directory Structure**

```plaintext
Linux_Patching/
├── ansible.cfg
├── collections/
│   └── requirements.yml
├── vars/
│   └── patchdefs.yml
├── playbooks/
│   ├── precheck.yml
│   ├── stage.yml
│   ├── apply.yml
│   └── reboot.yml
├── roles/
│   ├── healthcheck/
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   └── defaults/
│   │       └── main.yml
│   ├── rpmdb_fix/
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   └── defaults/
│   │       └── main.yml
│   ├── nfs_check_hang/
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   └── defaults/
│   │       └── main.yml
│   ├── download_patches/
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   └── defaults/
│   │       └── main.yml
│   ├── kernel_cleanup/
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   └── defaults/
│   │       └── main.yml
│   └── apply_updates/
│       ├── tasks/
│       │   └── main.yml
│       └── defaults/
│           └── main.yml
└── README.md
```

---

## **Ansible Configuration (`ansible.cfg`):**
Define the necessary configurations for your Ansible setup:
```ini
[defaults]
collections_paths = ./collections
roles_path = ./roles
host_key_checking = False
forks = 20

[ssh_connection]
retries = 3
pipelining = True
```

---

## **Collections (`collections/requirements.yml`):**
Specify required Ansible collections and roles:
```yaml
collections:
  - name: ansible.posix
  - name: community.general
roles:
  - name: linux_patching_roles
    src: https://github.com/example-repo/linux_patching_roles.git
```

---

## **Variables (`vars/patchdefs.yml`):**
Define patching-related variables based on OS versions:
```yaml
repos_enable:
  rhel_8:
    - rhel-8-server-rpms
  rhel_9:
    - rhel-9-server-rpms

repos_disable:
  rhel_8:
    - rhel-8-beta-rpms
  rhel_9:
    - rhel-9-beta-rpms
```

---

## **Playbooks**

### **1. Precheck (`precheck.yml`)**
Performs pre-patching checks.
```yaml
---
- name: Precheck for Linux patching
  hosts: all
  vars_files:
    - vars/patchdefs.yml
  pre_tasks:
    - name: Check if limit is defined
      fail:
        msg: "Limit must be defined when running this playbook."
      when: ansible_limit is undefined

    - name: Gather minimal facts
      setup:
        gather_subset:
          - min
        gather_timeout: 10

    - name: Set OS-specific variables
      set_fact:
        os_vars:
          os_version: "{{ ansible_distribution_major_version }}"
          architecture: "{{ ansible_architecture }}"

  roles:
    - healthcheck
    - rpmdb_fix
    - nfs_check_hang
```

### **2. Stage (`stage.yml`)**
Stages patches by downloading them.
```yaml
---
- name: Stage patches for Linux servers
  hosts: all
  vars_files:
    - vars/patchdefs.yml
  pre_tasks:
    - name: Check if limit is defined
      fail:
        msg: "Limit must be defined when running this playbook."
      when: ansible_limit is undefined

    - name: Gather minimal facts
      setup:
        gather_subset:
          - min
        gather_timeout: 10

    - name: Refresh subscription manager
      command: subscription-manager refresh

    - name: Set OS-specific variables
      set_fact:
        os_vars:
          os_version: "{{ ansible_distribution_major_version }}"
          architecture: "{{ ansible_architecture }}"

  roles:
    - download_patches
```

### **3. Apply (`apply.yml`)**
Applies the downloaded patches.
```yaml
---
- name: Apply patches for Linux servers
  hosts: all
  vars_files:
    - vars/patchdefs.yml
  pre_tasks:
    - name: Check if limit is defined
      fail:
        msg: "Limit must be defined when running this playbook."
      when: ansible_limit is undefined

    - name: Gather minimal facts
      setup:
        gather_subset:
          - min
        gather_timeout: 10

    - name: Set OS-specific variables
      set_fact:
        os_vars:
          os_version: "{{ ansible_distribution_major_version }}"
          architecture: "{{ ansible_architecture }}"

  roles:
    - kernel_cleanup
    - apply_updates
```

### **4. Reboot (`reboot.yml`)**
Reboots the servers.
```yaml
---
- name: Reboot Linux servers
  hosts: all
  gather_facts: false
  tasks:
    - name: Ensure limit is defined
      fail:
        msg: "Limit must be defined when running this playbook."
      when: ansible_limit is undefined

    - name: Reboot the server
      reboot:
        reboot_timeout: 300
```

---

## **Roles Structure**
Roles are organized as follows:
```plaintext
roles/
├── healthcheck/
├── rpmdb_fix/
├── nfs_check_hang/
├── download_patches/
├── kernel_cleanup/
└── apply_updates/
```
Each role contains:
- `tasks/main.yml`: Defines the tasks for the role.
- `defaults/main.yml`: Holds default variables for the role.

---

## **Execution Environment**
Use a standalone Linux jump server to execute these playbooks. Ensure the root public key is distributed to all target hosts for passwordless SSH access.

### **Create Execution Environment**
1. Install dependencies:
   ```bash
   podman build -t ansible-ee .
   ```
2. Push the image to your AAP environment.

---

## **Usage**
Run the playbooks from AAP, specifying the `u_pool` name in the limit field to target specific groups.
