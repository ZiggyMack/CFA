# LAG-1K review metadata r001: schema, field dictionary and score mappings
Follows the CFA Site Index / Codex handoff guidance of 2026-10-21 (CODEX_HANDOFF_SPEC_20261021.md) and the CFA REFERENCE_POLICY / REFERENCE_VALIDATION_GUIDE (2026-10-13.1). Missing or unassessed values are written as `null` (never 0). Every value comes from a named source file; nothing is invented.

## Files
| file | content |
|---|---|
| LAG1K_REVIEW_INDEX_r001.tsv | Common index. One row per declared original (1,000): 997 on disk plus 3 explicit DECLARED_NOT_ON_DISK placeholders. Tab-separated, UTF-8, header row. |
| LAG1K_REVIEW_EVIDENCE_r001.json | JSON sidecar: per-image identity, bot notes, V_1 input row, repair lineage, component status; all review records; stale/superseded entries; duplicate groups; disagreements. |
| D_PATH_MAP_r001.tsv | Every original and repair version mapped to its hash-verified D: path(s), plus in-package path for repair media. |
| EXCEPTIONS_AND_COVERAGE_r001.md | Reconciled totals, coverage, technical-vs-human split, packaging blockers, exceptions. |
| audit_sheets/v_team/ | Original V Team returns (V_1 meta input v001+v002, V1 dedup rollup/fixlist/summary/assignments, V2-V5 dedup lanes, V3_LAGFIX check v001-v005, redocheck v001-v004, V1 Ziggy-decisions v008) with their .sha256 files, and the V_1 dedup sheets. |
| audit_sheets/bot_preliminary/ | HaL/Z_5 fix logs, BUILD-AUDIT, ROLLUP, DUP-CLUSTERS, SHORTLIST, LEDGER, TEAM-RULES, CFA-VIEWER-OPTIONS (all PRELIMINARY). |
| audit_sheets/category_notes/ | The 45 category NOTES.md files (bot self-scores) and the C13 repairs NOTES. |
| media/repairs/ | Exact bytes of all 70 repair/fix versions (final, superseded and unverified). Originals are not copied; see D_PATH_MAP. |
| SHA256SUMS_r001.txt | sha256 of every file in the package (except itself). |

## Index columns (core first)
| column | meaning |
|---|---|
| image_id | Source frame ID = original filename without .jpg (e.g. C05-03_Z_10). Placeholders: LAG-1K-DECLARED-UNACCOUNTED-00n. |
| dup_group | V Team duplicate cluster ID (LAG-DUP-nnn) or null. |
| dup_keeper | Proposed keeper of that group (V Team, PRELIMINARY) or null when none was proposed. |
| class | V Team dedup tag: VARIANT, KEEP-IDEA-FIX-FACE, NOT-A-DUP, DRIFT-MULTIVERSE, DUPLICATE-KEEPER. PRELIMINARY until Ziggy. null = not in the dedup pass. |
| likenessRating | Validated character-likeness rating 1-5 (V Team or human). null for all rows in r001: none exist. |
| sceneQualityRating | Validated scene-craft rating 1-5. null for all rows in r001. |
| prelim_qa_score_suggestion | PRELIMINARY QA-score suggestion. Only set when a bot NOTES line carries an explicit overall number ("grade N", "score N", or a bare "N" / "N/5"); copied as-is. Not a likeness rating. |
| prelim_likeness_self | Drafting bot's L self-score (L1-L5) from NOTES. PRELIMINARY. |
| prelim_scene_self | Drafting bot's S self-score (S1-S5) from NOTES. PRELIMINARY. |
| raw_qa_grade | Raw provider QA text from NOTES, all lines for the frame joined with " / ". Preserved verbatim. |
| prelim_qa_class | Class derived by the mapping below. PRELIMINARY. |
| review_stage | Highest review that exists: V-TEAM fix-scope VALIDATED + dedup proposal / V-TEAM dedup proposal only / BOT PRELIMINARY note/self-score only / UNREVIEWED / UNKNOWN (no file). |
| final_passed_version | Fix version that holds the current V Team PASS (v002/v003/v005) or null. |
| final_passed_version_sha256 | Exact sha256 of that version. |
| final_passed_scope | Scope of that pass: claimed face/chin fix on that file only; not whole-image; not Ziggy acceptance. |
| ziggy_suggestion_flag | Y when the image is part of an open ZIGGY-PICK choice (015-B). |
| notes | V lane note, V_3 remaining defects on the final fix, fix versions without a pass, and pointers to the bot NOTES lines. |
| dataset, source_frame_id | LAG-1K and the frame ID. |
| inventory_status | ON_DISK or DECLARED_NOT_ON_DISK. |
| sha256, bytes, width, height | Full sha256, byte size and pixel size of the original, measured on the box. |
| rel_path | Path relative to /workspace/lisan-al-gaib/ (LAG-1K/<category>/<file>). |
| category, sub_shot_id | Category folder; V Team sub-shot ID where assigned. |
| cfa_asset_id | Existing CFA asset ID only if known; null for all rows (none of these images are in the CFA catalog files). |
| dup_member_type | useful-variant / useful-variant (fix-face) / not-a-duplicate / visual-duplicate (proposed keeper / non-keeper) / drift-multiverse (ZIGGY-PICK group); exact-byte duplicates would be appended (none found). |
| dedup_tag_status | "PRELIMINARY V Team proposal, PENDING ZIGGY" or null. |
| lane_suggestion | multiverse (V Team PRELIMINARY) when V Team flagged multiverse; else null. Multiverse is not approval. |
| keep_fix_remove, archive_state, human_acceptance | Ziggy's calls. null for every row. |
| production_stage | preliminary for all bot drafts. |
| technical_validation | "VALIDATED fix-scope (vNNN)" when a V Team pass exists; null otherwise. |
| v_team_reviewed | Y/N. |
| fix_versions_count | Number of repair/fix versions in lineage. |
| fix_drift_group | V_1 fix-list drift group (A-I) or null. |
| open_items_owner | Who must act on the open item. |
| score_source | Where the preliminary score came from. |

