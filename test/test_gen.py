import pathlib, subprocess, sys
import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
import gen


def test_generated_markdown_is_current():
    subprocess.run([sys.executable, str(gen.root / "scripts" / "gen.py"), "--check"], check=True)


def test_every_attribute_is_wt_namespaced_and_unique():
    doc = yaml.safe_load((gen.root / "attributes.yaml").read_text())
    names = [a["name"] for g in doc["groups"] for a in g["attributes"]]
    assert names and len(names) == len(set(names))
    assert all(n.startswith("wt.") for n in names)
