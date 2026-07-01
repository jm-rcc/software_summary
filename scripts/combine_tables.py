#!/usr/bin/env python3


import os
import json

working_dir = os.environ["MODS_WORKING_PATH"]

module_keys = None
with open(f"{working_dir}/module_keys.json") as f:
    module_keys = json.load(f)

table_arches = None
with open(f"{working_dir}/table_arches.json") as f:
    table_arches = json.load(f)

table_version = None
with open(f"{working_dir}/table_version.json") as f:
    table_version = json.load(f)

table_desc = None
with open(f"{working_dir}/table_desc.json") as f:
    table_desc = json.load(f)

output_table = {}
for i in module_keys:

    for modulename, modulepath in i.items():
        name_tokens = modulename.split('/')
        if len(name_tokens) == 2:
            name = name_tokens[0]
        else:
            continue

        module_arches = []
        if name in table_arches:
            module_arches = table_arches[name]
            
        module_versions = []
        if name in table_version:
            module_versions = table_version[name]

        module_desc = ""
        if name in table_desc:
            module_desc = table_desc[name]

        output_table[name] = {"architectures":module_arches, "versions":module_versions, "description":module_desc}

with open(f"{working_dir}/intermediate_tables.json", "w") as f:
    json.dump(output_table, f, indent = 4)