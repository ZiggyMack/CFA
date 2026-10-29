# CUR-DROP-20261009A: the Curator (cosmic avatar) handoff for Nova

From Ziggy to Nova. Built 2026-10-09 by Grok Bot. This is the first Nova drop for Ziggy's cosmic avatar, working name **"the Curator"** (the final name is not picked yet). It packs everything made for him so far: the character refs, the first turnaround/moods/settings run, the 50-scene orb/helmet set (with the proportion fixes), and the 75-frame storyboard of his five-arc saga with Lisan Al Gaib.

> **Nothing in this drop is approved.** Every file has one of these statuses: **KEEPER-candidate (needs_user_review)**, **DRAFT**, **SUPERSEDED** or **PROPOSAL**. Ziggy makes the final calls.

## 1. How to unpack

The drop is split into 4 zip parts, each under 24 MB. **Unzip all of them into the same folder** and they combine into `CUR-DROP-20261009A/`. Start with this README. `FILE_INDEX.csv` lists every file with its sha256, size, status, collection and zip part. Every collection folder has a `manifest.csv` (id, label, view, head, arc, story_beat, qa_note, status, file, sha256, source_path) and a labelled `_CONTACT_*.jpg` sheet for quick scanning.

| Part | Contents |
|---|---|
| part1of4 | Docs (this README, PDF, FILE_INDEX.csv), 01_CHARACTER_REFS, 02_TURNAROUND_MOODS_SETTINGS, 05_LISAN_SCENES, 90_SUPERSEDED |
| part2of4 | 03_SCENES_50_ORB_HELMET (25 scenes x 2 heads = 50) |
| part3of4 | 04_STORYBOARD_75: STORY-BIBLE.md, manifest.csv, Arcs 1-3 (45 frames) + contact sheets ARC1-3 |
| part4of4 | 04_STORYBOARD_75: Arcs 4-5 (30 frames) + contact sheets ARC4-5 |

## 2. The journey (what happened and what changed)

1. **Start.** Ziggy gave us one avatar image (`01_CHARACTER_REFS/CUR-REF-01`, cleaned to `CUR-REF-03_REF-CLEAN`, the design ground truth). Goal: flesh him out with a body, settings and scenes with Lisan Al Gaib. We wrote `CHARACTER.md` and `DESIGN-LOCK.txt`.
2. **First run (12 images, `02` + `05`).** Front/side/back, three settings (Observatory throne, desert galaxy night, noir city), five mood shots where the nebula head shifts, and the first meeting with Lisan. Some mood shots drifted off the suit (see section 6).
3. **Two interchangeable heads.** Ziggy liked the round **ORB** head and also the egg shape from the anger shot, the **EGG HELMET**. Both are now official, interchangeable head variants (`CUR-REF-04_HEAD-ORB`, `CUR-REF-05_HEAD-HELMET`).
4. **50-scene set (`03`).** 25 scenes, each rendered once with the orb head and once with the helmet, all in the black suit and tie.
5. **Proportion fix.** Ziggy flagged some renders as "too thick at the top" (bulky upper body). Scene 14 aurora (orb and helmet) and scene 07 moon (orb) were redone slim with normal proportions. The bulky v1s are in `90_SUPERSEDED`.
6. **Mentor saga + 75-frame storyboard (`04`).** Ziggy wants him as the saga's Gandalf-like wise figure. We wrote `STORY-BIBLE.md` (5 arcs, locations, artifacts) and made 15 frames per arc. Four frames were redone (ARC1-07 and ARC1-08 and ARC2-15 lost the suit; ARC4-06 gave Lisan the wrong face). The first versions are in `90_SUPERSEDED`.
7. **This drop.** Repackaged into Nova format with readable names. The generator hash (asset sha256) is kept in `source_path` for every image, so provenance survives the renames. Image bytes are unchanged (no re-encode).

## 3. Who he is (story background)

**Role:** the wise mentor of the saga, a Gandalf type. He is older than most stars, speaks rarely and in riddles, and guides rather than fights. When he does use big power it costs him: his nebula drains to **grey** and he has to rest in the dark (or in starlight) to refill.

**Powers:** the cube is a real pocket universe (store, step inside, pull out starlight, gravity, mass). Things near the cube orbit it, and he can slow or redirect them. The clenched star-fist holds a collapsed star (one punch is a small supernova, so he almost never throws it). Wayfinding: he reads the stars and can fold short doors between dark places.

**Personality:** calm, precise, dry, a gentleman detective older than the stars. His nebula gives his mood away. Caretaker, not conqueror, but a collector who struggles to let go.

**With Lisan Al Gaib:** part mentor, part uneasy ally. Lisan commands sand and worms; the Curator commands the sky. When Lisan looks into the head he sees possible futures, not his own face. Over the saga the Curator trains him, gives up his own light for him, and is brought back by Lisan's tear.

**Locations:** the Dune Sea (Lisan's homeland), the Sietch of Echoes (cliff city where voices of the past linger), the Glass Desert (sand fused to glass by an ancient star-fall), the Tomb of the First Worm, the Orrery Observatory (his home at the edge of space), the Celestial / Eclipse Court, the Moon, the Void Gate (a tear in the sky where celestial threats come through).

**Artifacts:** Shards of the Cube (pieces of his pocket universe), the Worm's Eye (pearl of the First Worm, shows the future), the Star Compass (points to dying stars), the Sun-Disc Amulet (matches the eye-sun on Lisan's throat, unlocks his destiny), the Lantern of First Dawn (holds the first light ever made).

**Celestial threats:** the Star-Eater (a devourer that swallows stars) and its herald and void swarm; the Moon-King, who betrays the court and rides the void serpent.

