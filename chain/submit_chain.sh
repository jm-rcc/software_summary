#!/bin/bash
# Usage: ./submit_chain.sh [config_file]
#   config_file defaults to chain.conf in the same directory as this script

# --- Resolve this script's own directory, following symlinks ---
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"

CONFIG_FILE="${1:-$SCRIPT_DIR/chain.conf}"
RUNNER="$SCRIPT_DIR/chain_runner.sh"

# Verify files exist before submitting
if [ ! -f "$CONFIG_FILE" ]; then
  echo "ERROR: Config file not found: $CONFIG_FILE"
  exit 1
fi

if [ ! -f "$RUNNER" ]; then
  echo "ERROR: Runner script not found: $RUNNER"
  exit 1
fi

# Submit, pinning the working directory to where the scripts live
sbatch --chdir="$SCRIPT_DIR" "$RUNNER" "$CONFIG_FILE"
