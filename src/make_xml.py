import glob
import json
import os

import jinja2
import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader
from AcdhArcheAssets.uri_norm_rules import get_normalized_uri

templateLoader = jinja2.FileSystemLoader(searchpath="src/templates")
templateEnv = jinja2.Environment(
    loader=templateLoader, trim_blocks=True, lstrip_blocks=True
)
out_dir = os.path.join("data/indices")

os.makedirs(out_dir, exist_ok=True)
files = glob.glob("./json_dumps/*.json")

for x in files:
    _, tail = os.path.split(x)
    with open(x, "r") as f:
        data = json.load(f)
    context = {}
    context["objects"] = [value for key, value in data.items()]
    ent_type = tail.replace("s.json", "")
    template_name = f"list{ent_type}.xml"
    try:
        template = templateEnv.get_template(template_name)
    except jinja2.exceptions.TemplateNotFound:
        continue
    xml_name = os.path.join(out_dir, template_name)
    xml_data = template.render(context).replace("&", "&amp;")
    doc = TeiReader(xml_data)
    for idno in doc.any_xpath(".//tei:body//tei:idno"):
        old_uri = idno.text
        try:
            new_uri = get_normalized_uri(old_uri)
        except TypeError:
            new_uri = old_uri
        idno.text = new_uri
    ET.indent(doc.any_xpath(".")[0], space="   ")
    doc.tree_to_file(xml_name)

os.rename("data/indices/listcalendar_entrie.xml", "data/indices/listevent.xml")
