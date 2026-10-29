# watchtower-conventions

Watchtower semantic conventions: the reserved `wt.*` namespace and the error, release, replay and LLM
attributes Watchtower adds on top of OpenTelemetry semconv. `attributes.yaml` is the source of truth;
[`conventions.md`](conventions.md) is generated from it.

Status: 0.x, early. Names marked `development` may change between minor versions.

## Install

This is a schema repository, not a package. Download `watchtower-conventions.zip` from the latest
release, or read the files in place.

## Quick start

```sh
pip install pyyaml
python scripts/gen.py          # regenerate conventions.md after editing attributes.yaml
python scripts/gen.py --check  # CI: fail when conventions.md is stale
```

```python
import yaml
names = {a["name"] for g in yaml.safe_load(open("attributes.yaml"))["groups"] for a in g["attributes"]}
```

## Contents

| File | What |
|---|---|
| `attributes.yaml` | Attribute groups: name, type, stability, scope, description |
| `conventions.md` | Generated reference tables |

## Configuration names (identical in every SDK)

| Name | Meaning |
|---|---|
| `WT_INGEST_KEY` | Secret ingest key (server SDKs); publishable key option for client SDKs |
| `WT_OTLP_ENDPOINT` | OTLP endpoint, default `http://localhost:4318` |
| `WT_SERVICE` | `service.name` |
| `WT_ENVIRONMENT` | `deployment.environment.name` |
| `WT_RELEASE` | `service.version` |

## Provenance

Every release artifact carries a GitHub build attestation. Verify one with
`gh attestation verify <file> --repo watchtowerobservability/watchtower-conventions`.

## License

Apache-2.0. Source of truth is the Watchtower monorepo; this repository is a published mirror.
