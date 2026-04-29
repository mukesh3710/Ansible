## README

- Captures the FTK Ansible role layout now hosted at `ftk/` and explains how to place artifacts, run the role, and customize variables for RHEL 7/8/9 hosts, aligning with the repo state mirrored on GitHub.[^1]


# FTK Ansible Role

This repository packages an Ansible role that prepares storage, uploads signed packages, and installs the FTK agent on Red Hat Enterprise Linux 7, 8, and 9 systems.[^1]

## Requirements

- Ansible 2.14+ on the control node.
- Managed hosts using LVM (`lvm2`) and `systemd`, reachable via SSH.
- FTK RPMs, GPG public keys, and TLS certificate available to copy into the role.

## Repository Layout

```markdown
ftk/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── tasks/
│   └── main.yml
├── templates/
│   └── agent.config.j2
└── files/
    ├── README.md          # replace with your certificate once available
    └── rhel7|rhel8|rhel9/
        ├── AD_Linux_RPM_Public.pgp
        └── ftk-agent_linux.rpm
```

Place production copies of `ftk.crt`, version-specific RPMs, and PGP keys inside `ftk/files/` before running the role.

## Usage

1. Populate `inventory.ini` with target hosts and copy FTK assets into `ftk/files/`.
2. Create a playbook such as:

```yaml
- name: Deploy FTK agent
  hosts: ftk_targets
  gather_facts: true
  roles:
    - role: ftk
      vars:
        ftk_agent_configuration: |
          # Example overrides
          server_url = https://ftk.example.com
          node_name = {{ inventory_hostname }}
```

3. Run the play:

```bash
ansible-playbook -i inventory.ini deploy-ftk.yml
```

## Customization

- Adjust defaults in `ftk/defaults/main.yml` (VG names, LV size, filesystem type, services to disable, etc.).
- Override `ftk_agent_configuration` with environment-specific settings.
- Extend tasks or handlers to meet internal standards.

## Contributing

1. Fork and branch from `main`.
2. Implement and test changes (Molecule recommended).
3. Submit a pull request summarizing updates.

[^1]: [Plateform-Linux – ftk role](https://github.com/mukesh3710/Plateform-Linux/tree/main/ftk)
```
