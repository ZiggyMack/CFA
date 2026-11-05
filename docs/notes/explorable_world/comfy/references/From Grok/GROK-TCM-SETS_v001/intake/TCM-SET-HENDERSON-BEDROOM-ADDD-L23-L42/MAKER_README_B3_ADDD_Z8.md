# README_B3_ADDD_Z8: HENDERSON-BEDROOM, Addendum D quality pass (rule of three), maker Z_8

PRELIMINARY. No selections, no ratings. Take-1 stills (L11-L20) are variant a; this lot adds variants b and c. Nothing existing was overwritten, renamed or deleted.

## Counts
- Bound positions (proof/needed per card section 6): P01-LS1, P02-LS2, P02-LS3, P03-LS2, P03-LS3, P04-LS1, P05-LS2, P05-LS3, P06-LS3, P07-LS3 = 10 slots x 2 = **20 new stills, L23-L42**.
- Exploratory, no variants: P08-LS3 (L21), P09-LS2 (L22).
- GenerateImage calls: 20, one image each, no retries, no aborted calls.
- Asset store: before 162 files (`out/_z8_assets_before_bed.txt`), after 182 (`out/_z8_assets_after_bed.txt`); `comm -13` = 20 new files, which matches the 20 calls (`out/_z8_new_bed.txt`). Each copied file's sha256 matches its asset name.
- Index: `BATCH_B3_ADDD_index.tsv` (12 columns, variantOf = take-1 stem).
- Light token in filenames follows the take-1 files (N1 = BED-LS1, N2 = BED-LS2, D1 = BED-LS3).

## Order
Positions V_1 tagged (relayed PRELIMINARY tag list) were done first: L11/P01, L12-L13/P02, L14/P03-N2, L16/P04, L19/P06, L20/P07. Untagged after: L15/P03-D1, L17/P05-N2, L18/P05-D1. P01-b was made before the tag list arrived, so it is a spec restatement and does not target the window miss.

## Per-image: the tagged miss targeted, and whether it looks fixed (my own look, not a V verdict)
| L | Slot | Targeted | Fixed? | Other defects |
|---|---|---|---|---|
| L23 | P01-N1-b | (made before tags) | NO: window still on the headboard wall; clock glyphs still there | near-copy of take 1 |
| L24 | P01-N1-c | window off the headboard wall; blank clock | WINDOW PARTLY (moved to the right side wall, near the foot); CLOCK NO (tick marks and numeral-like glyphs) | |
| L25 | P02-N2-b | window off the headboard wall | YES | clock tick marks; no lamp on the stand |
| L26 | P02-N2-c | window off the headboard wall | YES | clock tick marks |
| L27 | P02-D1-b | match the locked N2 layout; John's stand next to the exit | YES (same lock as L25) | clock tick marks; no lamp; slightly warm |
| L28 | P02-D1-c | match the locked N2 layout | YES (same lock as L26) | clock tick marks; dim/warm for day |
| L29 | P03-N2-b | hands-only clock; phone face down | CLOCK YES; PHONE MISSING | |
| L30 | P03-N2-c | hands-only clock; phone face down | CLOCK NO (blank face, no hands); PHONE present but glossy, may read face-up | mattress edge flips to the right |
| L31 | P03-D1-b | (untagged) | - | PHONE MISSING; warm |
| L32 | P03-D1-c | (untagged) | - | clean; framing almost the same as L31 |
| L33 | P04-N1-b | L01 bathroom look; centred full-height door | LOOK YES (white vanity, chrome); DOOR MOSTLY (slightly right of centre) | weak light wedge |
| L34 | P04-N1-c | same | LOOK YES; DOOR YES (slightly left of centre) | bed/stand now on the RIGHT edge (flips vs L33); weak wedge |
| L35 | P05-N2-b | (untagged) | - | door centred (better than take 1); dresser wider than a slice; clock tick marks |
| L36 | P05-N2-c | (untagged) | - | clean |
| L37 | P05-D1-b | (untagged) | - | room beyond the door is LIT and readable (F-THRESH/N7); clock numeral-like marks |
| L38 | P05-D1-c | (untagged) | - | dim beyond (good); whole frame reads dim/overcast, borderline for LS3 |
| L39 | P06-D1-b | foot half at about 35 degrees from the side; no window or clock | PARTLY: foot half, no window or clock, BUT seen from the foot, not the side | warm golden light |
| L40 | P06-D1-c | same | MOSTLY: about 35 degrees down, foot half, 3/4 from the foot corner | warm light |
| L41 | P07-D1-b | sliding closet | YES sliding, BUT panels pushed to both sides with the opening in the middle (odd track) | |
| L42 | P07-D1-c | sliding closet | YES (two by-pass panels, right half open) | square-on, not slightly angled |

No image shows people, hands, silhouettes, reflections of people, weapons, blood, brands, or legible text. Clock faces are the recurring weakness: the generator keeps adding tick marks, and on P01 and P05-D1-b numeral-like glyphs. L29, L31 and L32 have clean blank dials.

## Questions for the lead writer (Claude)
1. Window wall: card F-GEO1 and the writer's default put the window on the wall FACING THE FOOT of the bed. No ruling in TCM_HELD_POSITIONS_RULINGS_20261102.md or Addenda A-D changes this, so the variants follow the card. V_1's L21 (P08, exploratory) tag, bathroom door out of frame and window on the headboard wall, is still OPEN. P08 is exploratory, so it got no variants. Should P08 be re-cut as the room-map anchor?
2. Jill's side and the bathroom-door side: L33 and L34 put the bed on opposite edges of the frame. Which side of the bed does the bathroom door sit on, relative to the exit door?
3. P06 axis: the card says "from the side" while also asking for the foot half at 35 degrees. Is a 3/4 from the foot corner (L40) acceptable?
4. Clocks: would a clock turned away (allowed in the maps Notes) be preferred over blank dials, given how often the generator adds marks?
