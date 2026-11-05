# TCM-SET-PRECINCT-OFFICE - Addendum D rule of three - Z_9 - PRELIMINARY

Nothing here is a selection, rating or winner. Nothing pushed to D:.
Maker: Z_9. Written 2026-11-02 (America/New_York, UTC-5).

## What this lot is
- 24 new stills, L23-L46: b and c for all 12 bound slots (all 10 positions `needed`: P01 LS1+LS2, P02, P03, P04 LS1+LS2, P05-P08 LS1, P09 LS2, P10 LS2).
- Variant a = existing take-1 (L11-L22, BATCH_04_index.tsv), untouched.
- Index: BATCH_B3_ADDD_Z9_index.tsv (11 required columns + variantOf, variant, status); sha256/bytes from disk; honest per-row defects.
- Contact sheet: CONTACT_SHEET_B3_ADDD_Z9.jpg (rows per position/light: a take-1 | b | c). REVIEW AID ONLY.
- Saved byte-for-byte from the asset store; chmod 444; nothing overwritten, deleted or renamed.

## Order worked (V_1 miss list first; b/c written as corrections)
L14 P03 -> L23/L24; L15 P04-LS1 -> L25/L26; L16 P04-LS2 -> L27/L28; L17 P05 -> L29/L30; L18 P06 -> L31/L32; L19 P07 -> L33/L34; L20 P08 -> L35/L36; L21 P09 -> L37/L38.
Then: L11 P01-LS1 -> L39/L40 (exit sign: L39 blank green rectangle, L40 omitted); L12 P01-LS2 -> L41/L42; L13 P02 -> L43/L44; L22 P10 -> L45/L46 (no bezel mark, photos face-down).

## Miss-correction scorecard (my read, PRELIMINARY - screener to judge)
- Corrected in at least one of b/c: P03 (L24), P04-LS1 (L26), P04-LS2 (L28), P05 (L29, L30), P06 (L32), P07 (L34), P08 (L36 hardware), P09 (L37, L38).
- NOT corrected / repeats the miss: L27 (photos face-up again - also a figure-shape risk), L31 (inner office still reads through blinds). Partial: L23, L25, L33, L35. Recommend these be cut first; no rerolls made (one call per still, no retries).

## Method notes
- 24 GenerateImage calls, 24 images, 0 errors, 0 aborts, 0 rate limits, 0 retries, 0 extras. One save command was interrupted by the parent before it wrote anything (no file, no index row); it was re-run once with identical inputs and verified (L25/L26 each saved once).
- b variants mostly used L11/L12 as reference_image (strong architecture match, but the generator copies the reference composition); c variants mostly text-brief only (more varied, but finishes drift: drop ceilings, carpet, tiled floors, clean walls). Each case is in defects.

## Conflicts noted (Addendum D followed)
1. Naming: Addendum D literal pattern `TCM-SET-PRECINCT-OFFICE-L<nn>__P<pp>-<LS1|LS2>-<b|c>.jpg`; Z_8/Z_10 use `TCMSET_B3_<FAMILY>_L..`. Not renamed.
2. Period: v001 period-neutral vs Addenda A/D present day -> present day followed (flat dark monitors, present-day phones, smartphone in P04-LS2/P10).

## QUESTIONS FOR CLAUDE
1. Exit doors location. L01/L11 master (and V_1's P01-master ruling): glazed double doors on the FAR wall at right, beside the captain's glazing and the washroom door. Held-positions ruling: the glazed double doors are the entry on the END wall OPPOSITE the captain's office, with captain + washroom sharing the far wall. P01 card says camera "just inside the main double doors" looking at the far wall with the captain's office - which agrees with the ruling, yet the master also shows double doors on that far wall. Are there two sets of double doors, or should the far-wall pair go? (L40 has no far-wall doors; L39/L41/L42/L37/L38 keep them.)
2. P07 window side. Card: from the captain's doorway, "window wall at frame left". On the master, windows are on the LEFT from the entry; looking back from the captain's office (opposite end) they would be on the RIGHT. P02 card does put the windows at frame right for the same reverse direction. L34 follows the P07 card (left). Which is right?
3. Washroom door hardware: P01/P08 cards and BATH continuity say push plate; master L11 single door has a lever on its right (V_1 noted). Is the push plate the rule for every view (L35/L39 have levers; L36 push plate)?
4. Distressed/peeling wall finish of L01/L11 (writer to confirm per v001): keep? Several c variants have clean or heavily decayed walls.
5. P05 card does not name the washroom door hardware; P08 does - confirm the same leaf.
6. Exit glow size: L39's blank green rectangle is oversized; is "omit" preferred over a blank glow for LS1 day? (LS2 card asks for the blank glow at night.)
7. P04/P05 seat geometry: "camera at Diego's side of the pair" - adjacent side-by-side desks or facing pairs? L26 reads across the desk from the visitor side.

## Hard-rule risks to check (4x)
- L27: face-up photo prints with image content (possible figure shape) - recommend cut.
- Phone LCD panels / key label strips with faint marks: L23, L25, L26, L29, L30 (label strip), L35, L39, L43.
- Monitor bezel mark: L29 (small mark under screen, right monitor).
- Binder spines / letter trays / paper stacks: L34, L36, L42, L44.
- Green exit rectangles (must be glyph-free): L28 n/a, L37, L38, L39, L41, L42, L43, L44.

## Assumptions
- All 10 positions bound (all `needed`), none exploratory. Light tokens: OFF-LS1 -> LS1, OFF-LS2 -> LS2.
- serves_shots copied from the take-1 row for the same position/light.
- /workspace/v1_calib and /workspace/v1_push not opened.
