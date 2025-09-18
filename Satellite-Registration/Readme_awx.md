# AWX: Register hosts to Red Hat Satellite (secure, token-based)

This repo contains an Ansible playbook that registers hosts to a Red Hat Satellite server using an AWX-stored **Bearer token** and **Activation Key** (both stored as AWX credentials). The playbook avoids hard-coded secrets and uses the Ansible `uri` module to fetch the registration script.

## Files
- `register_to_satellite_awx.yml` — main secure playbook.
- `README.md` — this file.

## Overview
Flow:
1. AWX injects `satellite_bearer_token` and `satellite_activation_key` from a custom credential.
2. Playbook reads `/etc/node.class` to choose lifecycle environment `Development`, `Production`, or fallback `Library`.
3. Playbook calls Satellite registration endpoint with the token and activation key and receives a registration script.
4. The script is written to a secure temp file on the host, executed, then removed.
5. Sensitive tasks use `no_log: true` to avoid leaking secrets in AWX job output.

## AWX setup (summary)
1. **Create a Custom Credential Type** in AWX with fields:
   - `bearer_token` (secret)
   - `activation_key` (secret)
   Use injectors to map these as extra_vars:
