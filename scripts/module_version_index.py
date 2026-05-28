#!/usr/bin/env python3

# --------------------------------------------------------------
# module_version_index
#
# 
# 
# Generate a table of module names : versions. 
# --------------------------------------------------------------

import os
import json

if __name__ == '__main__':
    # Start the process
    print('start')
    
    # Read allmodules and noarchmodules
    # Parse module name into "name" and "version" and "extra_version"
    # Create a table of name : [versions]
    # Save version table

    version_table = {}

    with open("working/module_keys.json") as f:
        module_keys = json.load(f)
        # iterate list
        for i in module_keys:
            # iterate dict
            for modulename in i.keys():
                name_tokens = modulename.split('/')
                if len(name_tokens) == 2:
                    name = name_tokens[0]
                    long_version = name_tokens[1]
                    if '-' in long_version:
                        version = long_version.split('-')[0]
                    else:
                        version = long_version

                    if version.startswith('.'): 
                        version = version[1:]

                    if name not in version_table:
                        version_table[name] = []
                    
                    if version not in version_table[name]:
                        version_table[name].append(version)
                        version_table[name].sort()

    with open("working/table_version.json", "w") as f:
        json.dump(version_table, f)
