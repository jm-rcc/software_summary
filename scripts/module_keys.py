#!/usr/bin/env python3
#
# Read the raw files and create a list of modulename keys.
# (And the full module path.)
#

import os
import json

all_modules = []

with open("working/allmodules.txt") as f:
    for line in f.readlines():
        line = line.strip()
        if "/all/" in line:
            a, b = line.split("/all/")
            if "/" in b:
                all_modules.append({b: line})

with open("working/noarchmodules.txt") as f:
    archname = 'noarch'
    for line in f.readlines():
        line = line.strip()
        if not os.path.isfile(line):
            continue
        if "/modules/" in line:
            a, b = line.split("/modules/")
            if "/" in b:
                all_modules.append({b: line})

with open("working/module_keys.json", "w") as f:
    json.dump(all_modules, f)
