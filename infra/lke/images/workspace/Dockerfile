FROM codercom/code-server:latest

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip git curl && \
    rm -rf /var/lib/apt/lists/*

USER coder

ARG WORKSHOP_REPO=https://github.com/akamai-developers/ai-agents-workshop.git
ARG WORKSHOP_REF=main

# Fetch the specific ref (branch name or commit SHA) so build-image.sh can pin
# to a SHA for cache-busting. `git clone --branch` only accepts branches/tags,
# so we init + fetch the ref directly — works for both branch names and SHAs.
RUN mkdir -p /home/coder/workshop && cd /home/coder/workshop && \
    git init -q && \
    git remote add origin ${WORKSHOP_REPO} && \
    git fetch --depth=1 origin ${WORKSHOP_REF} && \
    git checkout -q FETCH_HEAD && \
    python3 -m venv .venv && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt

RUN code-server --install-extension ms-python.python

# Put the venv on PATH so terminals/processes find nba-stats-mcp and other entry points
# without needing to source .venv/bin/activate.
ENV PATH="/home/coder/workshop/.venv/bin:${PATH}"

WORKDIR /home/coder/workshop

EXPOSE 8080
