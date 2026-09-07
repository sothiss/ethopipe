# Use official Python slim image
FROM python:3.12-slim

# Install system dependencies needed for python packages and development tools
# hadolint ignore=DL3008
# kics-scan ignore-line
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv (astral-sh) for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create a non-root user for development
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir -p /workspace \
    && chown -R $USERNAME:$USERNAME /workspace

# Set working directory inside the container
WORKDIR /workspace

USER $USERNAME
