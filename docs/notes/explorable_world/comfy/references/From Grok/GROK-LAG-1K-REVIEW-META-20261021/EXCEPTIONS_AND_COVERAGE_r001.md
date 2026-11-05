# LAG-1K review-metadata package r001: exceptions and coverage report
Status: PREPARING (becomes READY only after the Chief's receipt, once every file is copied to D: and hash-verified). Built by HaL (Grok Bot) on 2026-10-21. Everything authored by HaL, the Z bots or the Chief is PRELIMINARY. Only V Team verdicts are VALIDATED, and only for their recorded scope. No Nova inspection is implied.

## 1. Reconciled totals
| item | count | source |
|---|---|---|
| Declared originals | 1000 | spec: one record per declared original |
| Originals on disk (box) | 997 | LAG-1K/C01-C45 top-level drafts; ROLLUP.md also says 997 |
| Declared but not on disk (placeholder rows) | 3 | LAG-1K-DECLARED-UNACCOUNTED-001..003; no ID/hash invented |
| Unique original sha256 | 997 | exact-byte duplicates among originals: 0 |
| Originals hash-verified on D: | 997 / 997 | D: scan 2026-10-21 about 11:15 EDT |
| Repair/fix versions (separate lineage, not originals) | 70 | 62 *-fix* files + 8 C13-04_Z_1 R1 repairs |
| ...on D: (hash match) | 55 | all 70 also shipped in media/repairs/ |
| Current scoped passes (final passed version per original) | 47 | V_3, face/chin fix scope only: v002 x35, v003 x11, v005 x1 |
| Superseded fix versions | 15 | 14 failed/partial (V_3) + 1 stale pass (parallel C37-06 Z_5 v002) |
| Fix versions with no V Team verdict | 8 | the 8 C13-04_Z_1 R1 repairs (bot self-scores only) |
| Stale / superseded pass or verdict entries | 4 | evidence JSON stale_or_superseded |
| V_3 fix-check rows (all return versions) | 294 | 62 rows in current returns (check v005, redocheck v004) |
| Dedup groups | 43 | 192 members; tags: VARIANT 128, KEEP-IDEA-FIX-FACE 47, NOT-A-DUP 11, DRIFT-MULTIVERSE 5, DUPLICATE-KEEPER 1 |
| Proposed duplicate keepers | 1 | LAG-DUP-019 keeper C21-05_Z_2 (V_3 proposal) |
| Open user choices (ZIGGY-PICK) | 1 | sub-shot 015-B: C15-14_Z_5, C15-20_Z_5, C15-22_Z_5 |
| Actual per-image Ziggy decisions | 0 | none recorded in any source; set-level Lisan rules (c02 worms, CAND-01 build, one ear hoop + brow ring, eyes variable) come from V1_TEAM-RULES_ziggy_decisions v008 |

## 2. Coverage (kept separate)
- Inventory coverage: 997 of 1000 declared originals are on disk, and 997 of 997 are hash-verified on D:. 3 declared originals are unaccounted for.
- Reviewed coverage (V Team): 192 of 1000 (19.2%) have V Team review. All 192 carry a dedup/multiverse proposal (PRELIMINARY until Ziggy), and 47 also have a VALIDATED fix-scope pass. 808 originals (805 on disk + 3 placeholders) have no V Team review. The 192-image dedup pass does NOT mean the whole set passed.
- Bot preliminary coverage (not validation): 714 on-disk originals have only a bot NOTES line or self-score, and 91 have nothing parseable. Preliminary classes for on-disk originals: STRONG 530, DEFECT 139, null 109, PASS (text only) 89, FAIL 50, FAIL (filename tag) 47, SOFT PASS (text only) 19, FAIL (text) 14.

## 3. Technical review completed vs human choice still needed
Technical review completed (V Team): 47 fix-scope passes (exact versions in the index); dedup tagging of 192 images in 43 groups; 12 failing v002-era fixes re-done and passed as v003 (C41-21 as v005).
Human choice still needed (owner Ziggy unless noted):
- All 192 dedup/multiverse tags (PENDING ZIGGY), including the 5 DRIFT-MULTIVERSE proposals and the LAG-DUP-019 keeper proposal.
- The 1 open pick, LAG-DUP-015 sub-shot 015-B (V_4 recommends redoing C15-20).
- The open set-wide items from V1_TEAM-RULES v008: LAG-1K set-wide younger face; LAG-1K flavor and ZIGGY-PICK sheets.
- Keep/fix/remove, lane, archive state and human acceptance are null for every row. They are Ziggy's calls, and nothing was inferred.
- C13-04_Z_1 R1 repairs (storyboard prime): try5-patch-c is the bot-preferred candidate, with no V Team verdict yet (owner: V Team, then Ziggy).
- 805 on-disk originals with no V Team review (owner: V Team, if a full pass is wanted).

## 4. Packaging blockers (separate from the review backlog)
- None open for this revision once the D: copy is hash-verified. The 3 unaccounted declared originals are an inventory question (owner: HaL/Chief), not a packaging fault; they are recorded as explicit UNKNOWN rows.
- Repair media not present on D: before this push: 15 (C13-05_Z_1@v002-Z_5, C21-13_Z_2_FAIL@v002-Z_5, C21-18_Z_2_FAIL@v002-HaL, C22-13_Z_2@v002-Z_5, C28-19_Z_3@v002-HaL, C32-18_Z_3@v002-Z_5, C37-06_Z_4_FAIL@v002-Z_5, C37-06_Z_4_FAIL@v002-HaL, C37-12_Z_4@v002-HaL, C38-11_Z_4@v002-HaL, C38-12_Z_4@v002-HaL, C41-21_Z_11@v002-HaL, C41-21_Z_11@v003-HaL, C41-21_Z_11@v004-HaL, C43-15_Z_2@v002-Z_5). They ship inside this package under media/repairs/.

## 5. Exceptions
- V_1 input vs V_3 returns: newest V_1 input is V1_LAG1K_meta_input_20261021T150944Z_v002.tsv (sha256 in audit_sheets). Its final fix version and verdict match the V_3 current returns on all 47 rows (0 disagreements). The spec named v001 (150004Z) as frozen; v002 arrived 9 minutes later and was used as "newest". v001 rows that differ from v002: 0.
- Lineage caution resolved: V_3's check v005 failed 12 v002-era files (C13-05, C21-13, C21-18, C22-13, C28-19, C32-18, C37-06 HaL, C37-12, C38-11, C38-12, C43-15 FAIL; C41-21 PARTIAL). They are kept as SUPERSEDED with V_3's verdicts; their passes are v003 (C41-21 v005, after v003 PARTIAL and v004 FAIL).
- C37-06_Z_4_FAIL has two parallel v002 fixes: Z_5 v002 PASS and HaL v002 FAIL, and HaL v003 PASS is the selected final (as in V_1 input). The Z_5 v002 pass is recorded as a stale pass valid only for its own file.
- C22-13_Z_2 v002: V_3 check v001-v003 said PARTIAL; v004/v005 changed it to FAIL per V_1 ruling 03:13 ET. The earlier PARTIALs are stale.
- Bot self-score vs V Team: 16 originals have a bot L4/L5 self-score but a V Team DRIFT-MULTIVERSE or KEEP-IDEA-FIX-FACE tag (C13-10_Z_11, C13-13_Z_11, C13-18_Z_11, C15-14_Z_5, C15-18_Z_5, C15-20_Z_5, C15-22_Z_5, C38-06_Z_4, C38-10_Z_4, C38-11_Z_4, C38-12_Z_4, C38-13_Z_4, C38-21_Z_4, C41-02_Z_11, C41-04_Z_11, C41-09_Z_11). V Team stands; bot scores remain PRELIMINARY.
- NOTES lines with ambiguous short IDs (not assigned): 3 (C11-canyon-fort/NOTES.md:24 C11-07 -> C11-07_Z_1/C11-07_Z_11; C12-cliff-sietch/NOTES.md:9 C12-07 -> C12-07_Z_1/C12-07_Z_11; C13-sandworm-rising/NOTES.md:9 C13-07 -> C13-07_Z_1/C13-07_Z_11).
- CFA asset IDs: none of the LAG-1K images appear in reference_validation.json or character_reference_board.json, so cfa_asset_id is null for every row (never guessed).
- V_3 fix-check rows do not record the reference asset ID/hash/version or a criteria version. Those fields are null; the applicable CFA scope is lisan-face (criteria 2026-10-13.1, sha256 46bc215b...).
- Per-component visibility (visible/occluded/missing/unknown) was not recorded for LAG-1K originals by any V Team return, so every component is "unknown" (not assessed, not wrong).
- likenessRating and sceneQualityRating are null for every row: no V Team or human likeness/scene ratings exist for LAG-1K. Bot L/S self-scores sit in prelim_likeness_self / prelim_scene_self only.
- The VIS-LAG chin-fix set (incl. 13_KISS-PUCKER, FIX at V_3 v002, v006 pending recheck) is a separate dataset and ships in its own folder, not in this package.

## 6. Reference files read (box copies, hashes verified against Z_6 .sha256 files)
- REFERENCE_POLICY.txt: 95afce1b17a8aaa81686f6efebb0c101b8489144359d40c07ac8438f0118376b
- REFERENCE_VALIDATION_GUIDE.txt: 5f59ce8bf24ae1f54aaa98332c68d8253bb2f38174d22e39d923da49c9d1d612
- reference_validation.json: e45c01dc2e64dd1e2586c35ffb5b6ced0d21f0ad423505444d8b6362ddc7913b
- character_reference_board.json: b6196f986e8a75ecca7a8664e970262087636c5703815a709482f4e6273780b4
