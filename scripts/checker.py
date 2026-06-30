import json
import os

output_dir = os.environ["MODS_OUTPUT_VERSION_REPO_PATH"]

labels = ["Description:", "Homepage:", "URL:", "Extensions:"]

moduledata = {}

print(f"{output_dir}/module_index.json")
with open(f"{output_dir}/module_index.json") as f:
    j = json.load(f)
    for k, v in j.items():
        moduledata[k] = {"":"", "Description:":"", "Homepage:":"", "URL:":"", "Extensions:":"", "Skip":""}
        desc = v["description"]
        lines = desc.split('\n')
        caught_label = ""
        for line in lines:
            if line.strip() == "": continue
            for label in labels:
                if line.startswith(label):
                    if len(moduledata[k][label]) > 0:
                        # Skip if that label has already been captured.
                        caught_label = "Skip"
                        continue
                    caught_label = label
                    line = line[len(label):]
            moduledata[k][caught_label] += f"{line}\n"

new_json = {}
export_labels = ["Description:", "Homepage:", "Extensions:", ""]
for i, j in moduledata.items():
    new_json[i] = {}
    for k in export_labels:
        if len(j[k].strip()):
            new_json[i][k] = j[k].strip()
    #if "Description:" not in new_json[i]:
    #    new_json[i]["Description:"] = j[""]

print(f"{output_dir}/module_index.json")
with open(f"{output_dir}/new_output.json", "w") as f:
    json.dump(new_json, f, indent = 4)

print(f"{output_dir}/module_index.md")
with open(f"{output_dir}/new_output.md", "w") as f:
    f.write(f"# Modules\n\n")
    for i, j in new_json.items():
        f.write(f"### {i}\n")
        for m, n in j.items():
            n = n.strip()
            if len(n):
                f.write(f"#### {m.strip(':')}\n")
                f.write(f"{n}\n")

