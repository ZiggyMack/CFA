# GROK-LAG-VIS-NATURAL-v002 (Z_5) — regen of 07, 15, 16, 18, 35
Natural teeth, no grill, no breather; prompts describe lip mechanics only. 26 tries kept (07 has 6).
Finding: when a face reference is attached, the model copies its mouth and ignores the mechanics (15a/16a/18a/35a = L5 S1). Text-only prompts move the mouth but drift the throat tattoos.
Usable: 35d (L4 S4), 18d (L4 S3). 07, 15 and 16 still don't render a true lip tuck or bite — CONTROVERSIAL, recommend a pixel or inpaint pass on the mouth of an L5 frame.
Passed shapes and Production mouths untouched.

## Z_2 local mouth edits (2026-10-12)
Base: 15a (L5, natural teeth). Method: pure PIL/OpenCV pixel compositing, no regen (GenerateImage was not available in this session). Vertical displacement warp of the lips only, with a per-column filled teeth mask layered on top and a contact shadow under the teeth, blended through a feathered ellipse around the mouth. AL, GAIB, the throat tattoos, eyes and hair are unchanged (diffs stay inside the mouth box). 6 tries kept.
- VIS-LAG-07_F-V_try-zA_Z_2.jpg: L5 S2. pixel warp from 15a: lower lip lifted 5px under upper teeth; contact too subtle
- VIS-LAG-07_F-V_try-zB_Z_2.jpg: L5 S3. pixel warp: lip lifted 8px, upper teeth rest on lower lip; faint seam at right canine - best 07
- VIS-LAG-15_BITE-LOWER-LIP_try-zA_Z_2.jpg: L5 S3. pixel warp: lip tucked 11px under upper teeth, reads as lower-lip bite; small shadow blotch left - best 15
- VIS-LAG-15_BITE-LOWER-LIP_try-zB_Z_2.jpg: L4 S3. deeper 14px tuck; slight lip smear and shadow blotch
- VIS-LAG-16_BITE-UPPER-LIP_try-zA_Z_2.jpg: L4 S2. upper lip pushed down + flipped-teeth lower row; reads as double teeth row, pink chip artifact
- VIS-LAG-16_BITE-UPPER-LIP_try-zB_Z_2.jpg: L3 S1. stronger push; teeth stack looks fake - reject pile
Verdict: 07-zB and 15-zA are usable (S3). 16 (lower teeth over the upper lip) isn't solved by pixel warp because the base frame has no lower teeth to borrow, so it stays CONTROVERSIAL and needs an inpaint or regen pass.

## Z_2 follow-up on 16 BITE-UPPER-LIP, try-zC (2026-10-12)
Base 15a. Step 1: took the visible lower-teeth row from 16e (x590-700, y325-343), tone-matched it to 15a's teeth, and pasted it with a feathered, arched alpha. The upper lip is warped down over the upper teeth, the lower lip is lifted to meet the graft, a pressure shadow is added on the upper lip, and the whole edit is blended in a feathered ellipse around the mouth only. Step 2 (GenerateImage) wasn't possible: the cursor namespace still isn't present.
- VIS-LAG-16_BITE-UPPER-LIP_try-zC1_Z_2.jpg: L5 S2. lower-teeth row from 16e grafted under the upper lip (6px push); upper-teeth tips still peek out, so it reads as clenched teeth, not a bite
- VIS-LAG-16_BITE-UPPER-LIP_try-zC2_Z_2.jpg: L5 S3. 10px lip push and 8px teeth overlap; the lower teeth sit against the upper lip edge, the closest to a bite - best 16, near miss
- VIS-LAG-16_BITE-UPPER-LIP_try-zC3_Z_2.jpg: L4 S2. 14px push; the upper teeth re-emerge below the graft, double-row artifact - reject pile
Verdict: zC2 is the best but still a near miss (S3). 16 stays CONTROVERSIAL until a GenerateImage or inpaint pass can draw the upper lip folding under the teeth.

