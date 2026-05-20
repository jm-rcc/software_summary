#!/bin/bash --login
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --job-name=module_help_index
#SBATCH --time=0:30:00
#SBATCH --qos=debug
#SBATCH --partition=general
#SBATCH -o job_output.txt
#SBATCH -e job_error.txt


# --- Load config ---
CONFIG_FILE="${1:-chain.conf}"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "ERROR: Config file '$CONFIG_FILE' not found."
  exit 1
fi

source "$CONFIG_FILE"

# Validate required config vars
: "${LIST_FILE:?'LIST_FILE must be set in config'}"
: "${PROCESS_SCRIPT:?'PROCESS_SCRIPT must be set in config'}"

LOCK_FILE="${LOCK_FILE:-${LIST_FILE}.lock}"

# --- Atomically grab the first item ---
(
  flock -x 200

  ITEM=$(head -n 1 "$LIST_FILE")

  if [ -z "$ITEM" ]; then
    echo "List is empty, exiting."
    exit 0
  fi

  tail -n +2 "$LIST_FILE" > "${LIST_FILE}.tmp" && mv "${LIST_FILE}.tmp" "$LIST_FILE"

  echo "$ITEM" > /tmp/current_item_$$

) 200>"$LOCK_FILE"

ITEM=$(cat /tmp/current_item_$$ 2>/dev/null)
rm -f /tmp/current_item_$$

if [ -z "$ITEM" ]; then
  echo "No item to process, stopping chain."
  exit 0
fi

echo "Processing: $ITEM"

# --- Run the processing script, passing the item as $1 ---
bash "$PROCESS_SCRIPT" "$ITEM"
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "WARNING: Processing script exited with code $EXIT_CODE for item: $ITEM"
  # Decide behaviour: stop chain, or continue anyway?
  # Uncomment to stop on failure:
  # exit $EXIT_CODE
fi

echo "Done processing: $ITEM"

# --- Re-submit if items remain ---
# if [ -s "$LIST_FILE" ]; then
#   echo "Items remain, submitting next job..."
#   sbatch chain_runner.sh "$CONFIG_FILE"
# else
#   echo "List exhausted, chain complete."
# fi

# --- Re-submit if items remain ---
if [ -s "$LIST_FILE" ]; then
  echo "Items remain, submitting next job..."
  SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
  sbatch --chdir="$SCRIPT_DIR" "$SCRIPT_DIR/chain_runner.sh" "$CONFIG_FILE"
else
  echo "List exhausted, chain complete."
fi
