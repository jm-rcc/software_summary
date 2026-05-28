# For each module
# Get the whatis
# Parse into lines and categorize,
# Save as a json table


#
# Generate a list of modules with their LMOD "help" text
# This list will be faster to lookup in bulk than calling "module help" 
#

import os
import subprocess
import json

subprocess.run(["module use /sw/auto/rocky8d/epyc3/modules/all"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["module use /sw/auto/rocky8d/epyc3_a100/modules/all"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["module use /sw/auto/rocky8d/epyc3_h100/modules/all"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["module use /sw/auto/rocky8d/epyc3_l40/modules/all"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["module use /sw/auto/rocky8d/epyc3_mi210/modules/all"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["module use /sw/auto/rocky8d/epyc4/modules/all"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["module use /sw/auto/rocky8d/epyc4_a16/modules/all"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["module use /sw/auto/rocky8d/epyc4_h100/modules/all"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["module use /sw/auto/rocky8d/epyc4_l40s/modules/all"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["module use /sw/auto/rocky8d/epyc4_mi210/modules/all"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["module use /sw/auto/rocky8d/xeonsp4/modules/all"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["module use /sw/auto/rocky8d/xeonsp4_h100/modules/all"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# The names of all modules (across all nodes)
# [module name, full path]
all_modules = []

def read_modules(filename):
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if "/all/" in line:
                a, b = line.split("/all/")
                if "/" in b:
                    all_modules.append([b, line])

read_modules("working/allmodules.txt")
read_modules("working/noarchmodules.txt")

# Use lmod to get the module help
def get_lmod_whatis(filepath):
    lines = []
    b = subprocess.run([f"module whatis {filepath}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    textout = b.stdout.decode('utf-8')
    for line in textout.split('\n'):
        if line.startswith('-'): continue
        if line.strip() == "": continue
        truncated_line = line[len(filepath) + 2:].strip()
        lines.append(truncated_line)
    return "\n".join(lines)

#whatis = get_lmod_whatis("lit/18.1.2-gcccore-12.3.0")
#print(whatis)
#exit(0)

# 1. Load the existing help index
help_index_data = {}
try:
    #with open("help_index.json") as f:
    with open("working/table_desc.json") as f:
        help_index_data = json.load(f)
except FileNotFoundError as e:
    print(e)
except PermissionError:
    print("Permission denied: table_desc.json")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


# 2. For all modules, find any that are missing, and get the module help
unsaved_changes = False
for i in all_modules:
    modulename, modulepath = i
    name_tokens = modulename.split('/')
    if len(name_tokens) == 2:
        name = name_tokens[0]
        if name not in help_index_data:
            help_index_data[name] = get_lmod_whatis(modulename)
            unsaved_changes = True

# 3. Save help index if it has been updated
if unsaved_changes:
    with open("working/table_desc.json", "w") as f:
        json.dump(help_index_data, f, ensure_ascii=False, indent=4)
