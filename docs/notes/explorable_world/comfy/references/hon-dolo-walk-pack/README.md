# Hon Dolo walk templates (HD-EXP-306–314)

Ground truth face: **HD-EXP-LOCK-FACE.jpg** (included). These are motion/pose scaffolds for Comfy (IP-Adapter + AnimateDiff / SVD), not a final locked walk.

## Still sheet
| # | Angle | Phase |
|---|-------|-------|
| 306 | front | contact |
| 307 | front | mid |
| 308 | front | push-off |
| 309 | side | contact |
| 310 | side | mid |
| 311 | side | push-off |
| 312 | 3/4 | contact |
| 313 | 3/4 | mid |
| 314 | 3/4 | push-off |

Contact sheet: `HD-EXP-WALK-CONTACT-SHEET.jpg`

## Clips (honest)
I cannot generate true AI video here. These are built from the stills:

- `HD-EXP-WALK-CLIP-keyframe-loop.mp4` — stepped keyframe loop (front then side)
- `HD-EXP-WALK-CLIP-morph.mp4` — motion-interpolated morph between those frames

Use stills as pose refs in Comfy for real walk consistency.

## QA
- **Usable-ish:** 306–311 (front + side). Face/tattoo drift still possible vs LOCK-FACE.
- **Weak / drifted:** 312 (wrong body scale), 313 (prop blaster in hand), 314 (look-back pose, extras). Prefer 306–311 for Comfy.
- Grill K9 length, piercings, eye/know, brow slit: verify every frame against LOCK-FACE before locking.

Outfit: cantina black leather + open white shirt (291 direction).
