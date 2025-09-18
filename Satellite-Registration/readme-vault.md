# Register to Satellite — Secure Ansible Playbook

This repository contains an Ansible playbook to register hosts to Red Hat Satellite / Foreman using the `theforeman.foreman.registration_command` module and an Ansible Vault to keep credentials secret.

## What this playbook does
1. Reads `/etc/node.class` (if present) and determines the lifecycle environment:
   - If `node.class` contains `Development` or `Production`, it uses that value.
   - Otherwise it falls back to `Library`.
2. Calls the Foreman/Satellite API (via `theforeman.foreman.registration_command`) to generate a host registration script/command tailored with activation keys, location, OS, etc.
3. Executes the generated registration command on the target host.

## Security design
- **No secrets are hard-coded** in the playbook.
- Use **Ansible Vault** for `foreman_username` and `foreman_password`.
- Prefer using a service account with limited permissions for the registration operation.
- If running in AWX/Tower, consider:
  - Storing `foreman_username`/`foreman_password` in the AWX credentials store and passing them as extra vars (or using a credential lookup workflow).
  - Using certificate-based TLS verification (`validate_certs: true`) and avoiding `validate_certs: false` in production.

## Prerequisites

### On the control node
- Ansible (2.9+ recommended, or the Ansible version that provides the `theforeman.foreman` collection you will use).
- Install the Foreman collection:
  ```bash
  ansible-galaxy collection install theforeman.foreman
