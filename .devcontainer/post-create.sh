#!/usr/bin/env bash
# post-create.sh — Builds and installs openEMS from source inside the devcontainer.
# This runs once after the container is first created.
set -euo pipefail

OPENEMS_INSTALL_DIR="$HOME/opt/openEMS"
REPOS_DIR="$HOME/repos"
PROJECT_DIR="$REPOS_DIR/openEMS-Project"

echo "================================================================"
echo " openEMS post-create install"
echo " Install prefix : $OPENEMS_INSTALL_DIR"
echo " Source clone   : $PROJECT_DIR"
echo "================================================================"
echo ""

# ── 0. Claude Code — bypass permission prompts inside the container ────────
# Writes to ~/.claude/settings.json (the vscode user's home dir, which lives
# entirely inside the container and is NOT a bind-mount from the host).
# "bypassPermissions" disables all tool-use confirmation prompts so Claude
# can freerun bash, edits, and writes without pausing for approval.
# This setting is intentionally container-scoped and is never committed.
echo "[0/5] Configuring Claude Code for freerun (bypassPermissions)..."
mkdir -p "$HOME/.claude"
cat > "$HOME/.claude/settings.json" << 'EOF'
{
  "defaultMode": "bypassPermissions"
}
EOF
echo "      ~/.claude/settings.json written."
echo ""

# ── 1. Clone openEMS-Project ───────────────────────────────────────────────
mkdir -p "$REPOS_DIR"
if [ -d "$PROJECT_DIR/.git" ]; then
    echo "[1/5] openEMS-Project already cloned — pulling latest..."
    git -C "$PROJECT_DIR" pull --recurse-submodules
else
    echo "[1/5] Cloning openEMS-Project (recursive)..."
    git clone --recursive https://github.com/thliebig/openEMS-Project.git "$PROJECT_DIR"
fi

# ── 2. Build openEMS with Python bindings ─────────────────────────────────
echo ""
echo "[2/5] Building openEMS (this takes 10–30 minutes)..."
cd "$PROJECT_DIR"
./update_openEMS.sh "$OPENEMS_INSTALL_DIR" --python

# ── 3. Activate the openEMS venv in shell profile ─────────────────────────
# update_openEMS.sh --python installs CSXCAD + openEMS Python bindings into
# an isolated venv at $OPENEMS_INSTALL_DIR/venv — no separate setup.py needed.
echo ""
echo "[3/5] Wiring openEMS venv into ~/.bashrc..."

VENV="$OPENEMS_INSTALL_DIR/venv"
BASHRC="$HOME/.bashrc"

add_if_missing() {
    local line="$1"
    grep -qxF "$line" "$BASHRC" 2>/dev/null || echo "$line" >> "$BASHRC"
}

add_if_missing "# openEMS"
add_if_missing "source \"$VENV/bin/activate\""
add_if_missing "export PATH=\"$OPENEMS_INSTALL_DIR/bin:\$PATH\""
add_if_missing "export LD_LIBRARY_PATH=\"$OPENEMS_INSTALL_DIR/lib:\$LD_LIBRARY_PATH\""

# Activate immediately for the rest of this script
# shellcheck source=/dev/null
source "$VENV/bin/activate"
export PATH="$OPENEMS_INSTALL_DIR/bin:$PATH"
export LD_LIBRARY_PATH="$OPENEMS_INSTALL_DIR/lib:${LD_LIBRARY_PATH:-}"

# ── 4. (reserved) ─────────────────────────────────────────────────────────
echo "[4/5] Paths wired."

# ── Smoke test ─────────────────────────────────────────────────────────────
echo ""
echo "[5/5] Smoke test"
echo "================================================================"
if python -c "import openEMS; import CSXCAD; print('openEMS + CSXCAD import OK')" 2>&1; then
    echo " openEMS Python bindings: OK"
    python -c "from openEMS.physical_constants import C0; print(f' C0 = {C0:.6e} m/s  (sanity check)')"
else
    echo " ERROR: openEMS Python bindings not importable from venv."
    echo "        Venv path: $VENV"
    ls "$VENV/lib/" 2>/dev/null || echo "        (venv/lib not found)"
fi

echo ""
echo "================================================================"
echo " openEMS install complete."
echo " If AppCSXCAD (GUI) shows a blank window, run on the HOST:"
echo "   xhost +local:docker"
echo "================================================================"
