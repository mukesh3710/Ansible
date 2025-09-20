# Ansible Complex Linux Post Build Role

## Overview

This repository provides a **complex, reusable Ansible role** designed for post-build configuration and hardening of Linux servers, specifically **RHEL 8**. It demonstrates advanced Ansible concepts including variables, secrets, facts, loops, conditions, handlers, error handling, custom Jinja2 templates, complex plays, host patterns, file and role imports, and usage of content collections from Ansible Galaxy.

The main automation tasks include:

- **System update**
- **User management** with secure SSH key handling and sudo setup
- **Filesystem creation** on LVM
- **Kernel hardening**
- **MongoDB deployment**, with test data using Jinja2
- **Simple web application deployment** (that connects to MongoDB)
- **Firewall disabling**
- **Robust, modular, and reusable role structure**

---

## Directory Structure

```
roles/
  post_build/
    defaults/         # Default variables for the role
    vars/             # Additional variables (like kernel tunables)
    secrets/          # Secret variables (to be encrypted with ansible-vault)
    tasks/            # Task files split by function, imported in main.yml
    handlers/         # Handlers (e.g., reload sysctl)
    templates/        # Jinja2 templates for webapp and MongoDB data
    files/            # Static files (e.g., SSH public key)
    meta/             # Role dependencies (Galaxy collections)
playbooks/
  site.yml            # Main playbook to execute the role
requirements.yml      # Required Ansible collections (e.g., community.general)
README.md             # This documentation
```

---

## Step-by-Step Explanation

### 1. **Ansible Galaxy Collections**

We use modules from the [community.general](https://galaxy.ansible.com/community/general) collection (for LVM, etc.).  
Install dependencies before running the playbook:

```bash
ansible-galaxy collection install -r requirements.yml
```

---

### 2. **Secrets Management**

Sensitive data (such as SSH public keys) is stored in `roles/post_build/secrets/vault.yml` and should be **encrypted** with `ansible-vault`:

```bash
ansible-vault encrypt roles/post_build/secrets/vault.yml
```

---

### 3. **Variables and Facts**

- **defaults/main.yml**: General variables (user names, filesystem sizes, etc.).
- **vars/main.yml**: Kernel hardening sysctl parameters.
- **facts**: Ansible facts are used for dynamic host information (e.g., IP addresses for webapp links).

---

### 4. **Role Tasks**

Each major function is a separate task file, imported into the main role task file.

#### a. **System Update**
  - Updates all system packages to the latest version.

#### b. **User Management**
  - Creates a `test` user.
  - Copies a public SSH key (from secrets or file).
  - Adds a sudoers entry for passwordless root access.

#### c. **Filesystem Management**
  - Creates new logical volumes on the `rhel` volume group.
  - Formats and mounts `/opt/test`, `/opt/mongo`, and `/opt/web`.

#### d. **Kernel Hardening**
  - Applies sysctl tunables for IP spoofing protection, disables ICMP redirects, and (optionally) disables IPv6.
  - Changes are made persistent and reloaded using handlers.

#### e. **MongoDB Deployment**
  - Installs MongoDB, ensures it is running.
  - Creates a `dbid` user.
  - Creates `/opt/mongo` filesystem.
  - Uses a Jinja2 template to generate JSON test data and imports it into MongoDB.
  - Verifies MongoDB connectivity.

#### f. **Web Application Deployment**
  - Creates a `webid` user.
  - Prepares `/opt/web` filesystem.
  - Deploys a simple HTML webapp using a Jinja2 template, which displays MongoDB connection info.
  - Launches a basic Python HTTP server as the web application.
  - Outputs the connection URL based on the server's IP.

#### g. **Firewall**
  - Stops and disables the firewall service.

#### h. **Handlers**
  - Example: Reloads sysctl if kernel parameters change.

#### i. **Error Handling**
  - Tasks for MongoDB import and other critical steps use `register`, `failed_when`, and `ignore_errors` for robust control.

#### j. **Loops and Conditions**
  - Used in kernel parameter hardening and other areas for flexibility and code reuse.

#### k. **Templates**
  - `mongodata.j2`: Provides test data for MongoDB.
  - `webapp.j2`: HTML template for the web application.

---

### 5. **Playbook Usage**

**Example:** `playbooks/site.yml`

```yaml
- name: Linux Post Build Tasks
  hosts: "rhel8_hosts:&datacenter"
  become: true
  roles:
    - post_build
```

- **hosts**: You can use any host pattern that matches your target hosts (e.g., `"rhel8_hosts"`, `"all"`, etc.).
- **become: true**: Ensures all tasks run with elevated privileges where required.

Run with:

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

---

## How to Use This Project

1. **Clone or copy the role and playbook structure** into your Ansible project.
2. **Customize variables** in `defaults/main.yml` and `vars/main.yml` as needed.
3. **Put your public SSH key** in `roles/post_build/files/id_rsa.pub` or encrypted in the vault.
4. **Install required collections** with `ansible-galaxy collection install -r requirements.yml`.
5. **Encrypt secrets** (`vault.yml`) with `ansible-vault encrypt`.
6. **Target the right hosts** in your inventory and playbook.
7. **Run the playbook** as shown above.

---

## Advanced Features Demonstrated

- **Variables, facts, secrets** (with vault)
- **Loops, conditions, and handlers**
- **Error handling and task control**
- **Custom files and Jinja2 templates**
- **Complex playbook and role structure**
- **Host patterns and dynamic inventory**
- **File/role imports and modularity**
- **Reusing roles**
- **Ansible Galaxy collections**
- **Content collection modules (e.g., LVM management)**

---

## Customization

- **MongoDB/WebApp**: You can replace the simple webapp and MongoDB setup with your own stack.
- **Hardening**: Adjust kernel parameters as needed in `vars/main.yml`.
- **Filesystem**: Change volume group, mount points, and sizes in `defaults/main.yml`.

---

## Troubleshooting

- Ensure that the `rhel` volume group exists and has enough free space.
- If a package/module is missing, install the required collection or RPM.
- Use `--ask-vault-pass` if your vault is encrypted.
- Check Ansible version compatibility; this role targets Ansible 2.9+.

---

## Authors

- **Your Name** (customize as needed)
- Inspired by real-world Linux post-build automation tasks

---

## License

MIT License (or your choice)
