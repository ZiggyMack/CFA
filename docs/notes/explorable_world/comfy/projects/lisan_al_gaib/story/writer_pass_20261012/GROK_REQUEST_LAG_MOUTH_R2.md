# Request to HaL's team — Lisan mouth shapes, round 2: the five unresolved shapes

From: Claude (lead writer), on Ziggy's go of 2026-10-13 about 02:00 UTC ("we want coverage of all mouths we need, and we want them to be good, so we got to regenerate them"; DECISIONS_20261012.md item 24). To: HaL and helpers, through the Pent House. Owner of intake: CFA Nova. Status: an image request within the current paid Grok allowance; ordinary batch; no purchases, no settings changes; every return is preliminary; nothing is accepted on arrival.

## What is asked

Regenerate the five mouth shapes that the first round (`GROK-LAG-VIS-NATURAL-v001`) could not deliver, natural teeth, no grill, no breather, Lisan's face per the lock:

| Shape | Name (VIS-HD numbering, which the v001 README says matches) | What v001 has | What failed |
| --- | --- | --- | --- |
| 07 | F-V (upper teeth on the lower lip) | `04_FAILS/VIS-07_F-V_r3_FAIL.jpg` only | the lip tuck would not render; the tool returned smiles |
| 15 | BITE-LOWER-LIP | `04_FAILS/VIS-15_r2_FAIL.jpg` only | the bite would not render |
| 16 | BITE-UPPER-LIP | no file | same |
| 18 | LIP-ROLL-IN | no file | same |
| 35 | TONGUE-IN-CHEEK | `04_FAILS/VIS-LAG-35_TONGUE-IN-CHEEK_Z_5_FAIL.jpg` and `_r2_Z_5_FAIL.jpg` | no cheek bulge |

## The identity, unchanged

Reference 1, always: `FACE-REF-v3.jpg` on the box, which is `lisan_al_gaib/01_Flagship_References/LAG-LOCK-FACE-NATURAL.jpg` on D: (SHA-256 `602a9fd4021dc356…`). Young man, exact face of the reference, messy black curls, electric-blue eyes, light stubble, natural white teeth, no grill, no fangs, no breather; small AL between the brows; small vertical G-A-I-B on the chin, four letters, the I included, one column; two open-jawed sandworm throat tattoos facing each other with the eye-in-sun-disc between them, flat black ink, not raised; one silver nostril hoop, one brow ring and one ear hoop on his left (image-right in a frontal view), the other side bare; nothing from Hon Dolo (no eye/know lettering, no neck blaster, no gold mouth, no lip rings). Frontal or near-frontal chest-up, plain background, even light, as the v001 visemes were framed, so the mouth is the only variable.

## How to beat the failure (round 1's lesson, applied)

In round 1, F/V, lip-bite and lip-tuck came out as smiles (HaL's warning, and the v001 README's "lip tuck/bite won't render"); describe the mechanics instead of naming the action, and cap the tries:
- **07 F-V:** the upper front teeth rest on the wet line of the lower lip, the lower lip drawn slightly in and up under them, lips otherwise relaxed, as at the start of the word "five".
- **15 bite lower lip:** the lower lip is held between the teeth, the upper teeth pressing a shallow dent into it, the lip's flesh bulging a little either side of the teeth, chin tension visible.
- **16 bite upper lip:** the lower teeth hold the upper lip, the lower jaw pushed forward, the upper lip folded down over the lower teeth.
- **18 lip roll in:** both lips rolled inward over the teeth so that no lip red shows, the mouth a thin pressed line, the chin dimpled.
- **35 tongue in cheek:** mouth closed, the tongue pushed hard into the inside of the left cheek so the cheek bulges outward in a round lump the size of a thumb tip, the opposite cheek flat.
Five tries per shape at most; keep every try; mark the best as the candidate and the rest as fails; if a shape still will not render after five, say so in NOTES and stop. Do not regenerate the thirty-nine shapes that already have passes, and do not touch the seven Production mouths (VIS-LAG-20, 20 r2, 21, 22, 22 r2, 23, 24).

## Where it lands and how it is recorded

`D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\GROK-LAG-VIS-NATURAL-v002\` with `01_VISEMES_R2\` (candidates, named `VIS-LAG-07_F-V_r4_<bot>.jpg` and so on, the try number continuing from v001's), `04_FAILS\` (every failed try, with `_FAIL`), `MANIFEST.csv` with v001's columns (file, collection, shape_no, prelim_likeness, prelim_scene, suggested_lane, suggested_scope, stage, score_status, defects, sha256) plus bytes, try, bot and a role column (character detail) per Nova's convention, `NOTES.md` (one line per file: `L# S# | defects | preserve: …`), and a mailbox message to `nova` and `claude` with the manifest hash when the package is complete. Write straight into that package folder if your harness can, and report the actual path; if it must download first, report the staging location for Nova to reconcile (Nova's convention, mailbox 21e64639). Scores are the team's provisional self-scores; CFA Nova intakes; Ziggy's review decides.

— Claude
