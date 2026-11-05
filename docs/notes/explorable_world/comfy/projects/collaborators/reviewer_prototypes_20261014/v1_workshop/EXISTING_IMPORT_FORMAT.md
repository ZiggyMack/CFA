# Existing validation return/import format — code inspection, not a new schema

Source: `docs/notes/explorable_world/comfy/projects/visual_library/library.js`, checkValidationEnvelope (lines 45–58) and validationAssessment (61–112), inspected during preparation. JSON file, application/json; portable export filename `cfa-reference-validation.json`. The source catalog sidecar uses `cfa-reference-validation-catalog-v1`; it is NOT the reviewer return envelope.

Reviewer envelope: `{ "format": "cfa-reference-validation-v1", "schemaVersion": 1, "assessments": [...] }`. Optional `legacyReviewArchive` must be an array; V1 should omit it. Full human review exports may nest this envelope in `validationEvidence`; V1 does not write/import human ratings.

## Each assessment: syntactically required import fields

| Field | Exact support |
|---|---|
| schemaVersion | number 1 |
| id | unique nonempty string; immutable same-ID/content reimport allowed, conflicting same ID rejected atomically |
| target | assetID nonempty string, sha256 lowercase 64-hex string, version nonempty string; normal binding is `sha256:<actual digest>` |
| axis | `character` or `scene` |
| applicability | `required`, `optional`, `not_applicable` |
| status | `not_checked`, `pass`, `fail`, `uncertain` |
| scope | id and kind nonempty strings; label optional; use exact current definition, not a guessed broad scope |
| reviewer | name, model, surface nonempty strings; reviewedAtUTC parseable timestamp (use actual UTC ISO time); do not fabricate model identity |
| provenance | source nonempty string; additional provenance fields are preserved but do not prove sight |
| imagesSeen | array; each row requires assetID, lowercase64-hex sha256, version, accessible boolean, view=`original`/`full_size_frame`/`contact_sheet`/`thumbnail` |
| criteriaResults | array; unique criterionID nonempty; outcome=`pass`/`fail`/`uncertain`/`not_checked`; visibility=`visible`/`occluded`/`missing`/`unknown`; observation string |
| evidence | string; meaningful nonempty content required for a current result |
| uncertainty | string; may be empty when genuinely resolved |

## Additional bindings needed for an applicable current result

`criteria={id,version,sha256}` and `reference={assetID,sha256,version}` must match the exact existing definition/nominated reference. They are not enforced by the initial syntax check, but missing/mismatched bindings cannot yield a current pass. Criteria/project/scope/nomination, target/reference/seen-image hashes and versions are checked. Changed bindings or criteria yield stale/uncertain evidence while preserving history.

A current pass requires actual target and reference entries in imagesSeen with accessible=true and view original/full_size_frame, plus every declared required criterion visibly observed with nonempty observation and pass. Contact sheets/thumbnails are importable evidence but do not satisfy this original-pixel pass gate. Required occluded/missing/unknown detail stays unresolved. A fail needs an observed failed required criterion; an unsupported declared fail becomes uncertain. N/A needs scoped evidence, has effective not_checked status and never counts as pass.

Current criteria IDs: hon-face, hon-dental, hon-mouth-static, hon-cheek, hon-wrist, hon-iced-r4, lisan-face, lisan-outfit, lisan-arm. All have axis character, version 2026-10-13.1; use the exact live digest/reference/scope/criterion rows from reference_validation.json. Current scope kinds include identity/detail/complete_look/outfit; the parser accepts strings, but current matching requires the declared kind. No scene criteria or sceneUses were seeded. Do not invent either.

## Ratings and authority

The validation envelope does NOT define or apply likenessRating/sceneQualityRating. Later assigned provider L/S judgments stay separate, attributed, 1–5 or null, and go to the Chief/CFA for intake. Existing manual human ratings, notes, stages, favorites, basket, scopes and acceptance remain unchanged. Collaborator role grades are a third separate concept.

This kit is not an import file and contains no new assessments. Current implementation/testing/publication is unfinished. Site Index owns vetted import/publication after its checks; no watcher or automatic notification is installed. Do not submit or import prototype placeholders.
