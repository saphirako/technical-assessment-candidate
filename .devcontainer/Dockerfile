ARG VARIANT=jammy
FROM mcr.microsoft.com/vscode/devcontainers/base:${VARIANT}

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libsqlite3-dev \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Prevents Python from writing pyc files and buffers stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

# Install Python 3.11+ (if not already available)
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and yarn using nvm. Keep NODE_VERSION in sync with .nvmrc at the repo root.
ENV NVM_DIR /home/vscode/.nvm
ENV NODE_VERSION 24.22.1
RUN mkdir -p $NVM_DIR && \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash && \
    . $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    nvm use default && \
    npm install -g yarn

ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Add NVM configuration to shell
RUN echo 'export NVM_DIR="$HOME/.nvm"' >> /home/vscode/.bashrc && \
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm' >> /home/vscode/.bashrc && \
    echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion' >> /home/vscode/.bashrc

# Switch to vscode user
USER vscode

# Install Poetry as vscode user
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Create python symlink for Poetry compatibility (Poetry looks for 'python' executable)
RUN mkdir -p /home/vscode/.local/bin && \
    ln -sf /usr/bin/python3.11 /home/vscode/.local/bin/python

ENV PATH="/home/vscode/.local/bin:${PATH}"

