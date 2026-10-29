#!/usr/bin/env python3
"""Render attributes.yaml to conventions.md. `gen.py --check` fails when conventions.md is stale."""
import sys, pathlib, yaml

root = pathlib.Path(__file__).resolve().parent.parent
TYPES = {"string", "int", "double", "boolean"}
STAB = {"stable", "development"}


def render(doc):
    out = ["# Watchtower semantic conventions", "",
           "Generated from `attributes.yaml`; do not edit. Built on OpenTelemetry semantic conventions.", "",
           "## The `wt.*` namespace", "", doc["namespace"]["rule"].strip(), ""]
    seen = set()
    for g in doc["groups"]:
        out += [f"## {g['title']}", ""]
        if g.get("desc"):
            out += [g["desc"], ""]
        if g.get("uses"):
            out += ["OpenTelemetry attributes used as is: " + ", ".join(f"`{u}`" for u in g["uses"]) + ".", ""]
        out += ["| Attribute | Type | Stability | Scope | Description |", "|---|---|---|---|---|"]
        for a in g["attributes"]:
            assert a["name"].startswith("wt."), a["name"]
            assert a["type"] in TYPES and a["stability"] in STAB, a
            assert a["name"] not in seen, "duplicate " + a["name"]
            seen.add(a["name"])
            out.append(f"| `{a['name']}` | {a['type']} | {a['stability']} | {a['scope']} | {a['desc']} |")
        out.append("")
        if g.get("notes"):
            out += [g["notes"], ""]
    return "\n".join(out)


if __name__ == "__main__":
    text = render(yaml.safe_load((root / "attributes.yaml").read_text()))
    target = root / "conventions.md"
    if "--check" in sys.argv:
        if not target.exists() or target.read_text() != text:
            sys.exit("conventions.md is stale: run python scripts/gen.py")
    else:
        target.write_text(text)
