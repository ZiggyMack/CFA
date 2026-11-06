# V Team rules: Ziggy decisions, v004 (supersedes v003 f9e39a6b)
Fixes v003: Y-SOUND is now DECIDED (Ziggy, in Chief's chat, 2026-10-21 01:48 ET).

Lisan Al Gaib, decided:
- Throat worms: c02 (116907b6).
- Build: CAND-01 frame, 6'1" semi-athletic, lean-natural. Height is a soft target.
- Ear: ONE hoop. Brow: RING.
- Eyes: VARIABLE. No glow (CAND-01) is the default; glow is allowed in dark scenes or when the mood calls for it. Neither is drift.

Hon Dolo mouths, decided:
- Y-SOUND gets up to 3 redo attempts as its own shape. If none pass, it merges into EE and does NOT go on the challenge list.

Still open with Ziggy:
- CH-SH v002 vs v003
- LAG-1K set-wide younger face
- LAG-1K flavor and ZIGGY-PICK sheets
- Falcon set-wide items via Chief: saucer chest ship, Hon looking younger, C05 Lurch teeth, and no lip hoops in iced prompts

## Added in v005 (2026-10-21, after the usage reset)

### Budget rule (Chief, at Ziggy's request)
- Each frame gets at most 2 fix rounds after its first review. After round 2, whatever is left goes to Chief for a call or onto Ziggy's pick list, tagged ROUND-CAP.
- A defect that only shows at 6x autocontrast or in the high-pass is ADVISORY, not FIX, and gets no redo.
- Any defect visible at 1x, 4x or plain 6x is still FIX, and so are the critical features (grill, tattoos, face, pistol lock).

### Inpaint ruling (V_1, on 301)
- Classical, non-model inpainting (OpenCV-style Telea or Navier-Stokes) with cloned texture on top is not "generated pixels".
- It is ADVISORY, with the method logged, if it isn't visible at 4x and doesn't touch the grill, face, pistol or ship ink.
- A model or diffusion inpaint goes to Chief.

### Chest scale (Ziggy; Chief applying it to every frame)
- The ship is a large chest piece. It is drawn at full chest scale (about 2-3x the old fitted size), centred on the sternum, with ink only on bare skin.
- The clothing stays byte-original and can hide part of the ship. Never shrink the ship to fit the opening.
- FLAG-SIZE, fit-around and the old 0.90-1.15x disc rule are retired. An undersized ship is a FIX, even on frames that passed before (for example 300 at 0.75x and 279 at 0.62x).
- Each big-ship check covers four things:
  - the clothing pixels are identical to the original;
  - the ship edges are clean where they meet the clothing;
  - the lines are redrawn crisp at the new size (not upscaled), with the weight matched to the blaster at 4x;
  - the old saucer is fully erased.

## Correction in v006 (Chief, 10:40 ET)
- The scope of the chest-scale rule is ON HOLD. Only C04-010 gets the big-ship redo for now. Ziggy reviews it, and then decides how far the rule goes.
- Until then, don't FIX any frame on size alone, and don't reopen frames that already passed. Log any undersized ship as SIZE-PENDING and keep checking everything else.
- The big-ship check list (byte-original clothing, clean edges at the clothing, crisp redrawn lines, old saucer fully erased) still applies to C04-010 and to any later big-ship redo.

## Alignment in v007 (Chief, 10:41 ET), replacing v006's interim size wording
- Until Ziggy picks the scope, score size on the CURRENT rules (the 0.90-1.15x disc rule with the 0.01 margin, plus FLAG-SIZE for real obstructions), and tag every row "size under review".
- The full-scale rule is applied only to the C04-010 v009 test. Keep measuring the full-scale ratio from C41-020 and C33-010, but don't score anything against it yet.

## v008 (Ziggy, 10:42 ET): full-scale rule applies to EVERY frame (replaces the holds in v006 and v007)
- Every Hon Dolo frame uses Ziggy's approved stencil at full chest scale (the C41-020 / C33-010 size, roughly 2-3x the old mini-saucer footprint). It sits centred on the sternum, is cropped by the original clothing, and shows ink only on bare skin.
- Stencils: /workspace/falcon1000/_chest_tattoo_audit_v001/_ref_ziggy_stencils_20261021/ZIGGY_STENCIL_sheet_twintower_v001.png, with the detailed saucer sheet next to it.
- Sizing to the old saucer (the 0.90-1.15x rule) and shrinking the ship to fit the opening are both RETIRED. An undersized ship is now a FIX, including on frames that already passed.
- Use V_2's full-scale ratio (shoulder span primary, face-width fallback) as the size check once it's frozen.
- The big-ship check list still applies. The 2-round budget rule counts from the first full-scale review.
