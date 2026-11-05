# Benchmark: lip-bite mouth shapes (known limitation)
Closed by Ziggy 2026-10-15 as a benchmark for future models.

Shapes: 15 (upper teeth biting lower lip), 16 (lower teeth biting upper lip), related 07 F/V.
Best stand-ins: 07 try-zB_Z_2 (L5 S3), 15 zA_Z_2 (L5 S3), 16 zC2_Z_2 (L5 S3) / zE07_Z_3 (L4 S3).

Failed methods: face-ref prompts (ref mouth copied), text-only, lip-mechanics wording,
hardest-detail-first ("inside out"), underbite, bulldog jaw, upside-down face, animation frame,
plain face with no tattoo and no ref (5/5 failed, so the tattoo is not the cause),
real-photo mouth swaps. Closest: pixel edits and flipped-15 composites.

## Cross-model test (run the same prompts on any other image/video model)
A. Plain: "Extreme close-up, front-on, of a young man's mouth. His upper front teeth press down into his lower lip, folding it inward. Soft even light."
B. Plain reverse: "...his lower front teeth press up into his upper lip, folding it inward..."
C. Lisan base prompt (breather v3 face, look 01, no breather, natural teeth) + A, then + B.
Score each L/S 1-5, 3 tries per prompt; log model, date, scores here.
| model | date | A | B | C-A | C-B | notes |
|---|---|---|---|---|---|---|
| Grok Bot image tool | 2026-10-14 | fail | fail | fail | fail | baseline |

## Hon Dolo four-gold grill challenges (Chief, 2026-10-21)
Source: HD-MOUTH v004 redo (`/workspace/out/HD-MOUTH-v004/`, MANIFEST_v004.tsv, REVIEW_fails.jpg). Each shape below failed 3 attempts on the Grok Bot image tool, using v003 VIS-HD-03_AH as the grill reference plus a pose reference.
GRILL LOCK (prefix for every test prompt): "Same man, same face, skin, marks, septum and lip rings, lighting, tight macro of the mouth and chin, no ears or neck. Grill: the two upper central teeth are natural white; the upper laterals and the upper canines are gold (four gold upper teeth); the canines are only slightly longer than the neighbouring teeth; the whole lower row is a silver grill."
Pass = reads as its own shape next to its partner + grill intact + framing matches v003 + dhash > 4 against the partner (build_clusters_v001.py method).

