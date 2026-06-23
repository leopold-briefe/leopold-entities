import json
import os
from collections import defaultdict

from config import JSON_FOLDER


d = defaultdict(list)


seed_file = os.path.join(JSON_FOLDER, "letters.json")
source_file = os.path.join(JSON_FOLDER, "new_letters.json")


with open(seed_file, "r") as f:
    seed_data = json.load(f)



for key, value in seed_data.items():
    for y in value["copy_of"]:
        d[y['value']].append(
            {
                "id": value['lb_id'],
                "kind": value['kind'],
                "relation_type": "Kopie von"
            }
        )
    for y in value["concept_for"]:
        d[y['value']].append(
            {
                "id": value['lb_id'],
                "kind": value['kind'],
                "relation_type": "Konzept für"
            }
        )

for _, value in seed_data.items():
    value["mentioned_letters"] = d.get(value["lb_id"], [])

    

with open(source_file, "w") as f:
    json.dump(seed_data, f, ensure_ascii=False, indent=2)