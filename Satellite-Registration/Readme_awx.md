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
(Example YAML for the Credential Type is provided in the documentation/Custom_Credential.md.)

2. **Create Credential Instance** of this type:
- Paste your Bearer token (JWT) and Activation Key.
- Save.

3. **Ensure Project & Inventory** exist and are configured.

4. **Create Job Template**:
- Playbook: `register_to_satellite_awx.yml`
- Attach:
  - The custom **Satellite API Token** credential (holds token & activation key)
  - A **Machine** credential used for SSH access to hosts
- Optionally set `extra_vars` to override defaults (e.g. `satellite_url`, `location_id`).

## Running
Launch the Job Template from AWX. The job output will show a short safe summary of the registration result but will not leak the token or returned registration script.

## Security notes
- **Do not** commit tokens to git.
- Use AWX credential store to hold secrets (recommended).
- Keep `no_log: true` for tasks that interact with the token or returned script.
- Prefer `validate_certs: true` in production and ensure AWX/control node trusts Satellite CA.
- Consider limiting the privileges of the token you use (use a service account/token with the minimal needed scopes).

## Troubleshooting
- If you receive errors from the Satellite endpoint:
- Test fetching the script from a control host using `curl` and the same token to validate connectivity.
- Check AWX job logs with `-vvv` (but remember `no_log` hides secrets).
- If AWX doesn't inject variables, confirm:
- The Credential Type `injectors.extra_vars` is configured correctly.
- The correct credential is attached to the Job Template.
- To see the generated `registration_url` for debugging, temporarily add a `debug` task for `registration_url` (but **do not** print the bearer token or returned script).

## Example Job Template Extra Vars (optional)
```yaml
satellite_url: "https://satellite.lab.local/register"
location_id: "4"
os_id: "2"
org_id: "3"
validate_certs: false
