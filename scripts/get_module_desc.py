
#
# Generate a list of modules with their LMOD "help" text
# This list will be faster to lookup in bulk than calling "module help" 
#

import os
import json
import sys
from contextlib import redirect_stderr

exec(open('/usr/share/lmod/lmod/init/env_modules_python.py').read())

# TODO use module paths (input?)
module("use", "/sw/auto/rocky8d/epyc3/modules/all")
module("use", "/sw/auto/rocky8d/epyc3_a100/modules/all")
module("use", "/sw/auto/rocky8d/epyc3_h100/modules/all")
module("use", "/sw/auto/rocky8d/epyc3_l40/modules/all")
module("use", "/sw/auto/rocky8d/epyc3_mi210/modules/all")
module("use", "/sw/auto/rocky8d/epyc4/modules/all")
module("use", "/sw/auto/rocky8d/epyc4_a16/modules/all")
module("use", "/sw/auto/rocky8d/epyc4_h100/modules/all")
module("use", "/sw/auto/rocky8d/epyc4_l40s/modules/all")
module("use", "/sw/auto/rocky8d/epyc4_mi210/modules/all")
module("use", "/sw/auto/rocky8d/xeonsp4/modules/all")
module("use", "/sw/auto/rocky8d/xeonsp4_h100/modules/all")

# ONly want on e module name
modulename = sys.argv[1]

# Use lmod to get the module help
def get_lmod_help(filepath):

    with open(os.devnull, 'w') as devnull:
        with redirect_stderr(devnull):

            b = module("help", filepath)
            return b[1].strip().split('\n')[1:]
        
# 1. Load the existing help index
help_index_data = {}
try:
    with open("working/table_desc.json") as f:
        help_index_data = json.load(f)
except FileNotFoundError as e:
    print(e)
except PermissionError:
    print("Permission denied: help_index.json")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# 2. For one module, get the module help
unsaved_changes = False
#for i in all_modules:
#    modulename, modulepath = i
if modulename not in help_index_data:
    help_index_data[modulename] = get_lmod_help(modulename)
    unsaved_changes = True

# 3. Save help index if it has been updated
if unsaved_changes:
    with open("help_index.json", "w") as f:
        json.dump(help_index_data, f, ensure_ascii=False, indent=4)
