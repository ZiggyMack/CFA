# V2 full-scale chest-ship reference ratio, v003 (20261021T145345Z)
v003 = v002 (V2_fullscale_ratio_20261021T145248Z_v002.md, sha256 47382f35d6ff..., frozen) plus ONE added ruling: the Chief 10:53 EDT bare-skin visibility / CENTRE-CLAMP rule, in the rulings section. No measurement changed. Crops are the v002 crops (returns/V2_fullscale_ratio_20261021T145248Z_v002_crops/). v002 is not edited, because frozen files get corrections only as new versions.

(v002 header follows)
# V2 full-scale chest-ship reference ratio, v002 (20261021T145248Z)
Author V_2. Supersedes v001 (V2_fullscale_ratio_20261021T144403Z_v001.md, sha256 477a42e2a05ec5bc99bd3580993922f573415bd04c71333e395b3168682163ec; still frozen). Everything from v001 is carried below unchanged except where a [v002] note says otherwise. New crops: returns/V2_fullscale_ratio_20261021T145248Z_v002_crops/ (4x annotated rim/neck-pit crops plus 4x equalized neck-pit crops). v001 crops are still valid for the v001 landmarks.

## v002 changes (summary)
1. Chief ruling: the 0.69 face-height vertical anchor is ADVISORY now, no longer the primary vertical.
2. New vertical measurement in DISC WIDTHS (dw): neck pit to the disc TOP RIM, disc centre below the neck pit, and horizontal offset from the sternum. Bands and crops are below.
3. C33-010 neck pit re-measured on a 4x equalized crop: (868,392) L-M, +/-10 px. v001 had (860,383) L. The tendon V converges lower than the v001 estimate.
4. Size rulings recorded: oversize is acceptable with no upper limit; there is a rule for non-frontal or cropped frames; and there is an interim placement rule.

## [v002] Size and placement rulings (Chief, 2026-10-21)
- SIZE, no upper limit: oversized is acceptable. Only an under-band disc is FIX-FULLSCALE. REV-HD-002 (disc/shoulder 0.354) is SIZE-PASS. The SIZE-OVER tag in V2_fullscale_retag_20261021T145020Z_v001.tsv is retired.
- Non-frontal or cropped frames (292, 298, 301, HIP-CASH, 299, SB-34, SB-12, SB-17):
  - The maker matches the disc size to the nearest front-facing frame of the same outfit, as a disc-to-head ratio.
  - V_2 checks it visually at 1x. There is no numeric band.
- INTERIM PLACEMENT, until the dw number below is adopted:
  - The disc sits on the sternum, with its top rim just below the collarbone notch (neck pit).
  - It may run off the frame bottom or under clothing.
  - Note: in both refs the top rim actually sits 74-79 px (0.47-0.69 dw) below the notch, and the masts fill that gap. "Just below" is therefore higher than either ref.
- [v003] VISIBILITY / CENTRE-CLAMP (Chief ruling, 2026-10-21 10:53 EDT):
  - Both spires and the disc's top rim must show on bare skin.
  - If the anatomical placement (the dw anchor, or the interim rule) would hide them under clothing or off the frame, lift the ship only as far as needed for both spires and the top rim to clear onto bare skin.
  - Log CENTRE-CLAMP with the offset: px and dw, measured from the anatomical target to the placed disc centre, with + = lifted.
  - CENTRE-CLAMP counts as a PASS, not a fail. The lower disc may still run under clothing or off the frame.

## [v002] Vertical/horizontal anchor in disc widths
Definitions:
- Disc width (dw) = rim-to-rim at the widest chord, from v001.
- Top rim = the top edge of the disc hull's back rim at the sternum line. This excludes the mast tips, the whole outline and the small central dome. Alt values with the dome top are given in the table.
- Disc centre = midpoint of the widest rim-to-rim chord, not the outline-box centre.
- + = below the notch / image right.

| landmark (px; conf.) | C41-020 | C33-010 |
|---|---|---|
| disc width | 159 (571-730) H | 115 (812-927) M +/-3 |
| disc top rim y | 460 M-H +/-3 (dome top ~457) | 471 M +/-4 (dome base; dome top ~462) |
| disc centre (rim-chord mid) | (650.5, 488.5) H | (869.5, 494) M |
| neck pit | (656, 386) M +/-8 (re-checked on 4x equalized; unchanged from v001) | (868, 392) L-M +/-10 (revised; v001 (860,383) L) |
| sternum x | 657 M | 866 M-L |

