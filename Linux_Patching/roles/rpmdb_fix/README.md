# Check RPM Database Role

This Ansible role checks if the RPM database (`rpmdb`) on a RHEL 8 or RHEL 9 system is corrupted and attempts to fix it.

## Requirements
- Ansible 2.9+
- RHEL 8 or RHEL 9 systems

## Role Variables
| Variable               | Default Value             | Description                           |
|------------------------|---------------------------|---------------------------------------|
| `rpmdb_check_command`  | `rpm --rebuilddb`         | Command to rebuild the RPM database. |
| `rpmdb_test_command`   | `rpm -qa`                | Command to test the RPM database.    |

## Example Playbook
```yaml
- hosts: all
  roles:
    - role: rpmdb_fix
