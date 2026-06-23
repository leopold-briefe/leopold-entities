import json
import os
from collections import defaultdict

from config import JSON_FOLDER


seed_file = os.path.join(JSON_FOLDER, "places.json")
source_file = os.path.join(JSON_FOLDER, "persons.json")

with open(seed_file, "r") as f:
    seed_data = json.load(f)

with open(source_file, "r") as f:
    source_data = json.load(f)

for key, value in source_data.items():
    old_values = value["place_of_birth"]
    new_values = []
    for x in old_values:
        new_values.append(seed_data[f"{x['id']}"])
    value["place_of_birth"] = new_values
    old_values = value["place_of_death"]
    new_values = []
    for x in old_values:
        new_values.append(seed_data[f"{x['id']}"])
    value["place_of_death"] = new_values

with open(source_file, "w") as f:
    json.dump(source_data, f, ensure_ascii=False, indent=2)


seed_file = os.path.join(JSON_FOLDER, "places.json")
source_file = os.path.join(JSON_FOLDER, "orgs.json")

with open(seed_file, "r") as f:
    seed_data = json.load(f)

with open(source_file, "r") as f:
    source_data = json.load(f)

for key, value in source_data.items():
    old_values = value["located_in"]
    new_values = []
    for x in old_values:
        new_values.append(seed_data[f"{x['id']}"])
    value["located_in"] = new_values

with open(source_file, "w") as f:
    json.dump(source_data, f, ensure_ascii=False, indent=2)

d = defaultdict(list)


seed_file = os.path.join(JSON_FOLDER, "letters.json")
source_file = os.path.join(JSON_FOLDER, "letters.json")

with open(seed_file, "r") as f:
    seed_data = json.load(f)

for key, value in seed_data.items():
    for y in value["copy_of"]:
        d[y["value"]].append(
            {"id": value["lb_id"], "kind": value["kind"], "relation_type": "Kopie von"}
        )
    for y in value["concept_for"]:
        d[y["value"]].append(
            {
                "id": value["lb_id"],
                "kind": value["kind"],
                "relation_type": "Konzept für",
            }
        )

for _, value in seed_data.items():
    value["mentioned_letters"] = d.get(value["lb_id"], [])

with open(source_file, "w") as f:
    json.dump(seed_data, f, ensure_ascii=False, indent=2)
