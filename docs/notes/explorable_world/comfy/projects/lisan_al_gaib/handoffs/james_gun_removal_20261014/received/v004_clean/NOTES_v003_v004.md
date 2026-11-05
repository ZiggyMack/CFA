# James reference v003 and v004
## v003: holster removed (957897bd45c4__HIP-COAT-01_JAMES-NOHOLSTER_v003.png, sha256 4c9472df…78ac)
Made from v002. Every brown-leather part of the holster rig was masked by color and shape: the holster body, the thigh strap and the left dangling strap (holster_mask_v003.png). The masked area was filled with trouser texture copied from the clean trousers, and the edges were softened. The belt keeps v002's rebuilt section.
Defects: faint vertical seams in the fill and a few dark specks near the hand.
## v004: clean (957897bd45c4__HIP-COAT-01_JAMES-CLEAN_v004.png, sha256 35bc7b17…7ee0; JPEG q95 copy sha256 21e83dad…f4)
1. Specks near the hand: non-skin pixels that differed from their local median were inpainted. This affected 326 pixels in the first pass, and a wider sweep followed.
2. Seams: inside the fill area only (skin excluded), the texture was smoothed horizontally while keeping 50% of the fine detail, then brightness-matched to the surrounding trousers.
Everything outside the hip fill and the speck zone is identical to v003: same pose, face, hair and background, with no gun and no holster.
Remaining: the fill is slightly flatter than the real fabric. At 3x zoom, one very faint vertical edge is visible at the left of the fill. The belt section is still plain.
