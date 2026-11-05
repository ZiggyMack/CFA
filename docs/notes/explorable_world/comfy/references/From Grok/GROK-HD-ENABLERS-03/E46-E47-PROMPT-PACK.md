# E46 + E47 GenerateImage prompt pack (for PARENT — executor has no cursor/GenerateImage)

**BLOCKER:** `cursor` / GenerateImage is not available to the executor subagent (CallDynamicTool returns "MCP server cursor is not available here"). Parent must call GenerateImage natively, then either:
1. Re-delegate to executor with asset paths for `z8save.py` + NOTES/SHA256SUMS, OR
2. Save themselves with `python3 /workspace/enablers03/z8save.py <cat> <asset> "note"`

Settings for every call: `aspect_ratio: "16:9"`. No people. No franchise logos. No readable text.

After each successful GenerateImage, note the returned asset path (hash.jpg under sand-data/agents/.../assets/). Order matters for sequential z8save numbering.

---

## E46-junky-ship — 18 images (candidates A/B/C × 6 angles)

Mapping for sequential filenames after z8save:
- **001–006 = candidate A** (long brick freighter)
- **007–012 = candidate B** (saucer-with-boxes)
- **013–018 = candidate C** (asymmetric claw)

Angles per candidate: (1) front three-quarter, (2) front, (3) rear, (4) port side, (5) starboard side, (6) top-ish / top three-quarter.

**Workflow:** Generate A001 (front 3/4) with text only → lock that image as `reference_image_paths` for A002–A006. Same for B and C.

### SHARED constraints (append to every E46 prompt)
```
Photoreal cinematic concept still, 16:9. Empty deep space with faint nebula and distant stars. NO people, NO crew, NO franchise silhouettes, NO Star Wars / Millennium Falcon / Venator / Star Destroyer shapes, NO logos, NO readable hull text or registry numbers, NO landing gear down (in-space float). Dirty patched plating, mismatched panels, weld scars, scorch marks, antennae and sensor blisters. Prefer photographic finish.
```

### Candidate A — long brick freighter
Overall: elongated rectangular brick hull, blunt nose, twin rectangular engine blocks at the stern, cargo containers bolted along the flanks, patched grey-brown plating.

**A001 / E46-001 — front three-quarter (DESIGN MASTER — no ref)**
```
[SHARED] Three-quarter front view of a long brick-shaped junky freighter floating in space. Elongated rectangular box hull, blunt flat nose with a small dark cockpit window strip, twin rectangular engine exhausts at the far stern, cargo container modules bolted along both flanks, dirty patched plating with mismatched panels and weld scars. Camera slightly low looking up at the nose and one long flank. Soft rim light from a distant sun. Distinct silhouette: long horizontal brick, not a saucer, not a claw.
```

**A002 / E46-002 — front (ref: A001)**
```
[SHARED] Same long brick junky freighter as the reference image — lock silhouette 1:1. Straight-on front view: blunt flat nose filling frame center, twin engine blocks visible at rear silhouette edges, cockpit window strip dark, dirty patched plating. Space background. Lock the brick proportions from the reference.
```
reference_image_paths: [<A001 asset>]

**A003 / E46-003 — rear (ref: A001)**
```
[SHARED] Same long brick junky freighter as the reference — lock silhouette 1:1. Straight-on rear view: twin rectangular engine exhausts glowing dull orange, cargo container ends on flanks, brick hull receding forward into space. Dirty patched plating. Lock brick proportions from the reference.
```
reference_image_paths: [<A001 asset>]

**A004 / E46-004 — port side (ref: A001)**
```
[SHARED] Same long brick junky freighter as the reference — lock silhouette 1:1. Full port-side profile: long horizontal brick from blunt nose (screen-left) to twin engines (screen-right), cargo containers along the flank, dirty patched plating. Camera level, whole ship in frame. Lock brick proportions from the reference.
```
reference_image_paths: [<A001 asset>]

**A005 / E46-005 — starboard side (ref: A001)**
```
[SHARED] Same long brick junky freighter as the reference — lock silhouette 1:1. Full starboard-side profile: engines screen-left, blunt nose screen-right (mirror of port), cargo containers along flank, dirty patched plating. Camera level, whole ship in frame. Lock brick proportions from the reference.
```
reference_image_paths: [<A001 asset>]

