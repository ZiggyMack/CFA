# FALCON-META rev v004: read me (status PREPARING)

Not for intake yet. Status stays PREPARING until the blockers in EXCEPTIONS_COVERAGE_v004.md are cleared and the Chief issues the READY receipt. Nothing was sent to Nova.

Files:
- `FALCON_METADATA_v004.tsv`: the common table, 1229 rows (1224 originals + 5 flagged version-only slots).
- `FALCON_EVIDENCE_v004.json`: reviews, components, repair lineage, stale passes, duplicate groups, human decisions, conflicts and the source inventory.
- `SCHEMA_FIELD_DICTIONARY_v004.md`: field meanings and score mappings.
- `EXCEPTIONS_COVERAGE_v004.md`: blockers kept separate from the backlog, reconciled totals, and the human-choice list.
- `MANIFEST_v004.sha256`: checksums for every v003 file.

Key rules: only V-Team verdicts validate, and Z-side review is PRELIMINARY. V3-PASS is scoped team validation, not site validation. Multiverse does not mean approved. Unassessed = null. Repairs don't inherit validation. Every chest pass scored under the old size rule is stale.
Status counts: {'NEEDS-ZIGGY': 108, 'IN-VALIDATION': 835, 'PARTIAL': 50, 'V3-PASS': 230, 'V3-FAIL': 1}.
