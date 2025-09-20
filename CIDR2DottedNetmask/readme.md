# Ansible Playbook: Convert CIDR to Dotted Netmask for Network Configurations

This playbook demonstrates how to use the `ansible.utils.ipaddr` filter to convert IP addresses in CIDR notation (e.g., `192.0.2.1/24`) into the classic dotted-quad netmask (e.g., `255.255.255.0`). This is useful when configuring network interfaces or services that require the netmask in dotted decimal format.

## Features

- **Extracts IP Address and Netmask:** Takes a CIDR input and splits it into IP address and netmask.
- **Renders a Network Interface Configuration File:** Uses a Jinja2 template to create a config file with the extracted values.
- **Easily Customizable:** Change the input CIDR or template for your needs.

---

## Requirements

- **Ansible 2.15+** (Recommended: 2.16+ for best compatibility)
- **ansible.utils Collection**
- **Python library `netaddr`** installed on the Ansible controller

### Install Requirements

```sh
ansible-galaxy collection install ansible.utils
pip install netaddr
```

---

## Files

### 1. Playbook: `convert_cidr_to_netmask.yml`

```yaml
---
- name: Convert CIDR Network Info to Dotted Netmask with ansible.utils.ipaddr
  hosts: all
  gather_facts: false
  vars:
    # Override this with --extra-vars "network_cidr=10.1.1.100/22" as needed
    network_cidr: "192.0.2.1/24"
  tasks:
    - name: Extract IP and Netmask from CIDR
      set_fact:
        ip_address: "{{ network_cidr | ansible.utils.ipaddr('address') }}"
        netmask: "{{ network_cidr | ansible.utils.ipaddr('netmask') }}"

    - name: Show extracted IP and netmask
      debug:
        msg:
          - "IP Address: {{ ip_address }}"
          - "Netmask: {{ netmask }}"

    - name: Render a config file with classic netmask format
      ansible.builtin.template:
        src: network_interface.conf.j2
        dest: /tmp/network_interface.conf
```

### 2. Template: `network_interface.conf.j2`

```jinja
# Network Interface Configuration

DEVICE=eth0
BOOTPROTO=static
IPADDR={{ ip_address }}
NETMASK={{ netmask }}
ONBOOT=yes
```

---

## Usage

1. **Clone or copy the playbook and template to your Ansible project directory.**
2. **Edit the `network_cidr` variable** in the playbook, or override it at runtime:
   ```sh
   ansible-playbook -i hosts.ini convert_cidr_to_netmask.yml --extra-vars "network_cidr=10.1.1.100/22"
   ```
3. **Run the playbook:**
   ```sh
   ansible-playbook -i hosts.ini convert_cidr_to_netmask.yml
   ```
4. **Result:** The file `/tmp/network_interface.conf` will be created on the target host with the correct IP and netmask.

---

## Troubleshooting

- **Missing `netaddr` error:**  
  Install with `pip install netaddr` in the Python environment used by Ansible.
- **Collection compatibility warning:**  
  Upgrade Ansible or use a compatible version of `ansible.utils`.
- **File not found on target:**  
  Ensure you are checking the correct host (`/tmp/` on the remote, not local).

---

## Customization

- Use your own template by editing or replacing `network_interface.conf.j2`.
- Extend the playbook to configure multiple interfaces or use as a role for larger projects.

---

## References

- [ansible.utils.ipaddr documentation](https://docs.ansible.com/ansible/latest/collections/ansible/utils/ipaddr_filter.html)
- [netaddr PyPI](https://pypi.org/project/netaddr/)
- [Ansible Collections](https://galaxy.ansible.com/ansible/utils)

---

**Author:** [mukesh3710](https://github.com/mukesh3710)