| shape | partner | tried (3x) | how it failed | cross-model test prompt (after GRILL LOCK) |
|---|---|---|---|---|
| BITE-UPPER-LIP (known) | HALF-SMILE | AH only; AH+BITE-LOWER-LIP; AH with mechanics spelled out | a1 no bite; a2/a3 bit the LOWER lip and rendered all upper teeth silver (same failure as v003) | "The silver LOWER teeth press up onto the outer edge of the UPPER lip, so the upper lip is tucked under and dented by the lower teeth; the gold and white upper teeth are hidden behind the upper lip; jaw pushed forward (underbite)." |
| KISS-TEETH (known, v003, not retried) | KISS-PUCKER | v003 only | the side teeth drifted to natural white; the gold laterals and canines were lost | "Lips pursed forward in a kissing suck-teeth (tchip), parted at the centre to show the two white centrals and BOTH gold laterals; the lower silver row is just visible." |
| EXHALE | EE | AH; AH+SMALL-O; AH | a1 EE spread; a2 collapsed into SMALL-O; a3 reads correctly (soft parted lips, breath haze) but hash to EE is only 4 | "Relaxed lips, loosely parted 1 cm with no smile, a cheek-puff release, a faint visible breath mist, teeth barely showing." |
| CLENCHED-JAW | EE | AH; AH+FROWN_a1; AH+EXHALE_a2 | always an EE-style smile spread; masseter tension and flat lips never appeared (dhash 1-4) | "Teeth clamped together, the lips pulled back flat and level (not smiling, corners neutral), jaw muscles bulging at the sides, chin tense." |
| S-T-K | EE | AH+REST; AH; AH | a1 collapsed into REST (closed lips); a2/a3 EE spread (dhash 1-2) | "Saying 'S': teeth nearly closed with a 2 mm gap, lips parted only in the centre about the width of the two centrals, corners not stretched, no smile." |
| SNARL | EE | AH+SNEER; AH; AH+both-sides SNEER composite | the upper lip never lifted; output was an EE spread every time | "Aggressive snarl: the upper lip curled UP and away from the teeth on both sides, showing the gums above the gold teeth, nose wrinkled, lower lip neutral." |
| GRIMACE | EE | AH; AH+FROWN_a1 x2 | EE spread; the mouth corners never pulled DOWN, platysma never tensed (dhash 5, visual fail) | "Pained grimace: teeth showing, but the mouth corners are pulled sharply DOWN and outward into a downturned rectangle, neck cords tense, brow strain." |
| RAP-MID-WORD | AH | AH+SNEER; AH; AH+RAP_a2 | a1/a3 symmetric AH copies; a2 lopsided correctly but its image-right gold lateral turned white | "Mid-syllable while rapping: the mouth open asymmetrically, the left corner higher, lower lip pushed forward, a medium opening (half of AH)." |
| BIG-LAUGH | AH | AH+GRIN; AH+BIG-LAUGH_a1; AH+GRIN_a1 | a1 correct read but framed too wide (ears, neck); a2/a3 AH copies | "Head-back belly laugh: the mouth wide open, the cheeks pushed up into crow's feet, the upper lip high above the gold teeth, tongue low; keep the exact v003 framing." |
| GRIN (v004 a2 placeholder) | EE / AH | a4; a5; a6 (Z_2, after V_5 FIX on a2) | a4/a6 near-duplicate AH, a5 reads as EE; never separated (V5_HDMOUTH_v004check_20261021T074700Z_v001.tsv, e5089f83) | "Broad closed-corner grin: the lips stretched wide and pulled UP at the corners, the cheeks lifted, the teeth only lightly parted with the gold laterals and canines showing; not an EE spread, the mouth is not open." |
| YEAH-ADLIB | AH | AH+SHOUT; AH+GRIT-LIPS-BACK; GRIT-LIPS-BACK+AH | AH copies every time; a2/a3 framed too wide | "Shouting a 'YEAH!' ad-lib: the lips pushed forward into a squared horizontal rectangle, jaw half-open, the cheeks flexed." |
| YAWN | JAW-DROP | AH; AH; AH+SING-VOWEL_a1 | lower teeth turned white (a2/a3); framing too wide; a1 showed every tooth like JAW-DROP | "Big yawn: the mouth stretched tall into an oval, the upper lip covering most of the teeth, eyes squeezing, the tongue low and the throat visible; the lower teeth stay silver." |
| LIP-ROLL-IN | LIPS-PRESSED-THIN | AH+HUM; HUM; LIP-ROLL-IN_a2 | the lips thinned but never vanished into the mouth | "Both lips rolled fully inward over the teeth so NO red lip shows; only a straight seam line with the skin folding in around it; lip rings pulled inward." |

| model | date | shapes tested | pass | notes |
|---|---|---|---|---|
| Grok Bot image tool | 2026-10-21 | 13 rows above | 0/13 | baseline (3 tries each on 11 shapes in v004, plus GRIN (a4–a6, 3 tries, added 2026-10-21); KISS-TEETH is v003 only, not retried) |

## Challenge list additions 2026-10-21
### 17 LIPS-PRESSED-THIN (Lisan natural teeth): lips rolled fully in to a single thin tense line, set framing (HaL)
Status: partial. Best stand-in GROK-LAG-VIS-NATURAL-v003-redo/01_VISEMES/VIS-LAG-17_LIPS-PRESSED-THIN_v005-try3-composite.jpg (L4 S3, pixel composite).
Tried (6 generations + 1 composite):
- Text prompt with the mouth first, set frame (01_REST) as reference: the reference's relaxed full lips were copied (v004-try1, S1).
- Text only, no reference: a thin tense line appears, but identity drifts (pale skin, light stubble, wider framing) (v004-try2).
- Feeding that output back as the reference to correct it: stubble became moustache+goatee and a lip sliver stayed (v004-try3, V5 FIX-FACE).
- Edit MBP "change only the lips": MBP's full lips copied (v005-try1, S1).
- Two references (MBP for the frame, try3 for the mouth): the frame reference was ignored and try3 came back (v005-try2).
- Composite: try2 mouth onto MBP, colour-matched, then a vertical warp to squeeze the lips into the seam. The lip sliver is gone, but a smoothed ghost-lip band remains under the seam and there's no chin bulge (v005-try3).
Why it fails: the model won't hide lip tissue (the same failure mode as the lip tuck/bite shapes), and any set frame given as a reference brings its full lips with it.
Cross-model test D: "Extreme close-up, front-on, of a young man's lower face. He presses his lips together so hard both lips roll inward and disappear, leaving one thin flat line; chin muscle bunched. Soft even light." Score L/S, 3 tries.
