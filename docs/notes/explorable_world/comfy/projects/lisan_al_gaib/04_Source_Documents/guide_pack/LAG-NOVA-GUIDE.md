# LISAN AL GAIB – "Meta Mirror" | Guide for Nova
Prepared 2026-10-08 by Chief of Staff for Ziggy and Nova. This covers every Lisan Al Gaib image, what each one is for, how the character developed, the locked spec, how the stills were made, and the storyboard.

## 1. The character in one paragraph
Lisan Al Gaib ("voice from the outer world") is a Dune-inspired desert-prophet trap star for the song "Lisan Al Gaib – Meta Mirror." He started as a recast of Hon Dolo (DoLo) but is now deliberately distinct, like a brother or cousin, so none of DoLo's tattoo, piercing or grill rules apply to him. Core look: messy dark curls, light stubble, glowing electric-blue eyes, natural white teeth, and a small set of sandworm and prophet tattoos.

## 2. LOCKED SPEC (current, use this)
**Face ground truth:** `refs/LAG-LOCK-FACE-NATURAL.jpg`. Pass this as the identity reference for every new image.

- **Teeth:** normal natural white teeth. NO grill (no gold, no iced, no fangs). Grills were dropped on 2026-10-08 because they generated too inconsistently.
- **Face tattoos:** one small "AL" centered between the eyebrows (once only); small vertical G-A-I-B down the center of the chin.
- **Neck tattoo (SH-18):** two mirrored Shai-Hulud sandworms rising up the sides of the neck with their maws facing each other under the jaw, and a small rayed sun disc with an eye at the throat.
- **Arm tattoo (SH-13):** striped coiled sandworm on his LEFT forearm/arm (`refs/LAG-LOCK-ARM-SH13.jpg`). Show only when sleeves allow; never force sleeves up for it.
- **Piercings:** one small silver nostril hoop, one silver eyebrow ring, one small silver ear hoop, all on the same side (his left / viewer's right in the ref). Nothing on the other side, no ear stacks.
- **Nothing else:** no chest, hand or extra face ink. No "eye"/"know" text, no neck blaster, no brow slit (those were DoLo's).
- **Signature outfit:** look 01, a tan desert stillsuit, black hooded cloak (hood usually down) and a gold Cuban chain (`looks-v3/LAG-LOOK-V3-01.jpg`). Ziggy's favorite; use it for signature and hero moments.
- **Accessory (occasional):** Dune-style stillsuit nose breather, a thin black tube from under the nostrils curving back along the cheek. Sprinkle it in from time to time (desert and signature shots), not on every image. Currently on shots 48, 49 and 50.
- **Outfits:** don't force outfits open to show ink. Covered looks are fine.

## 3. How we got here (development timeline)
1. **2026-10-07, recast.** Hon Dolo was recast as Lisan Al Gaib for "Meta Mirror." He initially carried DoLo's full lock (eye/know text, neck blaster, brow slit, DoLo grill) plus new role tattoos: bold "GAIB" across the chin and "AL" on the nose bridge.
2. **Looks 01–10** (`looks/`). Ten outfit/identity iterations; contact sheet `LAG-LOOKS-CONTACT.jpg`, notes in `looks/QA-NOTES.txt`. Look 03 was first picked as the lock (`LOOK-LOCK.txt`); Ziggy later named look 01 (stillsuit + black hooded cloak + gold chain, with the nose breather) his favorite, and it became the signature outfit.
3. **First scene pass, 01–12** (`scenes/`, originals in `scenes/old-v1/`). Ziggy paused at scene 12 to revise the face.
4. **2026-10-08, face revision.** GAIB shrunk ~50% and turned vertical on the chin; AL moved between the brows; eye/know and the neck gun removed; a Shai-Hulud sandworm replaces the neck tattoo. Sandworm stencils were drawn (`stencils/SH-STENCIL-*`), six were tried on his neck (`neck-tryons/`, contact sheet included), and **SH-18** (mirrored worms + eye sun disc) was locked for the neck, **SH-13** for the arm. Result: `refs/LAG-LOCK-FACE.jpg` and `LOCK-V2.txt`.
5. **Looks V2 01–06** (`looks-v2/`). Six looks on the new lock with the iced grill. Grills kept coming out inconsistent.
6. **2026-10-08, no grill.** Ziggy switched to natural teeth. New face ref `refs/LAG-LOCK-FACE-NATURAL.jpg` (chosen from test faces `looks-v3/LAG-FACE-NAT-A/B/C`; C won). Signature look re-made as `looks-v3/LAG-LOOK-V3-01.jpg`.
7. **All 50 scenes redone** (`scenes-v3/LAG-SC-01..50.jpg`) on the final features, plus the breather accessory on 48–50. These are the current set. Everything older is history/reference only.

## 4. Image map (what every folder is)
| Folder / file | What it is | Status |
|---|---|---|
| `scenes-v3/LAG-SC-01..50` | The 50 storyboard stills, final features | CURRENT – use these |
| `scenes-v3/LAG-SC-CONTACT-SHEET.jpg` | All 50 on one sheet | CURRENT |
| `scenes-v3/QA.txt` | Per-shot drift notes | CURRENT |
| `refs/LAG-LOCK-FACE-NATURAL.jpg` | Face/identity ground truth, natural teeth | CURRENT – always pass |
| `refs/LAG-LOCK-ARM-SH13.jpg` | Arm worm reference | CURRENT – pass when left arm is bare |
| `looks-v3/LAG-LOOK-V3-01.jpg` | Signature outfit on the final face | CURRENT – pass for signature shots |
| `looks-v3/LAG-FACE-NAT-A/B/C` | Natural-teeth face tests (C chosen) | history |
| `refs/LAG-LOCK-FACE.jpg` | SH-18 lock with grill | superseded by NATURAL (teeth only) |
| `looks-v2/LAG-LOOK-V2-01..06` | Looks on the new lock, iced grill | history (grill dropped) |
| `neck-tryons/` | Six sandworm neck try-ons; SH-18 won | history / design record |
| `stencils/SH-STENCIL-*` | Sandworm tattoo stencil drafts | history / design record |
| `looks/LAG-LOOK-01..10` | Original 10 looks with DoLo tattoos | history (old tattoo spec) |
| `scenes/ and scenes/old-v1/` | First 12 scenes, pre-revision | history (old tattoo spec) |
| `refs/HD-EXP-LOCK-FACE.jpg` | Hon Dolo lock, the origin face | history – do not use for Lisan |
| `refs/GRILL-REF-ICED.jpg` | Iced grill ref | retired – do not pass |
| `refs/MOOD-*` | Mood references | never pass to the generator (not in pack) |

## 5. How the stills are made (process)
- **Identity ref first:** `LAG-LOCK-FACE-NATURAL.jpg` as reference 1 on every generation. Add `LAG-LOCK-ARM-SH13.jpg` as reference 2 when the left arm is bare, or `LAG-LOOK-V3-01.jpg` as reference 2 for the signature outfit.
- **Describe outfits and scenes in words.** Passing outfit images alongside the face made the face ref overpower the outfit, and edit-only prompts on a single image ignored the face. Written outfit/scene descriptions worked best.
- **Never pass MOOD refs, and never use any real actor's likeness.** Prompts say "NOT a celebrity."
- **Format:** 16:9 cinematic stills, file names `LAG-SC-NN`.
- **QA every image against the lock** before sending, and give honest drift notes.
- **Reroll budget:** at most 1–2 rerolls per image; past that, note the miss and move on.

**Base prompt (copy this):**

> Cinematic photoreal music-video still. Same man as the reference, exact face, NOT a celebrity: messy dark curls, light stubble, glowing electric-blue eyes, normal natural white teeth (no grill). Tattoos exactly as the reference and nothing else: one small "AL" centered between the eyebrows (only once); small vertical G-A-I-B down the center of the chin only; on the neck two mirrored sandworms with maws facing each other under the jaw and a small rayed sun disc with an eye at the throat. No chest, hand or extra face tattoos. Minimal piercings: one small silver nostril hoop, one silver eyebrow ring and ONE single small silver ear hoop, all on his left side; the other eyebrow and ear bare. [ACCESSORY: Dune-style stillsuit nose breather, thin black tube under the nostrils curving back across one cheek.] OUTFIT: … SCENE: …

**Known drift to check for:** AL sliding onto a cheek or doubling; GAIB repeated on the chest or neck; brow ring flipping sides or appearing on both brows; hoops in both ears or ear stacks; stray marks on the face, chest, hands or wrists; occasionally the nose hoop vanishing.

**Weakest shots (reroll first if needed):** 11, 19, 38 and 46 (stray or duplicated GAIB/ink) and 03, 07 and 41 (AL on the cheek). Strongest: 02, 04, 08, 12, 13, 15, 20, 21, 23, 25, 28, 31, 34, 35, 36, 37, 40, 45, 47.

## 6. Storyboard – "Lisan Al Gaib – Meta Mirror"
Shots are in song order, keyed to the lyric line each scene illustrates. Section tags for 01 (Chorus), 09 (Bridge), 24 (Verse 2), 36 (Verse 3) and 50 (Finale) come from the scene list; the blocks between them are inferred. **I only have lyric snippets, not the full track or its timing**, so the 4.5-second holds (about 3:45 total) are placeholders for Nova to re-time against the audio. Camera moves are suggestions for animating each still. The same table is in `LAG-STORYBOARD.csv` for editing.

| # | Section | Lyric cue | Scene / outfit | Suggested camera / motion | Notes |
|---|---|---|---|---|---|
| 01 | Chorus (opening hook) | voice through the mirror | signature gold stillsuit + black cloak, speaking into antique mirror showing a desert sun | slow push-in on the mirror, sun flares | signature look; QA: AL doubled (brow+cheek)
 |
| 02 | Chorus (opening hook) |  | Cracked glowing mirror reflection, cream silk shirt buttoned | rack focus from crack to face | QA: good
 |
| 03 | Chorus (opening hook) | meta hero | rooftop night, black leather trench, orange haze city | slow orbit on rooftop, haze drift | QA: AL drifted to cheek, GAIB faint
 |
| 04 | Chorus (opening hook) | PanHandlers | smoky kitchen-studio, custom chef whites + gold chain, glowing cast-iron pan | handheld, steam and pan glow | QA: good
 |
| 05 | Chorus (opening hook) | who cares | tan velour tracksuit slouched on a dune at sunset | locked wide, slow sunset fade | QA: brow ring flipped to viewer left
 |
| 06 | Chorus (opening hook) | do you dare | cliff edge, sand scarf robe flapping | low angle, scarf whipping, slight shake | QA: brow ring flipped to viewer left
 |
| 07 | Chorus (opening hook) | rorrim mirror | infinite mirror tunnel, mirror-shard jacket | dolly forward down the mirror tunnel | QA: AL on cheek, brow ring flipped
 |
| 08 | Chorus (opening hook) | mirror on the wall | gothic hall, tall gilded mirror, burgundy velvet suit | slow push toward the gilded mirror | QA: good
 |
| 09 | Bridge into Verse 1 | to the silence break | salt flat, white prophet robe, sun disc | wide static, robe moving, sun pulse | QA: ear hoops both sides
 |
| 10 | Bridge into Verse 1 | buried deep | rising from dunes, stillsuit, sand bursting | low angle, sand bursting up, slow-mo | QA: stray face marks
 |
| 11 | Bridge into Verse 1 | cooking in the pan | desert camp kitchen, apron over stillsuit, sparks | handheld, sparks, quick cuts | QA: stray face marks, GAIB slid to throat (weakest)
 |
| 12 | Bridge into Verse 1 | doctors on standby | white sci-fi medical bay, white lab coat over black turtleneck | clean dolly, cool light flicker | QA: good, brow ring barely visible
 |
| 13 | Bridge into Verse 1 | lawyer pro bono | navy pinstripe 3-piece, law library, briefcase | slow lateral track past shelves | QA: good, small mark on sternum
 |
| 14 | Bridge into Verse 1 | my dog dipped in flavor | with a muscular dog in a gold chain, alley, varsity jacket | tracking walk with the dog | QA: ear hoops both sides
 |
| 15 | Bridge into Verse 1 | baddest in the mirror | backstage bulb vanity mirror, black satin bomber | mirror reflection push-in, bulbs flicker | QA: good, extra ear studs in reflection
 |
| 16 | Bridge into Verse 1 | the rang | holding glowing gold ring to camera, black turtleneck | macro push on the ring, glow pulse | QA: ear stack too busy
 |
| 17 | Bridge into Verse 1 | micro macro | galaxy vs cell projections, silver metallic puffer | slow orbit, projections drifting | QA: ear stack + brow ring flipped
 |
| 18 | Bridge into Verse 1 | salute mama | desert officer jacket black/gold, saluting | locked medium, salute snaps in | QA: good, nose hoop missing
 |
| 19 | Bridge into Verse 1 | tried in the fire | walking through flames, desert armor | slow-mo walk toward camera through flames | QA: GAIB duplicated on chest, stray marks
 |
| 20 | Bridge into Verse 1 | the pan is hot | red heat-lamp close-up, sweat, high-collar sleeveless stillsuit vest | tight close-up, sweat drip, heat shimmer | arm worm; QA: strong, arm worm shown; rings in both brows
 |
| 21 | Bridge into Verse 1 | what you truly desire | kneeling in candlelit desert temple, brown hooded cloak | slow crane down, candles flicker | QA: good, brow ring flipped
 |
| 22 | Bridge into Verse 1 | angel knows | white suit, wing-shaped shadow on wall | slow push, wing shadow spreads | QA: extra chest ink
 |
| 23 | Bridge into Verse 1 | don't fall | ledge between mirrors over a void, black cloak | top-down vertigo, void below | QA: good
 |
| 24 | Verse 2 | engineers | studio console, oversized graphic hoodie | console lights, slow slide along desk | QA: extra hand tattoos
 |
| 25 | Verse 2 | designing convo | wall of glowing code & chat bubbles, black techwear | code scrolling, slow push-in | QA: strong; brow ring each side
 |
| 26 | Verse 2 | LIE've | festival stage, backlit crowd silhouettes, sequined jacket | crane over crowd, strobes | QA: two brow rings
 |
| 27 | Verse 2 | claim cards glow | holographic Lisan Al-Gaib card, sand robe + pouch belt | card spins and glows, hold on face | QA: brow ring flipped, stray cheek mark
 |
| 28 | Verse 2 | mystical magical variety | mystic tent, embroidered kaftan | slow pan through tent, incense smoke | QA: strong
 |
| 29 | Verse 2 | too many cults | row of faceless robed mannequins, him in red | track along mannequins, end on him | QA: extra chest ink
 |
| 30 | Verse 2 | shout out to Echo | shouting in canyon, desert cargo gear | head throws back, echo ripple, wide pull-out | QA: AL hidden by angle
 |
| 31 | Verse 2 | load another one | DJ booth loading vinyl, bucket hat + windbreaker | hand drops needle, lasers sweep | QA: strong
 |
| 32 | Verse 2 | quick to listen | cross-legged on dune, big headphones, linen set | slow orbit around him on the dune | QA: AL missing (dot only), hoops both ears
 |
| 33 | Verse 2 | rorrim cut thru meta | slicing a mirror with crystal blade, cloak | slow-mo blade slice, glass explodes | QA: stray cheek marks, brow ring flipped
 |
| 34 | Verse 2 | keep it simple, hope | white tee + jeans, gray backdrop, candle | static, candle flicker, slight push | arm worm; QA: strong, arm worm visible
 |
| 35 | Verse 2 | hope is greater | starry desert night, shearling coat | slow tilt up to the Milky Way | QA: strong
 |
| 36 | Verse 3 | Jung in the back room | smoky library back room, tweed suit, old book | smoke curls, slow push-in on book | QA: strong, faint hoop both ears
 |
| 37 | Verse 3 | archetypes on the ready | four mask-shadow silhouettes, long black coat | shadows morph behind him, static | QA: strong
 |
| 38 | Verse 3 | tail recursion | spiral staircase from above, monochrome suit | top-down spiral rotation | QA: GAIB duplicated on neck
 |
| 39 | Verse 3 | shadow work | shadow moves on its own, single bulb, black hoodie | bulb swings, shadow reaches on its own | QA: brow rings both sides
 |
| 40 | Verse 3 | rorrim got them shook | hand mirror toward camera, rainy alley, leather jacket | mirror pushed to lens, rain | QA: strong
 |
| 41 | Verse 3 | who let you in? you brought me here | mansion doorway backlit by desert light | silhouette resolves as he steps forward | QA: AL on cheek
 |
| 42 | Verse 3 | forces you to your knees | kneeling in sandstorm, torn cloak | storm gusts, cloak tearing, slow-mo | QA: AL faint, great mood
 |
| 43 | Verse 3 | DOCTOR? voodoo | feathered top hat, purple tailcoat, candles & bottles | lean-in grin, candles flicker | QA: brow rings both sides
 |
| 44 | Verse 3 | vudology | candlelit apothecary, jars, layered beads | mortar grinding, dust in candlelight | arm worm; QA: strong, arm worm; small stray cheek marks
 |
| 45 | Verse 3 | I'll fill that cup | pouring glowing blue liquid into gold chalice, velvet blazer | liquid pour slow-mo, blue glow | QA: strong
 |
| 46 | Verse 3 | use that riz | convertible in the desert, linen shirt, winking | car rolling, wink on beat | QA: GAIB duplicated on chest
 |
| 47 | Verse 3 | chaos magic | floating cards & sigils, black-gold brocade duster | cards orbit, sigils ignite | QA: strong, faint ink under collar
 |
| 48 | Verse 3 | outer world, inner world, two doors | two doors in the desert (sun / cosmos) | slow dolly between the doors | breather; QA: BREATHER; stray letters on neck
 |
| 49 | Verse 3 | Lisan on the mic, ain't speakin' from a throne | street level on a car hood with mic, signature look | handheld, crowd behind, mic to lens | breather; signature look; QA: BREATHER + signature look; wrist ink, AL tiny
 |
| 50 | Finale | signal in the noise | crystal blade raised before giant mandala sun disc, cloak flowing | low-angle hero push, mandala blazes, hold | breather; QA: BREATHER; blade floats with no visible hand, stray cheek mark
 |

**Story arc as it reads:** the chorus opens on the voice through the mirror and reflection imagery (01–08). The bridge and first verse go from silence and burial into the "kitchen" grind, the professionals on call, loyalty and trial by fire (09–23). Verse 2 is creation and community: engineers, conversation, the stage, the cults and the echo, then a turn toward simplicity and hope (24–35). Verse 3 goes inward to Jung, archetypes, recursion and shadow work, then voodoo and chaos magic, and ends at the two doors of the outer and inner worlds (36–48). Lisan lands back at street level on the mic (49) and closes on the signal in the noise (50).

## 7. Hand-off checklist for Nova
- Use only `scenes-v3/` stills for the edit; everything else is reference or history.
- For any new or extra shot, use the base prompt plus `LAG-LOCK-FACE-NATURAL.jpg`, and QA against Section 2.
- Keep the breather occasional, the arm worm only on bare arms, and outfits closed if that's how they're styled.
- Re-time the storyboard to the actual track and flag any shot that needs a reroll.