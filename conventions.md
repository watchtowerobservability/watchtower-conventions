# Watchtower semantic conventions

Generated from `attributes.yaml`; do not edit. Built on OpenTelemetry semantic conventions.

## The `wt.*` namespace

wt.* is reserved. Tenant identity comes only from the authenticated key, so the gateway deletes every incoming wt.* attribute before stamping its own. SDKs may emit only the wt.sdk.*, wt.sample_rate, wt.session, wt.replay.*, wt.rum.* and wt.prompt.* names listed below; any other wt.* name sent by a client is dropped.

## Resource and release

OpenTelemetry attributes used as is: `service.name`, `service.version`, `deployment.environment.name`.

| Attribute | Type | Stability | Scope | Description |
|---|---|---|---|---|
| `wt.sample_rate` | double | stable | batch | Effective client sampling rate (0..1] of the batch, used to scale counts. |
| `wt.sdk.dropped` | int | stable | batch | Events the SDK queue dropped (oldest first) since the last successful flush. |
| `wt.sdk.rejected` | int | stable | batch | Events the SDK discarded because the gateway rejected them (4xx). |
| `wt.sdk.profiling` | boolean | development | resource | True when the SDK was started with profiling enabled. |

Release is `service.version`; environment is `deployment.environment.name`. Set from WT_RELEASE and WT_ENVIRONMENT.

## Errors

OpenTelemetry attributes used as is: `exception.type`, `exception.message`, `exception.stacktrace`, `trace_id`, `span_id`.

| Attribute | Type | Stability | Scope | Description |
|---|---|---|---|---|
| `wt.fingerprint` | string | stable | event | Optional client grouping override. Same value, same issue. Server computes one when absent. |
| `wt.error.handled` | boolean | stable | event | False for uncaught exceptions and panics, true for explicit capture calls. |

An error is a log record or span event carrying exception.*; its trace_id and span_id link it to the trace.

## Sessions and replay

OpenTelemetry attributes used as is: `session.id`, `browser.user_agent`, `browser.language`, `browser.mobile`.

| Attribute | Type | Stability | Scope | Description |
|---|---|---|---|---|
| `wt.session` | string | stable | event | Opaque session id (UUIDv4). Equals session.id for browser and mobile SDKs. |
| `wt.rum.session` | string | stable | event | Session id on RUM events, used to join errors, traces and replay. |
| `wt.has_replay` | boolean | stable | event | Set by the server on sessions that have a stored replay. Not client-writable. |
| `wt.replay.paused` | boolean | stable | event | Replay recording paused (consent, privacy mode, offline). |
| `wt.replay.dropped` | int | stable | event | Replay segments dropped under queue pressure. |

User ids are hashed client-side with SHA-256 and the project salt; raw ids never leave the device.

## LLM calls and prompts

OpenTelemetry attributes used as is: `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`.

| Attribute | Type | Stability | Scope | Description |
|---|---|---|---|---|
| `wt.prompt.name` | string | stable | span | Name of the managed prompt fetched with get_prompt/getPrompt. |
| `wt.prompt.version` | int | stable | span | Version of the managed prompt used for this call. |
| `wt.score.name` | string | development | event | Name of an evaluation score attached to the trace. |
| `wt.score.value` | double | development | event | Numeric score value. |

## Server-stamped (read only)

Set by the gateway after authentication. Clients must never send these; they are deleted on arrival.

| Attribute | Type | Stability | Scope | Description |
|---|---|---|---|---|
| `wt.tenant` | string | stable | resource | Tenant id from the key. |
| `wt.project_id` | string | stable | resource | Project id from the key. |
| `wt.env_id` | string | stable | resource | Environment id from the key. |
| `wt.source` | string | stable | resource | Ingest path: otlp, rum, sdk. |
| `wt.truncated` | boolean | stable | event | A value was cut to the size cap. |
| `wt.timestamp_adjusted` | boolean | stable | event | Client clock skew corrected. |
