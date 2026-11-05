# GROK-LAG-VIS-NATURAL-v003-redo — Lisan Al Gaib mouth shapes: redos + chin GAIB fix (for CFA Nova)

From HaL (Grok), 2026-10-21. **All scores are preliminary self-scores** unless marked V_5 / V_3.

## What this is
Follow-up to `GROK-LAG-VIS-NATURAL-v001` and `-v002` (both already on D: in `From Grok`). Two jobs:
1. **Redos of 3 mouth shapes** V_3 judged too close to other shapes (`V3_dedup_LAGMOUTH_20261021T060907Z_v001.tsv`): 11 GRIN (looked like 03 AH), 14 BLOW-KISS (looked like 06 OO-W), 17 LIPS-PRESSED-THIN (looked like 02 MBP / 01 REST). Natural white teeth, no grill.
2. **Chin GAIB fix** on 13 of the v001 frames whose chin read "GAIIB" (split I). Pixel edit only, no regeneration: about a 40x80 px chin box changes; the mouth is untouched (mean diff outside the box ~0.1/255).

Details, method and findings: `01_VISEMES/NOTES.md`. Prompts/refs/scores per file: `01_VISEMES/MANIFEST.csv`. V_5's check of the redos: `V5_LAGMOUTH_redo_20261021T061534Z_v001.tsv`.

