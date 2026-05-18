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

    # Read from module_keys
    #with open("working/module_keys.json") as f:
    #    module_keys = json.load(f)
    #    # iterate list
    #    for i in module_keys:
    #        # iterate dict
    #        for modulename, fullpath in i.items():
    #            name_tokens = modulename.split('/')
    #            if len(name_tokens) == 2:
    #               name = name_tokens[0]

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
                    modulename = line_tokens[6]
                    if modulename not in module_arches:
                        module_arches[modulename] = []
                    if archname not in module_arches[modulename]:
                        module_arches[modulename].append(archname)

    # Read from raw noarchmodules.txt file
    with open("working/noarchmodules.txt") as f:
        archname = 'noarch'
        for line in f.readlines():
            line = line.strip()
            if not os.path.isfile(line):
                continue
            if len(line.split('/')) < 7:
                continue
            if "/modules/" in line:
                a, b = line.split("/modules/")
                if "/" in b:
                    # Get the arch name
                    modulename = line.split('/')[6]
                    if modulename not in module_arches:
                        module_arches[modulename] = []
                    if archname not in module_arches[modulename]:
                        module_arches[modulename].append(archname)

    # Write out the module:arch table
    with open("working/table_arches.json", "w") as f:
        json.dump(module_arches, f)
