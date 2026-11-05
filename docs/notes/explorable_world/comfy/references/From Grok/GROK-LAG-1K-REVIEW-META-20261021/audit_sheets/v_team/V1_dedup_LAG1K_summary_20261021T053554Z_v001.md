# LAG-1K duplicate pass: roll-up for Ziggy (V_1, 20261021T053554Z)
Everything here is **pending Ziggy**. This was a tag-only pass. Nothing was moved or deleted.
Files: `V1_dedup_LAG1K_rollup_20261021T053554Z_v001.tsv` (sha256 2756cfb486dde70f70b675cadcbee16dde695140924cac9b5c16e63829fc9125) and `V1_dedup_LAG1K_fixlist_20261021T053554Z_v001.tsv` (sha256 4212d6122ebf3abd136638d5539d10b184a0516a6efecaf78aa353007108533e).

## Totals (192 images, 43 clusters, pending Ziggy)
| tag | V2 | V3 | V4 | V5 | total |
|---|---|---|---|---|---|
| VARIANT | 20 | 28 | 39 | 41 | 128 |
| KEEP-IDEA-FIX-FACE | 24 | 14 | 4 | 5 | 47 |
| NOT-A-DUP | 5 | 2 | 3 | 1 | 11 |
| DRIFT-MULTIVERSE | 0 | 2 | 2 | 1 | 5 |
| DUPLICATE-KEEPER | 0 | 1 | 0 | 0 | 1 |
| DUPLICATE | 0 | 0 | 0 | 0 | 0 |
| **images** | 49 | 47 | 48 | 48 | 192 |
V4 is final after v002 (9 landmark-swap rows went to VARIANT) and v003 (C23-04 went to KEEP-IDEA-FIX-FACE). There is one ZIGGY-PICK sub-shot: V4 015-B.

## Duplicates and review load (pending Ziggy)
- **0 DUPLICATE rows.** Under your rule, where lighting, FX, backdrop, landmark and expression changes all count as different, no image is purely redundant. The duplicate step does not shrink the 192.
- 5 images are DRIFT-MULTIVERSE (they add nothing and the character drifted), so they can go to the multiverse pile. If you agree, the working set is 187 (−2.6%).
- 11 images were grouped by mistake (NOT-A-DUP). They return to the general pool.

## Fix list: 47 images (KEEP-IDEA-FIX-FACE, pending Ziggy)
Each one is redone from the locked anchor with only the face changed. Images are grouped by the main feature that drifted:
- chin reads GAB (I missing): 11
- eye disc wrong (no eye / extra disc): 9
- identity: reads as a different / older / younger man: 8
- other chin GAIB misreads / misplacement: 5
- AL glyph wrong: 5
- throat worms broken (not just pre-c02 style): 4
- GAIB doubled: 2
- stray or non-canon face marks: 2
- teeth not natural: 1
- Many rows also carry secondary issues, such as worm style or stray marks. These are kept in the lane note column.

## Sheets (renders/dedup_sheets/, pending Ziggy)
- `SHEET_LAG-DUP-015-B_v001.jpg` (3 tiles of 3): choose which thumper version to redo on-model; V_4 recommends redoing C15-20 (all 3 faces drift).
- `SHEET_LAG-DUP-017-A_v001.jpg` (10 tiles of 10): pick favourite backdrops/lighting; C20-06, C20-18 on fix list, C20-20 multiverse.
- `SHEET_LAG-DUP-029-A_v001.jpg` (12 tiles of 12): pick favourite moods/lighting; C32-18 on fix list.
- `SHEET_LAG-DUP-040-A_v001.jpg` (4 tiles of 4): pick favourite; C43-15 on fix list.
- `SHEET_LAG-DUP-020-A_part1of2_v001.jpg` (10 tiles of 20): pick favourite backdrops; 7 of 20 on fix list.
- `SHEET_LAG-DUP-020-A_part2of2_v001.jpg` (10 tiles of 20): pick favourite backdrops; 7 of 20 on fix list.
- `SHEET_LAG-DUP-022-A_v001.jpg` (6 tiles of 6): pick favourite; 3 of 6 on fix list.
- `SHEET_LAG-DUP-033-A_v001.jpg` (4 tiles of 4): pick favourite; only C37-19 is on-model and its worms are cobra, not c02.
- `SHEET_LAG-DUP-042-A_v001.jpg` (4 tiles of 4): pick favourite; C44-01, C44-06 on fix list.
- `SHEET_LAG-DUP-019-ALL_part1of2_v001.jpg` (9 tiles of 18): pick favourite settings; C21-05 keeper vs C21-21 multiverse; 4 on fix list.
- `SHEET_LAG-DUP-019-ALL_part2of2_v001.jpg` (9 tiles of 18): pick favourite settings; C21-05 keeper vs C21-21 multiverse; 4 on fix list.
- `SHEET_LAG-DUP-035-A_v001.jpg` (8 tiles of 8): pick favourite setups; 6 of 8 have no eye in the sun disc (fix list).

## For you to decide
1. **Set-wide face baseline.** V_2, V_3, V_4 and V_5 all report that LAG-1K faces read younger, clean-shaven and slimmer in the jaw and neck than the CAND-01 target. C33 is the exception and reads older and heavier. Do you accept this as the LAG-1K baseline, or treat it as drift? Lanes tagged only drift beyond that baseline, so if you call it drift, the fix list grows to nearly the whole set.
2. **Worms.** Worm styles from before the c02 call are only noted. They are not counted as drift. Only broken worms (no heads or maws, feathers, claws) are on the fix list.
3. **Integrity flag.** V3 C21-05 is a DUPLICATE-KEEPER with no DUPLICATE. Its only redundant partner, C21-21, is DRIFT-MULTIVERSE. I suggest reading it as the keeper of that pair, with no archive action. The tag stays as filed for your call.
4. Piercings and eye glow are still open and were not used as tiebreaks.

Out-of-lane notes from V_5: C20-07, C32-06 and C37-14 have a black nose tube. C20-15 reads "A" instead of "AL". C20-13_FAIL and C20-17_FAIL have spurs on the throat worms.