| Arc | Title | Locations | Story |
|---|---|---|---|
| 1 | The Falling Shard | Dune Sea, crater, Sietch of Echoes | A cube shard falls; Lisan finds it; the Curator arrives, calms a worm, meets the elders, gives the first lesson; first glimpse of the Star-Eater |
| 2 | The Tomb of the First Worm | Glass Desert, worm-fossil canyon, the Tomb | Journey to claim the Worm's Eye; Lisan's sun tattoo opens the door; the Curator burns out grey and Lisan carries him home |
| 3 | The Star-Eater | Orrery Observatory, starlight bridge, a dying world | Star Compass; battle with the void swarm and the herald; the Worm's Eye shows the beast's weak heart; the star is reborn; the Star-Eater retreats |
| 4 | The Eclipse Court | Eclipse portal, Celestial Court, the Moon | Diplomacy with the Sun-Queen and Moon-King; the Curator pledges his cube; the Sun-Disc Amulet awakens Lisan; Moon-King betrays them; the Void Gate opens over home |
| 5 | The Last Light | Void Gate over the Dune Sea, the Observatory | Final battle; the Curator pours his light into the Lantern of First Dawn and falls; Lisan raises the Lantern; the Star-Eater dissolves; Lisan's tear reignites him; rebirth and reunion |

## 4. Locked character rules (check every new render against these)

- **Build: slim, tall, normal proportions.** Not bulky or "too thick at the top". This was Ziggy's explicit correction.
- **Suit:** matte black single-breasted suit, black shirt, **black tie** with **two small glowing orange glyph pins** stacked vertically on the tie (do not change the count). The dark under the collar is starfield, not skin.
- **Shoulders:** segmented **cyan LED trim** along the shoulder seams.
- **Hands:** **left hand = clenched fist made of starfield/nebula glass**; **right hand = black-gloved**.
- **Galaxy cube:** a clear glass cube with bright edges holding a miniature solar system (orange sun, planets, spiral galaxy). It **floats beside his right hand**; he never holds it (story beats like the pledge and the Lantern are deliberate exceptions).
- **Two interchangeable heads** (both faceless glass, nebula inside, thin teal rim light, no eyes/mouth/visor):
  - **ORB:** round glass sphere (`CUR-REF-04_HEAD-ORB`).
  - **EGG HELMET:** taller egg-shaped glass helmet, closest to the original art (`CUR-REF-05_HEAD-HELMET`, use for head shape only).
- **Mood colours (nebula "weather"):** calm = cool blue/teal; wonder/curiosity = violet galaxy; amused = gold flare; anger = stormy red; drained = **grey**.
- **Power drains him grey.** Big power use fades the nebula to grey (ARC2-14, ARC5-11 show this on purpose).
- Palette: black, deep navy/violet space, amber/orange nebula, cyan accents. Cinematic, photoreal.
- Do not: add a face, colour the suit, add logos, change the tie-pin count.

Lisan Al Gaib follows his own lock (LOCK-V2, natural teeth, no grill); his tattoos are not consistent in this drop (section 6).

## 5. Counts

| Collection | Images | Notes |
|---|---|---|
| 01_CHARACTER_REFS | 5 | Original art, clean ref, head refs + CHARACTER.md, DESIGN-LOCK.txt, first-run prompts |
| 02_TURNAROUND_MOODS_SETTINGS | 11 | 3 views, 3 settings, 5 moods |
| 03_SCENES_50_ORB_HELMET | 50 | 25 scenes x (orb + helmet). Includes 3 v2 proportion fixes |
| 04_STORYBOARD_75 | 75 | 5 arcs x 15 frames + STORY-BIBLE.md. 74 KEEPER-candidate, 1 DRAFT (ARC5-14) |
| 05_LISAN_SCENES | 1 | First meeting. Lisan also appears in scenes 09 and 16 (03) and throughout 04 |
| 90_SUPERSEDED | 7 | 3 bulky-proportion scene v1s + 4 replaced storyboard drafts |
| **Total images** | **149** | 2 of them are byte-identical duplicates by design (HEAD-ORB = TURN-01, HEAD-HELMET = MOOD-02) |

## 6. Known drift and failures (honest list)

