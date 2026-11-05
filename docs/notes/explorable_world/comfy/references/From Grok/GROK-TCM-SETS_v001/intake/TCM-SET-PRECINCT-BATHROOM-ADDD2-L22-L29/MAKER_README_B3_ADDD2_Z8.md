# TCM-SET-PRECINCT-BATHROOM — Addendum D pass 2 (Z_8), PRELIMINARY

New stills L22–L29 (8 files, b/c for 4 bound positions). Index: BATCH_B3_ADDD2_index.tsv (12 columns). No existing file was edited, renamed or deleted. P05 (L16 → L20/L21) was skipped as instructed.

## Bound vs exploratory (from card TCMSET_B2_..._card_v001.md priority/serves columns)
- Bound ("needed"): BATH-P01 LS1 (L11), P02 (L13), P03 (L14), P04 (L15), P05 (done earlier).
- Exploratory → NO variants: P01 **LS2** (L12; the card marks BATH-LS2 as "exploratory light state: binds no shot yet"), P06 (L17), P07 (L18), P08 (L19).
- So V_1's tagged misses on L12 (mirror order/stall fronts), L17 (double door) and L19 (door hardware) were NOT addressed; under Addendum D exploratory positions stay at one still. Flag for Claude/V_1 if they want those promoted.

## Files
| L | position | var | hash | targets | status |
|---|---|---|---|---|---|
| L22 | P01-LS1 | b | c6816261 | L11 advisory: door window + push plate | window FIXED; push plate NOT fixed (lever remains) |
| L23 | P01-LS1 | c | 78917b77 | same | window FIXED; push plate NOT fixed; single basin foreground (drift) |
| L24 | P02-LS1 | b | 88b36105 | untagged | DEFECTIVE: soap dispenser dropped, near copy of L13 |
| L25 | P02-LS1 | c | b0739813 | untagged | clean (one basin in counter, neighbours not visible) |
| L26 | P03-LS1 | b | eb46abcf | untagged | clean; close to L14 |
| L27 | P03-LS1 | c | a518910d | untagged | clean content; look drift (undermount counter, single-pane window) |
| L28 | P04-LS1 | b | ce92aa96 | untagged | minor: door lever not push plate |
| L29 | P04-LS1 | c | e50a9c5b | untagged | door window + push plate correct; stall doors read ajar (defect) |

## Open questions for Claude
- The ruling puts the window on the far short wall, opposite the door wall. L11 (and L22/L23, which keep its order) reflects the door, window and stalls on one back wall. This is because V_1 asked that L11's order be kept. Geometry fit is to be confirmed against BATH-P08 once it's anchored.
- The push plate was missed in 3 of 4 tries where the door is visible. Only L29 shows the card's full door hardware.

## Reconciliation
The assets store had 194 files before and 202 after. `comm -13` lists 8 new files, and `comm -23` lists 0 removed. The 8 new hashes exactly match the sha256 column of the index.