| ratio (dw) | C41 | C33 | band |
|---|---|---|---|
| neck pit to disc TOP RIM (PRIMARY, once adopted) | 0.465 (74/159) | 0.687 (79/115) | 0.442 - 0.721 |
| disc centre below neck pit | 0.645 (102.5/159) | 0.887 (102/115) | 0.613 - 0.931 |
| horizontal offset from sternum (+ = right) | -0.041 (-6.5/159) | +0.030 (+3.5/115) | -0.091 to +0.080 (near zero, so +/-0.05 dw absolute) |

Band rule: min/max of the two refs, +/-5% (or +/-0.05 dw absolute near zero). Recipe midpoints: top rim at 0.58 dw below the notch; centre at 0.77 dw below the notch.

Sensitivity and confidence:
- The C33 neck pit dominates the error: +/-10 px = +/-0.087 dw.
  - With the v001 pit (860,383), C33 would be gap 0.765 and centre 0.965 dw.
  - The C41 pit +/-8 px = +/-0.050 dw.
  - Rim-y errors are +/-0.02-0.03 dw.
- Using the dome top instead of the rim gives gaps of 0.447 (C41) and 0.609 (C33).
- In raw px the two refs agree closely (gap 74 vs 79, centre 102.5 vs 102). In dw they spread widely because C33's ship is about 20% smaller relative to the body (see the v001 reliability flags). So the dw band is wide.
- Effect on v001's advisory face-height metric: with the revised C33 pit, C33 centre-below-pit/FH = 0.624 (v001 0.690), so the advisory band would be 0.593 - 0.720 if recomputed. The v001 table is left as frozen.

v002 crops:
- C41-020_rim_notch_4x_annot.jpg, C33-010_rim_notch_4x_annot.jpg: red = neck pit with its +/- radius; orange = v001 pit (C33); magenta = top rim; green = rim chord and centre; yellow = sternum x.
- C41-020_neckpit_4x_equalized.jpg, C33-010_neckpit_4x_equalized.jpg: neck pits on equalized crops.

## [v002] Note on carried sections
- In v001's "Maker recipe" and "How to score" step 2, the "neck pit + 0.69 x face height" vertical is ADVISORY now.
- The interim placement rule above governs until the dw anchor is adopted.
- All other v001 content stands.

---
# Carried from v001 (unchanged)
Author V_2. Standard context: spec v014 6439c0f3. Units are full-res px (1280x720). Crops: returns/V2_fullscale_ratio_20261021T144403Z_v001_crops/ (landmark overlays plus gridded 2-5x crops).

## Sources (sha256 verified)
- C41-020: /workspace/falcon1000/C41-cockpit-ext/C41-cockpit-ext-020.jpg, df375140335081260c9e349b3c6cbdf1ede4832cf517cd701d74dd8678dc97e1
- C33-010: /workspace/falcon1000/C33-ramp-inside/C33-ramp-inside-010.jpg, d661f0eabe5aa06f2110fcb169722c840f148c3d6e68c2bbbed562c251cb5991
- Ziggy stencil sheet: /workspace/falcon1000/_chest_tattoo_audit_v001/_ref_ziggy_stencils_20261021/ZIGGY_STENCIL_sheet_twintower_v001.png, a906752ddb4c6136fd09e3272add4e32aa21ef1585a267d61dd4fdbbc053d67e

## Maker recipe (one line)
target disc px = 0.275 x the frame's shoulder px (fallbacks: 1.23 x eye-corner px, or 0.82 x cheekbone px); centre x = sternum midline; centre y = neck pit + 0.69 x face height (brow-to-chin); scale the stencil to that disc and let the clothing crop it.

## Measurements (px; confidence H/M/L)
| landmark | C41-020 | C33-010 |
|---|---|---|
| ship disc rim-to-rim | 159 (571-730 at y485-492, 5x) H | 115 (812-927 at y490-498, 5x) M (+/-3) |
| ship whole outline bbox | x571-731 y398-588 (h191) H | x812-927 y419-536 (h118) M |
| outline centre | (651, 493) | (869.5, 477.5) |
| shoulder span, acromion to acromion | 531 (L 412,385 / R 943,375; jacket silhouette, includes jacket bulk) M-L | 458 ESTIMATED: R 1095,362 measured (jacket silhouette); L hidden behind the gorilla, mirrored about the sternum x866. L |
| outer eye-corner span | 118 (593,187 / 711,177) H | 103 (770,173 / 872,156) H |
| cheekbone width | 167 (580-747) L (hair/ear edge) | 165 (755-920) L (hair) |
| face height | 156, BROW-to-chin (brow line y160 to chin y316). Hairline hidden by curls. M | 137, BROW-to-chin (brow y150 to chin y287). Hairline hidden. M |
| chin point | (668, 316) H | (843, 287) H |
| neck pit (suprasternal notch) | (656, 386) M-L | (860, 383) L |
| sternum midline x | 657 (notch, shirt-opening midpoint) M | 866 (shirt-opening and chain-V midpoint) M-L |
| head yaw / roll | yaw ~10 deg (eye widths 39 vs 31, nose 90/77 to the face edges); roll ~5 deg. Roughly frontal. | yaw ~0-5 deg (outer-to-bridge 51/51); roll ~9 deg. Frontal. |

