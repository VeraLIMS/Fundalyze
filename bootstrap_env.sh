#!/usr/bin/env bash

# bootstrap_env.sh
# POSIX‐compatible script to create .venv, activate it, and install requirements.

set -e

VENV_DIR=".venv"
REQ_FILE="requirements.txt"

# 1) Create .venv if missing
if [ ! -d "$VENV_DIR" ]; then
  echo "→ Creating virtual environment in $VENV_DIR…"
  python3 -m venv "$VENV_DIR"
  if [ ! -d "$VENV_DIR" ]; then
    echo "× Failed to create $VENV_DIR. Exiting."
    exit 1
  fi
  echo "√ Virtual environment created."
else
  echo "· Virtual environment $VENV_DIR already exists; skipping creation."
fi

# 2) Activate the venv in this shell
ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"
if [ ! -f "$ACTIVATE_SCRIPT" ]; then
  echo "× Could not find activation script at $ACTIVATE_SCRIPT"
  exit 1
fi

echo ""
echo "→ Activating venv…"
# shellcheck source=/dev/null
source "$ACTIVATE_SCRIPT"

# 3) Install requirements
if [ ! -f "$REQ_FILE" ]; then
  echo "× Cannot find $REQ_FILE. Please create it and list your dependencies."
  exit 1
fi

echo ""
echo "→ Upgrading pip and installing dependencies from $REQ_FILE…"
pip install --upgrade pip
pip install -r "$REQ_FILE"

echo ""
echo "√ All dependencies installed into $(pwd)/$VENV_DIR."
echo "You are now in the activated venv. Run 'python src/main.py' as usual."
