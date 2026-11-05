# James tattoo TRACE v006b (2026-10-14)

v006b traces James's **real** tattoo ink from the v004 photo (957897bd45c4__HIP-COAT-01_JAMES-CLEAN_v004.png). There is no Aramaic, no font text and no redraws. Every black pixel comes from ink visible in the photo. v006 (the Aramaic lettering overlay) was the wrong deliverable and is replaced by this set.

The stencils are placement aids only. The five boxes are the v003/v004 positions. Zone 5 is labelled L-FOREARM-HAND (character's left, viewer-right).

## Method (src/build.py, src/params.json)
For each box:
1. Crop the box and upscale it 4x (cubic).
2. Normalise the skin: lightness divided by a skin-only Gaussian (sigma 15 source px, 22 on the chest). I used skin-only because a plain blur normalised the dense dial away.
3. Detect ink with a dark-threshold OR (black-hat AND adaptive threshold), gated by local contrast so smooth shadows are rejected.
4. Inside the dial disc, use a tighter local threshold (sigma 2.5 px) so the bronze rings and spokes come out as open lines.
5. Apply exclusion masks:
   - **Chains:** bright gold pixels, dilated.
   - **Coat:** V below 30.
   - **Torso and arm:** hand-drawn skin polygons.
   - **Face:** small mark rectangles only, so eyes, brows, lips, teeth, earrings, hair and the nose ring are excluded.
   - **Neck:** the jaw-shadow area is masked, leaving only the side column and the throat line.
   - **Belt:** cut off by the polygons.
6. Clean up: median filter, removal of specks under 25–50 px (4x scale), then Gaussian smoothing and a re-threshold.

## How well each zone matches (honest)
1. **CHEST: good.** The astrolabe's real outer rings, the eight spokes, the hub and the dagger drop all trace where the ink is.
   - The shadowed left edge of the disc fills a bit heavy.
   - The inner tick and glyph detail is approximate (blobby at this source resolution).
   - The filigree on the upper chest between the chains is fragmentary.
   - The chains are cut out, so there are gaps where they cross ink.
2. **NECK: fair to poor.** The side column (viewer-right of the throat) and the small throat line are captured in roughly the right places.
   - Strokes are broken and the script isn't readable.
   - The ink under the chains is lost.
   - There are a few false strokes along chain shadows on the lower neck.
3. **FACE: fair.** The forehead mark, the swirl under the viewer-right eye and the dot-circle on the viewer-left cheek all land at the right spots.
   - The shapes are simplified blobs, not clean outlines.
   - The marks are a few pixels across in the source.
4. **ABDOMEN: fair to good.** Both flank columns and the navel or centre motif are traced in place.
   - The flourishes are fragmented, and the very edges next to the coat are missed.
5. **L-FOREARM-HAND: fair.** The sleeve's density, extent and the four knuckle marks are correct.
   - Individual script strokes merge into texture.
   - There are a couple of false vertical strokes at the arm edges and finger shadows.

## Limits
- The source is 1280x720, and the ink was AI-generated, so it has no clean line structure. Treat this trace as "where the ink is", not as clean flash.
- A hand ink-over on top of TRACE-OVERLAY-FULL would be the next step for crisp linework.

## Files
- **individual/:**
  - JAMES-TRACE-ZONE-*_v006b.png: 1-bit per zone, black ink on white, 4x scale.
  - TRACE-OVERLAY-FULL_v006b.png: 1280x720 RGBA, black ink on transparent, pixel-aligned to v004. I checked it by laying it over the photo.
  - TRACE-OVERLAY-FULL-4x_v006b.png: the same at 5120x2880.
- **sbs/:** PHOTO | TRACE side-by-side per zone.
- **sheets/:**
  - JAMES-TRACE-STENCIL-SHEET_v006b.png: 1-bit, panels 1–5.
  - JAMES-TATTOO-PLACEMENT-MAP_v006b.png: v003 style.
