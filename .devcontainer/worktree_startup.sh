#!/usr/bin/env bash
set -euo pipefail

WORKTREE="${OPENCODE_WORKTREE_PATH:-$(cd "$(dirname "$0")/.." && pwd)}"
UP_LOG="$WORKTREE/.devcontainer/devcontainer_up.log"
BAZZITE_CONFIG="$WORKTREE/.devcontainer/bazzite/devcontainer.json"

# The compose provider tags built images docker.io/library/<name>, but the
# devcontainer CLI's UID-remap build references localhost/<name>; alias and retry.
devcontainer up --workspace-folder "$WORKTREE" --config "$BAZZITE_CONFIG" >"$UP_LOG" 2>&1 || {
    BASE_IMAGE="$(grep -o 'BASE_IMAGE=[^ ]*' "$UP_LOG" | tail -1 | cut -d= -f2)"
    if [[ "$BASE_IMAGE" == localhost/* ]]; then
        podman tag "docker.io/library/${BASE_IMAGE#localhost/}:latest" "$BASE_IMAGE:latest"
        devcontainer up --workspace-folder "$WORKTREE" --config "$BAZZITE_CONFIG" >>"$UP_LOG" 2>&1
    else
        exit 1
    fi
}
echo "devcontainer provisioning finished; log: $UP_LOG"
