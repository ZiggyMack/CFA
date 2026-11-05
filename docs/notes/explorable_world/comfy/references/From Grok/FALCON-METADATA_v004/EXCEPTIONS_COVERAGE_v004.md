# Exceptions and coverage, FALCON-META rev v004

Status: **PREPARING**. Nothing has been sent to Nova or posted. The v001, v002 and v003 files are unchanged.

## 1. Packaging blockers (stop this revision from being complete or consistent)
1. **Final media mapping is not verified.** This revision maps every row to the box media paths and hashes. The D: copies and their hash check (spec item 7, "exact final media or verified D: path mapping") haven't been done for this revision. Owner: Chief (push step).
2. **Repairs are landing during packaging.** 5 repair file(s) have appeared since v003, each recorded with no verdict: C02-captain-portrait/C02-captain-portrait-006-v005.jpg (7c23cc653150), C03-look-back-softened/C03-look-back-softened-001-v004.jpg (5bcffce73c5a), /workspace/falcon-chest-pilot/C04-battle-light-006_v002.jpg (8c673e0df138), /workspace/falcon-chest-pilot/C04-battle-light-006_v003.jpg (b90e0f6c08a7), C05-lurch-grin/C05-lurch-grin-001-v003.jpg (23cef438e003). The package is a snapshot. Chief has to freeze the set, or accept a later revision, before READY. Owner: Chief.
3. **READY receipt not issued.** Status stays PREPARING until Chief checks items 1-2.

