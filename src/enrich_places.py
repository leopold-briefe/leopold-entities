import requests
from tqdm import tqdm
from config import br_client, BASEROW_DB_ID
from acdh_geonames_utils.gn_client import gn_as_object


place_table_id = br_client.get_table_by_name(BASEROW_DB_ID, "places")


items = []
filters = {"filter__field_46737__contains": "https", "filter__field_46759__empty": True}
for x in br_client.yield_rows(place_table_id, filters=filters):
    item = x
    items.append(item)

for x in tqdm(items):
    update_object = {}
    update_url = f"{br_client.br_base_url}database/rows/table/{place_table_id}/{x['id']}/?user_field_names=true"

    gn_object = gn_as_object(x["geonames_url"])
    update_object["latitude"] = gn_object.get("latitude")
    update_object["longitude"] = gn_object.get("longitude")
    try:
        if not update_object["latitude"] or not update_object["longitude"]:
            print(
                f"Missing coordinates for {x['id']} ({x.get('geonames_url')}), skipping."
            )
            continue

        r = requests.patch(
            update_url,
            headers={
                "Authorization": f"Token {br_client.br_token}",
                "Content-Type": "application/json",
            },
            json=update_object,
        )
        r.raise_for_status()
    except Exception as e:
        print(f"Failed to process {x['id']} ({x.get('geonames_url')}): {e}")
        continue
