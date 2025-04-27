# Satellite Package Cache Role

This Ansible role downloads and caches all packages from a Satellite server in the appropriate cache directory (`/var/cache/yum` for RHEL 8 and `/var/cache/dnf` for RHEL 9).

## Requirements
- RHEL 8 or RHEL 9
- Systems must be registered with the Satellite server.
- `yum` or `dnf` must be installed.

## Role Variables
| Variable          | Description                              |
|-------------------|------------------------------------------|
| `repos_enable`    | List of repositories to enable for each RHEL version. |
| `repos_disable`   | List of repositories to disable for each RHEL version. |
| `cache_dir_rhel8` | Cache directory for RHEL 8 (`/var/cache/yum`). |
| `cache_dir_rhel9` | Cache directory for RHEL 9 (`/var/cache/dnf`). |

## Example Playbook
```yaml
- hosts: all
  become: yes
  vars:
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
  roles:
    - download_patches
