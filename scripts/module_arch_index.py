#!/usr/bin/env python3

# --------------------------------------------------------------
# module_arch_index
#
# 
# 
# Generate a table of modules : architectures. 
# --------------------------------------------------------------

import os
import json

module_arches = {} # module_name : [arch_names]


if __name__ == '__main__':

    # Read from raw allmodules.txt file
    with open("working/allmodules.txt") as f:
        for line in f.readlines():
            line = line.strip()
            if "/all/" in line:
                a, b = line.split("/all/")
                if "/" in b:
                    # Get the arch name
                    line_tokens = a.split('/')
                    archname = line_tokens[4].replace('_', ' ')
                    if b not in module_arches:
                        module_arches[b] = []
                    module_arches[b].append(archname)

    # Read from raw noarchmodules.txt file
    with open("working/noarchmodules.txt") as f:
        archname = 'noarch'
        for line in f.readlines():
            line = line.strip()
            if not os.path.isfile(line):
                continue
            if "/modules/" in line:
                a, b = line.split("/modules/")
                if "/" in b:
                    # Get the arch name
                    if b not in module_arches:
                        module_arches[b] = []
                    module_arches[b].append(archname)

    # Write out the module:arch table
    with open("working/table_arches.json", "w") as f:
        json.dump(module_arches, f)
