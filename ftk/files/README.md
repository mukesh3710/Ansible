# FTK Role Artifacts

Place the platform-specific FTK installation assets in this directory before running the role:

- `ftk.crt`: TLS certificate placed directly in this directory.
- `rhel7/AD_Linux_RPM_Public.pgp` and `rhel7/ftk-agent_linux.rpm`
- `rhel8/AD_Linux_RPM_Public.pgp` and `rhel8/ftk-agent_linux.rpm`
- `rhel9/AD_Linux_RPM_Public.pgp` and `rhel9/ftk-agent_linux.rpm`

Files are intentionally omitted from source control. Supply your production copies (or symlink to a secure artifact repository) as part of your deployment process.

