# E42 + E43 GenerateImage prompt pack (executor blocker)

**Status:** Executor cannot call `cursor` / GenerateImage (MCP namespace unavailable to subagents).
Parent must run these calls natively, then either save with z8save or re-delegate save/NOTES/SHA256.

Save helper:
```
python3 /workspace/enablers03/z8save.py <CAT> <asset_path> "<note>"
```
CAT = `E42-dish-hoops` or `E43-grill-case`. Notes: `L- S# | defects | preserve: ...`

Aspect: `16:9`. After first strong image, pass it in `reference_image_paths` for continuity.

---

## Shared style
Photoreal cinematic prop study, 16:9. Soft quarters bureau / plain studio. No readable text, no logos, no franchise names. No faces except optional fingers for E42. **Iced grill NEVER in a mouth** — E43 prop-in-case only.

## Refs
### E42
- Empty dish / hoops continuity: after first keeper, use that file
- Optional mood: `/workspace/hd-sb/return/GROK-HD-SB-GRILLUP-v001/selects/SB-GRILL-04-rings-in-dish.jpg` (hand+dish mood only; exact hoop count may be wrong — force EXACTLY two plain open metal lip hoops)
- Storyset cousins (do NOT copy blindly): `/workspace/storyset02/N25-rings-in-dish/`

### E43
- Geometry lock (PROP only, short even canines NOT fang-long):
  - `/workspace/hd-sb/work/HEAD-HD-ICED-ANCHOR-LOCK-r4.jpg`
  - `/workspace/hd-sb/return/GROK-HD-SB-GRILLUP-v001/HEAD-HD-ICED-ANCHOR-LOCK-r4.jpg`
  - `/workspace/GRILL-REF-ICED.jpg` (iced look only; ignore mouth context; shorten canines vs this ref)
- Case mood: `/workspace/hd-sb/return/GROK-HD-SB-GRILLUP-v001/selects/SB-GRILL-05-case-open.jpg` (FLAG: canines too long — override to short even)
- Storyset cousins: `/workspace/storyset02/N26-the-case/` (best short-contour: 001, 007, 008, 009, 012)

**Canine wording tip:** never say "fang". Say "canines only slightly longer than neighbouring teeth, short even contours, real-teeth length."

---

## E42-dish-hoops — 15 prompts

Call shape:
```
CallDynamicTool namespace=cursor toolName=GenerateImage
arguments: {
  "description": "<prompt>",
  "aspect_ratio": "16:9",
  "reference_image_paths": [<after first keeper>]
}
```

1. EMPTY DISH master
Photoreal cinematic prop study, 16:9. Small plain shallow metal or ceramic dish EMPTY on a soft quarters bureau wood surface, warm practical lamp spill, closed dark jewelry case softly out of focus beside it optional. No jewelry in the dish. No hand. No face. No readable text. No logos. Soft bokeh cabin interior.

2. EMPTY DISH three-quarter
Same empty dish, three-quarter angle, brushed metal rim catching warm light, plain bureau, no hoops, no face, no text.

3. EMPTY DISH top-down
Overhead empty dish on worn wood bureau, soft lamp, shallow DOF, no jewelry, no face, no text.

4. TWO HOOPS IN DISH master (design for hoops)
Same dish now holding EXACTLY two plain open lower-lip style metal hoop rings (simple round open rings with a small captive bead or gap, NOT solid bands, NOT iced, NOT diamond). Top-down, warm practical, no hand, no face, no text. Exactly two.

5. TWO HOOPS IN DISH three-quarter
Exactly two plain metal lip hoops resting in the dish, three-quarter, soft cabin bokeh, no face, no text.

6. TWO HOOPS IN DISH macro
Extreme macro of exactly two open metal lip hoops in the dish, scratched dish floor, warm specular, no face, no text.

7. ONE HOOP IN FINGERS over empty dish
Tattooed or plain fingers hold ONE plain open metal lip hoop above the EMPTY dish (second hoop not yet placed). No face. Bureau warm light. No text. Simple ring hoop not a band.

8. ONE HOOP IN FINGERS, second already in dish
Fingers hold one plain open metal lip hoop; the other identical hoop already rests in the dish. Exactly two total. No face. No text.

9. RELEASING hoop into dish
Fingers just releasing one plain open metal lip hoop into the dish where one matching hoop already sits. Exactly two. Motion soft. No face. No text.

10. PINCH pair over dish
Fingers pinch both plain open metal lip hoops together above the dish before placing. Exactly two. No face. No text.

11. DISH + closed case still life
Empty dish and closed dark velvet jewelry case on bureau, warm lamp, no hoops yet, no face, no text. Bridge to grill-case beat.

12. DISH with two hoops + closed case
Exactly two plain metal lip hoops in dish, closed dark case beside, top-down, no face, no text.

13. Soft studio EMPTY dish
Plain soft-gray studio, empty dish only, clean prop catalog lighting, no face, no text.