## JSON sidecar keys
- images[]: image_id, identity, bot_preliminary_notes[{file:line, text, label}], v1_input_row (verbatim), repair_lineage[], components{face_identity, AL_brow, GAIB_chin, throat_worms_c02, eye_sun_disc, nostril_hoop, brow_ring, ear_hoop, build} each visible/occluded/missing/unknown (all "unknown" in r001).
- review_records[]: record_type (v_team_fix_check / v_team_dedup_proposal), reviewer, team, time_utc (from the return filename timestamp), source_file, source_file_sha256, source_row, target_path / target_rel_path, target_sha256, base_path, reference{criteria_set, reference_id_recorded, reference_sha256_recorded}, criterion, criterion_rule_version, scope, outcome, reason, max_diff_outside, note, supersedes_row, validation_label, currency (current / superseded_return_version / superseded_by_later_return_row).
- repair_lineage[]: version_id, original_id, version, path, rel_path, sha256, bytes, parent_id, parent_sha256 (measured), parent_sha256_logged, made_by, fix_log, requested_change, method, bot_prelim_score, bot_note, logged_sha_matches_file, v_team_current_verdict, v_team_verdict_source, remaining_defects, v_team_review_count, validation_label, inherits_original_validation (always false), superseded, status_in_lineage (FINAL_PASSED_SCOPED / SUPERSEDED / SUPERSEDED_PASS (stale) / NO_PASS_YET).
- stale_or_superseded[]: image_id, stale_claim, stale_reason.
- duplicate_groups[]: group_id, category, members[{image_id, sha256, sub_shot_id, tag, lane, lane_file, ziggy_pick_open, multiverse_flag}], exact_byte_duplicates, proposed_keeper, keeper_rationale, unresolved_user_choice, status.
- v1_vs_v3_disagreements[], notes_lines_ambiguous_short_id[].

## Score mappings (all PRELIMINARY)
- prelim_qa_class from the drafter's number (L self-score, else "grade/score N" or bare N): 4-5 = STRONG, 3 = DEFECT, 1-2 = FAIL. This is the ROLLUP.md convention.
- Without a number: a NOTES line containing FAIL or REJECT = "FAIL (text)"; a filename ending in _FAIL with no note = "FAIL (filename tag)"; "weak pass" / "pass (soft)" = "SOFT PASS (text only)"; "pass" = "PASS (text only)"; any other note = "DEFECT NOTE (text only)"; nothing = null.
- prelim_qa_score_suggestion is the explicit overall number only; it is never derived from text and never copied into likenessRating.
- V Team verdict labels: PASS = VALIDATED for the recorded fix scope only. FAIL / PARTIAL = not passed. V Team dedup tags = PRELIMINARY proposals pending Ziggy.
