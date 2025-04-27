# NFS Check Hang Role

This Ansible role checks for any unresponsive or hung NFS filesystems on a server.

## Requirements
- Ansible 2.9+
- Access to servers with NFS mounts

## Role Variables
| Variable                 | Default Value              | Description                                      |
|--------------------------|----------------------------|--------------------------------------------------|
| `nfs_mount_test_command` | `df -hT | grep nfs`        | Command to list NFS mounts.                     |
| `nfs_check_command`      | `timeout 5 ls -l {{ item }}` | Command to check if an NFS mount is responsive. |

## Example Playbook
```yaml
- hosts: all
  become: yes
  roles:
    - role: nfs_check_hang
