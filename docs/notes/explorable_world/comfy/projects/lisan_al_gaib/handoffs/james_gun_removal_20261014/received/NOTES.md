# James gun removal: BLOCKING DRAFT, NEEDS FIXES (NOT A MASTER)
Status: needs_fixes / blocking_draft. Not an approved James master. No rerolls were made. The source was preserved untouched.

## Source
- Name: 957897bd45c4__HIP-COAT-01_v001.jpg (HD-RETURN-957897bd45c4; this is the selected gun variant, NOT ancestor HD-DROP-45892924b234)
- SHA-256: 957897bd45c4fc03d685c4a40af7670385ab3970108cdbd319d839385dceacc1
- Size: 306212 bytes, 1280x720
- The source is not included in this folder; it stays at its original location.

## Output
- Name: 957897bd45c4__HIP-COAT-01_JAMES-NOGUN_v001.jpg
- SHA-256: 0223fd8d0c6f4c8af225a19daca05d213dd9d261322953aa89c04e6ed2b30a79
- Size: 291259 bytes, 1280x720

## Method (classical local repair; no generative model in the output)
Tools: Python 3 with OpenCV 5.0.0 and NumPy.
1. Hand-drawn polygon mask over the visible gun, dilated with a 5x5 kernel.
   - Mask bounding box: x553-659, y454-532 (cv2.boundingRect gives 553,454,107,79). It covers 5765 pixels.
   - The mask is JAMES-NOGUN_v001_edit_mask.png.
2. Belt band (y462-495, x552-639 within the mask): filled by tiling a 30px strip of the source belt from x522-551.
3. Rest of the mask: cv2.inpaint with INPAINT_TELEA, radius 9.
4. Edge blend: the mask was Gaussian-blurred (7x7) and used as alpha over the source.
5. Saved with cv2.imwrite as JPEG quality 95. There was NO full-frame lossless working PNG of this final version saved; only the mask and an upscaled 3x preview crop (x520-699, y430-579) are kept.

## Pixel-identity qualification (correcting my chat claim)
My earlier claim that every pixel outside the patch was identical was measured on the in-memory working array BEFORE JPEG encoding. It is NOT true of the decoded final JPEG.
Decoded final JPEG vs decoded source, outside box x553-659 / y454-532:
- 162,737 pixels differ by at least 1 level.
- 13 pixels differ by more than 8.
- Max difference is 9 levels; mean is 0.29.
These differences come from JPEG re-encoding. The picture content outside the box was not edited.

## Defects
1. The belt was rebuilt from a repeated tile: the holes and keeper seams repeat visibly, and the belt end/edge overlap looks wrong near the coat.
2. The trousers just above the holster mouth are grey and smeared (inpaint blur, no texture).
3. Small metal remnants are visible in the holster mouth; they were left to avoid touching the holster.
4. The soft blend edge is faintly visible around the patch.
5. JPEG re-encode drift across the whole frame (see the section above).
What was kept: the holster and straps, the face, smile, tattoos (astrolabe), coat, jewelry, pose, lighting, framing, hangar and ramp. None of these were inside the mask, except where the mask edge touches the strap/holster top.

## Rejected attempts (evidence in rejected_first_attempts/)
- ATTEMPT0_generator_REJECTED_identity_scene_loss.jpg (sha 426972391e1e95da30377b407e52cb14b3231f9e9acd88895d2ed8a434d388ae, 280636 bytes, 1280x720)
  - Made with an image-generation edit, using the source as a reference.
  - It returned a different man, outfit and hangar. Rejected; not used.
- ATTEMPT1_telea_only_full_lossless.png (sha a5afe3c4733ae00a9766df41b8fa11073b2b7331a2028a641370c6af6ef3fe77)
  - Same mask, with Telea inpaint at radius 7 only and no belt tiling.
  - The belt broke into a blur. Superseded by the output above.
  - The crop preview is ATTEMPT1_telea_only_crop_x3.png.
