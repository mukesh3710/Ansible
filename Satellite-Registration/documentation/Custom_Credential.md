## Custom Credential Type

1. Go to AWX → Administration → Credential Types → Add.
2. Define something like this:

Input configuration (YAML):
```yaml
fields:
  - id: activation_key
    type: string
    label: Activation Key
  - id: bearer_token
    type: string
    label: Bearer Token
    secret: true
required:
  - activation_key
  - bearer_token
```
Injector configuration (YAML):
```yaml
env:
  ACTIVATION_KEY: '{{ activation_key }}'
  BEARER_TOKEN: '{{ bearer_token }}'
```
Save it as “Satellite Registration” credential type.

Now when you create a Credential with this type, you’ll have two fields:

Activation Key

Bearer Token (masked/secret).

Your playbook can then safely reference:
```yaml
vars:
  activation_key: "{{ lookup('env', 'ACTIVATION_KEY') }}"
  bearer_token: "{{ lookup('env', 'BEARER_TOKEN') }}"
```
