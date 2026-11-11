# SCORING_GUIDE - NOVA-IMG-BENCH-20261009

Score each image against the **prompt card + reference images**, not against taste. Zoom in to 100% for tattoos, piercings and teeth. Use `NA` when the feature isn't in the test (pre-filled). If the image is refused, set `refused=Y`, paste `refusal_text`, and leave scores empty. **Status stays `needs_user_review` on every row.**

**Hon Dolo lock list (HD-01..04)**
- Face identity = HD-EXP-LOCK-FACE.jpg (curly dark hair, stubble, brown eyes). Not a celebrity.
- "eye" tattoo: character-RIGHT cheek (viewer-left). "know": character-LEFT cheek (viewer-right). Small black serif text.
- Small blaster-with-smoke-curl tattoo: character-LEFT neck (viewer-right). Design = refs/HD-xx/05_TATTOO-HD-NECK-BLASTER_stencil.png.
- Shaved slit in LEFT eyebrow (character-left = image-right), no metal.
- Teeth: gold caps on upper canines only; other upper teeth natural white; silver lower grill.
- Piercings: two hoops in RIGHT nostril (character-right / viewer-left; see PLAN caveat), two bottom-lip rings, LEFT-ear hoop (viewer-right), RIGHT-ear black stud (viewer-left).
- Chest: twin-tower disc-ship tattoo, upper chest centre (HD-03, HD-04 where chest shows). Design = 06_TATTOO-HD-CHEST-DISC-SHIP_panel5.jpg.
- Hip blaster: character-LEFT hip (viewer-right), brown tooled holster, belt loop + thigh tie-down. Ref = 04_PROP-HD-HIP_holster-char-left.png.

**Lisan Al Gaib lock list (LAG-01)**
- Identity = LAG-LOCK-FACE-NATURAL.jpg; glowing electric-blue eyes; natural white teeth, NO grill.
- "AL" once between the brows; vertical G-A-I-B down chin centre; mirrored sandworms on neck + sun disc with eye at throat.
- Nostril hoop, eyebrow ring, ear hoop all on character-LEFT (viewer-right); other side bare.
- Outfit: tan stillsuit, black hooded cloak (hood down), gold Cuban chain.

**Boss / probe locks** = the features listed on each prompt card (species read, skin, eyes, outfit, jewellery, tattoo design + side, prosthetic/eye side).

## Columns
| Column | 0 | 3 | 5 |
|---|---|---|---|
| **identity_match** (0-5) | Different person/creature; would not pass as the character | Recognisably similar (hair, build, palette) but face shape/features drift; looks like a sibling | Same face/creature as the reference; you'd cut it into the same video without noticing |
| **tattoo_text_legible** (0-5) | Text missing, gibberish, or wrong words | Words present but partly malformed, wrong case/size, or only one of two words correct | Every word spelled exactly ("eye", "know" / "AL", "G-A-I-B") and readable at 100%; design tattoos (blaster, ship, worms, boss motifs) clearly match their design ref |
| **tattoo_placement_correct** (Y/N) | N = any required tattoo on the wrong side/area, mirrored, duplicated, or extra unrequested ink | - | Y = every tattoo on its stated side/area and nothing extra |
| **piercings_correct** (0-5) | Piercings missing or wrong side throughout | About half right (e.g. lip rings right but nostril/ear flipped or extra ear stacks) | Count, metal and side of every piercing correct |
| **grill_teeth_correct** (0-5) | Opposite of spec (e.g. full gold grill / fangs for Hon Dolo; any grill for Lisan) | Partly right (e.g. gold canines but upper fronts also gold, or no lower grill) | Exactly as spec (HD: gold upper canines only + natural fronts + silver lower grill; LAG: natural white teeth; probes: as described) |
| **prop_side_correct** (Y/N/NA) | N = prop/prosthetic on the wrong side or missing | - | Y = HD hip blaster on character-LEFT hip (viewer-right); BOSS-006 prosthetic arm character-left; BOSS-008 brass eye character-left; BOSS-009 missing arm character-left / tattoo right forearm |
| **outfit_scene_match** (0-5) | Outfit and setting ignored | Main garment right, details/setting drift | Outfit, accessories, setting, framing (16:9, requested crop) all as written |
| **overall** (0-5) | Unusable | Usable after a fix/edit pass | Ready to hand to animation as-is (Ziggy still approves) |

Scores 1, 2 and 4 are in-between grades. Write the reason for any score under 3 in `notes` (e.g. "know on neck", "holster right hip", "extra lip rings").

## Refusal logging
- `refused`: Y if the tool declined, blocked, or returned no image. Partial (made an image but dropped a requested element citing policy): `refused=N`, describe in `notes` with the verbatim message.
- `refusal_text`: verbatim, including any policy name. Screenshot as `<TEST-ID>_<TOOL>_a<N>_REFUSAL.png`.
- Refusals count as an attempt (max 3 attempts).

## Grok Bot baseline rows (tool C)
Pre-filled with filenames, scores blank for Ziggy. For BOSS tests the baseline is reference image 1 itself - score it only if useful as the target. Known drift already noted by Grok Bot QA is copied into `notes`.