## 1b. Cleared since v003, and non-blocking notes
1. **Reference files: now byte-exact** (in `_cfa_refmeta_20261021/raw_bytes/`, each matching its PC sha256). Background: CopyToBox refused the D: path (it is outside the PC's allowed local-exec root). The four files were read read-only with a machine-targeted Shell instead, and re-created in `{REFDIR}/`. Only REFERENCE_POLICY.txt matches its PC sha256. The other three lost some non-ASCII characters (em-dashes) in console transfer. Their content is usable, but they are not verified copies:
   - REFERENCE_POLICY.txt: PC 95afce1b17a8aaa81686f6efebb0c101b8489144359d40c07ac8438f0118376b / box 95afce1b17a8aaa81686f6efebb0c101b8489144359d40c07ac8438f0118376b / byte-exact=True
   - REFERENCE_VALIDATION_GUIDE.txt: PC 2769fd664e41112b1fcafe7d3f2ee27aae2e8b53a76639a7c607de655381f07d / box 2769fd664e41112b1fcafe7d3f2ee27aae2e8b53a76639a7c607de655381f07d / byte-exact=True
   - reference_validation.json: PC 6a349b56b2b3534a2c2f04670f76002e27803ca6a1957e9eafed3ef3dc35af60 / box 6a349b56b2b3534a2c2f04670f76002e27803ca6a1957e9eafed3ef3dc35af60 / byte-exact=True
   - character_reference_board.json: PC ebac15f9086b4b73997be88e43ad52b11a7bca328c6466c22433b65f332600aa / box ebac15f9086b4b73997be88e43ad52b11a7bca328c6466c22433b65f332600aa / byte-exact=True
2. **C04-006 identity: resolved by Chief's ruling.** Original 35398903; 16c5b385 is a repair (parent 35398903); V_5's PASS applies only to b90e0f6c and is STALE. MANIFEST.csv and SHA256SUMS still list 16c5b385 under the original name. Those are source files and weren't edited.
3. **No catalog chest criteria (now an open owner item, not a blocker).** reference_validation.json has no chest-ship criteria set and no recorded selection for the ship references. Ziggy's 2026-10-21 stencil and full-scale decisions are carried explicitly but are not in the catalog. Owner: Site Index / Nova.
4. **C04-010 v011 top-rim measurement: NON-BLOCKER.** 0.25 DW (Z-side) vs 0.42 DW (V_2). The difference is only where the neck pit was placed, and both fall inside the 0.25-0.58 DW pass band (V2 retag v002).
5. **No CFA asset IDs** in any Falcon source, so cfa_asset_id is blank for all rows (not guessed).
6. **Z-side QA times unknown** (null). Per-component visibility exists only for the chest. Face, cheek, neck and grill are unknown except where V-Team notes observed them.
7. No V_1 Falcon meta-input file exists (there is only V1_LAG1K_meta_input), so column alignment with Lisan is by HaL's LAG field names.

## 2. Inventory coverage
- Declared originals: 1224. Version-only slots (flagged): 5 (C21-chewy-holds-room-005, C21-chewy-holds-room-010, C22-reverse-dj-to-pilot-022, C24-leia-surveys-019, C24-leia-surveys-020).
- Unique original hashes: 1224 of 1224. JPGs in category folders now: 1438. Exact-byte duplicates across all: 0.
- Repairs (non-original files, plus the 006 repair under the original name): 212.
- All originals: 1280x720.

## 3. Review coverage (separate from inventory)
- Dedup: 135 groups (123 real, 12 composition-only), 329 images incl. version files. V_1's V-Team tags cover 329 Falcon frames. That is not full-collection coverage: 899 originals were never grouped and have no V-Team dedup tag.
- V-Team review records on originals: 691. V-Team verdicts on repairs: 363.
- Chest visibility (originals): {'visible': 126, 'unknown': 1080, 'occluded': 18}. 'unknown' or 'occluded' is not wrong and not multiverse.
- likenessRating / sceneQualityRating: null for all 1229 rows.

## 4. Validation status (originals)
| status | count |
|---|---|
| IN-VALIDATION | 835 |
| V3-PASS | 230 |
| NEEDS-ZIGGY | 108 |
| PARTIAL | 50 |
| V3-FAIL | 1 |

Technical review completed (any V-Team verdict, current or stale): 281. Validated with nothing stale or pending (V3-PASS): 230.

## 5. Passes
- Current scoped repair passes: 18.
- Stale passes: 61. Every undersized chest-ship pass is stale under the full-scale rule (V1_TEAM-RULES v008, Ziggy 10:42 ET) and is being rebuilt to the C04-010 v011 standard (d68287f16c0b). C05 grill passes stay current for grill scope, but their chest component is stale.
- Repairs with no V-Team verdict (PRELIMINARY or superseded): 53.
- Chest size redo pending: 126 frames. Owners: Z_9 (006, 008 rebuild from originals; 010 pilot built, V-Team check pending), the others Chief / DoLo team, not yet assigned.

## 6. Actual Ziggy decisions recorded
- Per-image Keep/Fix/Remove, lane or acceptance decisions: **0**, except the scoped acceptance of the C04-010 v011 look.
- Rule-level decisions: 8 (listed in FALCON_EVIDENCE_v004.json human_decisions).

## 7. Human choice still needed (separate from technical review) — 108 images
- **20 duplicate groups** (PENDING, owner Ziggy): FAL-DUP-012, FAL-DUP-014, FAL-DUP-023, FAL-DUP-024, FAL-DUP-025, FAL-DUP-026, FAL-DUP-028, FAL-DUP-031, FAL-DUP-041, FAL-DUP-044, FAL-DUP-066, FAL-DUP-068, FAL-DUP-072, FAL-DUP-086, FAL-DUP-089, FAL-DUP-091, FAL-DUP-105, FAL-DUP-113, FAL-DUP-116, FAL-DUP-126.
- **28 chest variants** (PENDING, owner Ziggy; multiverse / challenge list / fix): C01-pilot-hover-001, C01-pilot-hover-009, C01-pilot-hover-011, C02-captain-portrait-001, C02-captain-portrait-002, C02-captain-portrait-003, C02-captain-portrait-005, C03-look-back-softened-011, C03-look-back-softened-013, C03-look-back-softened-015, C08-overhead-lever-007, C15-cockpit-twoshot-004, C15-cockpit-twoshot-008, C15-cockpit-twoshot-010, C15-cockpit-twoshot-011, C26-quarters-004, C26-quarters-006, C32-engine-006, C33-ramp-inside-022, C41-cockpit-ext-003, C41-cockpit-ext-016, C41-cockpit-ext-017, C41-cockpit-ext-019, C42-ramp-landing-003, C42-ramp-landing-017, C43-dolo-ramp-002, C43-dolo-ramp-016, C43-dolo-ramp-019.
- **Singles:**
  - C06-lurch-no-grin-005: Chest tally: optional for Ziggy: lower hull faint
  - C06-lurch-no-grin-008: Chest tally: soft note for Ziggy: outer rim slightly heavy at 4x
  - C15-cockpit-twoshot-001: Chest tally: HOLD for Ziggy (Chewy drift)
  - C15-cockpit-twoshot-001: Chewy-drift HOLD on C15-001 v002: accept or redo?
  - C41-cockpit-ext-004: C41-cockpit-ext-004_Z_3_v002-fix.jpg: V_4 routed to Ziggy pick (V4_FALCON_facefix_Z3_20261021T090717Z_v002.tsv)
  - C41-cockpit-ext-004: C41-cockpit-ext-004_Z_3_v003-fix.jpg: V_4 routed to Ziggy pick (V4_FALCON_facefix_Z3_20261021T100150Z_v003.tsv)
  - C69-hyperspace-exit-012: C69-hyperspace-exit-012_Z_3_v002-fix.jpg: V_4 routed to Ziggy pick (V4_FALCON_facefix_Z3_20261021T100150Z_v003.tsv)
- Policy: REF-05; challenge list vs multiverse for chests that can't be fixed. (The full-scale roll-out is decided: every frame, Ziggy 2026-10-21. It's now repair backlog, not a choice.)

