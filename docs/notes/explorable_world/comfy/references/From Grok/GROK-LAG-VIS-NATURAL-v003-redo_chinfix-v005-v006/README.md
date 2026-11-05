# GROK-LAG-VIS-NATURAL-v003-redo_chinfix-v005-v006 (HaL, 2026-10-21) — PRELIMINARY
Chin GAIB fixes (split-I "GAIIB" to GAIB) for the Lisan natural-teeth viseme set. Pixel edits only, no regeneration. This folder REPLACES the v004 chin fixes for 09, 11 (GRIN v004-try1), 12 and 13 in GROK-LAG-VIS-NATURAL-v003-redo. The other 10 v004 chin fixes (01, 02, 03, 04, 05, 06, 08, 10, 11_GRIN v001-base, 14) PASSED V_3 and stay as delivered.

## Lineage
| shape | base | v004 (V_3 v001 return) | v005 (V_3 v002 return) | v006 | current |
|---|---|---|---|---|---|
| 09_S-T-K | v001 original | FIX | PASS | — | VIS-LAG-09_S-T-K_v005-chinfix.jpg (sha 08b9252b) |
| 11_GRIN v004-try1 | GRIN v004-try1 redo | FIX | PASS (advisory: very faint smoother column) | — | VIS-LAG-11_GRIN_v004-try1_v005-chinfix.jpg (sha 72ea09d0) |
| 12_SHOUT | v001 original | FIX | PASS (B cut by frame bottom is a v001 crop defect) | — | VIS-LAG-12_SHOUT_v005-chinfix.jpg (sha fc03472e) |
| 13_KISS-PUCKER | v001 original | FIX | FIX (strip smoother and ~5 L darker) | made 2026-10-21, PENDING V_3 recheck (round 2 of 2) | VIS-LAG-13_KISS-PUCKER_v006-chinfix.jpg (sha b1a0f3f0) |

13 v006: rebuilt from the v001 base in one paste; strip around the I re-cloned from coarse-pore neighbour skin chosen by matching high-pass texture (offset -24,+3; no smoothing or blend-blur; min-error seams in a 3 px band); per-row tone matched to the side skin plus a +5 luma lift; the I is the same render as v005; one save at q100 4:4:4. Self-measured (PRELIMINARY): strip luma 102.2 vs side 100.1; strip/side high-pass texture 0.99/0.99/1.02 at sigma 1/2/3 (v005: 0.84/0.82/0.85 per V_3); 0 px over 12/255 outside the chin box x660-688 y523-590 (max 4); B unchanged (max diff 3). Before/after at 4x: SHEET-CHINFIX-GAIB_v006_13.jpg.
Only V_3's verdicts count as validation. The v005 PASSes are V_3 verdicts for the chin fix scope only, not whole-image or Ziggy acceptance. 13 v006 has no verdict yet.

## Files
VIS-LAG-*-chinfix.jpg (current fixes), SHEET-CHINFIX-GAIB_v005.jpg and _v006_13.jpg (before/after), MANIFEST.csv / SHA256SUMS / NOTES.md (full set manifest copies from the box), v3_returns/ (V_3 chinfix returns v001 and v002 with .sha256), FOLDER_SHA256SUMS.txt (this folder).
