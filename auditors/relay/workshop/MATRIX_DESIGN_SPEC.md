<!---
FILE: MATRIX_DESIGN_SPEC.md
PURPOSE: Phase 0 design kit for the Symmetry Matrix Visualizer (SMV)
STATUS: Draft (workshop)
OWNER: Nova (co-designer) + Claude (implementer)
CREATED: 2025-11-11
LAST_UPDATE: 2025-11-11 [Initial draft created]
NOTE: Review in workshop before promoting to docs/smv/
--->

# Symmetry Matrix Visualizer — Phase 0 Design Spec (Draft)

This draft captures the design intent Nova and Claude aligned on for SMV Phase 0. Once Claude reviews and we iterate, we will promote the final spec to `docs/smv/SMV_DESIGN_SPEC.md`.

---

## 1. Visualization Goals

1. **Auditor Triangle View**
   - Nodes: Claude (teleological), Grok (empirical), Nova (symmetry)
   - Edge thickness: degree of dialogue volume
   - Edge color: harmony ? tension (green ? amber ? red)
   - Node halo: active invariant flags (ethics, constraints, scope)

2. **Temporal Trace**
   - Timeline slider (ticks = discrete deliberation checkpoints)
   - Sparkline for each auditor pair showing tension over time
   - Vertical markers for Crux declarations or constraint breaches

3. **Ethics Overlay**
   - Uses Ethical Invariant YAML fields (Phase 1 manual annotations)
   - Displays which invariants are being examined, deferred, or missing

---

## 2. Mockup Descriptions

We will prototype three canonical scenarios using SVG sketches (attached once drafted):

1. **Scenario A: High Alignment**
   - Triangle edges thin & green
   - Timeline shows low variance (flat sparkline)
   - Ethics overlay shows "Examined" for all invariants

2. **Scenario B: Constructive Tension**
   - One edge amber & thicker (e.g., Claude?Grok pushing hard)
   - Timeline sparkline oscillates but trends back toward baseline
   - Ethics overlay shows "In Progress" badge for one invariant

3. **Scenario C: Invariant Breach Risk**
   - Edge flashes red with "Crux" marker
   - Timeline spike + annotation bubble
   - Ethics overlay flags "Unexamined" + timestamp

SVG placeholders will live beside this doc once drafted (`/relay/workshop/smv_mockups/`).

---

## 3. JSON Schema (Draft)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SMVInput",
  "type": "object",
  "required": ["session_id", "ticks", "auditors"],
  "properties": {
    "session_id": {"type": "string"},
    "worldview_pair": {"type": "string"},
    "auditors": {
      "type": "array",
      "items": {"type": "string", "enum": ["Claude", "Grok", "Nova"]},
      "minItems": 3,
      "maxItems": 3
    },
    "ticks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["tick_id", "timestamp", "edges", "ethics"],
        "properties": {
          "tick_id": {"type": "string"},
          "timestamp": {"type": "string", "format": "date-time"},
          "edges": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["pair", "tension", "volume", "notes"],
              "properties": {
                "pair": {
                  "type": "string",
                  "enum": [
                    "Claude-Grok",
                    "Claude-Nova",
                    "Grok-Nova"
                  ]
                },
                "tension": {"type": "number", "minimum": 0, "maximum": 1},
                "volume": {"type": "number", "minimum": 0, "maximum": 1},
                "notes": {"type": "string"}
              }
            }
          },
          "ethics": {
            "type": "object",
            "required": ["examined", "deferred", "missing"],
            "properties": {
              "examined": {"type": "array", "items": {"type": "string"}},
              "deferred": {"type": "array", "items": {"type": "string"}},
              "missing": {"type": "array", "items": {"type": "string"}}
            }
          },
          "crux": {
            "type": "object",
            "required": ["status"],
            "properties": {
              "status": {"type": "string", "enum": ["none", "potential", "declared"]},
              "id": {"type": "string"},
              "description": {"type": "string"}
            }
          }
        }
      }
    }
  }
}
```

Any feedback from Claude/Nova on these fields can be captured inline before we freeze the schema.

---

## 4. Mock Data Alignment

See `relay/workshop/MATRIX_MOCK_DATA.json` for three scenarios that validate against the schema above. Each scenario includes =3 ticks to exercise the timeline and ethics overlays.

---

## 5. Open Questions

1. Do we need a fourth scenario (e.g., stalled conversation) before Phase 1?
2. Should ethics badges also record which Tier 1 document supplied the invariant data?
3. How do we want to visually differentiate Nova-as-observer vs Nova-as-active participant when running fairness audits?

Add notes here or inline comments in the mockups as we iterate.
