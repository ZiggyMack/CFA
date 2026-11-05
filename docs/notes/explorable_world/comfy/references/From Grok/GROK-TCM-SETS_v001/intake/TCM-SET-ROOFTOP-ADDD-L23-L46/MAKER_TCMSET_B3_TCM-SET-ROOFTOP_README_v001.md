# TCMSET_B3 TCM-SET-ROOFTOP: Addendum D variants b and c (lot 1), v001

PRELIMINARY. No selections, no ratings. Made by HaL's lane on 2026-11-02 (America/New_York). No ZIP made; nothing pushed to D:. No existing file, index or ZIP modified or deleted.

## Sources read
- TCM_HELD_POSITIONS_RULINGS_20261102.md (sha256 74cfc1e6d66463a4d4a7bc84c6f4f14d0630167de6e00724c3d87f202b9ad6a3, per Chief)
- Addendum A cf5300516fdeb14fde62b319112701e0cd526039f1f3842629f8853b1531d2c5; Addendum B ae51ec7b0fd1c55bce066ea93d0cb64836853ddc031dc2f4dc6b86f43e91950d; Addendum C 7aea1e51ddcb3a585c0538ac8228c4591393fcd8b7bb11327d8a3c85d021d81b; Addendum D 2a10c3961a50db331f10773cbc17f326bc37dc12b8b7f332453430a2748282b0 (all verified on disk)
- TCM_SET_CAMERA_MAPS_v001_20261031.md, ROOFTOP section (MAPS:L183-L198)
- cards_setround_v001/TCMSET_B2_TCM-SET-ROOFTOP_card_v001.md; screening/V4_TCMSET_20261031T182817Z_v002.tsv; screening/V4_TCMSET_RR_20261031T183805Z_v002.tsv
- BATCH_05_index.tsv (take 1, L11-L22), BATCH_05_REROLL_index.tsv (X01)

## What was made
24 stills, L23-L46, one GenerateImage call each, no retries, 0 FAILED, 0 extras. All 1280x720 (16:9). Variant a = the take-1 still L11-L22 (unchanged). Every bound ROOFTOP position/light state (all eight positions are "needed"; 12 position-light rows) got b and c. Order: V_1's misses first (L12, L17, L15, L18, L19, L20, L21), then L16 (QUALITY-FAIL), L22 (ADVISORY), then the OK rows L11, L13, L14.

| Position / light | a (take 1) | b | c |
|---|---|---|---|
| RT-P01 RT-LS1 | L11 | L41 | L42 |
| RT-P01 RT-LS3 | L12 | L23 | L24 |
| RT-P02 RT-LS1 | L13 | L43 | L44 |
| RT-P03 RT-LS1 | L14 | L45 | L46 |
| RT-P04 RT-LS3 | L15 | L27 | L28 |
| RT-P05 RT-LS2 | L16 | L37 | L38 |
| RT-P05 RT-LS3 | L17 | L25 | L26 |
| RT-P06 RT-LS2 | L18 | L29 | L30 |
| RT-P06 RT-LS3 | L19 | L31 | L32 |
| RT-P07 RT-LS2 | L20 | L33 | L34 |
| RT-P08 RT-LS2 | L21 | L35 | L36 |
| RT-P08 RT-LS3 | L22 | L39 | L40 |

Files: TCMSET_B3_TCM-SET-ROOFTOP-L<nn>__P<pos>-LS<n><b|c>.jpg; index TCMSET_B3_TCM-SET-ROOFTOP_INDEX_v001.tsv (variantOf = take-1 filename; sha256/bytes from disk); contact sheet TCMSET_B3_TCM-SET-ROOFTOP_CONTACT_SHEET_v001.jpg (a | b | c per row, labelled by filename). Images, index, README and contact sheet chmod 444.

## Assumptions
- Reference images per call: the take-1 still of the same position + TCM-SET-ROOFTOP-L01 (canonical brick bulkhead); for P07 the second reference is L11 (door handedness anchor) instead of L01.
- Door handedness for every still: knob/deadbolt on the left, hinges on the right, as V_1 read L11/L13/L19.
- Building three storeys (rulings). Police vehicles: present-day police SUVs, two-tone blue, unlettered, light bar, no emblems/badges/plates, blank grille (rulings + brief). LS2 two SUVs at angles; LS3 one SUV parallel at the kerb under the ledge (maps).
- X01 (reroll of L16) is not variant a; L16 is (take 1).
- ROOFTOP L01-L10 (looks) are not take 1 and got no variants.

## Self-flags (PRELIMINARY-SELFFLAG, 1x glance only; V_1 screens)
17 of 24 self-flagged: L23, L24, L25, L26, L29, L30, L31, L32, L35, L36, L37, L38, L39, L40, L42, L44, L46. Reasons per row in the index `defects` column. Summary:
- Emblem/brand on vehicles: L24 (round door disc), L35, L36 (oval maker-style grille badges), L38 (shield/crest door decals, same fault as L16); small grille/plate blobs in L23, L37, L39, L40.
- V_1 miss not repaired or only partly: L23, L24 (SUV down the street, not directly under ledge); L25, L26 (SUV mid-road; L26 reads as a sedan); L29 partly, L30 not, L31 not, L32 partly (P06 reverse angle); L35, L36 (SUVs not at angles); L37, L38 (over a neighbouring roof again).
- Storey count: L35, L39, L40 read two storeys + bulkhead; L36 reads four storeys and has no street.
- Livery: L23, L39, L40 show white panels rather than two blues.
- Near-duplicates: L42 (of L41), L44 (of L43), L46 (of L45).
- Repaired as asked (no self-flag): L27, L28 (P04 bulkhead out of frame, puddle lower centre); L33, L34 (P07 handedness matches L11/L13/L19); L41, L43, L45.
No person, hand, face, figure, weapon, blood or legible character seen at 1x in any of the 24.

## Questions logged for Claude (batch ruling)
1. Addendum A s3 says the ROOFTOP/BAR-STREET SUV has "lettering and seals illegible"; the rulings say "unlettered", and the brief says no emblems. I followed the rulings (later): unlettered, no seals. Confirm.
2. "Two-tone blue livery": which two blues, and is a white or light panel acceptable? (L23, L39, L40 came out with white panels.)
3. On police SUVs the generator keeps adding maker-style grille ovals and door crests (L35, L36, L38; earlier L16). Should these be cleaned at compositing or recut, given the no-individual-rerolls rule?
4. Using the take-1 still as reference pulled the corrective variants back toward take 1's faulty framing (P06 from L18/L19, P05 from L16/L17). For future corrective variants, may the maker leave out the take-1 reference where V_1 tagged the geometry?
5. Addendum D s1 says variants never change "the geometry", but D s2 says the variants of V_1's misses are "corrections of the miss" (P06 angle, P07 handedness, P04 edges). I used s2 for the miss rows. Confirm.
6. RT-LS3: the maps have one patrol car parallel under the ledge, and the rulings have two SUVs present from the police's arrival. Should the second SUV stay in frame in LS3? (I made one, per the maps.)
7. Three storeys can't be read in the ledge-down views (P05). The P08 variants came out at 2+bulkhead or 4. Is a storey count needed in P08 only?
8. P04 RT-LS3: V_1's continuity question (door closed in L15 vs open in P06 LS3). L27/L28 keep the bulkhead out of frame, so the door doesn't show. Should the door state be ruled for any recut that shows it?
9. Filename form: Addendum D's example is `...-LS01-a.jpg`, and the Chief's brief is `TCMSET_B3_...__P<pos>-<LIGHT><variant>.jpg`. I followed the brief. Confirm.
