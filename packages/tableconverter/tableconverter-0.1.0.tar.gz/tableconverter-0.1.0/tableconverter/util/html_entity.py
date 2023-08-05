import os.path
import json

with open(os.path.join(os.path.dirname(__file__), "html_entity.json")) as f:
    txt = f.read()
HTML_ENTITY_MAP = json.loads(txt)
REVERSE_ENTITY_MAP = dict((v, k) for k, v in HTML_ENTITY_MAP.items())
