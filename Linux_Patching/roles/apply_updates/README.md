# Apply Cached Patches Role

This Ansible role applies previously cached patches on RHEL 8 and RHEL 9 systems.

## Requirements
- Packages must be cached in `/var/cache/yum` for RHEL 8 or `/var/cache/dnf` for RHEL 9.

## Role Variables
No variables are required for this role.

## Example Playbook
```yaml
- hosts: all
  become: yes
  roles:
    - apply_updates
