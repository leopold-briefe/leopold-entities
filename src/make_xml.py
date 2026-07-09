import glob
import json
import os
import re

import jinja2
import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader
from AcdhArcheAssets.uri_norm_rules import get_normalized_uri

templateLoader = jinja2.FileSystemLoader(searchpath="src/templates")
templateEnv = jinja2.Environment(
    loader=templateLoader, trim_blocks=True, lstrip_blocks=True
)
out_dir = os.path.join("data/indices")


def convert_event_markup(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r"~~(.*?)~~", r'<hi rend="del">\1</hi>', text)
    return re.sub(r"\[([^\]]+)\]", r'<hi rend="unclear">\1</hi>', text)


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
    if template_name == "listcalendar_entrie.xml":
        for item in context["objects"]:
            item["text"] = convert_event_markup(item.get("text"))
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


search = """<?xml version='1.0' encoding='UTF-8'?>"""
replace = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>"""

for x in glob.glob(f"{out_dir}/*.xml"):
    with open(x, "r", encoding="utf-8") as f:
        xml_text = f.read()
    if search in xml_text and "<?xml-model" not in xml_text:
        xml_text = xml_text.replace(search, replace, 1)
        with open(x, "w", encoding="utf-8") as f:
            f.write(xml_text)

os.rename("data/indices/listcalendar_entrie.xml", "data/indices/listevent.xml")
