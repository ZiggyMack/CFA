# TCM-SET-CAPTAIN-OFFICE - Addendum D rule of three - Z_9 - PRELIMINARY

Nothing here is a selection, rating or winner. Nothing pushed to D:.
Maker: Z_9. Written 2026-11-02 (America/New_York, UTC-5).

## What this lot is
- 24 new stills, L23-L46: variants b and c for every bound position/light slot in the family (all 9 positions are `needed`; 12 slots: P01-P03 DAY+NIGHT, P04-P08 DAY, P09 NIGHT).
- Variant a = the existing take-1 still (L11-L22, BATCH_04_index.tsv); not regenerated, not touched.
- Index: BATCH_B3_ADDD_Z9_index.tsv (11 required columns + variantOf, variant, status). sha256/bytes measured from disk. Defects are per row and honest.
- Contact sheet: CONTACT_SHEET_B3_ADDD_Z9.jpg - one row per position/light, a (take-1) | b | c. REVIEW AID ONLY, not a candidate.
- Files saved byte-for-byte from the generator asset store (jpg, unconverted); chmod 444. No existing file overwritten, deleted or renamed.

## Order worked (V_1 miss list first)
V1_TCMSET_B3_ADDD_MISSLIST_CO_PO_PE_20261102_v001.tsv rows for this family were cut first, b/c written as corrections of the logged miss:
- L14 P02-NIGHT (SCRIPT-MISS) -> L23 b, L24 c
- L11 P01-DAY (DRIFT) -> L25 b, L26 c
- L16 P03-NIGHT (DRIFT) -> L27 b, L28 c
- L18 P05-DAY (DRIFT) -> L29 b, L30 c
- L19 P06-DAY (DRIFT) -> L31 b, L32 c
- L20 P07-DAY (DRIFT) -> L33 b, L34 c
Then the rest: L12 P01-NIGHT -> L35/L36; L13 P02-DAY -> L37/L38; L15 P03-DAY -> L39/L40; L17 P04-DAY -> L41/L42; L21 P08-DAY -> L43/L44; L22 P09-NIGHT -> L45/L46.

## Method notes
- One GenerateImage call per still, max 2 in flight, no automatic retries. 24 calls, 24 images, 0 errors, 0 aborts, 0 rate limits, 0 extras.
- References: b variants mostly used the take-1 still (or L12/L15 look anchors) as reference_image; several c variants were made from the text brief only ("none (text brief only)" in reference_ids) because the generator tends to copy a reference composition nearly verbatim (b and c, and DAY vs NIGHT, came out near-identical). The text-only variants buy variety at the cost of finish match to the L12 master (lighter/modern desks, different chairs). Each case is in the defects column.
- Known near-duplicates: L25/L26 (P01-DAY b/c), L23/L37 (P02 NIGHT b vs DAY b, same layout relit), L27/L39 (P03 NIGHT b vs DAY b).

## Conflicts noted (Addendum D followed over earlier assumptions)
1. Naming: Addendum D literal pattern used: `TCM-SET-CAPTAIN-OFFICE-L<nn>__P<pp>-<DAY|NIGHT>-<b|c>.jpg`. Other makers (Z_8, Z_10) used `TCMSET_B3_<FAMILY>_L<nn>__P<pp>-<light>-<b|c>`. Not renamed; flagged for packaging.
2. Period: v001 maps say period-neutral; Addenda A/D say present day (flat dark monitors, present-day desk phones). Present day followed; any CRT/typewriter cue would be a defect (none intended).

## QUESTIONS FOR CLAUDE
1. Door wall. Held-positions ruling: door in the glazed wall toward the bullpen, centre-right from the captain's chair; window wall with blinds behind the captain's chair. v001 CO-P01 card puts the door "at the right edge" from the corner opposite the door; CO-P02 card puts it "in the far wall centre-right" from behind the captain's chair. The L12 master has a frosted door on the RIGHT side wall. L13/L19 (take-1) have mirrored hinges. Which is canonical for P02/P06/P08 - side wall right, or the wall facing the captain? (L44's plate puts the door at LEFT of frame; L43 at RIGHT.)
2. Door swing for 1332 (kicked open): inward vs outward/free-swinging? The b/c stills show it closed or ajar; hinge side not consistent across L31/L32 vs L19.
3. "Glazed wall toward the bullpen" (ruling) vs v001's single door with a frosted/wired panel and plain/paneled walls - should a glazed partition with blinds appear in P02/P06 frames? L38 shows bullpen through interior blinds; others do not.
4. CO-P03 background: "window blinds (or filing cabinets, per the wall decision)". Ruling puts the window behind the chair, so blinds were used. Confirm.
5. CO-P04 card says "the one clear patch" and "lamp base and a cup at the edges": L41 shows a large tidy patch (two stacks only), L42 a large patch ringed by stacks. How small should the patch read relative to the badge?
6. CO-P08 card says "paneling"; the master has wainscot below painted wall. L43 = wainscot+paint; L44 = full-height raised panels. Which?
7. Desk lamp: green banker's shade (L36, L02) vs black/brass (L12 master). One lamp for the family?
8. Phone keypads / label strips (L24 and others): blank keys pass at 1x; please confirm the 1x-legibility rule is the test (not 4x).

## Assumptions
- All 9 CAPTAIN positions treated as bound (all `needed` in v001); no exploratory positions in this family.
- Light tokens: CO-DAY -> DAY, CO-NIGHT -> NIGHT.
- serves_shots copied from the take-1 row in BATCH_04_index.tsv for the same position/light.
- /workspace/v1_calib and /workspace/v1_push were not opened.
