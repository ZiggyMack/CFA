# Schema addendum r002 (LINEAGE_CORRECTIONS_r002.tsv and companions)
Fields not listed here keep their r001 meaning (SCHEMA_FIELD_DICTIONARY_r001.md).

## LINEAGE_CORRECTIONS_r002.tsv
| field | meaning |
|---|---|
| dataset | LAG-1K |
| frame_family | stable frame ID of the root original (r001 image_id) |
| version_id | r001 repair version ID (<frame>@<version>-<maker>) |
| version_sha256 | full sha256 of this repair file |
| root_original_sha256 | full sha256 of the frame family's original (what r001 called parent_sha256 and V_1 called final_fix_parent_sha256) |
| base_sha256 | full sha256 of the pixels this version was actually edited or pasted onto; UNKNOWN if the logs don't establish it |
| donor_sha256s | ;-separated full sha256 of donor images (earlier patches/versions); NONE = method names no donor image; UNKNOWN = a donor image is described but its hash is not logged (renders, reference crops, cross-frame donors) |
| base_source | log file + data row + method text (or NOTES.md text) the base comes from |
| parent_confidence | confidence in base_sha256: LOGGED (maker's log source-hash column, consistent with method) / INFERRED_FROM_METHOD (read from method/NOTES text) / UNKNOWN |
| donor_confidence | NONE_REQUIRED / INFERRED_FROM_METHOD / UNKNOWN (any UNKNOWN donor makes it UNKNOWN unless an in-lineage donor was inferred) |
| donor_notes | what the donors are, in words |
| v_team_verdict, v_team_verdict_source | current V_3 verdict for this exact file (from r001), VALIDATED for fix scope only |
| lineage_status | r001 status_in_lineage, with the C37-06 Z_5 v002 relabel |
| r001_parent_sha256, r001_parent_sha256_logged | r001 values, kept for comparison |
| correction_vs_r001 | plain-language difference from r001 |

## LINEAGE_DISAGREEMENTS_r002.tsv
version_id, field, r001_or_v1_value, r002_value, source, note. Field-level rows first, then per-version rows where the actual base differs from the r001/V_1 parent.

## STATUS_UPDATES_r002.tsv
dataset, item_id, version_sha256, field, r001_value, r002_value, authority, evidence_file, evidence_sha256, evidence_row, note.

## LISAN_START_HERE_ROWS_r002.tsv
Z_6's START_HERE columns, in order: dataset, package_id, revision, d_root, manifest_file, manifest_sha256, file_count, source_root_map, authoritative (yes/superseded), metadata_verified, media_available (ALL/PARTIAL/NONE + counts), supersedes, notes.
