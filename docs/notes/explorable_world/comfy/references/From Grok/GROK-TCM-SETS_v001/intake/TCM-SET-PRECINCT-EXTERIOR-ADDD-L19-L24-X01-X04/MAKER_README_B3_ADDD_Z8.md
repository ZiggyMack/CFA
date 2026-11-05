# TCM-SET-PRECINCT-EXTERIOR, B3 Addendum D variants (Z_8), PRELIMINARY

Maker: Z_8 (SCRUM TEAM 6). Date: 2026-11-02. Status: PRELIMINARY. No selections made.
Rule: Addendum D (sha256 2a10c396...82b0 verified). For each bound position, b and c are added and take 1 is a. Exploratory positions are skipped.
Pre-check: before this lot the folder held only L01-L18 and BATCH_01-04_index.tsv. There were no B3 files and no other makers' files, so nothing was touched.
L-numbers: the highest existing L was L18, so new stills are L19-L24. Each image was made in a single call, with no retries.

## Bound vs exploratory (card TCMSET_B2_TCM-SET-PRECINCT-EXTERIOR_card_v001.md, slot table)
- BOUND, done: S01 EXT-P01/EXT-LS1 (a = L11), S03 EXT-P02/EXT-LS1 (a = L13, V_1 SCRIPT-DRIFT, cut first), S04 EXT-P03/EXT-LS1 (a = L14).
- EXPLORATORY, skipped: S02 EXT-P01/EXT-LS2 (L12), S05 P04 (L15), S06 P05 (L16), S07 P06 (L17), S08 P07 (L18).
- L17 and L18 carry V_1 SCRIPT-DRIFT tags, but the card marks both P06 and P07 as "exploratory: binds no shot yet", so they were skipped under Addendum D. This is an open question for Claude/Chief.

## Per image
| L | pos | sha8 | variantOf | targets | fixed? | defects |
|---|---|---|---|---|---|---|
| L19 | P02-LS1-b | cb2f584a | L13__P02-LS1 | V_1 DRIFT (not frontal/low) | NOT FIXED | FAIL as P02: same three-quarter street wide as L11 (reference dominated); near-dup of L21/L24 |
| L20 | P02-LS1-c | 79aad035 | L13__P02-LS1 | V_1 DRIFT | FIXED (low, square-on, bollards, flat jambs) | light dusky (from L14 ref); camera near kerb edge; blank panel and red bin in bay, no text/figures at 4x |
| L21 | P01-LS1-b | f20a30b6 | L11__P01-LS1 | no tag | n/a | near-duplicate of L11; otherwise clean |
| L22 | P01-LS1-c | 4f0820b6 | L11__P01-LS1 | no tag | n/a | identity drift: two-storey main block, bay in a low annex, columned portico |
| L23 | P03-LS1-b | 16e60c06 | L14__P03-LS1 | L14 maker flags (dusky light) | light FIXED | camera at the kerb, not on the street centreline; crosswalk parallel to the kerb again; identity drift (plain concrete box) |
| L24 | P03-LS1-c | 95a38bcc | L14__P03-LS1 | L14 maker flags | NOT FIXED | FAIL as P03: P01-style street wide with a crosswalk; not a driver's-eye view |

Every image was checked at 4x for people/silhouettes (none), vehicles (none, so Addendum B did not apply), plates/badges/text (none), weapons/blood (none), and flag/crest (none).

## Open questions for Claude
1. Should L17 (P06) and L18 (P07) get b/c? They are tagged SCRIPT-DRIFT but sit at exploratory positions.
2. P02: L20 is the only frontal candidate, and it is dusky. Allow one extra overcast P02 call with no reference?
3. P03: neither variant is a true street-centreline turn view. Allow one call with no reference and an explicit oblique turn angle?
4. Whenever the L11 reference is used, the result collapses to the L11 frame (L19, L21, L24). Should future P02/P03 calls avoid L11 as a reference?
5. V_1 noted a projecting stone portal at L13. L20 has a flat limestone surround. Which matches the master?
