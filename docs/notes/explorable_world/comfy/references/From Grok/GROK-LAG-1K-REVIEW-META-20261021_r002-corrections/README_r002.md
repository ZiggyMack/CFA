# GROK-LAG-1K-REVIEW-META-20261021_r002-corrections
**CFA-META-20261021 r002, "Lisan r002 corrections".** Built by HaL (Grok Bot), 2026-10-21. A small companion to r001. **r001 (`GROK-LAG-1K-REVIEW-META-20261021`) is frozen and unchanged**; read r001 first, then apply this folder. No media is re-sent and nothing was regenerated.

## What changed
1. **Lineage (LINEAGE_CORRECTIONS_r002.tsv, 70 rows, one per repair version).** r001's `parent_id` / `parent_sha256` hold the frame family's **root original**, not the edit input. r002 splits this into `root_original_sha256`, `base_sha256` (the pixels actually edited or pasted onto) and `donor_sha256s` (patches/versions used as donors), each with its source text and confidence. V_1's `final_fix_parent_sha256` is also the root original (V_1 clarification) and maps to `root_original_sha256` only. No chain was built from filenames.
   - base: LOGGED 62, INFERRED_FROM_METHOD 3, UNKNOWN 5.
   - donors: NONE_REQUIRED 23, INFERRED_FROM_METHOD 12, UNKNOWN 35 (mostly GenerateImage renders and reference crops whose hashes were never logged).
   - **C37-06_Z_4_FAIL:** Z_5 v002 (a07407f4) base = original; ALTERNATE V-PASS, does not ship. HaL v002 (1d1ed9cc, V_3 FAIL) base = Z_5 v002. HaL v003 (45775acd, **ships**) base = original a85b7707, donors a07407f4 (AL box, carried via 1d1ed9cc) and 1d1ed9cc (chin/disc box + B erase).
   - HaL v003 single-saves (C21-18, C28-19, C38-11, C38-12): base = original, donor = own v002. C37-12 v003: base original, no donor. C41-21 v003/v004/v005: each built on the original with the v002 throat-erase box as donor plus an unlogged face render; no v003->v004->v005 chain.
   - C13-04 R1: try1-try5 base UNKNOWN (re-renders, inputs not logged); try5-patch/-b/-c base = try5 (74a4e7d9), donor = root original chin ink (inferred from repairs/NOTES.md).
2. **LINEAGE_DISAGREEMENTS_r002.tsv:** every field where r001 or V_1 named a parent that differs from the logs (9 row-level + 2 field-level re-labels).
3. **STATUS_UPDATES_r002.tsv:** VIS-LAG-13_KISS-PUCKER v006 (b1a0f3f0) pending -> **V3-PASS** (V_3 return v003, sha 05b6879080d9899495ed8b99306e7a1135ed4b3b808437a5c5488dfa3da2e7c1, copy in `v_team/`); chin-fix set now 14/14 V3-PASS (chin scope only). C37-06 Z_5 v002 re-labelled ALTERNATE_V_PASS_NOT_SHIPPED.
4. **START_HERE:** `LISAN_START_HERE_ENTRY_r002.md/.json` and `LISAN_START_HERE_ROWS_r002.tsv` (rows in Z_6's START_HERE columns) for Z_6's combined START_HERE.

## Rules
Only V Team verdicts count as VALIDATED, and only for the recorded scope. HaL, Z bot and Chief scores are PRELIMINARY. No timestamps, comparisons or scores were invented; UNKNOWN means the logs don't establish it. Metadata verification and media availability are stated separately in the START_HERE entry.

## Files
- README_r002.md
- SCHEMA_ADDENDUM_r002.md
- LINEAGE_CORRECTIONS_r002.tsv
- LINEAGE_DISAGREEMENTS_r002.tsv
- STATUS_UPDATES_r002.tsv
- LISAN_START_HERE_ENTRY_r002.md
- LISAN_START_HERE_ENTRY_r002.json
- LISAN_START_HERE_ROWS_r002.tsv
- v_team/V3_LAG_chinfix_GAIB_20261021T152422Z_v003.tsv
- v_team/V3_LAG_chinfix_GAIB_20261021T152422Z_v003.tsv.sha256
- SHA256SUMS_r002.txt
