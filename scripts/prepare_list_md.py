#!/usr/bin/env python3


import os
import json

module_keys = None
with open("working/module_keys.json") as f:
    module_keys = json.load(f)

table_arches = None
with open("working/table_arches.json") as f:
    table_arches = json.load(f)

table_version = None
with open("working/table_version.json") as f:
    table_version = json.load(f)

table_desc = None
with open("working/table_desc.json") as f:
    table_desc = json.load(f)

output_page = ""
for i in module_keys:
    # Need to restructure keys
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

        #output_page[name] = {"architectures":module_arches, "versions":module_versions, "description":module_desc}

        output_page += "# {name}\n"
        output_page += "Architectures: {module_arches}\n\n"
        output_page += "Versions: {module_versions}\n\n"
        output_page += "Additonal module information: {module_desc}\n\n"

with open("output.md", "w") as f:
    f.write(output_page)
