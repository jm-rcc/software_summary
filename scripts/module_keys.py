#!/usr/bin/env python3
#
# Read the raw files and create a list of modulename keys.
# (And the full module path.)
#

import os
import json

all_modules = []

working_dir = os.environ["MODS_WORKING_PATH"]

with open(f"{working_dir}/allmodules.txt") as f:
    for line in f.readlines():
        line = line.strip()
        if "/all/" in line:
            a, b = line.split("/all/")
            if "/" in b:
                all_modules.append({b: line})

with open(f"{working_dir}/noarchmodules.txt") as f:
    archname = 'noarch'
    for line in f.readlines():
        line = line.strip()
        if not os.path.isfile(line):
            continue
        if "/modules/" in line:
            a, b = line.split("/modules/")
            if "/" in b:
                all_modules.append({b: line})

with open(f"{working_dir}/module_keys.json", "w") as f:
    json.dump(all_modules, f)
