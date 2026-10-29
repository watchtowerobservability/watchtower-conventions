"""Print every wt.* attribute a client may NOT send (server-stamped). Run: python examples/list_attributes.py"""
import pathlib
import yaml

doc = yaml.safe_load((pathlib.Path(__file__).resolve().parent.parent / "attributes.yaml").read_text())
for g in doc["groups"]:
    if g["id"] == "server_stamped":
        print("\n".join(a["name"] for a in g["attributes"]))
