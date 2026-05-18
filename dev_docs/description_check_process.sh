#!/bin/bash
ITEM="$1"
echo "Doing work on: $ITEM"

# e.g.:
# python my_pipeline.py --input "$ITEM"

# Running it:
#mkdir -p logs
# sbatch description_check_job.sh /path/to/chain.conf
# sbatch chain_runner.sh /path/to/chain.conf