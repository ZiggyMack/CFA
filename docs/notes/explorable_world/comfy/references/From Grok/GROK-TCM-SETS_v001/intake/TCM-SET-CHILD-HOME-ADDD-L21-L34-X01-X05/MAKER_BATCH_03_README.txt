TCM-SET-CHILD-HOME - BATCH 03 (Addendum D quality pass) - PRELIMINARY
All images are PRELIMINARY candidates. No selections, no winners. Take 1 (L11-L17) = variant a, untouched.
Maker: Z_7 (this agent). HOSPITAL is Z_10's and was not touched. Nothing deleted, overwritten or renamed.
Pre-check: no other maker's TCMSET_B3_ files/notes in this folder before starting.

SOURCES READ: map section (P01-P08), Addenda A-D, rulings file (nothing on CHILD-HOME), card
cards_setround_v001/TCMSET_B2_TCM-SET-CHILD-HOME_card_v001.md, V_4 tags
screening/V4_TCMSET_CH_20261031T183128Z_v001.tsv. No V_1 CHILD-HOME notes exist.

SLOT ORDER (V_4 SCRIPT-DRIFT first, b/c aimed at the named fault), L21-L34, no gaps:
  P03-L1 (L14 SCRIPT-DRIFT: copy of corner master)      -> L21 b, L22 c
  P03-L2 (L15 SCRIPT-DRIFT: room mirrored)              -> L23 b, L24 c
  P04-L1 (L16 SCRIPT-DRIFT: doorway centre-right, sharp footboard, hinge flipped, light door) -> L25 b, L26 c
  P01-L1 (L11 OK)  -> L27 b, L28 c
  P01-L2 (L12 OK)  -> L29 b, L30 c
  P02-L1 (L13 OK)  -> L31 b, L32 c
  P05-L1 (L17 OK; lighter door finish noted) -> L33 b, L34 c
SKIPPED (exploratory, per brief): P06-L1 (L18), P07-L2 (L19), P08-L1 (L20).

CORRECTION OUTCOMES (honest):
  P03-L1: L21 partial (geometry right, but frontal ~35mm, floor shows). L22 FAILED - near-copy of L21 (L21 was its reference).
  P03-L2: L23 mirror fault CORRECTED (bed reads too wide). L24 mostly a re-crop of L23; knee cut met.
  P04-L1: L25 hinge/door finish/dark hall CORRECTED; doorway still right-of-centre, footboard still sharp (FAILED on those two).
          L26 FAILED - near-duplicate of L25 (mean abs diff 4.7/255).
  P01-L1: L27 dressing varied; bed axis ambiguous; dark. L28 text-only, geography consistent, more frontal, white window trim.
  P01-L2: L29 harder flash achieved but bed MALFORMED (extra spindle rail). L30 coherent bed, light-logic mismatch (dark glass, bright pane shadows).
  P02-L1: L31 rug removed, hall fully black (near-identical framing to L13 by design). L32 new framing but door reads as out-swing; single 4-pane window.
  P05-L1: L33 door darker (partial) but bed end NOT softened; near-duplicate of L17 (diff 4.6/255).
          L34 text-only: door at frame edge, bed end soft, black under-door gap - closest to the P05 brief; walls greener, no lamp in frame.

DISCLOSURES:
  - The generator copies reference framing almost exactly even when told not to (L22, L24, L26, L33). One call per image; no rerolls.
  - Reference used per image is in the index reference_ids column ("none (text-only)" where none).
  - Map's "mother on the floor" deliberately NOT drawn per user instruction: floor kept empty in every image.
  - No people, hands, figures, silhouettes, framed photos, text, numbers or brands seen in any image (all viewed).
    Small blank box on nightstand appears in some (no digits).
  - Index defects column holds the per-image defect notes; every row prefixed PRELIMINARY.

QUESTIONS FOR CLAUDE:
  1. Rug or no rug? L11 master has none; L13 and L14 (take 1) have a braided rug. This batch went no-rug.
  2. Bed width: L23/L24 read wider than a single. Is a single bed locked?
  3. P03 framing: the generator resists a 50mm diagonal from ~1 m inside the door. Accept the frontal reads (L21/L23) or re-spec P03?
  4. P05 light-line policy: with the dark hall, is a black under-door gap correct (as done), or is any line wanted?
  5. Hinge side: confirm door hinged on the window-side jamb (knob on the right of the closed door from inside), opening inward.
  6. Door trim: white (L13, L17) or dark-stained (L31, L34)?
  7. Window trim: dark (L11/L12) vs white (L28/L30) - which is locked?
