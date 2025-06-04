#!/usr/bin/env bash

# bootstrap_env.sh
# POSIX‐compatible script to create .venv, activate it, and install requirements.

set -e

# Ensure python3 is available
if ! command -v python3 >/dev/null 2>&1; then
  echo "× python3 not found. Please install Python 3 and re-run this script." >&2
  exit 1
fi

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
  PYTHON_VERSION="$($VENV_DIR/bin/python --version 2>&1)"
  echo "√ Virtual environment created using $PYTHON_VERSION."
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
echo "You are now in the activated venv."
echo "To activate later, run: source $VENV_DIR/bin/activate"
echo "Then start the app with: python scripts/main.py"
