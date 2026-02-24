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

# ── 3. Install Python bindings ────────────────────────────────────────────
echo ""
echo "[3/5] Installing openEMS Python bindings..."

# setup.py requires OPENEMS_INSTALL_PATH to locate headers and libraries
export OPENEMS_INSTALL_PATH="$OPENEMS_INSTALL_DIR"

cd "$PROJECT_DIR/CSXCAD/python"
python setup.py install --user

cd "$PROJECT_DIR/openEMS/python"
python setup.py install --user

# ── 4. Persist environment variables in shell profile ─────────────────────
echo ""
echo "[4/5] Updating ~/.bashrc with openEMS paths..."

BASHRC="$HOME/.bashrc"

add_if_missing() {
    local line="$1"
    grep -qxF "$line" "$BASHRC" 2>/dev/null || echo "$line" >> "$BASHRC"
}

add_if_missing "# openEMS"
add_if_missing "export PATH=\"$OPENEMS_INSTALL_DIR/bin:\$PATH\""
add_if_missing "export LD_LIBRARY_PATH=\"$OPENEMS_INSTALL_DIR/lib:\$LD_LIBRARY_PATH\""

# Make the paths available immediately in the current session
export PATH="$OPENEMS_INSTALL_DIR/bin:$PATH"
export LD_LIBRARY_PATH="$OPENEMS_INSTALL_DIR/lib:${LD_LIBRARY_PATH:-}"

# ── Quick smoke test ────────────────────────────────────────────────────────
echo ""
echo "[5/5] Smoke test"
echo "================================================================"
if python3 -c "import openEMS; import CSXCAD; print('openEMS import OK')" 2>&1; then
    echo " openEMS Python bindings: OK"
else
    echo " WARNING: openEMS Python bindings not found on PYTHONPATH."
    echo " You may need to open a new terminal or run: source ~/.bashrc"
fi

echo ""
echo "================================================================"
echo " openEMS install complete."
echo " If AppCSXCAD (GUI) shows a blank window, run on the HOST:"
echo "   xhost +local:docker"
echo "================================================================"