## Ratios and bands (band = min/max of the two refs, +/-5%)
| ratio | C41 | C33 | band |
|---|---|---|---|
| disc / shoulder span (MAIN) | 0.299 | 0.251 (est) | 0.239 - 0.314 |
| disc / eye-corner span (fallback 1) | 1.347 | 1.117 | 1.061 - 1.415 |
| disc / cheekbone width (fallback 2) | 0.952 | 0.697 | 0.662 - 1.000 |
| centre below chin / face height | 1.135 (177/156) | 1.391 (190.5/137) | 1.078 - 1.460 |
| centre below neck pit / face height (PRIMARY vertical) | 0.686 (107/156) | 0.690 (94.5/137) | 0.652 - 0.725 |
| centre offset from sternum / face height (+ = image right) | -0.038 | +0.026 | -0.088 to +0.076 (+/-5% is taken as +/-0.05 face height absolute, because the values are near zero) |
Recipe midpoints: shoulder 0.275, eye 1.23, cheek 0.82, notch 0.69.

## Reliability flags
- Both refs are roughly frontal (yaw <=10 deg), so both are used.
- C33's shoulder span is a mirrored estimate (left shoulder hidden), so disc/shoulder rests mostly on C41.
- Shoulders are jacket silhouettes in both frames, not bony acromia (the jacket adds roughly 10-20 px a side).
- Cheekbone edges sit under hair in both frames, so that ratio has low confidence.
- The two refs disagree on ship scale by about 20% relative to the face (C33's ship is smaller), which is why the bands are wide. The vertical position below the neck pit agrees within 0.6%, so it is the robust anchor; below-chin varies with head tilt and should only be a fallback.

## Stencil match (Ziggy sheet a906752d)
Panels 1 and 3 (identical) and panel 2 are PLAN-view twin-tower ships: a round disc seen from above, two spires at the top, a dish/pod on the disc. Panel 5 is a non-twin saucer.
- Panel 1/3: disc 207-208 px, whole outline height 332-333 -> disc/height 0.625; spire outer span at the base 81 -> 0.39 of the disc; tip-to-tip 55 -> 0.26.
- Panel 2: disc about 200 (233 with the side pods); spire outer span 61 -> about 0.30.
- Ref chest ships are SIDE-elevation saucers with twin masts. Their design does NOT match the stencil.
  - disc/height: C41 159/191 = 0.83, C33 115/118 = 0.97 (stencil 0.625).
  - Spire outer span / disc: C41 ~65/159 = 0.41, C33 ~43/115 = 0.37. This matches stencil panel 1/3's 0.39.
  - So the DISC-WIDTH anchors above transfer to the stencil, but outline height and bbox centre do NOT. Project the stencil from the disc width, not from the refs' outline height.

## How to score
1. Anchor order:
   - shoulder span, only when both acromia (or the jacket shoulder points) are visible;
   - then outer eye-corner span;
   - then cheekbone width.
   - Log which anchor was used. Correct head roll by measuring along the tilted line (Euclidean distance).
2. Vertical: neck pit + 0.69 x face height (brow-to-chin). Fallback: chin + 1.26 x face height. Horizontal: the sternum midline (shirt-opening or notch midpoint).
3. Clothing crop:
   - Scale Ziggy's stencil so its disc = ratio x anchor px.
   - Place its DISC centre at (sternum x, the vertical anchor). The ref ratios use the outline-box centre; on the stencil, use the disc centre and let the spires extend above it.
   - Draw the full projected outline even where clothing covers it.
   - Score the visible ink against the projected outline: size from the visible rim arc fit to the projected disc; centre from the projected outline, not from the visible box (same as the FLAG-CENTRE frame-bottom rule).
4. Validity: the measurement is invalid if head or torso yaw is over 20 deg (eye-width asymmetry beyond about 0.7, or one eye corner hidden), or roll is over 15 deg uncorrected, or the anchor landmark is hidden. Then use the next fallback, and if none is valid, flag the frame for a Ziggy pick.
