# TCM-SET-IMPALA — B3 variants (LOT 9), PRELIMINARY

Stage: PRELIMINARY. No selections made. Set only, cabin and driver position empty, present day.
Date: 2026-11-02 (America/New_York). Index: TCMSET_B3_TCM-SET-IMPALA_INDEX_v001.tsv (16 columns). Contact sheet: TCMSET_B3_TCM-SET-IMPALA_CONTACT_SHEET_v001.jpg (rows a|b|c, take 1 = a).

## Scope
- Positions in this lot: P01, P02, P04, P05, P07, P10. Before starting I checked every index in this folder; none of these take-1 stills already had b/c variants.
- I skipped Z_10's positions P03, P06, P08, P11–P14 and ID01 (L42–L57). I did not touch X05–X12; X12 was left alone.
- Take-1 stills skipped:
  - L12 P01-LS03 and L14 P01-LS05: they bind no shot in BATCH_04 serves_shots.
  - L15 P01-LS06: exploratory.
- L58–L79 were allocated with fixes first:
  - L58/59 P02-LS01 (L16 MISS)
  - L60/61 P02-LS03 (L18 MISS)
  - L62/63 P04-LS04 (L23 MISS)
  - L64/65 P10-LS01 (L36 MISS)
  - L66/67 P05-LS05 (L24 DRIFT)
  - L68/69 P07-LS04 (L32 DRIFT)
  - L70/71 P01-LS01
  - L72/73 P01-LS04
  - L74/75 P02-LS02
  - L76/77 P02-LS04
  - L78/79 P05-LS04
- Counts: 22 slots. 21 stills written and 1 empty slot (L65). 13 stills carry a SELFFLAG, plus the empty slot.

## Interruption
- The user interrupted the parallel run of L62–L65. Afterwards I checked the store and found three assets: 49f2f102… (L62), 507d7c81… (L63) and 687e46f5… (L64). I matched them to their slots by what each image shows.
- The L64 asset could fit either P10 prompt. I assigned it to b because b was issued first.
- No asset appeared for L65 (P10-LS01c). I did not re-issue the call (one call per image, no retries), so the slot is empty and marked INTERRUPTED in the index.

## Car reference
- The order named Z_10's L52, L55 and L57 as the car reference. In V2 v007, all three are tagged SCRIPT-DRIFT on camera. Their body and cabin are correct.
- The c variants of L55 and L57 carry faults (V2 v015).
- For night I used L54 (P12-LS01, V2 OK), which is the best clean anchor. For day I used L55 (fault is on camera only).
- For P05-LS05 I added HENDERSON-EXTERIOR-L03 as the house reference.
- No take-1 still with a named fault was used as a reference.

## Self-flags, including what I saw on the contact sheet
- P02 rear-seat repeat. L58, L59, L60, L61, L74, L76 and L77 all came out as a rear-seat view behind the driver headrest. That repeats V_1's take-1 miss (Addendum B §2 fix list), so the L16/L18 fix has NOT been achieved. L75 is the only P02 still on the passenger-side axis, and it is framed wider than a close.
- P04 (L62, L63):
  - L63's axis is reversed (it reads from the driver sill looking right).
  - L62 has motion blur on the cabin mat, and its sill or door is open at frame left.
- P10 (L64): the driver door reads as closed, not open.
- P07 (L68, L69): the axis is reversed, with the front of the car at frame left; take-1 L32 has the same read. The adjacent car's glass is light rather than dark-tinted.
- L69: there are faint glyph-like marks on the road surface. They are not legible at 2x and need a check at 4x.
- Added from the contact sheet after the index was chmod 444:
  - L70 and L71 are close in composition to take-1 L11, and to each other.
  - L72 and L73 are close to take-1 L13.
  - In each pair the b and c differ only in camera height and distance.
  - These should count as weak variants.
- Checks of every still at 1x, with crops at 2x:
  - No figures in the cabin, behind glass or in reflections.
  - No legible text.
  - No emblems on vehicles.
  - Screens are dark.

## Naming
- The files use the order's form, e.g. `TCMSET_B3_TCM-SET-IMPALA-L58__P02-LS01b.jpg`.
- Z_10 used `TCMSET_B3_IMPALA_L42__P03-LS01-b.jpg`, which has no TCM-SET- prefix, uses `_` before the L number, and puts `-` before the variant letter.

## Questions
1. Naming: should the user's form (TCMSET_B3_TCM-SET-IMPALA-Lnn__Pxx-LSxxv) or Z_10's form (TCMSET_B3_IMPALA_Lnn__Pxx-LSxx-v) be the standard? I have not renamed anything.
2. L65 (P10-LS01c) is empty because of the user interruption. Will Chief allow one call to fill it?
3. P02 keeps rendering as a rear-seat view in 7 of 8 tries. Should P02 go to a reference-driven approach, for example a passenger-axis anchor once one exists? L75 is the closest.
4. The stated car reference (L52/L55/L57) is all SCRIPT-DRIFT on camera. Is using L54 as the night anchor acceptable?
5. L12 and L14 bind no shot and L15 is exploratory, so I skipped them. Confirm.
6. I found no V_1 list beyond V2's tags and the Addendum B §2 note on L16/L18. Is there a newer V_1 list?
