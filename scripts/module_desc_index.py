#!/usr/bin/env python3

# --------------------------------------------------------------
# module_desc_index
#
# 
# 
# Generate a table of modules : descriptions. 
# --------------------------------------------------------------

import os
import json

if __name__ == '__main__':
    # Start the process
    print('start')
    
    # Read the raw files and create a list of module descriptions

    # Load the module keys
    module_keys = None
    with open("working/module_keys.json") as f:
        module_keys = json.load(f)

    # Load the existing module table
    table_desc = None
    with open("working/table_desc.json") as f:
        table_desc = json.load(f)

    # Create a list of anything that's missing from the module description table
    missing_things = []
    for i in module_keys:
        a, b = i
        if a not in table_desc:
            missing_things.append(i)
    
    # Save a list of modules with missing description
    with open("working/missing_things.txt", "w") as f:
        json.dump(missing_things, f)

