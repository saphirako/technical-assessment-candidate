# Project Instructions

## Dev environment

All build, run, and database work happens inside the devcontainer, on rootless Podman (Bazzite). The devcontainer CLI shells out to a `docker` binary on `PATH`, so the host carries a one-time shim to `podman`:

```bash
printf '#!/bin/sh\nexec podman "$@"\n' > ~/.local/bin/docker && chmod +x ~/.local/bin/docker
```

Also required on the host: the devcontainer CLI (`npm install -g @devcontainers/cli`) and a compose provider — this machine uses `~/.docker/cli-plugins/docker-compose`, which `podman compose` picks up automatically.

Never run `poetry`, `yarn`, `npm`, or `python` directly on the host — the toolchain only exists inside the container.

### Bring the stack up

```bash
bash .devcontainer/worktree_startup.sh
```

Idempotent: returns quickly when the stack is already running. OpenCode Desktop worktrees run this automatically in the background; its log is at `.devcontainer/devcontainer_up.log`. If a command fails because the stack isn't up yet, run the command above and retry.

The stack runs on the committed `bazzite/devcontainer.json`, which points at `docker-compose.bazzite.yml` — a compose file that builds off the portable base via `include:` and layers on the SELinux and rootless-uid settings. If the base `devcontainer.json` changes, regenerate the twin: `devcontainer read-configuration --workspace-folder . | jq 'del(.configuration.configFilePath) | .configuration | .dockerComposeFile = "../docker-compose.bazzite.yml"' > .devcontainer/bazzite/devcontainer.json`. Plain `devcontainer up --workspace-folder .` uses only the base compose and fails on this host's rootless Podman setup — always go through the startup script.

### Run everything inside

```bash
devcontainer exec --workspace-folder . poetry install
devcontainer exec --workspace-folder . poetry run python backend/app.py
devcontainer exec --workspace-folder . yarn dev
```

### Ports (published to the host)

| Service         | URL                                |
| ------------- | ---------------------------------- |
| Flask backend   | http://localhost:8000              |
| Vite frontend   | http://localhost:5173              |
| PostgreSQL      | localhost:5432 (postgres/password) |
| MongoDB         | localhost:27017                    |

Inside the container the hosts are `postgres` and `mongodb`. Full env lives in `.devcontainer/devcontainer.env`.

### Secrets

Copy `backend/secrets.json.example` to `backend/secrets.json` and fill in the API key and server URL provided by the interviewer. `secrets.json` is gitignored.

### Worktrees

Ports are fixed, so only one worktree's stack can run at a time. Before bringing up another worktree's stack, stop the running one (`podman ps`, then `podman stop` its app/postgres/mongo containers).
