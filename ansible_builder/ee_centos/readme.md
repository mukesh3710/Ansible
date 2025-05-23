# Custom Ansible Execution Environment with CentOS Stream 9 minimum image 
---
Prerequisites:
- Installation Steps for Prerequisites
```bash
# Enable the Ansible Automation Platform 2.4 repository
sudo subscription-manager repos --enable=ansible-automation-platform-2.4-for-rhel-9-aarch64-rpms

# Install Ansible Builder
sudo dnf install ansible-builder

# Install Ansible Runner
sudo dnf install ansible-runner

# Log in to Red Hat's container registry (required for base images like UBI if you switch later)
# This step might not be strictly necessary for quay.io/centos, but it's good practice for Red Hat ecosystem.
podman login registry.redhat.io
```
---
Execution Environment Structure:
- The core components of this custom Execution Environment are defined in the following files:
- base_ee.Dockerfile: Defines a custom base image (my_custom_ee_base) which includes system dependencies, Python 3.9 setup, and Ansible Core 2.15. This image serves as the foundation for the Ansible EE.
- execution-environment.yml: The main Ansible Builder definition file. It specifies the base image, Python, Galaxy, and system dependencies for the EE.
- requirement.yml: Defines Ansible collections to be installed (e.g., community.aws).
- requirement.txt: Specifies Python package dependencies for the EE (e.g., boto3, botocore).
- bindep.txt: Lists system-level package dependencies that are conditionally installed based on the platform.
- project/: This directory holds your Ansible playbooks, roles, and other Ansible content.
- inventory: Your Ansible inventory file.
---
Building the Custom Execution Environment:
- Create the Custom Base Image: First, build the my_custom_ee_base image using the base_ee.Dockerfile. This image pre-installs Python 3.9, its tools, and Ansible Core.
```bash
# Navigate to the directory containing base_ee.Dockerfile
# cd /path/to/your/custom_ee

podman build -t my_custom_ee_base:latest -f base_ee.Dockerfile .
```
- Define Dependencies: requirement.yml, requirement.txt & bindep.txt
- execution-environment.yml: This file instructs ansible-builder to use your custom base image and install additional dependencies.
- Build the Execution Environment Image: `ansible-builder build -t my_ee -v 3` . This command will create a new image tagged localhost/my_ee, which includes your custom base image, Ansible collections, and Python dependencies.
---
Running Playbooks with the Execution Environment:
- To execute an Ansible playbook using your newly built Execution Environment, ensure your playbooks are placed inside the project/ subdirectory.
- For example, if you have a ping.yml playbook and an inventory file: `ansible-runner run . --container-image=localhost/my_ee --inventory inventory/hosts -p ping.yml --process-isolation`
- ansible-runner run .: Tells ansible-runner to run in the current directory, which serves as the "private data directory."
- container-image=localhost/my_ee: Specifies the custom Execution Environment image to use.
- inventory inventory: Points to your inventory file.
- ping.yml: Specifies the playbook to run. ansible-runner will look for this inside the project/ directory.
- process-isolation: Runs the Ansible process in an isolated environment (requires podman or docker).