## Rule: originals are kept, fixes sit beside them
Nothing on D: was replaced or deleted. The v001 originals stay in `GROK-LAG-VIS-NATURAL-v001\01_VISEMES\` (all 14 confirmed on D: by sha256 before this push, so they are not duplicated here). The new files use the same shape name plus a `_v004-…` / `_v005-…` suffix. Use the new file in place of the v001 one for that shape.

## Which file to use (fix → original it replaces)
| shape | USE THIS (in 01_VISEMES/) | replaces (D: `GROK-LAG-VIS-NATURAL-v001\01_VISEMES\`) | what changed | check | self-score (prelim) |
|---|---|---|---|---|---|
| 01 REST | VIS-LAG-01_REST_v004-chinfix.jpg | VIS-LAG-01_REST.jpg | chin GAIIB → GAIB (pixel) | not yet V-checked | – |
| 02 MBP | VIS-LAG-02_MBP_v004-chinfix.jpg | VIS-LAG-02_MBP.jpg | chin GAIIB → GAIB | not yet V-checked | – |
| 03 AH | VIS-LAG-03_AH_v004-chinfix.jpg | VIS-LAG-03_AH.jpg | chin GAIIB → GAIB | not yet V-checked | – |
| 04 EE | VIS-LAG-04_EE_v004-chinfix.jpg | VIS-LAG-04_EE.jpg | chin GAIIB → GAIB | not yet V-checked | – |
| 05 OH | VIS-LAG-05_OH_v004-chinfix.jpg | VIS-LAG-05_OH.jpg | chin GAIIB → GAIB | not yet V-checked | – |
| 06 OO-W | VIS-LAG-06_OO-W_v004-chinfix.jpg | VIS-LAG-06_OO-W.jpg | chin GAIIB → GAIB | not yet V-checked | – |
| 08 L-TH | VIS-LAG-08_L-TH_v004-chinfix.jpg | VIS-LAG-08_L-TH.jpg | chin GAIIB → GAIB | not yet V-checked | – |
| 09 S-T-K | VIS-LAG-09_S-T-K_v004-chinfix.jpg | VIS-LAG-09_S-T-K.jpg | chin GAIIB → GAIB | not yet V-checked | – |
| 10 CH-SH | VIS-LAG-10_CH-SH_v004-chinfix.jpg | VIS-LAG-10_CH-SH.jpg | chin GAIIB → GAIB | not yet V-checked | – |
| 11 GRIN | **VIS-LAG-11_GRIN_v004-try1-chinfix.jpg** | VIS-LAG-11_GRIN.jpg | NEW distinct grin (teeth closed edge to edge, wide lips) + chin GAIB fix | V_5 FIX-FACE on try1 (GAIIB only) → fixed here by chinfix; chinfix not yet re-checked | L4 S5 |
| 12 SHOUT | VIS-LAG-12_SHOUT_v004-chinfix.jpg | VIS-LAG-12_SHOUT.jpg | chin GAIIB → GAIB (B still cut by frame bottom, v001 crop) | not yet V-checked | – |
| 13 KISS-PUCKER | VIS-LAG-13_KISS-PUCKER_v004-chinfix.jpg | VIS-LAG-13_KISS-PUCKER.jpg | chin GAIIB → GAIB | not yet V-checked | – |
| 14 BLOW-KISS | **VIS-LAG-14_BLOW-KISS_v004-try3.jpg** | VIS-LAG-14_BLOW-KISS.jpg | NEW distinct blown kiss (forward pucker + releasing hand); GAIB already correct | **V_5 PASS** | L4 S5 |
| 17 LIPS-PRESSED-THIN | **VIS-LAG-17_LIPS-PRESSED-THIN_v005-try3-composite.jpg** (stand-in) | VIS-LAG-17_LIPS-PRESSED-THIN.jpg | thin pressed line, composite on the MBP chinfix base | PARTIAL (see open items); v004-try3 was V_5 FIX-FACE | L4 S3 |

Alternates / history (keep for reference, don't use as the pick): `VIS-LAG-11_GRIN_v004-try1.jpg` (pre-chinfix), `VIS-LAG-11_GRIN_v004-chinfix.jpg` (old v001 grin, only letters fixed; v001 grin was judged too close to AH), `VIS-LAG-14_BLOW-KISS_v004-try1/-try2.jpg` (V_5 FAIL / FIX-FACE), `VIS-LAG-14_BLOW-KISS_v004-chinfix.jpg` (old v001 blow-kiss, letters fixed only), `VIS-LAG-17_…_v004-try1/2/3.jpg` and `_v005-try1/2.jpg` (failed tries).

Sheets: `SHEET-11_GRIN_vs_03_AH_v004.jpg`, `SHEET-14_BLOW-KISS_vs_06_OO-W_v004.jpg`, `SHEET-17_LIPS-PRESSED-THIN_vs_02_MBP_01_REST_v004.jpg`, `SHEET-17_LIPS-PRESSED-THIN_v005_vs_02_MBP_01_REST.jpg`, `SHEET-CHINFIX-GAIB_before_after_v004.jpg` (all in 01_VISEMES/).

## BENCHMARK-LIP-BITE.md (updated copy)
`BENCHMARK-LIP-BITE.md` at the top of this folder is the **updated** benchmark (8,062 bytes, 2026-10-21). It adds the Hon Dolo four-gold grill challenges and "Challenge list additions 2026-10-21" (17 LIPS-PRESSED-THIN).
**D: already has an OLDER copy** at `GROK-LAG-VIS-NATURAL-v002\BENCHMARK-LIP-BITE.md` (1,282 bytes, sha256 3d52a3fd…). That old copy was left untouched; this one is a separate copy. Use this newer one.

## Open items
- **LIPS-PRESSED-THIN is partial** and on the challenge list (see BENCHMARK-LIP-BITE.md). The composite is the best stand-in: no lip sliver and on-model surroundings, but a smoothed band under the seam can read as a pale ghost lower lip and there's no real chin bulge. Keep-as-stand-in vs leave-on-challenge-list is waiting on Ziggy.
- **SING-VOWEL: r2 is proposed** (`GROK-LAG-VIS-NATURAL-v001\01_VISEMES\VIS-LAG-50_SING-VOWEL_r2_Z_5.jpg`, already on D:) but **awaiting Ziggy's pick**.
- The 13 chinfix files and the GRIN try1-chinfix have not been re-checked by V Team yet. Caveat: the new I is slightly sharper than the soft AI letters next to it.
- C41-21 brow ring (LAG-1K frame) is logged separately in `GROK-LAG-1K-FIXES-20261021`.
- All scores are preliminary.

## Checksums
- `SHA256SUMS` (this folder) covers every file in the package, including this README.
- `01_VISEMES/SHA256SUMS` is the original per-image list (covers the images; not MANIFEST.csv/NOTES.md).
