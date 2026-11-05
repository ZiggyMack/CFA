# GROK-LAG-1K-FIXES-20261021 — Lisan Al Gaib LAG-1K tattoo / face fixes (for CFA Nova)

From HaL (Grok), 2026-10-21. **All self-scores are preliminary.** V_3 verdicts come from V Team (files in `_verdicts_V3/`).

## What this is
The final passing fix for each of **47 LAG-1K frames** that had tattoo or face errors (chin GAIB letters, AL glyph, sun-disc eye, brow rings, throat tattoo, mouth grill, face identity drift). Fixes are by HaL and Z_5. Each frame has exactly ONE fix file here: the latest version that passed V_3 (v003 where a redo was needed, v005 for C41-21, otherwise v002). Older superseded versions are not included.

Every fix was pasted onto the ORIGINAL frame pixels and saved once at high quality. V_3 confirmed 0 px over 12/255 changed outside each fix area. **All 47 are V_3 PASS.**

## Rule: originals are kept, fixes sit beside them
- Nothing on D: was replaced or deleted. The originals are still in their existing `From Grok` folders (paths in the table, all sha256-verified on D: before this push), so they are **not** duplicated here.
- Fix files keep the original name plus a suffix (`_v00N-fix-HaL`, `_v00N-fix-Z5` or `_Z_5_v00N-fix`) and sit in the same category subfolder name as the original (e.g. `C41-ash-dunes/`).
- To use a fix: use the fix file in place of the original for that frame. Keep the original unless Ziggy says otherwise.

## Folder layout
- `C??-<category>/` — the fix files (47)
- `FIX_INDEX.tsv` — same table as below, machine-readable, with fix sha256s
- `_sheets/` — before/after sheets (Z_5 DGH and F groups; HaL v003 C21-18/C37-06/C37-12; C41-21 v003/v004/v005 history; V_3 identity crops for C41-21 v004/v005)
- `_verdicts_V3/` — V_3 check `V3_LAGFIX_check_20261021T071557Z_v005.tsv` plus every `V3_LAGFIX_redocheck_*` (latest = `..073629Z_v004`), with .sha256 sidecars
- `_fix_logs/` — the fixers' own logs (HaL_FIXES_v001.tsv, Z5_fixes_DGH_v001.tsv, Z5_FG_v001.tsv, Z5_v003_redos_v001.tsv; these list every attempt incl. superseded ones)
- `SHA256SUMS` — every file in this package

