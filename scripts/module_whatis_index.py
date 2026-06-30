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

# The names of all modules (across all nodes)
# [module name, full path]
all_modules = []

# clinicalomx is not available

def read_modules(filename):
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if "/all/" in line:
                a, b = line.split("/all/")
                if "/" in b:
                    all_modules.append([b, line])
                    
if __name__ == '__main__':

    working_dir = os.environ["MODS_WORKING_PATH"]
    module_dir = os.environ["MODS_MODULE_PATH"]
    module_noarch_dir = os.environ["MODS_NOARCH_PATH"]

    with open(f"{working_dir}/allmodules.txt") as f:
        for line in f.readlines():
            line = line.strip()
            if "/all/" in line:
                a, b = line.split("/all/")
                if "/" in b:
                    all_modules.append([b, line])

    with open(f"{working_dir}/noarchmodules.txt") as f:
        archname = 'noarch'
        for line in f.readlines():
            line = line.strip()
            if not os.path.isfile(line):
                continue
            if "/modules/" in line:
                a, b = line.split("/modules/")
                if "/" in b:
                    all_modules.append([b, line])

    modules_errored = []
    modules_indexed = []

    module_use_string = f"module use {module_noarch_dir}/eait/modules; module use {module_noarch_dir}/imb/modules; module use {module_noarch_dir}/neuro/modules; module use {module_noarch_dir}/qcif/modules; module use {module_noarch_dir}/rcc/modules; module use {module_dir}/epyc3/modules/all; module use {module_dir}/epyc3_a100/modules/all; module use {module_dir}/epyc3_h100/modules/all; module use {module_dir}/epyc3_l40/modules/all;"

    # Use lmod to get the module help
    def get_lmod_whatis(filepath):
        lines = []
        #b = subprocess.run([f"echo $MODULEPATH"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        b = subprocess.run([f"{module_use_string} module whatis {filepath}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #b = subprocess.run([f"module spider {filepath}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        textout = b.stderr.decode('utf-8')
        #texterr = b.stderr.decode('utf-8')
        #print("OUT:    ", textout)
        #print("ERR:    ", texterr)
        for line in textout.split('\n'):
            line = line.strip()
            if line.startswith('------'): continue
            if line.startswith('ERROR:'): continue
            if line == "": continue
            if line.startswith(filepath):
                first_colon = line.find(':')
                line = line[first_colon + 1:].strip()
            lines.append(line)
        if lines == []: 
            modules_errored.append(filepath)
            print(f"Error text:    {filepath}")
            print(textout)
        else: modules_indexed.append(filepath)
        return "\n".join(lines)

    # 1. Load the existing help index
    help_index_data = {}
    try:
        with open(f"{working_dir}/table_desc.json") as f:
            help_index_data = json.load(f)
    except FileNotFoundError as e:
        print(f"Missing file: Error: {e}")
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
                whatis = get_lmod_whatis(modulename)
                if whatis == "": continue
                help_index_data[name] = whatis
                unsaved_changes = True

    # 3. Save help index if it has been updated
    if unsaved_changes:
        with open(f"{working_dir}/table_desc.json", "w") as f:
            json.dump(help_index_data, f, ensure_ascii=False, indent=4)

    print("ERROR'd:")
    for i in modules_errored: print(i)
    print("ADD'd")
    for i in modules_indexed: print(i)

    #print(help_index_data)