- **ARC5-14 REUNION: DRAFT, needs a redo.** Lisan's face came out too soft / feminized.
- **ARC5-13 REBIRTH used the ORB head**, not the planned helmet. Ziggy to say if that's fine.
- **Lisan's tattoos are inconsistent** across shots (scenes 09/16, the Lisan meeting, many storyboard frames). Ziggy accepted them "for posterity", but do not use these frames as a Lisan tattoo reference.
- **Head and suit read loosely in some frames.** Head shape sometimes sits between orb and egg; in some storyboard frames the tie pins, cyan trim or star-fist are small, hidden or soft. Head tags in the manifests come from a thumbnail review (`none (not in frame)` where he isn't shown).
- **First-run mood shots are off-suit:** MOOD-01 calm, MOOD-02 anger and MOOD-03 wonder wear a high-collar tech/armoured jacket with no visible tie; MOOD-05 is a glowing bodysuit figure. They show the mood colours, not the outfit.
- **TURN-02 SIDE** reads three-quarter rather than true profile; **TURN-03 BACK** is ambiguous at small size. No clean slim turnaround in the final suit exists yet.
- **Proportions:** only scene 07 orb and scene 14 orb/helmet were redone. The other 47 scene images passed a thumbnail check but were not each re-measured for "too thick at the top".
- `CHARACTER.md` lists planned file paths (`-02-side.png`, `settings/...png`) that were never created under those names; the images are the `02` files here. `turnaround/COSMIC-TURN-01-front.png` on the box is actually JPEG data (same bytes as TURN-01).
- `DESIGN-LOCK.txt` was written before the orb/helmet split and only describes the egg head. Section 4 above is the current rule set.

## 7. Pending decisions (Ziggy)

1. **Final name.** Working name "the Curator". Other ideas in CHARACTER.md: Orrery, Mr. Nebula / Neb, the Keeper of the Cube, Ziggurat.
2. **ARC5-14 reunion redo** (fix Lisan's face).
3. Orb vs helmet for ARC5-13 rebirth, and whether either head should be the default for the saga.
4. Which images to promote from KEEPER-candidate. Nothing is approved yet.
5. Optional: a clean slim full turnaround (front/side/back) in the final suit for both heads, and a Lisan-tattoo-correct pass on the Lisan frames.

## 8. Per-image mapping

Paths are relative to `CUR-DROP-20261009A/`. Full sha256 and source paths are in `FILE_INDEX.csv` and each `manifest.csv`.

### 01_CHARACTER_REFS (part 1)
| File | Head | Note | Status |
|---|---|---|---|
| CUR-REF-01_ORIGINAL-SCREENSHOT.png | helmet (original egg) | Input from Ziggy | KEEPER-candidate |
| CUR-REF-02_ORIGINAL-1024.jpg | helmet (original egg) | Downscale of CUR-REF-01 | KEEPER-candidate |
| CUR-REF-03_REF-CLEAN.jpg | helmet (original egg) | Design ground truth | KEEPER-candidate |
| CUR-REF-04_HEAD-ORB.jpg | orb | Interchangeable head A | KEEPER-candidate |
| CUR-REF-05_HEAD-HELMET.jpg | helmet | Interchangeable head B; image shows anger mood and armoured jacket, so use it for HEAD SHAPE only | KEEPER-candidate |

Also in 01 (part 1): `CHARACTER.md`, `DESIGN-LOCK.txt`, `PROMPTS-FIRST-RUN.jsonl` (PROPOSAL).

### 02_TURNAROUND_MOODS_SETTINGS (part 1)
| File | View | Head | Note | Status |
|---|---|---|---|---|
| CUR-TURN-01_FRONT-ORB.jpg | full-body front | orb | First render. Same bytes as refs/HEAD-ORB.jpg and turnaround/COSMIC-TURN-01-front.png (that file is actually JPEG data). Suit, tie, pins, cube OK | KEEPER-candidate |
| CUR-TURN-02_SIDE.jpg | full-body side / three-quarter | orb | Reads three-quarter more than true 90-degree profile | KEEPER-candidate |
| CUR-TURN-03_BACK.jpg | full-body back | orb | Back view reads ambiguous at small size; cyan fist glow visible | KEEPER-candidate |
| CUR-SET-01_OBSERVATORY-THRONE.jpg | wide | orb | Setting: his Orrery Observatory throne room | KEEPER-candidate |
| CUR-SET-02_DESERT-GALAXY-NIGHT.jpg | wide | orb | Setting: Dune Sea under the galaxy | KEEPER-candidate |
| CUR-SET-03_NOIR-CITY.jpg | wide | orb | Setting: rain-soaked noir city; wears an overcoat over the suit | KEEPER-candidate |
| CUR-MOOD-01_CALM-BLUE.jpg | chest-up | orb | Mood: calm (cool blue/teal nebula). DRIFT: outfit reads as a high-collar tech jacket with cyan piping, no visible tie | KEEPER-candidate |
| CUR-MOOD-02_ANGER-RED.jpg | chest-up | helmet | Mood: anger (stormy red nebula). Origin of the EGG HELMET head (same bytes as refs/HEAD-HELMET.jpg). DRIFT: armoured jacket, not suit and tie | KEEPER-candidate |
| CUR-MOOD-03_WONDER-VIOLET.jpg | chest-up | orb | Mood: wonder/curiosity (violet spiral galaxy). DRIFT: tech jacket, no visible tie | KEEPER-candidate |
| CUR-MOOD-04_DRAINED-GREY.jpg | chest-up | orb | Mood: drained after big power use (nebula gone grey). Black overcoat over the suit | KEEPER-candidate |
| CUR-MOOD-05_TRANSCENDENT-INSIDE-CUBE.jpg | wide | orb | Mood/power: him inside his own cube universe, golden glow. DRIFT: no suit (glowing bodysuit figure) | KEEPER-candidate |

### 03_SCENES_50_ORB_HELMET (part 2)
| File | Head | Scene | QA | Status |
|---|---|---|---|---|
| CUR-SCENE-01_ORB-CHESS-OVER-CITY.jpg | orb | Rooftop chess game with planet pieces above a night city | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-01_HELMET-CHESS-OVER-CITY.jpg | helmet | Rooftop chess game with planet pieces above a night city | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-02_ORB-JAR-LIBRARY.jpg | orb | Library of bottled galaxies; he shelves a jar | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-02_HELMET-JAR-LIBRARY.jpg | helmet | Library of bottled galaxies; he shelves a jar | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-03_ORB-DESERT-TRAIN-DINING-CAR.jpg | orb | Dining car of a night train crossing the desert, moon outside | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-03_HELMET-DESERT-TRAIN-DINING-CAR.jpg | helmet | Dining car of a night train crossing the desert, moon outside | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-04_ORB-JAZZ-PIANO.jpg | orb | Playing piano in a smoky jazz club | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-04_HELMET-JAZZ-PIANO.jpg | helmet | Playing piano in a smoky jazz club | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-05_ORB-BLACK-HOLE-WALK.jpg | orb | Walking out of an accretion disk / black hole | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-05_HELMET-BLACK-HOLE-WALK.jpg | helmet | Walking out of an accretion disk / black hole | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-06_ORB-WATCHMAKER-WORKSHOP.jpg | orb | Repairing tiny clockwork at a watchmaker bench | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-06_HELMET-WATCHMAKER-WORKSHOP.jpg | helmet | Repairing tiny clockwork at a watchmaker bench | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-07_ORB-MOON-SURFACE.jpg | orb | Standing on the Moon with Earth behind | v2 proportion fix (slim, normal build); v1 bulky version in 90_SUPERSEDED | KEEPER-candidate |
| CUR-SCENE-07_HELMET-MOON-SURFACE.jpg | helmet | Standing on the Moon with Earth behind | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-08_ORB-DEEP-SEA.jpg | orb | Walking the deep-sea floor among jellyfish | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-08_HELMET-DEEP-SEA.jpg | helmet | Walking the deep-sea floor among jellyfish | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-09_ORB-WORM-RIDE-WITH-LISAN.jpg | orb | Riding a sandworm with Lisan at golden hour | ok at thumbnail level (suit, tie, cube present); Lisan in shot, tattoos not matched to Lisan lock | KEEPER-candidate |
| CUR-SCENE-09_HELMET-WORM-RIDE-WITH-LISAN.jpg | helmet | Riding a sandworm with Lisan at golden hour | ok at thumbnail level (suit, tie, cube present); Lisan in shot, tattoos not matched to Lisan lock | KEEPER-candidate |
| CUR-SCENE-10_ORB-NEON-CROSSWALK.jpg | orb | Crossing a rainy neon crosswalk in a crowd | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-10_HELMET-NEON-CROSSWALK.jpg | helmet | Crossing a rainy neon crosswalk in a crowd | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-11_ORB-CATHEDRAL.jpg | orb | Stained-glass galaxy cathedral | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-11_HELMET-CATHEDRAL.jpg | helmet | Stained-glass galaxy cathedral | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-12_ORB-STORM-PEAK.jpg | orb | Mountain peak in a lightning storm, holding the storm in his hand | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-12_HELMET-STORM-PEAK.jpg | helmet | Mountain peak in a lightning storm, holding the storm in his hand | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-13_ORB-NIGHT-BAZAAR.jpg | orb | Night bazaar stall of glass orbs | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-13_HELMET-NIGHT-BAZAAR.jpg | helmet | Night bazaar stall of glass orbs | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-14_ORB-AURORA-FOREST.jpg | orb | Snowy forest under the aurora | v2 proportion fix (slim, normal build); v1 bulky version in 90_SUPERSEDED | KEEPER-candidate |
| CUR-SCENE-14_HELMET-AURORA-FOREST.jpg | helmet | Snowy forest under the aurora | v2 proportion fix (slim, normal build); v1 bulky version in 90_SUPERSEDED | KEEPER-candidate |
| CUR-SCENE-15_ORB-GALAXY-RIFT-OVER-CITY.jpg | orb | Tearing open a galaxy rift over a city skyline | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-15_HELMET-GALAXY-RIFT-OVER-CITY.jpg | helmet | Tearing open a galaxy rift over a city skyline | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-16_ORB-CAMPFIRE-WITH-LISAN.jpg | orb | Campfire talk with Lisan under the stars | ok at thumbnail level (suit, tie, cube present); Lisan in shot, tattoos not matched to Lisan lock | KEEPER-candidate |
| CUR-SCENE-16_HELMET-CAMPFIRE-WITH-LISAN.jpg | helmet | Campfire talk with Lisan under the stars | ok at thumbnail level (suit, tie, cube present); Lisan in shot, tattoos not matched to Lisan lock | KEEPER-candidate |
| CUR-SCENE-17_ORB-PYRAMIDS-CONSTELLATION.jpg | orb | Pyramids at night, tracing constellations | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-17_HELMET-PYRAMIDS-CONSTELLATION.jpg | helmet | Pyramids at night, tracing constellations | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-18_ORB-GALAXY-ROULETTE-CASINO.jpg | orb | Casino table with a galaxy roulette wheel | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-18_HELMET-GALAXY-ROULETTE-CASINO.jpg | helmet | Casino table with a galaxy roulette wheel | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-19_ORB-OPERA-BOX.jpg | orb | Private opera box, cosmic stage | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-19_HELMET-OPERA-BOX.jpg | helmet | Private opera box, cosmic stage | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-20_ORB-ECLIPSE-SUNFLOWERS.jpg | orb | Sunflower field under an eclipse | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-20_HELMET-ECLIPSE-SUNFLOWERS.jpg | helmet | Sunflower field under an eclipse | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-21_ORB-LIGHTHOUSE-WORLD-EDGE.jpg | orb | Lighthouse at the edge of the world; cube beams like a lamp | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-21_HELMET-LIGHTHOUSE-WORLD-EDGE.jpg | helmet | Lighthouse at the edge of the world; cube beams like a lamp | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-22_ORB-FLOATING-ISLANDS.jpg | orb | Walking floating islands in a nebula | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-22_HELMET-FLOATING-ISLANDS.jpg | helmet | Walking floating islands in a nebula | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-23_ORB-SUBWAY-NEWSPAPER.jpg | orb | Reading a newspaper on a subway through space | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-23_HELMET-SUBWAY-NEWSPAPER.jpg | helmet | Reading a newspaper on a subway through space | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-24_ORB-WORMHOLE-TUNNEL.jpg | orb | Walking through a blue wormhole tunnel | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-24_HELMET-WORMHOLE-TUNNEL.jpg | helmet | Walking through a blue wormhole tunnel | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-25_ORB-GIANT-CUBE-OVER-PLANET.jpg | orb | Standing inside a giant cube above a planet | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |
| CUR-SCENE-25_HELMET-GIANT-CUBE-OVER-PLANET.jpg | helmet | Standing inside a giant cube above a planet | ok at thumbnail level (suit, tie, cube present) | KEEPER-candidate |


### 04_STORYBOARD_75, Arc 1: The Falling Shard (part 3)

Locations: Dune Sea, crash crater, Sietch of Echoes.

| # | File | Shot | Head | Story beat | QA | Status |
|---|---|---|---|---|---|---|
| 01 | CUR-SB-ARC1-01_SHARD-FALLS.jpg | wide | none (not in frame) | A shard of his cube streaks across the night sky and falls into the Dune Sea | ok at thumbnail level | KEEPER-candidate |
| 02 | CUR-SB-ARC1-02_LISAN-FINDS-CRATER.jpg | medium | none (not in frame) | Lisan finds the glowing shard in a fresh crater | ok at thumbnail level | KEEPER-candidate |
| 03 | CUR-SB-ARC1-03_SHARD-CLOSEUP.jpg | close-up | none (not in frame) | Close-up: Lisan holds the shard, a galaxy inside it | ok at thumbnail level | KEEPER-candidate |
| 04 | CUR-SB-ARC1-04_CURATOR-MATERIALIZES.jpg | medium | orb | The Curator materializes out of the sand storm | ok at thumbnail level | KEEPER-candidate |
| 05 | CUR-SB-ARC1-05_STANDOFF.jpg | medium | helmet | Standoff: Lisan with the shard vs the faceless stranger | ok at thumbnail level | KEEPER-candidate |
| 06 | CUR-SB-ARC1-06_VISION-IN-ORB.jpg | medium | orb | Lisan sees a vision inside the orb head | ok at thumbnail level | KEEPER-candidate |
| 07 | CUR-SB-ARC1-07_WORM-ATTACK.jpg | wide | orb | A sandworm attacks; the Curator shields Lisan | v2: redo with suit restored (v1 lost the suit, see 90_SUPERSEDED) | KEEPER-candidate |
| 08 | CUR-SB-ARC1-08_CALMING-THE-WORM.jpg | wide | orb | He calms the worm with orbiting rings of light | v2: redo with suit restored (v1 lost the suit, see 90_SUPERSEDED) | KEEPER-candidate |
| 09 | CUR-SB-ARC1-09_WALK-TO-SIETCH.jpg | wide | orb | The two walk to the Sietch of Echoes | ok at thumbnail level | KEEPER-candidate |
| 10 | CUR-SB-ARC1-10_SIETCH-ELDERS.jpg | medium | helmet | He meets the sietch elders | ok at thumbnail level | KEEPER-candidate |
| 11 | CUR-SB-ARC1-11_STAR-LESSON.jpg | medium | orb | Star lesson: he teaches Lisan the constellations | ok at thumbnail level | KEEPER-candidate |
| 12 | CUR-SB-ARC1-12_SHARD-MAP.jpg | close-up | none (not in frame) | The shard projects a map of the other scattered shards | Curator only implied (hand/shard); head not in frame | KEEPER-candidate |
| 13 | CUR-SB-ARC1-13_CUBE-HEALED.jpg | medium | orb | The shard rejoins and heals the cube | ok at thumbnail level | KEEPER-candidate |
| 14 | CUR-SB-ARC1-14_STAR-EATER-GLIMPSED.jpg | wide | orb (tiny) | First glimpse of the Star-Eater darkening the sky | ok at thumbnail level | KEEPER-candidate |
| 15 | CUR-SB-ARC1-15_DAWN-DEPARTURE.jpg | wide | orb | They depart together at dawn | ok at thumbnail level | KEEPER-candidate |

### 04_STORYBOARD_75, Arc 2: The Tomb of the First Worm (part 3)

Locations: The Glass Desert, worm-fossil canyon, the Tomb, the pearl cavern.

| # | File | Shot | Head | Story beat | QA | Status |
|---|---|---|---|---|---|---|
| 01 | CUR-SB-ARC2-01_GLASS-DESERT.jpg | wide | orb | Crossing the Glass Desert | ok at thumbnail level | KEEPER-candidate |
| 02 | CUR-SB-ARC2-02_GLASS-STORM-SHIELD.jpg | medium | helmet | He raises a bubble shield against a glass-shard storm | ok at thumbnail level | KEEPER-candidate |
| 03 | CUR-SB-ARC2-03_RAIDER-AMBUSH.jpg | medium | orb | Raiders ambush them | ok at thumbnail level | KEEPER-candidate |
| 04 | CUR-SB-ARC2-04_STAR-FLARE.jpg | medium | orb | He blinds the raiders with a star-flare | ok at thumbnail level | KEEPER-candidate |
| 05 | CUR-SB-ARC2-05_WORM-FOSSIL-RIBS.jpg | wide | orb | Walking through the ribs of a worm fossil | ok at thumbnail level | KEEPER-candidate |
| 06 | CUR-SB-ARC2-06_TOMB-ENTRANCE.jpg | wide | orb | The tomb entrance | ok at thumbnail level | KEEPER-candidate |
| 07 | CUR-SB-ARC2-07_STAR-DIAL-DOOR.jpg | medium | helmet | The star-dial door | ok at thumbnail level | KEEPER-candidate |
| 08 | CUR-SB-ARC2-08_SUN-TATTOO-UNLOCK.jpg | close-up | none (not in frame) | Lisan unlocks the door with his sun-disc tattoo | ok at thumbnail level | KEEPER-candidate |
| 09 | CUR-SB-ARC2-09_PEARL-CAVERN.jpg | wide | orb | The pearl cavern of stars | ok at thumbnail level | KEEPER-candidate |
| 10 | CUR-SB-ARC2-10_GUARDIAN-WORM-SPIRIT.jpg | wide | orb | The guardian worm spirit rises | ok at thumbnail level | KEEPER-candidate |
| 11 | CUR-SB-ARC2-11_KING-VISION.jpg | medium | none (not in frame) | Lisan sees himself as king | ok at thumbnail level | KEEPER-candidate |
| 12 | CUR-SB-ARC2-12_WORMS-EYE-PEARL.jpg | close-up | orb | The Worm's Eye pearl, held out in the Curator's hands | ok at thumbnail level | KEEPER-candidate |
| 13 | CUR-SB-ARC2-13_TOMB-COLLAPSE.jpg | medium | helmet | The tomb collapses as they escape | ok at thumbnail level | KEEPER-candidate |
| 14 | CUR-SB-ARC2-14_GREY-BURNOUT.jpg | wide | orb (grey, drained) | The Curator burned out: kneeling, nebula gone grey | Grey nebula is intentional (power drain lore) | KEEPER-candidate |
| 15 | CUR-SB-ARC2-15_CARRIED-HOME.jpg | medium | orb | Lisan carries him home at sunset | v2: redo with suit restored (v1 lost the suit, see 90_SUPERSEDED) | KEEPER-candidate |

### 04_STORYBOARD_75, Arc 3: The Star-Eater (part 3)

Locations: The Orrery Observatory, the starlight bridge, a dying world.

| # | File | Shot | Head | Story beat | QA | Status |
|---|---|---|---|---|---|---|
| 01 | CUR-SB-ARC3-01_OBSERVATORY.jpg | wide | none (not in frame) | Establishing: the floating Orrery Observatory | ok at thumbnail level | KEEPER-candidate |
| 02 | CUR-SB-ARC3-02_ORRERY-HALL.jpg | medium | orb | The giant orrery hall; Lisan arrives | ok at thumbnail level | KEEPER-candidate |
| 03 | CUR-SB-ARC3-03_STARLIGHT-RECHARGE.jpg | wide | orb | The Curator recharges in a column of starlight | ok at thumbnail level | KEEPER-candidate |
| 04 | CUR-SB-ARC3-04_STAR-COMPASS.jpg | close-up | none (not in frame) | The Star Compass in its case | Only the gloved hand is in frame | KEEPER-candidate |
| 05 | CUR-SB-ARC3-05_COMPASS-LESSON.jpg | medium | orb | Lisan's first lesson with the compass | ok at thumbnail level | KEEPER-candidate |
| 06 | CUR-SB-ARC3-06_STAR-EATER-FEEDS.jpg | wide | unclear (silhouette) | The Star-Eater feeds on a red giant | ok at thumbnail level | KEEPER-candidate |
| 07 | CUR-SB-ARC3-07_STARLIGHT-BRIDGE.jpg | wide | orb | Running across the starlight bridge | ok at thumbnail level | KEEPER-candidate |
| 08 | CUR-SB-ARC3-08_DYING-WORLD.jpg | wide | helmet | Arriving on a dying world | ok at thumbnail level | KEEPER-candidate |
| 09 | CUR-SB-ARC3-09_VOID-SWARM.jpg | wide | none (not in frame) | Lisan fights the void swarm | ok at thumbnail level | KEEPER-candidate |
| 10 | CUR-SB-ARC3-10_PLANET-RING-SWEEP.jpg | medium | orb | He sweeps the swarm with a planet ring | ok at thumbnail level | KEEPER-candidate |
| 11 | CUR-SB-ARC3-11_HERALD-DUEL.jpg | medium | orb | Duel with the Star-Eater's herald | ok at thumbnail level | KEEPER-candidate |
| 12 | CUR-SB-ARC3-12_WORMS-EYE-WEAKNESS.jpg | close-up | none (not in frame) | The Worm's Eye reveals the beast's weak heart | ok at thumbnail level | KEEPER-candidate |
| 13 | CUR-SB-ARC3-13_COMBINED-STRIKE.jpg | medium | orb | Combined strike: Lisan and the Curator together | ok at thumbnail level | KEEPER-candidate |
| 14 | CUR-SB-ARC3-14_STAR-REBORN.jpg | medium | helmet | The star is reborn; the people watch | ok at thumbnail level | KEEPER-candidate |
| 15 | CUR-SB-ARC3-15_STAR-EATER-RETREATS.jpg | wide | orb (tiny) | The Star-Eater retreats, to return later | ok at thumbnail level | KEEPER-candidate |

### 04_STORYBOARD_75, Arc 4: The Eclipse Court (part 4)

Locations: The eclipse portal, the Celestial Court, the Moon.

| # | File | Shot | Head | Story beat | QA | Status |
|---|---|---|---|---|---|---|
| 01 | CUR-SB-ARC4-01_ECLIPSE-PORTAL.jpg | wide | orb | Walking into the eclipse portal on the dunes | ok at thumbnail level | KEEPER-candidate |
| 02 | CUR-SB-ARC4-02_CELESTIAL-COURT.jpg | wide | orb | The Celestial Court | ok at thumbnail level | KEEPER-candidate |
| 03 | CUR-SB-ARC4-03_CURATOR-WARNING.jpg | medium | orb | The Curator warns the court about the Star-Eater | ok at thumbnail level | KEEPER-candidate |
| 04 | CUR-SB-ARC4-04_SUN-QUEEN.jpg | wide | none (not in frame) | The Sun-Queen | ok at thumbnail level | KEEPER-candidate |
| 05 | CUR-SB-ARC4-05_MOON-KING.jpg | wide | none (not in frame) | The Moon-King | ok at thumbnail level | KEEPER-candidate |
| 06 | CUR-SB-ARC4-06_TRIAL.jpg | wide | none (not in frame) | Lisan's trial in the circle of judges | v2: redo; v1 gave Lisan the wrong face (see 90_SUPERSEDED). Curator not in frame | KEEPER-candidate |
| 07 | CUR-SB-ARC4-07_PLEDGE-OF-CUBE.jpg | medium | orb | The Curator kneels and pledges his cube | ok at thumbnail level | KEEPER-candidate |
| 08 | CUR-SB-ARC4-08_AMULET-GIVEN.jpg | close-up | none (not in frame) | The Sun-Disc Amulet is handed down | ok at thumbnail level | KEEPER-candidate |
| 09 | CUR-SB-ARC4-09_AMULET-AWAKENS-LISAN.jpg | close-up | none (not in frame) | The amulet awakens Lisan | ok at thumbnail level | KEEPER-candidate |
| 10 | CUR-SB-ARC4-10_COURT-BOWS.jpg | wide | orb | The court bows to Lisan | ok at thumbnail level | KEEPER-candidate |
| 11 | CUR-SB-ARC4-11_MOON-KING-BETRAYAL.jpg | medium | orb | The Moon-King's betrayal | ok at thumbnail level | KEEPER-candidate |
| 12 | CUR-SB-ARC4-12_ESCAPE.jpg | medium | orb | Escape from the court through fire | ok at thumbnail level | KEEPER-candidate |
| 13 | CUR-SB-ARC4-13_MOON-LANDING.jpg | wide | orb | Crash-landing on the Moon | ok at thumbnail level | KEEPER-candidate |
| 14 | CUR-SB-ARC4-14_FIRESIDE-TRUTH.jpg | medium | orb | Fireside truth: the Curator tells Lisan what is coming | ok at thumbnail level | KEEPER-candidate |
| 15 | CUR-SB-ARC4-15_VOID-GATE-OVER-HOME.jpg | wide | orb | The Void Gate opens over home | ok at thumbnail level | KEEPER-candidate |

### 04_STORYBOARD_75, Arc 5: The Last Light (part 4)

Locations: The Void Gate above the Dune Sea, the battlefield, the Observatory.

| # | File | Shot | Head | Story beat | QA | Status |
|---|---|---|---|---|---|---|
| 01 | CUR-SB-ARC5-01_RALLY.jpg | medium | orb | Lisan rallies the Fremen army, the Curator at his side | ok at thumbnail level | KEEPER-candidate |
| 02 | CUR-SB-ARC5-02_STAR-EATER-RISES.jpg | wide | none (not in frame) | The Star-Eater rises through the Void Gate | ok at thumbnail level | KEEPER-candidate |
| 03 | CUR-SB-ARC5-03_WORM-RIDER-CHARGE.jpg | wide | none (not in frame) | Worm-rider charge | ok at thumbnail level | KEEPER-candidate |
| 04 | CUR-SB-ARC5-04_PLANET-DOME-SHIELD.jpg | wide | orb | The Curator holds a planet-dome shield over the army | ok at thumbnail level | KEEPER-candidate |
| 05 | CUR-SB-ARC5-05_MOON-KING-SERPENT.jpg | wide | none (not in frame) | The Moon-King rides the void serpent | ok at thumbnail level | KEEPER-candidate |
| 06 | CUR-SB-ARC5-06_LANTERN-OF-FIRST-DAWN.jpg | close-up | none (not in frame) | The Lantern of First Dawn revealed (cube-lantern in his gloved hand) | Only his gloved hand with cyan trim is in frame | KEEPER-candidate |
| 07 | CUR-SB-ARC5-07_CURATOR-GIVES-HIS-LIGHT.jpg | medium | orb | The Curator pours his light into the Lantern | ok at thumbnail level | KEEPER-candidate |
| 08 | CUR-SB-ARC5-08_CURATOR-FALLS.jpg | wide | orb | He falls from the sky; Lisan catches the Lantern | ok at thumbnail level | KEEPER-candidate |
| 09 | CUR-SB-ARC5-09_LISAN-RAISES-LANTERN.jpg | medium | none (not in frame) | Lisan raises the Lantern; the dawn beam hits the Star-Eater | ok at thumbnail level | KEEPER-candidate |
| 10 | CUR-SB-ARC5-10_STAR-EATER-DISSOLVES.jpg | wide | none (not in frame) | The Star-Eater dissolves in the dawn | ok at thumbnail level | KEEPER-candidate |
| 11 | CUR-SB-ARC5-11_GRIEF.jpg | wide | orb (grey, drained) | Grief: Lisan holds the grey, fallen Curator | Grey nebula is intentional (he gave his light) | KEEPER-candidate |
| 12 | CUR-SB-ARC5-12_TEAR-REIGNITES-ORB.jpg | close-up | orb (extreme close-up) | A tear reignites the orb | ok at thumbnail level | KEEPER-candidate |
| 13 | CUR-SB-ARC5-13_REBIRTH.jpg | wide | orb | Rebirth: the Curator stands again | Planned as helmet; came out ORB. Head choice for rebirth beat is open | KEEPER-candidate |
| 14 | CUR-SB-ARC5-14_REUNION.jpg | medium | orb | Reunion with Lisan and the people | DRAFT: Lisan's face came out too soft / feminized. Needs redo | DRAFT |
| 15 | CUR-SB-ARC5-15_OBSERVATORY-FINAL.jpg | wide | orb | Final: the two at the Observatory looking out at the stars | ok at thumbnail level | KEEPER-candidate |

### 05_LISAN_SCENES (part 1)
| File | Head | Beat | Note | Status |
|---|---|---|---|---|
| CUR-LAG-01_DESERT-MEETING.jpg | orb | First meeting of the Curator and Lisan | First meeting with Lisan Al Gaib on night dunes; he offers the cube. Lisan tattoos not checked against Lisan lock | KEEPER-candidate |

### 90_SUPERSEDED (part 1)
| File | Why | Status |
|---|---|---|
| CUR-SCENE-07_ORB-MOON-SURFACE_v1-BULKY_cc0e4d27d27ef3f05c2fd7650bb7824c1b8840fd5946f34a38b7b64332888af1.jpg | Scene 07 moon, orb head, v1: too thick/bulky at the top. Replaced by CUR-SCENE-07_ORB-MOON-SURFACE (v2, 083c1c99) | SUPERSEDED |
| CUR-SCENE-14_ORB-AURORA-FOREST_v1-BULKY_1bc0725e4df31f4243791d0ae94b4ac18dea471ad0e00d700207321d1ed673a4.jpg | Scene 14 aurora, orb head, v1: too thick/bulky at the top. Replaced by v2 (9adc3c04) | SUPERSEDED |
| CUR-SCENE-14_HELMET-AURORA-FOREST_v1-BULKY_48e6cc177dbdb50c559e8223945f8ec1274ebf80e26c40854d16b763d42e06f5.jpg | Scene 14 aurora, helmet head, v1: too thick/bulky at the top. Replaced by v2 (7395c055) | SUPERSEDED |
| CUR-SB-ARC1-07_WORM-ATTACK_v1-NO-SUIT_2272d5159ce6899919359ee3e361988c8be74426cce9ef6a4f5b4c828e914112.jpg | Storyboard ARC1-07 v1: lost his suit (prompt trimmed). Replaced by v2 (6d9f581c) | SUPERSEDED |
| CUR-SB-ARC1-08_CALMING-THE-WORM_v1-NO-SUIT_425118de2e00602d9e2feb7a4681c3eac5c058e16fe2275aabd740db7aebe44e.jpg | Storyboard ARC1-08 v1: lost his suit. Replaced by v2 (69aed8a2) | SUPERSEDED |
| CUR-SB-ARC2-15_CARRIED-HOME_v1-NO-SUIT_c56e84637367872d2445b80118b97dd09749cc37613945deeb1813da696e26b0.jpg | Storyboard ARC2-15 v1: lost his suit. Replaced by v2 (ee272fe2) | SUPERSEDED |
| CUR-SB-ARC4-06_TRIAL_v1-WRONG-LISAN-FACE_a829141fd8dc3f22b91bcd99105edf3af9651025b0b1c3d9408c76e7d9290438.jpg | Storyboard ARC4-06 v1: wrong face for Lisan. Replaced by v2 (7099da65) | SUPERSEDED |

## 9. Status of every file

Images are listed in section 8. Everything else:

| Path | What it is | Status | Part |
|---|---|---|---|
| `NOVA_README.md` / `NOVA_README.pdf` | This handoff doc | PROPOSAL | 1 |
| `FILE_INDEX.csv` | Path, sha256, size, status, collection, part, what, source for every file | PROPOSAL | 1 |
| `01_CHARACTER_REFS/DESIGN-LOCK.txt` | Design lock V1 rules (written before the orb/helmet split; README section 4 has the current rules) | PROPOSAL | 1 |
| `01_CHARACTER_REFS/CHARACTER.md` | Character sheet: name ideas, look, powers, personality, Lisan relationship | PROPOSAL | 1 |
| `01_CHARACTER_REFS/PROMPTS-FIRST-RUN.jsonl` | Prompts for the first 7 planned jobs (turnaround, settings, first Lisan scene) | PROPOSAL | 1 |
| `04_STORYBOARD_75/STORY-BIBLE.md` | Story bible: mentor role, locations, artifacts, 5 arcs | PROPOSAL | 3 |
| `01_CHARACTER_REFS/manifest.csv` | Per-collection manifest (5 rows) | PROPOSAL | 1 |
| `02_TURNAROUND_MOODS_SETTINGS/manifest.csv` | Per-collection manifest (11 rows) | PROPOSAL | 1 |
| `03_SCENES_50_ORB_HELMET/manifest.csv` | Per-collection manifest (50 rows) | PROPOSAL | 2 |
| `04_STORYBOARD_75/manifest.csv` | Per-collection manifest (75 rows) | PROPOSAL | 3 |
| `05_LISAN_SCENES/manifest.csv` | Per-collection manifest (1 rows) | PROPOSAL | 1 |
| `90_SUPERSEDED/manifest.csv` | Per-collection manifest (7 rows) | SUPERSEDED | 1 |
| `01_CHARACTER_REFS/_CONTACT_SHEET.jpg` | Labelled contact sheet SHEET | PROPOSAL | 1 |
| `02_TURNAROUND_MOODS_SETTINGS/_CONTACT_SHEET.jpg` | Labelled contact sheet SHEET | PROPOSAL | 1 |
| `03_SCENES_50_ORB_HELMET/_CONTACT_1of2.jpg` | Labelled contact sheet 1of2 | PROPOSAL | 2 |
| `03_SCENES_50_ORB_HELMET/_CONTACT_2of2.jpg` | Labelled contact sheet 2of2 | PROPOSAL | 2 |
| `04_STORYBOARD_75/_CONTACT_ARC1.jpg` | Labelled contact sheet ARC1 | PROPOSAL | 3 |
| `04_STORYBOARD_75/_CONTACT_ARC2.jpg` | Labelled contact sheet ARC2 | PROPOSAL | 3 |
| `04_STORYBOARD_75/_CONTACT_ARC3.jpg` | Labelled contact sheet ARC3 | PROPOSAL | 3 |
| `04_STORYBOARD_75/_CONTACT_ARC4.jpg` | Labelled contact sheet ARC4 | PROPOSAL | 4 |
| `04_STORYBOARD_75/_CONTACT_ARC5.jpg` | Labelled contact sheet ARC5 | PROPOSAL | 4 |
| `05_LISAN_SCENES/_CONTACT_SHEET.jpg` | Labelled contact sheet SHEET | PROPOSAL | 1 |
| `90_SUPERSEDED/_CONTACT_SHEET.jpg` | Labelled contact sheet SHEET | PROPOSAL | 1 |

### Not in this drop (by design)

- The earlier delivery zips (`cosmic-avatar-set.zip`, `curator-storyboard.zip`, `curator-all-zips-part*.zip`): every image in them is here under a readable name.
- Hash-named working copies under `/workspace/cosmic-avatar/zip/` and the generator asset store (provenance is kept in `source_path`).
