# E44-slab — prompt pack (executor blocked: GenerateImage unavailable)

## Refs (use as reference_image_paths)
Primary face/identity: `/workspace/hd-sb/recovery/_review/lf_full.png`
Strongest slab pose/prop:
- `/workspace/storyset02/N19-slab/N19-slab-008.jpg` (L5 S5)
- `/workspace/storyset02/N19-slab/N19-slab-015.jpg` (L5 S5)
- `/workspace/storyset02/N20-slab-prop/N20-slab-prop-001.jpg` (front/3-4/hand detail triptych; gold curb on char-right)
- `/workspace/storyset02/N20-slab-prop/N20-slab-prop-004.jpg` (hero plinth, side panels with red LEDs)
- `/workspace/storyset02/N20-slab-prop/N20-slab-prop-014.jpg` (face + chain macros)

After first strong save: self-ref that jpg for remaining shots.

## Hard locks
- Carbonite RELIEF (not living flesh, not a person standing in front of a slab)
- Raised hands palms-out flanking head
- Gold curb bracelet + dark band on character-RIGHT wrist (= viewer-LEFT when slab faces camera)
- Youthful curly-haired likeness matching lf_full / N19-008/015
- No readable text/logos
- aspect_ratio 16:9; save via `python3 /workspace/enablers03/z8save.py E44-slab <asset> "L- S# | ... | preserve: ..."`

## Shot list (15)
1. FRONT, no vapor — design master, full slab upright, raised hands, curb+dark band on char-right wrist
2. FRONT, with vapor — same as 001 + cool vapor sheets
3. THREE-QUARTER from viewer-left, no vapor — show side control panel / red LEDs
4. THREE-QUARTER with vapor
5. HAND DETAIL — char-right wrist macro: gold curb + dark band, relief metal texture
6. FACE DETAIL in relief — closed/calm eyes, curly hair frost, carbonite pits
7. FRONT low hero angle + vapor
8. FRONT high angle, no vapor
9. EDGE-ON / near-profile of slab thickness + relief protrusion, no vapor
10. HANDS PAIR detail (both palms) with curb+band visible on char-right
11. FACE + upper torso relief macro, vapor whisper
12. Prop on chamber cradle / hover platform with vapor (chamber context, slab still hero)
13. Blue cinematic cool light, vapor, front
14. Warm practical spill, no vapor, three-quarter
15. Flat prop-shop / workbench hero, no vapor, full front + slight 3/4

## Prompt skeleton
Cinematic 16:9 still of a dark gunmetal carbonite relief slab prop. Upper torso of a young man with dense curly hair frozen in raised-hands pose (palms out beside head). Material is matte pitted frozen metal, not living skin. Gold curb-link bracelet and a dark leather/metal band on the figure's RIGHT wrist (viewer LEFT on front view). Side of slab has recessed greeble panels with small red LEDs. No readable text. [FRAMING] [VAPOR ON/OFF]. Match reference likeness and pose.
