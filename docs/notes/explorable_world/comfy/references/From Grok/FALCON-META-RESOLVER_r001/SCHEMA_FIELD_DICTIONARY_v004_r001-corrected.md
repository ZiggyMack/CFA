> CORRECTED COPY (resolver r001). Wording fixes only; see CORRECTIONS_r001.md. The frozen original in FALCON-METADATA_v004 is unchanged and remains the hashed v004 file.

# Schema and field dictionary, FALCON-META rev v004

Status: PREPARING. Common table: `FALCON_METADATA_v004.tsv` (tab-separated, UTF-8, 1229 rows = 1224 originals + 5 version-only slots). Evidence sidecar: `FALCON_EVIDENCE_v004.json`. The columns follow HaL's shared format (V1_LAG1K_meta_input) where the fields overlap, so Falcon and Lisan line up. Falcon-specific fields are added at the end of each group.

## Columns
- **package_rev**: Always "FALCON-META rev v004".
- **dataset**: GROK-HD-FALCON-1000.
- **record_type**: original, or VERSION-ONLY SLOT (5 slots with no unversioned original; base = -v001 file).
- **frame_id**: Slot name, e.g. C04-battle-light-010.
- **cfa_asset_id**: Existing CFA asset ID. Blank: no source gives one for Falcon frames, and none is guessed.
- **provider_asset_ref**: MANIFEST.csv source_asset_prefix (generation asset prefix). Not a CFA asset ID.
- **category**: Category folder (C##-slug).
- **shot**: Shot number within the category.
- **original_path**: Relative to the Falcon root, except C04-006 (absolute path of the pre-fix original).
- **original_sha256**: FULL sha256 of the original identity, hashed today.
- **original_identity_source**: Why this file is the original.
- **byte_size / width / height**: Of the original.
- **final_version_path / final_version_sha256**: The one version that goes forward now, from the tally, V returns or ROLLUP. Blank = the original is used, no repair.
- **final_version_scope**: What the pass covered. No whole-image or Ziggy acceptance is implied.
- **final_version_pass_state**: current pass (scoped) / STALE pass / grill scope current, chest STALE / pending / none.
- **pilot_version_path / _sha256**: A trial version not yet adopted (C04-010 v011).
- **dup_group_id / dup_role**: FAL-DUP group; suggested keeper / variant / duplicate / unique / awaiting Ziggy pick (PRELIMINARY proposals).
- **dup_class**: useful-variant / visual-duplicate / not-a-dup. There are no exact-byte duplicates.
- **multiverse_flag / multiverse_reason**: candidate + why. A flag is never approval or a lane assignment.
- **likenessRating / sceneQualityRating**: null for every row. No scoped, attributed comparison exists. Never 0 or 5 for unassessed.
- **provider_L_prelim / provider_S_prelim**: Provider self-scores (likeness / scene) copied from qa*.tsv. PRELIMINARY, not likenessRating.
- **provider_lane_prelim**: Provider-suggested lane from qa*.tsv, if given.
- **provider_qa_grade / _basis / _reason**: Raw provider QA. Grade STRONG/defect/FAIL. Basis: explicit = word in note; derived = from L/S (L<=2 FAIL; no defects and L>=4 STRONG; else defect). Reason verbatim.
- **qa_score_suggestion / _basis**: PRELIMINARY 1-5. Mapping: existing MANIFEST prelim_score first, then NOTES.md prelim_score, then provider L. Only if none exist: STRONG=4, defect=3, FAIL=2, none=null. Not likenessRating.
- **defect_tags_prelim**: Keyword tags from the provider defect text. PRELIMINARY.
- **chest_visibility**: visible / occluded / missing / unknown. "Not visible" in the audit is unverified, not wrong or multiverse.
- **chest_class**: Design class: correct ship / plain saucer = multiverse / other-wrong / stencil-variant? / not visible.
- **chest_size_redo**: "chest size redo pending" under the full-scale stencil rule (126 frames).
- **triage_keep_fix_remove**: Ziggy's Keep/Fix/Remove. Blank: no decisions recorded.
- **suggested_triage**: PRELIMINARY recommendation only.
- **creative_lane**: Prime/Multiverse decision. Blank: none recorded.
- **suggested_lane**: PRELIMINARY.
- **production_stage**: Blank/unknown: no production stage recorded for Falcon.
- **technical_validation**: V-Team verdicts summary, or "none (Z-side PRELIMINARY only)".
- **human_acceptance**: Explicit human acceptance with scope/version/source. Only the C04-010 v011 look so far.
- **validation_status**: UNREVIEWED (none) / IN-VALIDATION (Z-side PRELIMINARY review only, awaiting V-Team) / V3-PASS (V-Team pass, scoped, nothing stale or pending) / V3-FAIL (V-Team flagged for fix) / PARTIAL (V-Team pass exists but a component is stale or pending, e.g. chest size redo) / NEEDS-ZIGGY (a human choice is open).
- **reviewer**: V-Team reviewers with verdicts on the frame or its repairs, else the Z-side authors.
- **pending_items**: Explicit PENDING items, each with owner and the exact versions/hashes covered.
- **ziggy_open_question**: Human choice still needed.
- **reference_ids**: Bound catalog/reference IDs (applicable set, not a pass).
- **rule_versions**: Rules in force for this row.
- **source_file**: Source files the row was drawn from.
- **notes**: Condensed notes (carried from v002).

## Score mappings
- qa_score_suggestion (PRELIMINARY): an existing finer score is used first, in this order: MANIFEST.csv prelim_score, NOTES.md prelim_score, then the provider likeness L. Only when none exists is it auto-mapped STRONG=4, defect=3, FAIL=2, none=null. Counts: {'finer score from MANIFEST.csv prelim_score': 1066, 'finer score': 36, 'finer score from NOTES.md prelim_score': 49, 'auto-mapped from qa_grade': 71, 'null': 2}.
- provider_qa_grade, derived when the note has no explicit word: L<=2 = FAIL; defects field 'none' and L>=4 = STRONG; otherwise defect. For no-Dolo frames (L-), S plus the defects field is used the same way.
- likenessRating and sceneQualityRating: null for every row. Per REFERENCE_POLICY (2026-10-11 section), these need a scoped comparison against the canonical reference. None exists for Falcon, and provider self-scores are not human ratings.

## Status mapping from v002
awaiting Ziggy -> NEEDS-ZIGGY; V-Team flagged for fix -> V3-FAIL; V-Team passed -> V3-PASS, or PARTIAL when chest size redo or a stale pass applies; PRELIMINARY (Z-side) -> IN-VALIDATION; none -> UNREVIEWED.

## Evidence JSON layout
`records[]` (per frame: original identity, `reviews[]` with team/reviewer/time/source_file/source_row/target hash/reference/rule_version/scope/outcome/reason/standing, `components{}` visibility, `repairs[]` lineage with parent hash, requested change, verdicts, own_verdict, pass_state, stale_reason, inherits_original_validation=false, `pending[]`), plus `duplicate_groups[]`, `superseded_passes[]`, `repairs_index[]`, `human_decisions[]`, `conflicts[]`, `references`, `reference_file_copies`, `source_inventory` (path to sha256). Unknown times are null and never invented. Times from V return filenames are converted from UTC to ET.
