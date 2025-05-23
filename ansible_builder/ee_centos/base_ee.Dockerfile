# base_ee.Dockerfile
FROM quay.io/centos/centos:stream9

# Install required system packages
RUN dnf -y update && \
    dnf -y install gcc gcc-c++ make wget tar git \
                   python3.9 python3.9-devel python3.9-pip python3.9-setuptools && \
    dnf clean all

# Create Python symlinks
RUN ln -sf /usr/bin/python3.9 /usr/bin/python && \
    ln -sf /usr/bin/python3.9 /usr/bin/python3 && \
    ln -sf /usr/bin/pip3.9 /usr/bin/pip

# Upgrade pip, setuptools, and wheel
RUN python3 -m pip install --upgrade pip setuptools wheel

# Install ansible-core
RUN python3 -m pip install ansible-core==2.15

# Optional: Add any other common utilities or configurations you need in your base EE
# For example, you might want to install vim, less, etc.
# RUN dnf -y install vim less && dnf clean all

CMD ["/usr/bin/python3"]