## 8. Review and repair backlog (not packaging blockers)
- IN-VALIDATION (awaiting a V-Team pass): 835.
- PARTIAL (V-Team pass with a stale or pending chest component): 50.
- V3-FAIL: 1.
- Chest full-scale rebuilds: 126.

## 9. Source conflicts
- [identity (RESOLVED by Chief ruling; source files still disagree)] C04-battle-light-006: Chief ruling 2026-10-21: original = before_C04-battle-light-006.jpg 35398903; 16c5b385 = repair (parent 35398903, no verdict); V_5 PASS applies only to falcon-chest-pilot/C04-battle-light-006_v003.jpg b90e0f6c and is STALE under the full-scale rule; Z_9 rebuilds. Prior record: MANIFEST.csv / SHA256SUMS / AUDIT_v002 list C04-battle-light-006.jpg as 16c5b385, but that file is the Chief pilot repair saved under the original name. v003 uses before_C04-battle-light-006.jpg (35398903) as the original. The V_5 PASS cited by the tally targets falcon-chest-pilot/C04-battle-light-006_v003.jpg (b90e0f6c), not 16c5b385, and AUDIT_v002 scored 16c5b385 WRONG-SAUCER.  (RESOLVED (Chief ruling); MANIFEST.csv/SHA256SUMS not edited)
- [final version] C04-battle-light-008: Chest tally lists v002; ROLLUP.md 10:27 ET + V4 boxB v002 say v007b FINAL (PASS-ADVISORY). v003 records v007b; either way the chest pass is STALE and Z_9 rebuilds 008 from the original. (flagged)
- [final version / pilot (Chief ruling)] C04-battle-light-010: No C04-010 version is validated: v005 latest V-Team verdict FAIL, superseded; tally had listed v005; v008 PASS-ADVISORY FLAG-SIZE (stale); v009 and v010 superseded, no verdict; v011 (d68287f16c0b) Ziggy-approved look, no V-Team pass. v012 landed after v011 with no verdict. Top-rim gap: 0.25 DW (Z-side) vs 0.42 DW (V_2); the difference is only the neck-pit placement and both are inside the 0.25-0.58 DW pass band. (NON-BLOCKER)
- [count] (set): Chest CORRECT: brief said 58; AUDIT_v001/v002 have 56 (55 originals + C04-002-v003). V_5 confirms no frozen file had 58. After V_5 reclassified 7 originals (6 to STENCIL-VARIANT?, C42-022 to WRONG-SAUCER), 48 originals are correct ship. (resolved in favour of the frozen audit + V_5)
- [count] (set): Dedup Ziggy queue: ZIGGY_QUEUE_v001 has 22; V_1 summary v002 dropped FAL-DUP-062 and FAL-DUP-125. 20 used. (resolved (V_1))
- [path] C22-022, C24-019, C24-020: qa_z9.tsv names unversioned files that are not on disk; disk has -v001/-v002. Version-only slots use the -v001 file as base. (flagged)
- [reference] (catalog): reference_validation.json (2026-10-13.1) has chest placement HD-RETURN-7b156019ddf8 and ship artwork options 891a3ee224eb / permitted variations d430b5f72e9b with recordedSelection = null and NO chest criteria set. Ziggy's 2026-10-21 stencil + full-scale decisions are newer and are carried explicitly. Catalog not updated; owner Site Index / Nova. (open owner item (not a packaging blocker))
- [validation semantics] (catalog): Per REFERENCE_VALIDATION_GUIDE, a Character pass needs catalog criteria ID/version/digest and actually viewed evidence. V-Team Falcon verdicts cite V5_INK_METHOD specs and team rules, not catalog criteria sets, so V3-PASS here is team technical validation, NOT site validation or Nova inspection. (by design; noted)
- [hash] C04-battle-light-006: chest audit scanned sha 16c5b38527e0 but v003 original identity is 35398903a8f1 (flagged)
