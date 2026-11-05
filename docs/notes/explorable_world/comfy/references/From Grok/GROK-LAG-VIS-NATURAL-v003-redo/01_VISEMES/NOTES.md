# GROK-LAG-VIS-NATURAL-v003-redo / 01_VISEMES (HaL, 2026-10-21) — PRELIMINARY
Redo of the 3 shapes V_3 judged TOO-CLOSE-REDO (V3_dedup_LAGMOUTH_20261021T060907Z_v001.tsv).
Natural white teeth, no grill. Tool: cursor GenerateImage, 16:9. Mouth described first in every prompt. Originals in v001 untouched; nothing deleted or overwritten.

| shape | lookalike | best | L | S | reads distinct? |
|---|---|---|---|---|---|
| 11 GRIN | 03_AH | VIS-LAG-11_GRIN_v004-try1.jpg | 4 | 5 | yes: teeth closed edge to edge, lips stretched wide, no open jaw |
| 14 BLOW-KISS | 06_OO-W | VIS-LAG-14_BLOW-KISS_v004-try3.jpg | 4 | 5 | yes: forward pucker + releasing hand beside mouth |
| 17 LIPS-PRESSED-THIN | 02_MBP, 01_REST | VIS-LAG-17_LIPS-PRESSED-THIN_v004-try3.jpg | 3 | 4 | yes: thin tense line, chin bulge, corner creases |

Findings
- Confirmed again: referencing a set frame whose mouth differs (01_REST) gets that mouth copied (14 try1, 17 try1). GRIN try1 was the exception: the grin overrode the REST ref.
- Better: reference a frame with a mouth close to the target (13_KISS-PUCKER for 14), or go text-only and then use that output as the ref for an identity/framing correction (17 try2 → try3).
- Residual: 17 best is a shade paler and framed a bit wider (more nose) than the set; a sliver of lip still shows (not a full roll-in). 14 best hand partly overlaps right jaw. 11 GAIB reads GAIIB (known set defect).
- Side-by-sides vs lookalikes: SHEET-*.jpg. No shape failed, so nothing was added to BENCHMARK-LIP-BITE.md.
- Scores are self-scores, pending V Team check.

## Round 2 (HaL, 2026-10-21) — after V Team check V5_LAGMOUTH_redo_20261021T061534Z_v001.tsv
V5: BLOW-KISS v004-try3 PASS; GRIN v004-try1 FIX-FACE (GAIIB); LIPS-PRESSED-THIN v004-try3 FIX-FACE (light skin, wide framing, lip sliver, moustache+goatee stubble).

### 1) Chin GAIB fix (pixel edit, no regen)
Checked every file in v001/01_VISEMES plus the v003-redo bests by chin zoom. The split-I GAIIB (I drawn as two short stacked bars) is on all 13 of HaL's v001 frames 01-14 and on GRIN v004-try1. Z_5 frames 19-50, BLOW-KISS v004-try3 and 17 v001 already read GAIB, so they were left alone.
Method (like Z_2's try3_pixelfix-tall, no GenerateImage): find the G/A/I/I/B ink parts, cover both short I bars with skin texture cloned from about 22px to the side (low-frequency colour matched), draw one serif I at A/B letter height in the ink tone sampled from B, and re-save with the source JPEG quantisation tables. Only about a 40x80px chin box changes. Outside it the mean difference is about 0.1/255 (JPEG re-encode noise, max 7-10 on a handful of pixels), so the mouth is untouched.
Files: VIS-LAG-{01_REST,02_MBP,03_AH,04_EE,05_OH,06_OO-W,08_L-TH,09_S-T-K,10_CH-SH,11_GRIN,12_SHOUT,13_KISS-PUCKER,14_BLOW-KISS}_v004-chinfix.jpg and VIS-LAG-11_GRIN_v004-try1-chinfix.jpg. Before/after: SHEET-CHINFIX-GAIB_before_after_v004.jpg.
Caveats: the new I is slightly cleaner/sharper than the soft AI letters next to it. 12_SHOUT's B is still cut off by the frame bottom (v001 crop defect).

### 2) LIPS-PRESSED-THIN v005
- try1 (edit MBP, lips only): the model copied MBP's full lips. FAIL.
- try2 (MBP for the frame and try3 for the mouth): returned the try3 look again (wide framing, moustache+goatee). The frame reference was ignored.
- try3-composite: the MBP chinfix base keeps the set framing, skin, even stubble and GAIB. The try2 mouth goes in through a soft mask with LAB colour matching. A vertical warp squeezes both lips into the seam, the pink is removed, and the seam and corner tension are shaded in. BEST, L4 S3 (partial): no lip sliver and on-model surroundings, but a smoothed band under the seam can read as a pale ghost lower lip, and there's no real chin bulge.
Generation alone can't produce a fully rolled-in, set-matched pressed mouth. Added to BENCHMARK-LIP-BITE.md 'Challenge list additions 2026-10-21'. Comparison: SHEET-17_LIPS-PRESSED-THIN_v005_vs_02_MBP_01_REST.jpg.
Scripts: /workspace/lag-chinfix/ (detect.py, fix.py, comp17.py, warp17.py).
