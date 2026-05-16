#!/usr/bin/env python3


import os
import json

module_keys = None
with open("working/module_keys.json") as f:
    module_keys = json.load(f)

table_arch = None
with open("working/table_arch.json") as f:
    table_arch = json.load(f)

table_version = None
with open("working/table_version.json") as f:
    table_version = json.load(f)

table_desc = None
with open("working/table_desc.json") as f:
    table_desc = json.load(f)

output_table = {}
for i in module_keys:
    module_arches = []
    module_versions = []
    module_desc = ""

    output_table[i] = {"architectures":module_arches, "versions":module_versions, "description":module_desc}

with open("output.json") as f:
    json.dump(output_table, f)
