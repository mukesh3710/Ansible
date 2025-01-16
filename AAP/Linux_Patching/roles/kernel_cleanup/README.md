# Clean Kernels Role

This Ansible role removes all but the latest 2 kernels on RHEL 8 and RHEL 9 systems.

## Requirements
- RHEL 8 or RHEL 9
- `yum` and `repoquery` commands must be available.

## Role Variables
No variables are required for this role.

## Example Playbook
```yaml
- hosts: all
  become: yes
  roles:
    - kernel_cleanup
