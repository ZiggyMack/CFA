# FALCON_METADATA_v002: read me, Nova

v002 replaces v001: load `FALCON_METADATA_v002.tsv` (or `.json`). The v001 files are kept unchanged for history. There are 1224 rows, one per original Falcon (Hon Dolo) image, plus 5 version-only slots in `FALCON_METADATA_VERSION_ONLY_SLOTS_v002.tsv`.

## What changed from v001
1. Ziggy's rule: **only V-Team verdicts count as validated; Z-side scoring is preliminary.** The 834 rows that v001 called `auto-reviewed` are now `PRELIMINARY (Z-side, awaiting V-Team)`. They are **not** reviewed.
2. Validated = `V-Team passed` only (280). The one `V-Team flagged for fix` row is kept.
3. C04-010: v011 (`C04-battle-light/C04-battle-light-010-v011.jpg`, sha d68287f16c0b6b9189579c501ecf9c80a1f94870f16b3aacfd06d826038f8b93) is the full-scale stencil pilot. It is preliminary and pending Ziggy. v009 and v010 are superseded, with no verdict. final_version_path stays at v005 until v011 is approved and V-Team passed.
4. Two separate piles:
   - **(a) Ziggy's decision pile: 109 images.** These are his decisions.
   - **(b) V-validation backlog: 834 images.** These are preliminary rows waiting on a V-Team pass. This is not Ziggy's work. Counts by set are in SUMMARY_v002.md.
5. **126 frames carry `chest size redo pending`** under the new full-chest-scale stencil rule. C04-010 v011 is the pilot.

## Columns
- **image_id**: slot name, e.g. C04-battle-light-010.
- **category**, **original_path** (relative to the Falcon root GROK-HD-FALCON-1000 / falcon1000), **original_sha256** (hashed from disk today).
- **qa_grade**: STRONG, defect or FAIL. **qa_grade_basis**: `explicit` when the QA note uses those words; `derived` when the note only has L/S scores (L<=2 = FAIL; no defects and L>=4 = STRONG; otherwise defect). So "defect" includes minor notes on 4/5 images.
- **qa_reason**: the QA note as written.
- **score_1to5**: preliminary score. A finer existing score is used first (MANIFEST.csv prelim_score, then NOTES.md prelim_score, then the likeness L in the qa file). Only when none exists is it **auto-mapped** from the grade: STRONG=4, defect=3, FAIL=2, none=blank. **score_basis** says which. All scores are preliminary Z-side self-scores, not V-Team or Ziggy verdicts.
- **dup_group_id**: FAL-DUP-### from the tag-only dedup pass. **dup_role**: `suggested keeper`, `duplicate`, `variant` (in a group but a meaningful variant, keep), `unique` (no group, or grouped by composition only), `awaiting Ziggy pick` (one of the 20 groups with no clear keeper). **dup_v_type**: V_1 team's validated tag.
- **chest_class**: correct ship / plain saucer = multiverse / other-wrong / stencil-variant? / not visible. From the chest audit AUDIT_v002, with V_5's chestcheck applied where it disagrees.
- **multiverse_flag**: set when the original has the plain saucer (the passed fix carries the approved ship), when dedup flagged character drift, or when Ziggy is deciding multiverse for a chest variant.
- **chest_size_redo_flag**: `chest size redo pending` on every chest-tally frame and every visible-chest frame. Ziggy ruled on 2026-10-21 that every chest ship is redone from his approved stencil at full chest scale (about 2-3x the old saucer), cropped by the clothing. C04-010 is the pilot; the rest is on hold until he sees it. The current passed fix is still the version to use until a new supplement replaces it. The young-Hon flashback exemption (Cockpit R2-04) is not in the Falcon set, so it didn't apply.
- **fix_status**: none / fixed-passed / fix-in-progress / pending Ziggy. **final_version_path** / **final_version_sha256**: the one version that goes forward now (chest tally, C05 grill PASS file, Z_3 face-fix PASS, etc.). Earlier versions are superseded and kept on disk.
- **validation_stage**: `V-Team passed` (validated: a V-Team verdict passed the image or its fix) / `V-Team flagged for fix` / `PRELIMINARY (Z-side, awaiting V-Team)` (Z-side QA, scores and audits only; **not validated**) / `awaiting Ziggy`. Under Ziggy's rule only V-Team verdicts count as validated.
- **pilot_version_path / pilot_version_sha256 / pilot_status / superseded_versions** (new in v002): a trial version under review that has not replaced final_version_path yet. Only C04-010 uses them now (v011 full-scale stencil pilot, preliminary, pending Ziggy; v009/v010 superseded).
- **ziggy_open_question**: what Ziggy still has to decide for this image, if anything.
- **notes**: condensed from QA, NOTES.md, chest audit, V returns and the tally.
- **suggested_decision** / **suggested_reason**: **recommendations only, not decisions.** Values start with "suggest:". Per Ziggy's rule, nothing is suggested for removal; 1-2 scores go to the concept pile.
- **ziggy_decision**: left blank on purpose. Only Ziggy fills it.
- **sources**: the files each row was drawn from.

## Counts
- Rows 1224: V-Team passed (validated) 280, V-Team flagged for fix 1, preliminary backlog 834, awaiting Ziggy 109.
- Chest size redo pending: 126.
- suggested_* values are recommendations, never decisions. ziggy_decision is blank on purpose.