## Z_3 zD (16 inpaint, text-only)
zD1-3: text-only mouth macros (no ref). All three render a normal closed bite, upper teeth in front; the generator would not fold the upper lip behind the lower teeth. Kept as unblended source tries, L1 S1, not blended into 15a. 16 stays CONTROVERSIAL; zC2 is still the best.

## Shape 16 zE run (Z_3, 2026-10-12)
- FAIL paths (zE01-06): inside-out prompt order, profile underbite, bulldog/reverse-beaver wording, upside-down framing. Controls show the generator can't draw even a normal LOWER-lip bite from text, so prompt wording is a dead end for both 15 and 16.
- SUCCESS path (zE07/zE09): vertically flip the solved 15 mouth (15-zA) and feather it into 15a. The bite geometry inverts into lower teeth over a tucked upper lip. zE07 L4 S3 is the new 16 candidate alongside zC2.
- Ran 9 of the planned ~50; I stopped early because the remaining text methods were all variants of a proven dead end.

- Plain-face test (zE10-12, HaL request 2026-10-14): no tattoo, no Lisan, no reference image. All three were a normal bite or grimace. Together with zE04-05 that's 5/5 plain-face fails, so the limit is in the generator, not the tattoo. Next: Z_2's real-photo mouth swap.

## Z_2 real-photo mouth swap, try-zF (2026-10-14)
Ziggy approved the real-photo mouth swap. Sources, all free-licence (attribution required, and BY-SA means share-alike if published):
- w1 "Lip biting anticipation", Alberto Alonso G, CC BY-SA 2.0. https://commons.wikimedia.org/wiki/File:Lip_biting_anticipation.jpg
- o07 "Biting lip", Lee J Haywood, CC BY-SA 2.0. https://www.flickr.com/photos/45034206@N06/6163609387
- o10 "Who doesn't like a little lip bite", FashionbyHe, CC BY 2.0. https://www.flickr.com/photos/49795400@N08/8220011854
Full list in /workspace/z2vis/photos/SOURCES.md. No free-licence UPPER-lip bite photo was found (Commons, Openverse/Flickr CC, Pexels/Unsplash search), so there is no zF for 16.
Method (base 15a): similarity transform from the photo's mouth corners to 15a's corners (562,397)-(710,410), Lab luminance and chroma matching (lip and skin chroma shifted separately, teeth left neutral), noise grain matched to 15a, feathered ellipse around the mouth only (changes fall within y356-449, x541-727; AL, eyes and throat tattoos untouched, GAIB's G clear of the mask). zF4/zF5 graft only the photo teeth onto 15a's own lips with a lower-lip lift. Scripts: /workspace/z2vis/vF.py, vF2.py.
- VIS-LAG-15_BITE-LOWER-LIP_try-zF1_Z_2.jpg: L3 S3. whole-mouth swap from o07 (Haywood CC BY-SA 2.0); real upper teeth on lower lip read as a bite, but the lips turn greyish, teeth yellow with dark gaps, and the skin tone seam is visible
- VIS-LAG-15_BITE-LOWER-LIP_try-zF2_Z_2.jpg: L3 S2. whole-mouth swap from w1 (Alonso CC BY-SA 2.0); teeth only resting, pale lips, bluish blotch on lower lip
- VIS-LAG-15_BITE-LOWER-LIP_try-zF3_Z_2.jpg: L2 S2. whole-mouth swap from o10 (FashionbyHe CC BY 2.0); glossy female lips, red seam - reject
- VIS-LAG-15_BITE-LOWER-LIP_try-zF4_Z_2.jpg: L4 S1. teeth-only graft from o07 onto 15a lips; the auto teeth mask segments into flat slabs - reject
- VIS-LAG-15_BITE-LOWER-LIP_try-zF5_Z_2.jpg: L4 S1. teeth-only graft from w1; same slab segmentation - reject
Verdict: none of the zF tries beats the previous bests. The free photos are low-res, different-lit and mostly small in frame, so the swapped lips don't match Lisan's skin and lip tone. Best 15 stays zA (L5 S3), with zF1 the best photo try (L3 S3). Best 16 stays Z_3 zE07 (L4 S3) / Z_2 zC2 (L5 S3).
