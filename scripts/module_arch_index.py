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

working_dir = os.environ["MODS_WORKING_PATH"]

if __name__ == '__main__':

    # Read from raw allmodules.txt file
    with open(f"{working_dir}/allmodules.txt") as f:
        for line in f.readlines():
            line = line.strip()
            if "/all/" in line:
                a, b = line.split("/all/")
                if "/" in b:
                    # Get the arch name
                    line_tokens = a.split('/')
                    archname = line_tokens[4].replace('_', ' ')        
                    modulename = b.split('/')[0]
                    if modulename not in module_arches:
                        module_arches[modulename] = []
                    if archname not in module_arches[modulename]:
                        module_arches[modulename].append(archname)

    # Read from raw noarchmodules.txt file
    with open(f"{working_dir}/noarchmodules.txt") as f:
        archname = 'noarch'
        for line in f.readlines():
            line = line.strip()
            if not os.path.isfile(line):
                continue
            if len(line.split('/')) < 8:
                continue
            if "/modules/" in line:
                a, b = line.split("/modules/")
                if "/" in b:
                    # Get the arch name
                    modulename = line.split('/')[7]
                    if modulename not in module_arches:
                        module_arches[modulename] = []
                    if archname not in module_arches[modulename]:
                        module_arches[modulename].append(archname)

    # Write out the module:arch table
    with open(f"{working_dir}/table_arches.json", "w") as f:
        json.dump(module_arches, f)
