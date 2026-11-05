# Falcon validation summary v002 (20261021T055333Z)
Fixes v001 (822483c2): FAL-DUP-020 and FAL-DUP-030 were tagged backwards.
The v001 files were already rejected on 2026-10-12 for proportion drift: Chewy rendered bulkier than the DJB ref (see C21 NOTES.md and build-audit-20261012/HD-BUILD-AUDIT.csv).
The v002 files are Ziggy's requested redos, and Chief has already pushed them to Nova as the replacements. Raised by Z_6 and verified by V_1 against both sources.
- C21-005-v002 and C21-010-v002 are now DUPLICATE-KEEPER. Each needs a minor wardrobe fix: the bandolier became a studded strap.
- C21-005-v001 and C21-010-v001 are now REJECT-PROPORTION, kept for history only.
Everything else in summary v001 still stands. New v_type totals: {'VARIANT': 272, 'KEEP-IDEA-FIX-FACE': 24, 'NOT-A-DUP': 27, 'REJECT-PROPORTION': 2, 'DUPLICATE-KEEPER': 3, 'DRIFT-MULTIVERSE': 1}
Ziggy-picks: 20 (062 and 125 dropped, each with a clear keeper).
Rollup: V1_dedup_FALCON_rollup_20261021T055333Z_v002.tsv. Overrides: V1_dedup_FALCON_overrides_20261021T055333Z_v002.tsv (33 rows).