14. Soft studio TWO HOOPS
Studio, dish with exactly two plain open metal lip hoops, catalog lighting, no face, no text.

15. Wide bureau insert
Wider bureau top: empty dish or two-hoops variant (prefer exactly two hoops), lamp, drawer edge, optional closed case, no face, no readable text.

Suggested notes examples:
`L- S5 | empty dish master | preserve: shallow dish, warm bureau, no jewelry`
`L- S5 | exactly two open lip hoops in dish | preserve: open-ring geometry not bands`
`L- S4 | hoop in fingers; count OK | preserve: plain metal hoop, dish`

---

## E43-grill-case — 15 prompts

**Hard rules:** iced upper+lower rows as PROP in case only; short even canines (only slightly longer than neighbours); NEVER show grill in a mouth; no face; no readable text.

Refs every call until a strong case+grill master exists:
`reference_image_paths`: [
  "/workspace/hd-sb/work/HEAD-HD-ICED-ANCHOR-LOCK-r4.jpg",
  "/workspace/GRILL-REF-ICED.jpg"
]
Then add the first strong E43 jpg as continuity ref. Extract iced grill GEOMETRY from the lock refs; do NOT copy the mouth/face.

1. CLOSED CASE master
Photoreal cinematic prop study, 16:9. Closed slim dark velvet or brushed jewelry case for dental grill rows, latch, on soft quarters bureau wood, warm practical. Case alone, closed. No grill visible. No face. No text. No logos.

2. CLOSED CASE three-quarter studio
Closed case, three-quarter, soft studio, latch detail, no face, no text.

3. CLOSED CASE on bureau with empty dish nearby
Closed case + empty small dish on bureau (hoops not required), warm lamp, no face, no text.

4. OPEN CASE empty foam (no grill yet)
Open case, empty molded velvet/foam slots for upper and lower grill rows, no grill pieces yet, no face, no text.

5. OPEN + ICED GRILL master (design master)
Open jewelry case on bureau. Inside: iced gold-pavé UPPER dental grill row and iced silver/white-gold pavé LOWER dental grill row as loose PROP pieces nestled in velvet (NOT worn, NOT in any mouth). Upper canines only slightly longer than neighbouring teeth — short even contours, real-teeth length, NOT elongated, NOT vampire. Joined rows, clean single set. No face. No text. No logos.

6. OPEN + ICED GRILL top-down
Same iced upper+lower rows in open case, top-down, short even canines, velvet, no face, no text.

7. OPEN + ICED GRILL three-quarter low angle
Lid raised, iced rows visible, short even canines, warm lamp, no face, no text.

8. OPEN + ICED GRILL macro upper row
Macro of iced upper row in velvet: pavé stones, gold frame, canines only slightly longer than neighbours, short even contour. No mouth. No face. No text.

9. OPEN + ICED GRILL macro lower row
Macro of iced lower row in velvet, even contour, pavé. No mouth. No face. No text.

10. OPEN case + iced grill + dish with exactly two plain hoops
Continuity still life: open case with iced rows (short even canines) and small dish with exactly two plain metal lip hoops beside it. Grill never in mouth. No face. No text.

11. Gloved or bare fingers lifting upper iced row from case
Fingers lifting the iced UPPER grill PROP from the open case; lower row remains in case. Short even canines. No face, no mouth wearing grill. No text.

12. Case lid mirror / interior detail
Open case lid interior (soft mirror or velvet) reflecting iced rows loosely, short even canines, no face portrait, no text.

13. Soft studio open case + iced grill catalog
Clean soft-gray studio, open case with iced upper+lower props, short even canines, no face, no text.

14. Wide quarters bureau: open case with iced grill
Wider cabin bureau shot, open case with iced rows (short even), lamp, optional empty dish, no face, no text.

15. Closed vs open pair thought (single frame open preferred if pair risks text)
Open case with iced rows, short even canines, soft practical, strongest hero angle, no face, no text.

Suggested notes:
`L- S5 | closed case master | preserve: slim dark shell, latch, bureau`
`L- S5 | open iced rows short even canines; design master | preserve: joined upper+lower, pavé, NOT fang-long, NOT in mouth`
`L- S3 | canines too long/fang-like | preserve: velvet case layout | fix: shorten canines`

---

## After parent generates
For each asset path returned:
```
python3 /workspace/enablers03/z8save.py E42-dish-hoops /path/to/asset.jpg "L- S5 | ..."
python3 /workspace/enablers03/z8save.py E43-grill-case /path/to/asset.jpg "L- S5 | ..."
```
Then write NOTES.md, run `sha256sum *.jpg > SHA256SUMS` inside each folder, confirm 15 jpg each and qa_z8.tsv lines.

Folders pre-created empty:
- `/workspace/enablers03/E42-dish-hoops/`
- `/workspace/enablers03/E43-grill-case/`