## Fix → original table
| frame | fix file (in category folder) | ver | replaces original (on D:, under From Grok) | what changed | by | V_3 | self-score (prelim) |
|---|---|---|---|---|---|---|---|
| C03-13_Z_11 | `C03-wasteland-highway/C03-13_Z_11_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C03\C03-wasteland-highway\C03-13_Z_11.jpg` | chin GAB -> GAIB | HaL | PASS | 4 |
| C03-17_Z_11 | `C03-wasteland-highway/C03-17_Z_11_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C03\C03-wasteland-highway\C03-17_Z_11.jpg` | chin GAB -> GAIB | HaL | PASS | 4 |
| C06-11_Z_5 | `C06-convoy-chase/C06-11_Z_5_Z_5_v002-fix.jpg` | v002 | `GROK-LAG-1K-G1\C06-convoy-chase\C06-11_Z_5.jpg` | throat tattoo -> c02 style: gen edit (src + c02 throat crop), soft-ellipse throat composite (also listed in Z… | Z_5 | PASS | L4/S4 |
| C13-05_Z_1 | `C13-sandworm-rising/C13-05_Z_1_v003-fix-Z5.jpg` | v003 | `GROK-LAG-1K-C13\C13-sandworm-rising\C13-05_Z_1.jpg` | face fix toward LAG-LOCK-FACE: same gen 46c9f3dc composited onto untouched original; feathered mask clipped t… | Z_5 | PASS | L4/S4 |
| C13-10_Z_11 | `C13-sandworm-rising/C13-10_Z_11_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C13\C13-sandworm-rising\C13-10_Z_11.jpg` | chin GIB -> GAIB | HaL | PASS | 4 |
| C13-13_Z_11 | `C13-sandworm-rising/C13-13_Z_11_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C13\C13-sandworm-rising\C13-13_Z_11.jpg` | chin GAB -> GAIB | HaL | PASS | 4 |
| C13-18_Z_11 | `C13-sandworm-rising/C13-18_Z_11_Z_5_v002-fix.jpg` | v002 | `GROK-LAG-1K-C13\C13-sandworm-rising\C13-18_Z_11.jpg` | throat tattoo -> c02 style: gen edit (src + c02 throat crop), soft-ellipse throat composite (also listed in Z… | Z_5 | PASS | L4/S4 |
| C15-18_Z_5 | `C15-worm-tracks-thumper/C15-18_Z_5_v002-fix-Z5.jpg` | v002 | `GROK-LAG-1K-C15\GROK-LAG-1K-C15\C15-18_Z_5.jpg` | face fix toward LAG-LOCK-FACE: gen face edit (src + LAG-LOCK-FACE-NATURAL face crop), aligned, soft-ellipse f… | Z_5 | PASS | L4/S4 |
| C15-20_Z_5 | `C15-worm-tracks-thumper/C15-20_Z_5_v002-fix-Z5.jpg` | v002 | `GROK-LAG-1K-C15\GROK-LAG-1K-C15\C15-20_Z_5.jpg` | face fix toward LAG-LOCK-FACE: gen face edit (src + LAG-LOCK-FACE-NATURAL face crop), aligned, soft-ellipse f… | Z_5 | PASS | L4/S4 |
| C16-20_Z_1 | `C16-oil-refinery-ruins/C16-20_Z_1_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-G1\C16-oil-refinery-ruins\C16-20_Z_1.jpg` | black cheek stripe removed | HaL | PASS | 4 |
| C20-06_Z_2 | `C20-dry-riverbed/C20-06_Z_2_v002-fix-Z5.jpg` | v002 | `GROK-LAG-1K-G1\C20-dry-riverbed\C20-06_Z_2.jpg` | face fix toward LAG-LOCK-FACE: gen face edit (src + LAG-LOCK-FACE-NATURAL face crop), aligned, soft-ellipse f… | Z_5 | PASS | L4/S4 |
| C20-18_Z_2 | `C20-dry-riverbed/C20-18_Z_2_v002-fix-Z5.jpg` | v002 | `GROK-LAG-1K-G1\C20-dry-riverbed\C20-18_Z_2.jpg` | face fix toward LAG-LOCK-FACE: gen face edit (src + LAG-LOCK-FACE-NATURAL face crop), aligned, soft-ellipse f… | Z_5 | PASS | L4/S4 |
| C21-04_Z_2_FAIL | `C21-glass-desert/C21-04_Z_2_FAIL_v002-fix-Z5.jpg` | v002 | `GROK-LAG-1K-G1\C21-glass-desert\C21-04_Z_2_FAIL.jpg` | face fix toward LAG-LOCK-FACE: gen face edit (src + LAG-LOCK-FACE-NATURAL face crop), aligned, soft-ellipse f… | Z_5 | PASS | L4/S4 |
| C21-08_Z_2_FAIL | `C21-glass-desert/C21-08_Z_2_FAIL_Z_5_v002-fix.jpg` | v002 | `GROK-LAG-1K-G1\C21-glass-desert\C21-08_Z_2_FAIL.jpg` | AL glyph fix: pixel edit: triangle AL inpainted, donor AL (C22-09) stamped tone-matched | Z_5 | PASS | L4/S4 |
| C21-13_Z_2_FAIL | `C21-glass-desert/C21-13_Z_2_FAIL_Z_5_v003-fix.jpg` | v003 | `GROK-LAG-1K-G1\C21-glass-desert\C21-13_Z_2_FAIL.jpg` | AL glyph fix: pixel: erase+donor AL as v002, pasted patch-only box 601,113,648,157 onto untouched original; q… | Z_5 | PASS | L4/S4 |
| C21-18_Z_2_FAIL | `C21-glass-desert/C21-18_Z_2_FAIL_v003-fix-HaL.jpg` | v003 | `GROK-LAG-1K-G1\C21-glass-desert\C21-18_Z_2_FAIL.jpg` | chin GAB -> GAIB | HaL | PASS | 4 |
| C22-05_Z_2_FAIL | `C22-bone-fields/C22-05_Z_2_FAIL_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-G1\C22-bone-fields\C22-05_Z_2_FAIL.jpg` | duplicate GAIB removed; missing eye sun-disc added (c02 style) | HaL | PASS | 4 |
| C22-08_Z_2_FAIL | `C22-bone-fields/C22-08_Z_2_FAIL_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-G1\C22-bone-fields\C22-08_Z_2_FAIL.jpg` | second eye disc removed | HaL | PASS | 4 |
| C22-09_Z_2_FAIL | `C22-bone-fields/C22-09_Z_2_FAIL_Z_5_v002-fix.jpg` | v002 | `GROK-LAG-1K-G1\C22-bone-fields\C22-09_Z_2_FAIL.jpg` | AL glyph fix: pixel edit: extra small AL removed (inpaint + skin texture), main AL kept | Z_5 | PASS | L4/S4 |
| C22-13_Z_2 | `C22-bone-fields/C22-13_Z_2_Z_5_v003-fix.jpg` | v003 | `GROK-LAG-1K-G1\C22-bone-fields\C22-13_Z_2.jpg` | mouth grill removed: pixel, no render: worked from the ORIGINAL (keeps parted lips/expression); metal lower p… | Z_5 | PASS | L4/S4 |
| C22-14_Z_2_FAIL | `C22-bone-fields/C22-14_Z_2_FAIL_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-G1\C22-bone-fields\C22-14_Z_2_FAIL.jpg` | chin GAICB -> GAIB, moved fully onto chin | HaL | PASS | 4 |
| C22-15_Z_2_FAIL | `C22-bone-fields/C22-15_Z_2_FAIL_Z_5_v002-fix.jpg` | v002 | `GROK-LAG-1K-G1\C22-bone-fields\C22-15_Z_2_FAIL.jpg` | AL glyph fix: pixel edit: own A and L moved together between brows, stray L in hairline removed | Z_5 | PASS | L4/S4 |
| C22-22_Z_2_FAIL | `C22-bone-fields/C22-22_Z_2_FAIL_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-G1\C22-bone-fields\C22-22_Z_2_FAIL.jpg` | chin GAIBI -> GAIB | HaL | PASS | 4 |
| C23-04_Z_2_FAIL | `C23-buried-city/C23-04_Z_2_FAIL_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-G1\C23-buried-city\C23-04_Z_2_FAIL.jpg` | doubled GAIB below disc removed; chin GAIB kept | HaL | PASS | 4 |
| C24-01_Z_5 | `C24-night-desert-stars/C24-01_Z_5_Z_5_v002-fix.jpg` | v002 | `GROK-LAG-1K-G1\C24-night-desert-stars\C24-01_Z_5.jpg` | throat tattoo -> c02 style: gen edit (src + c02 throat crop), soft-ellipse throat composite (also listed in Z… | Z_5 | PASS | L4/S4 |
| C24-19_Z_5_FAIL | `C24-night-desert-stars/C24-19_Z_5_FAIL_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-G1\C24-night-desert-stars\C24-19_Z_5_FAIL.jpg` | chin GAB -> GAIB | HaL | PASS | 4 |
| C24-21_Z_5 | `C24-night-desert-stars/C24-21_Z_5_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-G1\C24-night-desert-stars\C24-21_Z_5.jpg` | stroke through lips removed; GAIB intact | HaL | PASS | 4 |
| C28-11_Z_3 | `C28-harpoon-war-pole/C28-11_Z_3_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-G1\C28-harpoon-war-pole\C28-11_Z_3.jpg` | eye added to sun disc | HaL | PASS | 4 |
| C28-19_Z_3 | `C28-harpoon-war-pole/C28-19_Z_3_v003-fix-HaL.jpg` | v003 | `GROK-LAG-1K-G1\C28-harpoon-war-pole\C28-19_Z_3.jpg` | dot-only disc now has an eye | HaL | PASS | 4 |
| C29-03_Z_3 | `C29-dust-duel/C29-03_Z_3_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C29\C29-dust-duel\C29-03_Z_3.jpg` | stray letters removed | HaL | PASS | 4 |
| C32-18_Z_3 | `C32-prayer-on-dune/C32-18_Z_3_v003-fix-Z5.jpg` | v003 | `GROK-LAG-1K-C32\C32-18_Z_3.jpg` | face fix toward LAG-LOCK-FACE: gen d37fdab2 box-clipped composite; wrong-side ring inpainted; single clean ri… | Z_5 | PASS | L4/S4 |
| C37-06_Z_4_FAIL | `C37-tanker-explosion/C37-06_Z_4_FAIL_v003-fix-HaL.jpg` | v003 | `GROK-LAG-1K-C37\C37-06_Z_4_FAIL.jpg` | Z_5 AL + HaL chin GAIB + c02 eye disc combined in one save | HaL | PASS | 4 |
| C37-11_Z_4 | `C37-tanker-explosion/C37-11_Z_4_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C37\C37-11_Z_4.jpg` | chin GAB -> GAIB | HaL | PASS | 4 |
| C37-12_Z_4 | `C37-tanker-explosion/C37-12_Z_4_v003-fix-HaL.jpg` | v003 | `GROK-LAG-1K-C37\C37-12_Z_4.jpg` | chin GAB -> GAIB at full letter size | HaL | PASS | 4 |
| C38-06_Z_4 | `C38-sinkhole-collapse/C38-06_Z_4_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C38\C38-06_Z_4.jpg` | eye added to plain sun disc | HaL | PASS | 4 |
| C38-10_Z_4 | `C38-sinkhole-collapse/C38-10_Z_4_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C38\C38-10_Z_4.jpg` | eye added to plain sun disc | HaL | PASS | 4 |
| C38-11_Z_4 | `C38-sinkhole-collapse/C38-11_Z_4_v003-fix-HaL.jpg` | v003 | `GROK-LAG-1K-C38\C38-11_Z_4.jpg` | eye added to sun disc | HaL | PASS | 4 |
| C38-12_Z_4 | `C38-sinkhole-collapse/C38-12_Z_4_v003-fix-HaL.jpg` | v003 | `GROK-LAG-1K-C38\C38-12_Z_4.jpg` | eye added to sun disc | HaL | PASS | 4 |
| C38-13_Z_4 | `C38-sinkhole-collapse/C38-13_Z_4_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C38\C38-13_Z_4.jpg` | eye added to disc; stray letters under disc removed | HaL | PASS | 4 |
| C38-21_Z_4 | `C38-sinkhole-collapse/C38-21_Z_4_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C38\C38-21_Z_4.jpg` | clear eye added to sun disc | HaL | PASS | 4 |
| C41-02_Z_11 | `C41-ash-dunes/C41-02_Z_11_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C41\C41-ash-dunes\C41-02_Z_11.jpg` | chin GAB -> GAIB | HaL | PASS | 4 |
| C41-04_Z_11 | `C41-ash-dunes/C41-04_Z_11_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C41\C41-ash-dunes\C41-04_Z_11.jpg` | chin GAB -> GAIB | HaL | PASS | 4 |
| C41-09_Z_11 | `C41-ash-dunes/C41-09_Z_11_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C41\C41-ash-dunes\C41-09_Z_11.jpg` | chin GAB -> GAIB | HaL | PASS | 4 |
| C41-21_Z_11 | `C41-ash-dunes/C41-21_Z_11_v005-fix-HaL.jpg` | v005 | `GROK-LAG-1K-C41\C41-ash-dunes\C41-21_Z_11.jpg` | face regen toward LAG-LOCK-FACE incl. brows/eyes/nose; light stubble blended into neck | HaL | PASS | 4 |
| C43-15_Z_2 | `C43-rig-rooftop-sentinel/C43-15_Z_2_v003-fix-Z5.jpg` | v003 | `GROK-LAG-1K-G1\C43-rig-rooftop-sentinel\C43-15_Z_2.jpg` | face fix toward LAG-LOCK-FACE: gen 53907a30 box-clipped composite; upper ring fragment inpainted, one clean r… | Z_5 | PASS | L4/S4 |
| C44-01_Z_4_FAIL | `C44-oasis-ruins/C44-01_Z_4_FAIL_v002-fix-HaL.jpg` | v002 | `GROK-LAG-1K-C44\C44-oasis-ruins\C44-01_Z_4_FAIL.jpg` | chin GAB -> GAIB | HaL | PASS | 4 |
| C44-06_Z_2 | `C44-oasis-ruins/C44-06_Z_2_Z_5_v002-fix.jpg` | v002 | `GROK-LAG-1K-C44\C44-oasis-ruins\C44-06_Z_2.jpg` | throat tattoo -> c02 style: gen edit (src + c02 throat crop), soft-ellipse throat composite (also listed in Z… | Z_5 | PASS | L4/S4 |

Self-scores: HaL uses a single 1–5 score; Z_5 uses L (likeness) / S (spec) 1–5. V_3 notes for each row (minor, out-of-scope items such as pre-c02 worm styles) are in `FIX_INDEX.tsv` and `_verdicts_V3/`.

## Superseded / not included
- C37-06_Z_4_FAIL: Z_5's `C37-06_Z_4_FAIL_Z_5_v002-fix.jpg` (AL fix) is superseded by HaL's `C37-06_Z_4_FAIL_v003-fix-HaL.jpg`, which combines Z_5's AL + HaL's chin GAIB + disc eye in one save on the original. Use v003 only.
- C41-21: v002–v004 were rejected by V_3 (face identity). Only v005 is included.
- C37-12: an ALT 0.9x GAIB version also passed but was not picked; the delivered 1.0x (v003) is the pick.
- C13-05, C21-13, C32-18, C43-15, C22-13 (Z_5) and C21-18, C28-19, C38-11, C38-12 (HaL): v002s failed V_3 (mostly JPEG re-save noise); only the passing v003s are here.

## Open items
- **C41-21 brow ring** (and nostril hoop): absent on v005, but also absent in the original frame, so outside this fix. Logged separately; not a blocker. V_3 also accepted: nose slightly narrow, face slightly lean, cooler overcast grade than the warm lock.
- **C37-06** (optional): chin A and B are 0.72x / 0.64x the size of the G. Left as-is because full-size B would run past the jaw onto the sun disc; frame passed.
- **LIPS-PRESSED-THIN** is partial and on the challenge list; **SING-VOWEL r2** is proposed but awaiting Ziggy (both in the viseme package `GROK-LAG-VIS-NATURAL-v003-redo`).
- Old-style (pre-c02) worm tattoos are not failed while Ziggy decides.

## SHA256SUMS
See `SHA256SUMS` in this folder (covers every file except SHA256SUMS itself; README.md is hashed too, as written at packaging time). Check with `sha256sum -c SHA256SUMS` or PowerShell `Get-FileHash`.
