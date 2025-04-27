# Readme

- Separation of Concerns: The bash script only handles environment preparation and delegates logic to Python.
- Flexibility: Adding new features or logic is easier in Python.
- Security: Credentials are sourced securely from the cred_file and passed via environment variables.
- Maintainability: Code is modular and well-structured for enhancements.

# Usage Examples

## Generate and save inventory:
```bash
inventory.sh --action --generate --output /tmp/patching_inventory.json
```

## List full inventory:
```bash
inventory.sh --action --list
```

## List all groups:
```bash
inventory.sh --action --groups
```

## List hosts in a specific group:
```bash
inventory.sh --action --group pool_1
```

## List groups a specific host belongs to:
```bash
inventory.sh --action --host host_name
```

## List hosts with specific prefixes:
```bash
inventory.sh --action --prefix web,app
```

