### VM auto provisioning in VMware with Ansible 
---
Prerequisites:
- A VM (virtual machine), that will be used as an ansible controller node, with network access to a VMware vCenter.
- A VMware vCenter and VMware vSphere hypervisor platform or a standalone ESXi server.
- A VMware vCenter user with enough privileges for creating and administering VMs.
- Installed pyvmomi package. It is the Python SDKs for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.
- Python >= 3.6 must be installed. (v3.9) 
- Installed Ansible tool (v2.15).
- Installed community.vmware ansible collection. `ansible-galaxy collection install community.vmware`
---
Prepare the VM for Customization: 
- Create VM template, which will be used for creating new VMs in the ansible playbooks
- A VM template should have installed VMware tools package, perl package and in order to allow guest customizations on a Linux VM. If guest customization is not enabled, ansible modules can not set network settings on the VM as they are defined in the ansible-playbook file.
```bash
# Install Perl
dnf install -y perl

# Enable vmware-tools customization (Important)
yum install -y open-vm-tools
systemctl enable --now vmtoolsd

# General Cleanup
yum clean all
rm -rf /tmp/*
rm -rf /var/tmp/*
truncate -s 0 /var/log/wtmp /var/log/lastlog
rm -f /etc/udev/rules.d/70-persistent-net.rules
rm -f /etc/ssh/ssh_host_*

- Set Networking to DHCP (or your default provisioning config)
- Shutdown the VM and create a template
```
---
Ansible Role: Deploy VMs on VMware:
- This Ansible project automates the deployment of virtual machines from templates in a VMware vSphere environment using the `community.vmware.vmware_guest` module. It is designed to run on `localhost` and leverages `host_vars` and `group_vars` to enable dynamic and scalable VM builds with shared and unique configurations.

```bash
.
├── deploy_vm.yml # Main playbook
├── group_vars/
│ └── all.yml # Global shared variables (datacenter, cluster, template, etc.)
├── host_vars/
│ ├── vm01.yml # VM-specific settings for vm01
│ └── vm02.yml # VM-specific settings for vm02
├── inventory/
│ └── hosts.ini # Inventory file listing VM names
├── roles/
│ └── deploy_vm/
│ └── tasks/
│ └── main.yml # Role tasks to deploy the VMs
└── vars/
└── password.yml # Vault-encrypted vCenter password
```
---
Ansible Vault for Passwords:
- You must encrypt the vCenter password using Ansible Vault:
```bash
ansible-vault encrypt vars/password.yml
cat vars/password.yml # example
vcenter_password: "SuperSecretPassword"
```
- Use --ask-vault-password or --vault-password-file when running the playbook.
---
Running the Playbook
```
ansible-playbook -i inventory/hosts.ini deploy_vm.yml --ask-vault-password
ansible-playbook -i inventory/hosts.ini deploy_vm.yml --vault-password-file ~/.vault_pass.txt
```
---
### Support
For questions, feel free to ask or extend this role with:
- Custom post-deploy tasks (cloud-init, guest customization)
- Integration with CI/CD or GitOps pipelines