**A006 / E46-006 — top-ish (ref: A001)**
```
[SHARED] Same long brick junky freighter as the reference — lock silhouette 1:1. High three-quarter / top-down-ish view looking down on the dorsal spine: elongated rectangular planform, blunt nose, twin engine blocks at stern, cargo modules on flanks, dirty patched roof plating with antennae. Lock brick planform from the reference.
```
reference_image_paths: [<A001 asset>]

### Candidate B — saucer-with-boxes
Overall: round/oval central saucer hull with rectangular cargo boxes and scaffold modules welded on top and underside, short stubby engine cluster aft, mismatched grey plating.

**B001 / E46-007 — front three-quarter (DESIGN MASTER — no ref)**
```
[SHARED] Three-quarter front view of a saucer-with-boxes junky freighter floating in space. Round/oval central disc hull with rectangular cargo boxes and scaffold modules welded on top and underside, short stubby multi-engine cluster at the aft rim, small dark cockpit blister near the forward rim, dirty patched plating. Distinct silhouette: round saucer body with boxy add-ons — NOT a long brick, NOT a claw. Soft rim light.
```

**B002 / E46-008 — front (ref: B001)**
```
[SHARED] Same saucer-with-boxes junky freighter as the reference — lock silhouette 1:1. Straight-on front: round disc face, cargo boxes stacked on top, stubby engines peeking at rear silhouette, cockpit blister dark. Lock saucer-plus-boxes proportions from the reference.
```
reference_image_paths: [<B001 asset>]

**B003 / E46-009 — rear (ref: B001)**
```
[SHARED] Same saucer-with-boxes junky freighter as the reference — lock silhouette 1:1. Straight-on rear: stubby multi-engine cluster glowing dull blue-white, round disc rim, underside cargo boxes visible. Lock saucer-plus-boxes proportions from the reference.
```
reference_image_paths: [<B001 asset>]

**B004 / E46-010 — port side (ref: B001)**
```
[SHARED] Same saucer-with-boxes junky freighter as the reference — lock silhouette 1:1. Full port-side profile: round disc edge-on with cargo boxes stacked above and below the equator, stubby engines aft (screen-right), cockpit blister forward (screen-left). Lock saucer-plus-boxes proportions from the reference.
```
reference_image_paths: [<B001 asset>]

**B005 / E46-011 — starboard side (ref: B001)**
```
[SHARED] Same saucer-with-boxes junky freighter as the reference — lock silhouette 1:1. Full starboard-side profile: engines screen-left, cockpit blister screen-right, cargo boxes on dorsal and ventral. Lock saucer-plus-boxes proportions from the reference.
```
reference_image_paths: [<B001 asset>]

**B006 / E46-012 — top-ish (ref: B001)**
```
[SHARED] Same saucer-with-boxes junky freighter as the reference — lock silhouette 1:1. High three-quarter / top-down-ish: round disc planform with rectangular cargo boxes and scaffolds on the roof, stubby engine cluster at aft rim. Lock saucer planform from the reference.
```
reference_image_paths: [<B001 asset>]

### Candidate C — asymmetric claw
Overall: compact core with one long asymmetric claw/prong arm reaching forward on one side only, offset engine pod on the opposite flank, scavenged plating, unbalanced silhouette.

**C001 / E46-013 — front three-quarter (DESIGN MASTER — no ref)**
```
[SHARED] Three-quarter front view of an asymmetric claw junky freighter floating in space. Compact scavenged core hull with ONE long claw/prong arm reaching forward on the viewer's left (character-port), an offset engine pod on the opposite flank, dirty mismatched plating, small dark cockpit set into the core. Distinct silhouette: asymmetric — one long forward claw, NOT a brick, NOT a round saucer. Soft rim light.
```

**C002 / E46-014 — front (ref: C001)**
```
[SHARED] Same asymmetric claw junky freighter as the reference — lock silhouette 1:1. Straight-on front: long claw/prong extending toward camera on one side, compact core centered, offset engine pod on the other side. Lock the asymmetric claw proportions from the reference.
```
reference_image_paths: [<C001 asset>]

