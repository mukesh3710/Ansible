# Readme

## This is a solution for a bash script and the associated Python program that will dynamically generate and manage the inventory for patching. The script uses arguments for flexibility and fetches credentials from an external file for security.

---

# Usage Examples

## Generate and save inventory:
```bash
inventory.sh --generate
```

## List full inventory:
```bash
inventory.sh --list
```

## List all groups:
```bash
inventory.sh --groups
```

## List hosts in a specific group:
```bash
inventory.sh --group pool_1
```

## List groups a host belongs to:
```bash
inventory.sh --host host_name
```

## List hosts with a specific prefix:
```bash
inventory.sh --prefix web,app
```
