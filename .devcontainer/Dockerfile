# Hardened Dev Container for Agentic Development
# Based on security best practices from the functional specification

FROM mcr.microsoft.com/devcontainers/python:3.12

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        build-essential \
        curl \
        git \
        jq \
        vim \
        less \
        ca-certificates \
        gnupg \
        lsb-release \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install OpenShift CLI (oc)
RUN curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable/openshift-client-linux.tar.gz \
    && tar -xzf openshift-client-linux.tar.gz -C /usr/local/bin \
    && rm openshift-client-linux.tar.gz \
    && chmod +x /usr/local/bin/oc /usr/local/bin/kubectl

# Set up vscode user (non-root)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Ensure vscode user exists with correct permissions
RUN if ! id -u $USERNAME > /dev/null 2>&1; then \
        groupadd --gid $USER_GID $USERNAME \
        && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME; \
    fi

# Install Python packages globally for all users
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

# Create workspace directory with proper permissions
RUN mkdir -p /workspace && chown -R $USERNAME:$USERNAME /workspace

# Security: Shell hardening
# Prevent sensitive environment variable leaks
RUN echo 'export HISTCONTROL=ignoreboth:erasedups' >> /home/$USERNAME/.bashrc \
    && echo 'export HISTIGNORE="*API_KEY*:*SECRET*:*PASSWORD*:*TOKEN*"' >> /home/$USERNAME/.bashrc

# Set working directory
WORKDIR /workspace

# Switch to non-root user for all subsequent operations
USER $USERNAME

# Health check (optional, useful for monitoring)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD pgrep python > /dev/null || exit 1

# Default command
CMD ["/bin/bash"]