**C003 / E46-015 — rear (ref: C001)**
```
[SHARED] Same asymmetric claw junky freighter as the reference — lock silhouette 1:1. Straight-on rear: offset engine pod glowing, compact core, the long claw arm visible extending away on one side. Lock asymmetric proportions from the reference.
```
reference_image_paths: [<C001 asset>]

**C004 / E46-016 — port side (ref: C001)**
```
[SHARED] Same asymmetric claw junky freighter as the reference — lock silhouette 1:1. Full port-side profile emphasizing the long claw arm running forward (screen-left), compact core midships, engine pod aft. Lock asymmetric claw proportions from the reference.
```
reference_image_paths: [<C001 asset>]

**C005 / E46-017 — starboard side (ref: C001)**
```
[SHARED] Same asymmetric claw junky freighter as the reference — lock silhouette 1:1. Full starboard-side profile: engine pod prominent, claw arm on far side partially visible past the core. Lock asymmetric proportions from the reference.
```
reference_image_paths: [<C001 asset>]

**C006 / E46-018 — top-ish (ref: C001)**
```
[SHARED] Same asymmetric claw junky freighter as the reference — lock silhouette 1:1. High three-quarter / top-down-ish: compact core with one long claw arm extending forward on one side only, offset engine pod opposite — clear asymmetric planform. Lock from the reference.
```
reference_image_paths: [<C001 asset>]

### E46 z8save note templates (after parent generates)
```
python3 /workspace/enablers03/z8save.py E46-junky-ship <asset> "L- S# | candidate A front 3/4 design master | preserve: long brick silhouette, blunt nose, twin stern engines | A001"
# ... map 001-006=A, 007-012=B, 013-018=C in every note
```

---

## E47-warship — 15 images

Imposing capital warship, grey/dark hull, lit hangar bay mouths glowing. Expand beyond brief's "three angles": hull angles, hangar bay close-ups, fleet scale, approach. No franchise shapes (no Star Destroyer wedge / Venator). Empty space/nebula OK. No people.

Optional soft ref (scene craft only, not silhouette lock): prior C36 warship hulls under `/workspace/falcon1000/C36-warship-pass/` — prefer generating a NEW distinct capital hull so E47 is not a franchise wedge clone. Design master first, then ref it.

### SHARED constraints (append to every E47 prompt)
```
Photoreal cinematic concept still, 16:9. Empty deep space with faint nebula. NO people, NO fighters launching unless specified as tiny specs, NO franchise silhouettes (no triangular Star Destroyer wedge, no Venator), NO logos, NO readable hull text. Grey to dark gunmetal capital-ship plating, lit hangar bay mouths glowing pale amber/white from within. Prefer photographic finish. Imposing scale.
```

**E47-001 — design master, three-quarter bow (no ref)**
```
[SHARED] Large capital warship three-quarter bow view. Long dark-grey armoured hull with a broad flat-topped command superstructure amidships (NOT a triangular wedge), rows of lit hangar bay mouths glowing pale amber along the flank, subtle sensor towers. Camera slightly low looking up — imposing. Distinct original silhouette.
```

**E47-002 — port flank full (ref: 001)**
```
[SHARED] Same capital warship as the reference — lock hull design 1:1. Full port-side profile: long dark hull filling frame horizontally, band of lit hangar bay mouths glowing along the mid-flank, command superstructure amidships. Whole ship in frame. Lock silhouette from the reference.
```
reference_image_paths: [<E47-001 asset>]

**E47-003 — starboard flank (ref: 001)**
```
[SHARED] Same capital warship as the reference — lock hull 1:1. Full starboard-side profile, lit hangar bay mouths along mid-flank, command tower amidships. Lock from the reference.
```
reference_image_paths: [<E47-001 asset>]

**E47-004 — bow-on front (ref: 001)**
```
[SHARED] Same capital warship as the reference — lock hull 1:1. Straight-on bow view: broad armoured prow filling frame, hangar mouths visible as glow slits on flanks, superstructure rising behind. Lock from the reference.
```
reference_image_paths: [<E47-001 asset>]

**E47-005 — stern / engines (ref: 001)**
```
[SHARED] Same capital warship as the reference — lock hull 1:1. Rear three-quarter: massive engine banks glowing cool blue-white, dark hull receding forward, hangar glow visible on flank edge. Lock from the reference.
```
reference_image_paths: [<E47-001 asset>]

