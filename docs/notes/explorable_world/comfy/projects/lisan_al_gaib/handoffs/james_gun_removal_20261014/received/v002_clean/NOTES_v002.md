# James gun removal v002: CLEANED, LOCKED REFERENCE for the James exploration variants
Ziggy directed this by voice on 2026-10-14. James has no gun in the new variants, so the reference must be gun-free. v001 and the original source are untouched.

## Files
- Lossless PNG (this is the locked reference used for generation): 957897bd45c4__HIP-COAT-01_JAMES-NOGUN_v002.png, sha256 534f77cad9d47f4f78863d5233973467e8ae6cd34dea2d826e4a0fa70cbaf498, 1374349 bytes, 1280x720
- JPEG q95 copy: 957897bd45c4__HIP-COAT-01_JAMES-NOGUN_v002.jpg, sha256 63fc3c8df54cde28525004205cf6459f3a3e7ab90081313a9be3c71638596fa7, 290303 bytes, 1280x720
- Source: 957897bd45c4__HIP-COAT-01_v001.jpg, sha256 957897bd45c4fc03d685c4a40af7670385ab3970108cdbd319d839385dceacc1
- PNG vs. decoded source: changes are confined to x550-662, y451-542 (6168 pixels). The JPEG copy adds encode noise across the whole frame.

## What changed from v001
v002 starts fresh from the source with the same mask; it is not built on top of v001.
1. Belt: rebuilt from the clean belt's per-row median color profile (x470-550) plus slight noise, with brightness matched. This replaces v001's repeating hole pattern.
2. Belt end: stopped at the coat edge (x634), and the coat was restored on the right.
3. Area above the holster: filled with trouser texture from the left (x470-530), replacing v001's grey smear.
4. Metal remnant in the holster mouth: covered with a dark holster-interior shadow, so no metal shows.
5. Rest of the mask: OpenCV Telea inpaint at radius 5, then a 3x3 blur inside the mask and a 9x9 feathered blend.
Tools: Python and OpenCV 5.0.0. No generative model was used in the final pixels.
A rejected try: an image-generator edit of a crop around the hip (asset 1ef21602...) came back fully re-rendered, so it was not used.

## Remaining defects (judged acceptable as a reference)
- The belt patch is flat, with no tooling or holes, and its edge is soft compared with the real belt.
- The empty brown holster and straps are KEPT, per Nova's original brief. Note: an empty holster may tempt generators to add a gun. Variant prompts explicitly say there is no gun.
Status: locked as the generation reference for exploration. Not an approved James master.