**E47-006 — hangar bay mouth close-up (ref: 001)**
```
[SHARED] Same capital warship as the reference — lock plating language. Extreme close-up of one lit hangar bay mouth: rectangular bay opening glowing pale amber from within, thick armoured surround, scuffed plating, no readable markings, empty bay (no ships visible inside). Macro scale of the hull.
```
reference_image_paths: [<E47-001 asset>]

**E47-007 — hangar bay row (ref: 001)**
```
[SHARED] Same capital warship as the reference — lock hull 1:1. Medium shot along the flank: a row of three to five lit hangar bay mouths glowing in sequence, dark plating between them, slight perspective recession. Lock plating from the reference.
```
reference_image_paths: [<E47-001 asset>]

**E47-008 — underside with hangar glow (ref: 001)**
```
[SHARED] Same capital warship as the reference — lock hull 1:1. Low angle looking up at the underbelly: dark ventral plating, hangar bay mouths glowing along the side edge, imposing mass overhead. Lock from the reference.
```
reference_image_paths: [<E47-001 asset>]

**E47-009 — dorsal / top three-quarter (ref: 001)**
```
[SHARED] Same capital warship as the reference — lock hull 1:1. High three-quarter looking down on the dorsal deck: command superstructure, sensor towers, flat armoured topside, hangar glow along the rim. Lock from the reference.
```
reference_image_paths: [<E47-001 asset>]

**E47-010 — approach / bow closing (ref: 001)**
```
[SHARED] Same capital warship as the reference — lock hull 1:1. Dramatic approach shot: camera racing toward the bow from ahead and slightly below, hull looming, hangar mouths starting to resolve as glowing slits, stars streaking faintly. Lock silhouette from the reference.
```
reference_image_paths: [<E47-001 asset>]

**E47-011 — fleet scale distant (ref: 001)**
```
[SHARED] Same capital warship design as the reference as the LEAD ship. Wide establishing: the warship mid-frame with two smaller escort silhouettes farther back (same design language, scaled down), nebula backdrop, tiny scale. Lead ship matches the reference hull. No franchise shapes.
```
reference_image_paths: [<E47-001 asset>]

**E47-012 — hangar interior mouth looking out (ref: 001)**
```
[SHARED] From inside an empty hangar bay of the same warship looking OUT through the bay mouth into space: thick armoured bay frame in foreground, pale amber interior bay light spill, stars beyond, dark empty deck — no people, no parked craft. Plating language matches the reference.
```
reference_image_paths: [<E47-001 asset>]

**E47-013 — flank lit by nearby star (ref: 001)**
```
[SHARED] Same capital warship as the reference — lock hull 1:1. Three-quarter midships: harsh white sunlight raking the dark plating, hangar mouths glowing in the shadow side, long hull perspective. Lock from the reference.
```
reference_image_paths: [<E47-001 asset>]

**E47-014 — passing above camera (ref: 001)**
```
[SHARED] Same capital warship as the reference — lock hull 1:1. Camera under the hull as the ship passes overhead: ventral plating filling the frame, hangar bay mouths glowing along one edge, sense of enormous mass and speed. Lock from the reference.
```
reference_image_paths: [<E47-001 asset>]

**E47-015 — distant silhouette against nebula (ref: 001)**
```
[SHARED] Same capital warship as the reference — lock silhouette 1:1. Far distant silhouette against a vivid nebula; hangar mouths as tiny glow points; whole ship small in frame for scale. Lock silhouette from the reference.
```
reference_image_paths: [<E47-001 asset>]

### E47 z8save note templates
```
python3 /workspace/enablers03/z8save.py E47-warship <asset> "L- S# | three-quarter bow design master | preserve: non-wedge capital hull, lit hangar mouths, dark grey plating"
```

---

## After all assets exist — executor (or parent) finish checklist
1. Save all 18 E46 + 15 E47 via z8save in order.
2. Write NOTES.md in each folder with A/B/C mapping and prelim scores.
3. `cd /workspace/enablers03/E46-junky-ship && sha256sum *.jpg > SHA256SUMS` (same for E47).
4. Report counts, A/B/C file ranges, best picks, NOTES paths.
