# Lisan Al Gaib — 500-Image Look Pack: Guide for Nova

Hi Nova! This is your map of the finished Lisan Al Gaib look pack. Everything you need is in here: what's in the pack, how the files are named, how to update the ledger, which images have QA notes, and which ones we think are the strongest.

## What the pack is

- **50 looks × 10 images = 500 images.** Each look is one outfit + setting for the same character.
- Every look has the same 10 shots, in this order:
  - **5 reference views:** V1 chest-up · V2 front (full body) · V3 left profile (full body) · V4 right profile (full body) · V5 back (full body)
  - **5 story scenes:** S1 · S2 · S3 · S4 · S5 (each look has its own five scene ideas — see the table below)
- **Every image is 16:9** (1280 × 720 JPEG), including the chest-ups and back views. (LOOKS.md still mentions 4:3 / 9:16 from an early plan; that is out of date — all final files are 16:9.)
- **V3, V4 and V5 were generated from each look's V2 front image**, so the outfit matches across the views. (This method was locked in during looks L02–L04, per the QA log; look L01's profiles were made just before that. A handful of views still show small outfit drift — those are noted in the CSV.)

## How the files are packaged

The master package is split into **8 parts** because of the 25 MB attachment limit:

> **README — about the parts:** `LAG-500-MASTER-part01.zip` … `LAG-500-MASTER-part08.zip` are each a complete, normal zip — open any of them on its own (they are *not* a split archive, no need to join them). Together they hold all 50 per-look zips in order. **Part 01 also contains this guide, LEGEND-500.csv, QA.txt and CONTACT-INDEX.jpg.**

| Part | Contains |
|---|---|
| `LAG-500-MASTER-part01.zip` | NOVA-GUIDE-500.md, LEGEND-500.csv, QA.txt, CONTACT-INDEX.jpg + looks L01–L06 (6 look zips) |
| `LAG-500-MASTER-part02.zip` | looks L07–L13 (7 look zips) |
| `LAG-500-MASTER-part03.zip` | looks L14–L20 (7 look zips) |
| `LAG-500-MASTER-part04.zip` | looks L21–L27 (7 look zips) |
| `LAG-500-MASTER-part05.zip` | looks L28–L34 (7 look zips) |
| `LAG-500-MASTER-part06.zip` | looks L35–L41 (7 look zips) |
| `LAG-500-MASTER-part07.zip` | looks L42–L48 (7 look zips) |
| `LAG-500-MASTER-part08.zip` | looks L49–L50 (2 look zips) |

Inside the parts there is **one zip per look**, e.g. `LAG-L01-mirror-voice-signature.zip`. Each look zip unpacks to a folder of the same name holding:

```
LAG-L01-mirror-voice-signature/
  LAG-L01-mirror-voice-signature__V1-chestup.jpg
  LAG-L01-mirror-voice-signature__V2-front.jpg
  LAG-L01-mirror-voice-signature__V3-left.jpg
  LAG-L01-mirror-voice-signature__V4-right.jpg
  LAG-L01-mirror-voice-signature__V5-back.jpg
  LAG-L01-mirror-voice-signature__S1-worm-ride-sunrise.jpg
  ... S2 to S5 ...
  CONTACT-LAG-L01-mirror-voice-signature.jpg   <- 5x2 contact sheet of the 10 images
```

- **Contact sheet** (one per look): a 5 × 2 grid — top row V1–V5, bottom row S1–S5 — each thumbnail captioned with its ledger row number and short name (e.g. `#458  S3 sand-rally`). Hero picks are tagged **[HERO]**, flagged images **[FLAG]**.
- **CONTACT-INDEX.jpg**: one V1 chest-up thumbnail per look in a 10 × 5 grid, labelled `L## slug` — the quickest way to find a look.
- **LEGEND-500.csv**: the row-by-row ledger for all 500 images (details below).
- **QA.txt**: the raw QA log from generation, for reference.

## Naming scheme — how to read a filename

`LAG-L46-riz-convertible-linen__S3-sand-rally.jpg`

| Piece | Meaning |
|---|---|
| `LAG` | Lisan Al Gaib project prefix |
| `L46` | Look number (L01–L50) |
| `riz-convertible-linen` | Look slug (short name for the look) |
| `__` | Separator between the look and the shot |
| `S3` | Shot code: V1–V5 = reference views, S1–S5 = story scenes |
| `sand-rally` | Short name of the shot (for V shots: `chestup`, `front`, `left`, `right`, `back`) |

**Row (ledger) number** = (look number − 1) × 10 + shot position, where V1–V5 are positions 1–5 and S1–S5 are positions 6–10. Example: L46 S3 → 450 + 8 = **row 458**.

## Using LEGEND-500.csv to update the ledger

**The `row` column is the ledger number (1–500).** Open the CSV in Excel/Sheets, sort by `row`, and match it to your ledger line for line. Columns:

| Column | What it holds |
|---|---|
| `row` | Ledger number 1–500 |
| `look_num` | L01–L50 |
| `look_slug` | Full look name, e.g. `LAG-L46-riz-convertible-linen` |
| `shot` | V1–V5 / S1–S5 |
| `shot_name` | Short label, e.g. `V1 chest-up`, `S3 sand-rally` |
| `filename` | Exact JPG filename (inside the look's zip folder) |
| `zip_name` | Which per-look zip the image is in |
| `outfit` | Outfit as specified for that image |
| `setting` | Setting (V shots) or scene description (S shots) |
| `breather` | Y if the stillsuit nose-tube breather was requested |
| `arm_worm` | Y if the SH-13 forearm worm was meant to show (sleeves allow) |
| `qa_status` | OK / OK-note / FLAG |
| `qa_note` | The QA comment for that image (blank = nothing to note) |
| `hero` | Y = hero pick (see Hero Picks below) |

Tip: filter `qa_status` = FLAG or OK-note to see everything with a caveat; filter `hero` = Y for the best frames.

## The character — locked features

These are the features that should be the same in every image (useful when checking QA notes):

- **Teeth:** natural white teeth — no grill.
- **Forehead:** small **"AL"** tattoo between the brows.
- **Chin:** small vertical **G-A-I-B** running down the chin (chin only — never the neck or chest).
- **Neck:** two **mirrored sandworms** facing each other under the jaw, with an **eye sun-disc** at the throat.
- **Arm:** **SH-13 worm** tattoo on his **LEFT forearm only**, shown only when sleeves allow.
- **Piercings — all on his left side:** one nostril hoop, one brow ring, one ear hoop.
- **Signature look:** stillsuit + black hooded cloak + gold chain (looks L01, L10, L49).
- **Breather:** stillsuit nose-tube breather, used occasionally (marked `breather = Y` in the CSV; 69 images).

## All 50 looks

| # | Slug | Outfit | Setting (reference views) | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|---|---|---|
| L01 | `LAG-L01-mirror-voice-signature` | SIGNATURE: tan stillsuit + black hooded cloak + gold Cuban chain; tan stillsuit desert boots | simplified sunlit desert dunes with an antique gilded mirror on a stand, warm golden-hour light | Riding the Maker at Sunrise (`worm-ride-sunrise`) | The Mirror Council (`mirror-council`) | Calling the Maker (`thumper-call`) | Convoy Swallowed (`convoy-swallowed`) | After the Storm (`statue-reflection`) |
| L02 | `LAG-L02-cracked-mirror-silk` | cream silk shirt fully buttoned, tailored charcoal trousers; polished brown leather loafers | simplified dark studio with a large cracked glowing mirror panel, cool blue rim light | Gallery of Cracks (`gallery-of-cracks`) | The Reflection Refuses (`reflection-refuses`) | Glass Rain (`glass-rain`) | The Mirror Auction (`mirror-auction`) | Gold in the Cracks (`gold-in-cracks`) |
| L03 | `LAG-L03-meta-hero-rooftop` | black leather trench coat over a black knit sweater, dark cargo trousers; black combat boots | simplified night rooftop above an orange-haze city skyline, sodium orange and cyan rim light | Rooftop Pursuit (`rooftop-leap`) | Standoff Above the City (`water-tower-standoff`) | Hijacking the Signal (`hijack-signal`) | The Ledge Rescue (`ledge-rescue`) | Hero Off Duty (`hero-off-duty`) |
| L04 | `LAG-L04-panhandlers-chef-whites` | custom white chef jacket with gold buttons, gold Cuban chain, black chef trousers; black leather kitchen clogs | simplified smoky kitchen-studio with steel counters, warm amber light and a glowing cast-iron pan | Midnight Rush (`midnight-rush`) | The Cook-Off (`cook-off-rival`) | Feeding the Block (`feeding-the-block`) | Spice Market Run (`spice-bazaar`) | Forging the Pan (`forging-the-pan`) |
| L05 | `LAG-L05-who-cares-velour-dune` | tan velour tracksuit zipped up, gold chain; cream retro sneakers | simplified sunset dunes with warm orange backlight | Dune Board Descent (`dune-board`) | Nap Interrupted (`nap-interrupted`) | Desert Pirate Radio (`pirate-radio`) | Oasis Hangout (`oasis-hangout`) | Dust Devil (`dust-devil`) |
| L06 | `LAG-L06-dare-cliff-scarf-robe` | flowing sand-colored scarf robe wrapped over a linen tunic, wide wrap belt; leather sandal boots | simplified rocky cliff edge above a desert canyon, bright windy daylight | Leap of Faith (`leap-onto-worm`) | Canyon Pursuit (`canyon-skimmer-chase`) | The Dare (`blindfold-bridge`) | Lookout (`hawk-lookout`) | Rappelling the Wall (`canyon-rappel`) |
| L07 | `LAG-L07-rorrim-mirror-shard-jacket` | jacket covered in mirror-shard tiles over a black tee, black slim trousers; black chelsea boots | simplified infinite mirror tunnel, cool silver-blue light | Duel in the Mirror Realm (`mirror-realm-duel`) | Shard Storm (`shard-storm`) | Hall of Selves (`hall-of-selves`) | Breaking Out (`breaking-out`) | The Guide (`maze-guide`) |
| L08 | `LAG-L08-mirror-wall-velvet-suit` | burgundy velvet suit over a black silk shirt, gold pocket chain; black patent leather oxfords | simplified gothic hall with a tall gilded mirror, candlelight and moonlight | The Masquerade (`masquerade-entrance`) | Audience with the Mirror Queen (`mirror-queen`) | Ballroom Duel (`ballroom-duel`) | Behind the Mirror (`behind-the-mirror`) | Dawn After the Ball (`dawn-after-ball`) |
| L09 | `LAG-L09-silence-salt-prophet` | flowing white prophet robe with the hood down, rope belt; white wrapped sandals | simplified white salt flat with a pale sun disc, bright high-key light | Sermon on the Salt (`salt-sermon`) | Salt Cracks (`salt-cracks-worm`) | Silent Procession (`lantern-procession`) | The Blinding (`blinding-truth`) | Breaking the Silence (`salt-pool-night`) |
| L10 | `LAG-L10-buried-deep-stillsuit` | SIGNATURE: tan stillsuit + black hooded cloak + gold Cuban chain; tan stillsuit desert boots | simplified open dunes with sand spray in the air, bright hazy daylight | Riding the Worm's Crest (`worm-crest-ride`) | Ornithopter Dogfight (`ornithopter-dogfight`) | Return to the Cave City (`sietch-return`) | Buried Ambush (`buried-ambush`) | The Water Debt (`water-debt`) |
| L11 | `LAG-L11-desert-camp-kitchen` | tan stillsuit with a leather apron over it, cloth head wrap pushed back off the forehead; desert boots | simplified desert camp kitchen under canvas, fire sparks, warm dusk light | Feast Before the Ride (`feast-before-ride`) | Dinner Bell (`dinner-bell`) | Raid on the Camp (`camp-raid`) | Spice Harvest (`spice-harvest`) | Lessons by the Fire (`fire-lesson`) |
| L12 | `LAG-L12-doctors-standby-medbay` | white lab coat over a black turtleneck, black tailored trousers; white minimalist sneakers | simplified white sci-fi medical bay, cool clean light | Code Red (`code-red`) | Diagnosing the Signal (`holo-diagnosis`) | Lab Breach (`lab-breach`) | The Sample (`glowing-sample`) | Night Rounds (`night-rounds`) |
| L13 | `LAG-L13-pro-bono-pinstripe` | navy pinstripe three-piece suit, white shirt, navy tie, gold watch chain; brown leather brogues | simplified classic law library with wooden shelves, warm desk-lamp light | The Closing Argument (`closing-argument`) | Boardroom Showdown (`boardroom-showdown`) | Pro Bono Hours (`pro-bono-hours`) | Serving the Papers (`serving-papers`) | Found in the Archive (`archive-prophecy`) |
| L14 | `LAG-L14-dog-dipped-varsity` | black and gold varsity jacket over a white tee, black jeans, gold chain; black high-top sneakers | simplified graffiti alley with purple and amber neon | Block Parade (`block-parade`) | Alley Standoff (`alley-standoff`) | Training Day (`rooftop-training`) | Search in the Rain (`search-in-rain`) | Late Diner (`late-diner`) |
| L15 | `LAG-L15-baddest-mirror-bomber` | black satin bomber jacket over a black tee, black tapered trousers; white leather sneakers | simplified backstage with bulb-lit vanity mirrors, warm bulb light | The Walkout (`arena-walkout`) | Green Room Confrontation (`green-room-contract`) | Crowd Surf (`crowd-surf`) | Vision in the Vanity (`vanity-vision`) | After the Show (`after-the-show`) |
| L16 | `LAG-L16-the-rang-turtleneck` | black ribbed turtleneck, black wool trousers, a glowing gold ring on one finger; black leather chelsea boots | simplified dark velvet backdrop with a single warm spotlight | Forging the Rang (`forging-the-rang`) | The Vault (`vault-laser-grid`) | The Oath (`ring-oath`) | Ring Thief (`night-market-thief`) | Light in the Dark (`light-in-the-dark`) |
| L17 | `LAG-L17-micro-macro-puffer` | silver metallic puffer jacket zipped up, black joggers; chunky silver sneakers | simplified planetarium dome with galaxy and cell projections | The Observatory (`observatory`) | Down to the Cell (`down-to-the-cell`) | Zero-G Drift (`zero-g-drift`) | Data Storm (`data-storm`) | Frozen Dune (`frozen-dune`) |
| L18 | `LAG-L18-salute-mama-officer` | black and gold desert officer jacket with epaulettes, black cargo trousers; tall black leather boots | simplified desert military camp with banners, harsh daylight | Review of the Troops (`troop-review`) | Worm Cavalry (`worm-cavalry`) | War Council (`war-council`) | Letter Home (`letter-home`) | Honor the Lost (`memorial-cairn`) |
| L19 | `LAG-L19-fire-trial-armor` | dark bronze desert armor plates over a tan undersuit, armored gauntlets; armored desert boots | simplified scorched desert ground with low flames, orange firelight | Trial by Fire (`trial-by-fire`) | Battle at the Dunes (`dune-battle`) | Worm vs. Harvester (`worm-vs-harvester`) | Forged (`armor-forge`) | Embers (`embers`) |
| L20 | `LAG-L20-pan-hot-sleeveless-vest` | sleeveless high-collar tan stillsuit vest and trousers, fingerless gloves; desert boots | simplified desert outpost workshop with red heat-lamp glow | Climbing the Worm (`climbing-the-worm`) | Heat of the Forge (`heat-of-forge`) | Market Brawl (`bazaar-brawl`) | The Cistern (`hidden-cistern`) | Fixing the Thumper (`fixing-thumper`) |
| L21 | `LAG-L21-desire-temple-cloak` | brown hooded cloak (hood down) over a cream linen tunic, leather belt; wrapped desert boots | simplified candlelit desert temple, warm candlelight | Vision of Desire (`temple-vision`) | Worm Shrine (`worm-shrine`) | Defending the Temple (`temple-defense`) | The Pilgrim Road (`pilgrim-road`) | The Confession (`the-confession`) |
| L22 | `LAG-L22-angel-knows-white-suit` | crisp white suit, white shirt buttoned to the collar; white leather loafers | simplified white studio wall with a wing-shaped shadow, clean soft light | Cathedral Light (`cathedral-wings`) | The Guardian (`gala-catch`) | Light Duel (`light-duel`) | Bedside (`bedside-sunrise`) | Feathers Over the City (`feathers-over-city`) |
| L23 | `LAG-L23-dont-fall-black-cloak` | black hooded cloak (hood down) over a black fitted tunic and trousers; black wrapped boots | simplified ledge between giant mirrors over a void, cool dim light | Bridge Over the Void (`void-bridge`) | Into the Chasm (`into-the-chasm`) | Don't Fall (`dont-fall`) | Shadows on the Ledge (`shadows-on-ledge`) | Starfall (`starfall`) |
| L24 | `LAG-L24-engineers-graphic-hoodie` | oversized black graphic hoodie with a gold sun print (hood down), black cargo pants; black-and-white high-top sneakers | simplified recording studio with a large console and colored LEDs | 4 A.M. Session (`four-am-session`) | The Machine Wakes (`machine-wakes`) | Blackout (`studio-blackout`) | Field Recording (`field-recording`) | Rooftop Cypher (`rooftop-cypher`) |
| L25 | `LAG-L25-designing-convo-techwear` | black techwear jacket with straps and pockets, black cargo trousers; black tactical sneakers | simplified wall of glowing code and chat bubbles, blue screen light | The Den (`hacker-den`) | Meeting the Echo (`echo-interface`) | Corporate Escape (`atrium-escape`) | The Drop (`neon-drop`) | Server Farm in the Sand (`server-farm-sand`) |
| L26 | `LAG-L26-lieve-sequin-stage` | gold and black sequined jacket over a black tee, black leather trousers; black platform boots | simplified festival stage with backlit haze and strobes | Headliner (`headliner`) | Sabotage (`stage-sabotage`) | Festival in the Dunes (`dune-rave`) | The Fan (`backstage-fan`) | Strobe Prophet (`strobe-prophet`) |
| L27 | `LAG-L27-claim-cards-sand-robe` | sand-colored robe with the hood down, leather pouch belt with brass buckles; wrapped desert boots | simplified desert market stall with holographic glow, warm afternoon light | High Stakes in the Tent (`tent-card-game`) | The Worm Card (`worm-card`) | Card Duel (`amphitheater-card-duel`) | Caravan Trade (`caravan-trade`) | Fortune for a Child (`fortune-for-child`) |
| L28 | `LAG-L28-mystic-kaftan-tent` | richly embroidered purple and gold kaftan, layered gold necklaces; embroidered velvet slippers | simplified mystic tent with lanterns and rugs, incense haze | The Seance (`the-seance`) | Night Bazaar (`night-bazaar`) | Tent Raid (`tent-raid`) | Oracle Pool (`mercury-oracle`) | Caravan at Dawn (`caravan-dawn`) |
| L29 | `LAG-L29-cults-red-robe` | deep red hooded robe (hood down) with a black sash; black leather sandals | simplified hall of faceless robed mannequins, cold gray light, him in red | Infiltration (`infiltration`) | Unmasking (`unmasking`) | Catacomb Chase (`catacomb-chase`) | Idols Fall (`idols-fall`) | The Freed (`the-freed`) |
| L30 | `LAG-L30-echo-canyon-cargo` | tan utility jacket, scarf around the neck, cargo trousers with pouches; scuffed desert boots | simplified red rock canyon, warm reflected light | The Echo Answers (`echo-answers`) | Canyon Worm Run (`canyon-worm-run`) | Canyon Ambush (`canyon-ambush`) | Petroglyph Find (`petroglyph-find`) | Canyon Campfire (`canyon-campfire`) |
| L31 | `LAG-L31-load-another-dj` | black bucket hat tilted back (forehead visible), teal-purple retro windbreaker, black track pants; white running sneakers | simplified DJ booth with laser sweeps, purple light | Warehouse Rave (`warehouse-rave`) | Crate Digging (`crate-digging`) | Raid Lights (`raid-lights`) | Pirate Broadcast (`pirate-ship-set`) | Sunrise Set (`sunrise-set`) |
| L32 | `LAG-L32-quick-listen-linen` | loose white linen shirt and wide linen trousers, big over-ear headphones around his neck; woven leather sandals | simplified soft pastel sunset dunes | Listening to the Dunes (`listening-to-dunes`) | Singing Sands (`singing-sands`) | The Mediator (`the-mediator`) | Monastery of Silence (`monastery-silence`) | Dream Frequency (`dream-frequency`) |
| L33 | `LAG-L33-crystal-blade-mirror` | charcoal hooded cloak (hood down) over a black fitted tunic, crystal blade on the belt; black wrapped boots | simplified dark hall with a giant shattered mirror, cool white light | Crystal Duel (`crystal-duel`) | The Worm's Tooth (`worms-tooth`) | Cutting Through (`cutting-through`) | Shadow Legion (`shadow-legion`) | Vigil (`blade-vigil`) |
| L34 | `LAG-L34-keep-simple-white-tee` | plain white tee, straight blue jeans; worn white canvas sneakers | simplified plain gray backdrop with soft candlelight | Laundromat Hope (`laundromat-hope`) | Candle Vigil (`candle-vigil`) | Bus Stop (`bus-stop-rain`) | Rooftop Garden (`rooftop-garden`) | Last Gas Station (`last-gas-station`) |
| L35 | `LAG-L35-hope-shearling-night` | brown shearling coat with a cream wool collar over a black knit, dark trousers; brown suede desert boots | simplified starry desert night, cool moonlight and the Milky Way | Worm Under the Stars (`worm-under-stars`) | Night Caravan (`night-caravan`) | Beacon (`mesa-beacon`) | Frostbite Ambush (`frost-ambush`) | Stargazing (`stargazing`) |
| L36 | `LAG-L36-jung-library-tweed` | brown tweed three-piece suit, cream shirt, knit tie; brown leather oxford boots | simplified smoky library back room, green banker's lamp light | Dream Analysis (`dream-analysis`) | The Red Book (`red-book`) | Library Fire (`library-fire`) | The Back Room Society (`back-room-society`) | Night Train (`night-train`) |
| L37 | `LAG-L37-archetypes-black-coat` | long black wool coat over a black turtleneck, black trousers; black leather boots | simplified dark stage with four mask-shaped shadow silhouettes | The Four (`the-four`) | Shadow War (`shadow-war`) | Mask Maker (`mask-maker`) | Masks in the Crowd (`masks-in-station`) | Integration (`integration`) |
| L38 | `LAG-L38-tail-recursion-monochrome` | monochrome black-and-white geometric suit, black shirt; black-and-white wingtip shoes | simplified white spiral staircase seen from above, high-contrast light | Infinite Staircase (`infinite-staircase`) | The Loop (`the-loop`) | Clock Tower (`clock-tower`) | Fractal Battle (`fractal-battle`) | Spiral Garden (`spiral-garden`) |
| L39 | `LAG-L39-shadow-work-hoodie` | black hoodie (hood down), black joggers; black sneakers | simplified bare concrete room with a single hanging bulb, hard shadows | The Shadow Escapes (`shadow-escapes`) | Duel with the Shadow (`shadow-duel`) | Circle (`the-circle`) | Shadowboxing (`shadowboxing`) | City of Shadows (`city-of-shadows`) |
| L40 | `LAG-L40-shook-rain-leather` | black leather moto jacket over a charcoal hoodie (hood down), black jeans; black combat boots | simplified rainy alley with cyan and red neon | Interrogation (`mirror-interrogation`) | Rain Chase (`rain-chase`) | Alley Fight (`alley-fight`) | The Informant (`noodle-informant`) | Puddle Mirror (`puddle-mirror`) |
| L41 | `LAG-L41-who-let-you-in-mansion` | cream silk shirt with an open collar, tan linen trousers; tan suede loafers | simplified grand mansion doorway flooded with desert light, sand on marble | Uninvited (`uninvited`) | The Desert Reclaims (`desert-reclaims`) | Who Let You In (`who-let-you-in`) | Courtyard of Mirrors (`courtyard-mirrors`) | Terrace at Sunset (`sunset-terrace`) |
| L42 | `LAG-L42-knees-sandstorm-torn-cloak` | torn weathered dark cloak (hood down) over a dusty tan stillsuit; sand-crusted desert boots | simplified desert sandstorm, swirling orange haze | Out of the Storm (`out-of-storm`) | Battle in the Storm (`storm-battle`) | Brought to His Knees (`brought-to-knees`) | Through the Storm (`through-the-storm`) | When the Storm Clears (`storm-clears`) |
| L43 | `LAG-L43-doctor-voodoo-tophat` | feathered black top hat tilted back (forehead visible), purple velvet tailcoat, black waistcoat and trousers; black buckled boots | simplified candlelit room with bottles and candles | Bayou Ceremony (`bayou-ceremony`) | Midnight Cemetery (`midnight-cemetery`) | Potion Duel (`potion-duel`) | Second Line (`second-line`) | Riverboat Game (`riverboat-game`) |
| L44 | `LAG-L44-vudology-apothecary` | oatmeal linen shirt, sleeves rolled to the elbow, wooden bead necklaces, brown canvas trousers; worn leather boots | simplified candlelit apothecary with shelves of jars | The Remedy (`the-remedy`) | Herb Gathering (`herb-gathering`) | Apothecary Raid (`apothecary-raid`) | The Reaction (`the-reaction`) | Desert Bloom (`desert-bloom`) |
| L45 | `LAG-L45-fill-cup-velvet` | deep emerald velvet blazer over a black silk shirt, black trousers; black velvet loafers | simplified dark lounge with a gold chalice and blue glow | The Banquet (`the-banquet`) | The Poisoned Cup (`poisoned-cup`) | Fountain (`cave-fountain`) | Chalice Heist (`chalice-heist`) | Last Call (`last-call`) |
| L46 | `LAG-L46-riz-convertible-linen` | light blue linen shirt, white linen trousers, gold chain, aviator sunglasses pushed up into his hair; tan leather loafers | simplified desert highway beside a vintage convertible, bright sun | Desert Road Trip (`desert-road-trip`) | Roadside Charm (`roadside-charm`) | Sand Rally (`sand-rally`) | Worm Crossing (`worm-crossing`) | Motel Pool (`motel-pool`) |
| L47 | `LAG-L47-chaos-magic-brocade` | black and gold brocade duster coat over a black shirt, black trousers; black leather boots | simplified dark void with floating cards and sigils | Sigil Ritual (`sigil-ritual`) | Chaos Unleashed (`chaos-unleashed`) | Gravity Flip (`gravity-flip`) | The Game (`the-game`) | Aftermath (`magic-aftermath`) |
| L48 | `LAG-L48-two-doors-desert-robe` | tan hooded wrap robe (hood down) draped over a sand tunic, rope belt; wrapped desert sandal boots | simplified desert with two freestanding doors, one sunlit and one cosmic, golden light | The Choice (`the-choice`) | Worm of Stars (`worm-of-stars`) | Door Guardians (`door-guardians`) | Field of Doors (`field-of-doors`) | Inner World (`inner-world`) |
| L49 | `LAG-L49-mic-street-signature` | SIGNATURE: tan stillsuit + black hooded cloak + gold Cuban chain; tan stillsuit desert boots | simplified street level beside a parked car at night, streetlights | Block Concert (`block-concert`) | Worm Under the City (`worm-under-city`) | Street Battle (`street-battle`) | Desert Arrival (`desert-arrival`) | Car Hood Quiet (`car-hood-quiet`) |
| L50 | `LAG-L50-signal-mandala-finale` | black hooded cloak (hood down) over a black tunic, thin gold chain, crystal blade; black wrapped desert boots | simplified rocky desert under a giant golden mandala sun disc | The Final Ride (`the-final-ride`) | Signal (`signal-raised`) | The Final Duel (`final-duel`) | Rebuilding (`rebuilding`) | Signal in the Noise (`walk-into-dunes`) |

## QA summary (honest version)

Every image was reviewed during generation. Final status counts across all 500:

| Status | Count | Meaning |
|---|---|---|
| **OK** | 220 | Clean — nothing worth noting |
| **OK-note** | 271 | Usable, with a small drift or quirk noted in `qa_note` |
| **FLAG** | 9 | Kept as the best available after rerolls, but has a visible issue |

Where a row was rerolled, the last QA entry for that row is the one used. Six early rows (1, 2, 5, 6, 82, 86) had no line in QA.txt; they were spot-checked during packaging and the note says so.

**Flagged images:**

| Row | File | Issue |
|---|---|---|
| 4 | `LAG-L01-mirror-voice-signature__V4-right.jpg` | both rerolls broke (3D worms popping off the neck, then a bobblehead); kept the first pass, which has flat ink but slightly stocky proportions. FLAG. |
| 19 | `LAG-L02-cracked-mirror-silk__S4-mirror-auction.jpg` | both passes put GAIB on the chest; kept the reroll (better face/composition). FLAG. |
| 61 | `LAG-L07-rorrim-mirror-shard-jacket__V1-chestup.jpg` | FLAG. After 2 tries, GAIB still appears on the neck below the sun disc; kept the better one. The base prompt now says "no letters anywhere on the neck". |
| 192 | `LAG-L20-pan-hot-sleeveless-vest__V2-front.jpg` | FLAG. Arm worm correct, but proportions are still dwarfed (big head, short legs) after 3 tries; V3-V5 inherit from it. |
| 200 | `LAG-L20-pan-hot-sleeveless-vest__S5-fixing-thumper.jpg` | FLAG (minor). Beautiful sunset thumper repair with breather, but the arm worm is on his right (near) arm again in three-quarter view. |
| 216 | `LAG-L22-angel-knows-white-suit__S1-cathedral-wings.jpg` | FLAG (minor). Gorgeous cathedral wing-light, but "GAI" repeats on the throat above the sun disc after two tries. |
| 291 | `LAG-L30-echo-canyon-cargo__V1-chestup.jpg` | FLAG. GAIB repeats on the throat between the worms on both tries; face, AL and piercings are otherwise good. Kept as the best available. |
| 301 | `LAG-L31-load-another-dj__V1-chestup.jpg` | FLAG. GAIB repeats large on the throat between the worms (try1 also put it on the chest). Kept as the best available; the tee and windbreaker are correct. |
| 319 | `LAG-L32-quick-listen-linen__S4-monastery-silence.jpg` | FLAG. GAIB repeats on the chest below the sun disc on both tries. Kept as the best available. |

**Recurring drift types** (rows listed so you can find them; the CSV `qa_note` has the specifics — some rows fall in more than one group):

- **Piercings mirrored to his right side (or doubled on both sides)** — 72 rows: 1, 49, 57, 86, 119, 126, 130, 136, 141, 149, 151, 158, 160-161, 169, 171, 176, 179, 187-191, 197-198, 201, 221, 231, 240-241, 246, 267, 277, 279, 281, 287-288, 330, 356, 368, 371, 377, 381, 387-388, 396, 401, 410-411, 416, 419-421, 429, 431, 441, 446, 451, 456, 459, 461, 468-469, 476-478, 480-481, 488-489, 491, 499
- **GAIB drift (horizontal, doubled/repeated, on the throat or chest, garbled, faint or missing)** — 48 rows: 7, 19, 61, 66, 68, 108, 110, 126, 128, 180, 190, 216, 228, 249, 260, 277-279, 291, 301, 319, 330, 336, 346, 363, 368, 377, 380, 396-398, 406, 408, 410, 418-420, 426, 428, 430, 441, 447, 449-450, 457-458, 461, 478
- **Shirt/neckline falling open, extra chest marks or ink below the sun disc** — 42 rows: 18, 71, 76, 78, 88, 147, 162, 171, 208, 217-220, 226, 260, 270, 287, 297, 319, 321, 357-360, 366, 378, 402, 406-409, 426, 432, 436-437, 439, 446, 448, 452, 457, 460, 467
- **Arm worm mirrored (on his right forearm)** — 5 rows: 200, 436-438, 440
- **V3/V4 side profiles facing the same way (weak right profile / mirrored direction)** — 7 rows: 453-454, 463-464, 473-474, 484
- **Breather tube path mirrored or off (wrong side, ends at mouth, short curl, missing)** — 11 rows: 407, 440, 458, 476, 486-487, 489, 496-498, 500

**All rows with a note (OK-note or FLAG), 280 total:** 1, 4-5, 7, 10-11, 15, 18-20, 30, 32, 37, 47-49, 52-57, 59, 61, 63, 66, 68-69, 71, 76, 78, 83-84, 86-90, 92, 94, 97-100, 102, 108, 110, 112, 117-119, 122-123, 126, 128-130, 132-133, 135-137, 141-145, 147, 149-151, 153, 158, 160-163, 166-173, 176, 178-180, 182, 186-192, 195-198, 200-201, 203, 205-206, 208, 210, 213, 216-221, 223, 226, 228, 231, 233, 235, 238, 240-241, 243-244, 246-249, 256-260, 262, 264-265, 267, 270-271, 276-279, 281, 283-285, 287-288, 291, 293-294, 297-298, 301-303, 306-307, 311-313, 316, 319-322, 324, 330, 332, 336-340, 342-343, 345-346, 348, 352, 355-360, 363, 366, 368, 371-375, 377-378, 380-381, 387-389, 392, 396-402, 406-411, 416, 418-422, 426, 428-432, 436-441, 446-461, 463-464, 466-470, 473-474, 476-478, 480-482, 484, 486-492, 496-500

Other small things that come up in the notes: faint hand/wrist ink, blue eye-glow bleeding onto the skin in full-body shots, neck worms simplified or drawn as crescents, and the odd outfit detail differing slightly between views.

## Hero Picks

75 hero-candidate frames — the strongest images in the pack (from the QA log plus the hero list):

| Row | Look | Shot | Filename | QA |
|---|---|---|---|---|
| 177 | L18 | S2 worm-cavalry | `LAG-L18-salute-mama-officer__S2-worm-cavalry.jpg` | OK |
| 188 | L19 | S3 worm-vs-harvester | `LAG-L19-fire-trial-armor__S3-worm-vs-harvester.jpg` | OK-note |
| 196 | L20 | S1 climbing-the-worm | `LAG-L20-pan-hot-sleeveless-vest__S1-climbing-the-worm.jpg` | OK-note |
| 207 | L21 | S2 worm-shrine | `LAG-L21-desire-temple-cloak__S2-worm-shrine.jpg` | OK |
| 227 | L23 | S2 into-the-chasm | `LAG-L23-dont-fall-black-cloak__S2-into-the-chasm.jpg` | OK |
| 239 | L24 | S4 field-recording | `LAG-L24-engineers-graphic-hoodie__S4-field-recording.jpg` | OK |
| 250 | L25 | S5 server-farm-sand | `LAG-L25-designing-convo-techwear__S5-server-farm-sand.jpg` | OK |
| 261 | L27 | V1 chest-up | `LAG-L27-claim-cards-sand-robe__V1-chestup.jpg` | OK |
| 267 | L27 | S2 worm-card | `LAG-L27-claim-cards-sand-robe__S2-worm-card.jpg` | OK-note |
| 268 | L27 | S3 amphitheater-card-duel | `LAG-L27-claim-cards-sand-robe__S3-amphitheater-card-duel.jpg` | OK |
| 271 | L28 | V1 chest-up | `LAG-L28-mystic-kaftan-tent__V1-chestup.jpg` | OK-note |
| 277 | L28 | S2 night-bazaar | `LAG-L28-mystic-kaftan-tent__S2-night-bazaar.jpg` | OK-note |
| 280 | L28 | S5 caravan-dawn | `LAG-L28-mystic-kaftan-tent__S5-caravan-dawn.jpg` | OK |
| 286 | L29 | S1 infiltration | `LAG-L29-cults-red-robe__S1-infiltration.jpg` | OK |
| 289 | L29 | S4 idols-fall | `LAG-L29-cults-red-robe__S4-idols-fall.jpg` | OK |
| 296 | L30 | S1 echo-answers | `LAG-L30-echo-canyon-cargo__S1-echo-answers.jpg` | OK |
| 297 | L30 | S2 canyon-worm-run | `LAG-L30-echo-canyon-cargo__S2-canyon-worm-run.jpg` | OK-note |
| 299 | L30 | S4 petroglyph-find | `LAG-L30-echo-canyon-cargo__S4-petroglyph-find.jpg` | OK |
| 308 | L31 | S3 raid-lights | `LAG-L31-load-another-dj__S3-raid-lights.jpg` | OK |
| 309 | L31 | S4 pirate-ship-set | `LAG-L31-load-another-dj__S4-pirate-ship-set.jpg` | OK |
| 310 | L31 | S5 sunrise-set | `LAG-L31-load-another-dj__S5-sunrise-set.jpg` | OK |
| 311 | L32 | V1 chest-up | `LAG-L32-quick-listen-linen__V1-chestup.jpg` | OK-note |
| 316 | L32 | S1 listening-to-dunes | `LAG-L32-quick-listen-linen__S1-listening-to-dunes.jpg` | OK-note |
| 318 | L32 | S3 the-mediator | `LAG-L32-quick-listen-linen__S3-the-mediator.jpg` | OK |
| 326 | L33 | S1 crystal-duel | `LAG-L33-crystal-blade-mirror__S1-crystal-duel.jpg` | OK |
| 327 | L33 | S2 worms-tooth | `LAG-L33-crystal-blade-mirror__S2-worms-tooth.jpg` | OK |
| 328 | L33 | S3 cutting-through | `LAG-L33-crystal-blade-mirror__S3-cutting-through.jpg` | OK |
| 331 | L34 | V1 chest-up | `LAG-L34-keep-simple-white-tee__V1-chestup.jpg` | OK |
| 341 | L35 | V1 chest-up | `LAG-L35-hope-shearling-night__V1-chestup.jpg` | OK |
| 346 | L35 | S1 worm-under-stars | `LAG-L35-hope-shearling-night__S1-worm-under-stars.jpg` | OK-note |
| 347 | L35 | S2 night-caravan | `LAG-L35-hope-shearling-night__S2-night-caravan.jpg` | OK |
| 351 | L36 | V1 chest-up | `LAG-L36-jung-library-tweed__V1-chestup.jpg` | OK |
| 357 | L36 | S2 red-book | `LAG-L36-jung-library-tweed__S2-red-book.jpg` | OK-note |
| 361 | L37 | V1 chest-up | `LAG-L37-archetypes-black-coat__V1-chestup.jpg` | OK |
| 367 | L37 | S2 shadow-war | `LAG-L37-archetypes-black-coat__S2-shadow-war.jpg` | OK |
| 369 | L37 | S4 masks-in-station | `LAG-L37-archetypes-black-coat__S4-masks-in-station.jpg` | OK |
| 370 | L37 | S5 integration | `LAG-L37-archetypes-black-coat__S5-integration.jpg` | OK |
| 376 | L38 | S1 infinite-staircase | `LAG-L38-tail-recursion-monochrome__S1-infinite-staircase.jpg` | OK |
| 379 | L38 | S4 fractal-battle | `LAG-L38-tail-recursion-monochrome__S4-fractal-battle.jpg` | OK |
| 386 | L39 | S1 shadow-escapes | `LAG-L39-shadow-work-hoodie__S1-shadow-escapes.jpg` | OK |
| 390 | L39 | S5 city-of-shadows | `LAG-L39-shadow-work-hoodie__S5-city-of-shadows.jpg` | OK |
| 396 | L40 | S1 mirror-interrogation | `LAG-L40-shook-rain-leather__S1-mirror-interrogation.jpg` | OK-note |
| 397 | L40 | S2 rain-chase | `LAG-L40-shook-rain-leather__S2-rain-chase.jpg` | OK-note |
| 398 | L40 | S3 alley-fight | `LAG-L40-shook-rain-leather__S3-alley-fight.jpg` | OK-note |
| 400 | L40 | S5 puddle-mirror | `LAG-L40-shook-rain-leather__S5-puddle-mirror.jpg` | OK-note |
| 407 | L41 | S2 desert-reclaims | `LAG-L41-who-let-you-in-mansion__S2-desert-reclaims.jpg` | OK-note |
| 410 | L41 | S5 sunset-terrace | `LAG-L41-who-let-you-in-mansion__S5-sunset-terrace.jpg` | OK-note |
| 416 | L42 | S1 out-of-storm | `LAG-L42-knees-sandstorm-torn-cloak__S1-out-of-storm.jpg` | OK-note |
| 420 | L42 | S5 storm-clears | `LAG-L42-knees-sandstorm-torn-cloak__S5-storm-clears.jpg` | OK-note |
| 427 | L43 | S2 midnight-cemetery | `LAG-L43-doctor-voodoo-tophat__S2-midnight-cemetery.jpg` | OK |
| 429 | L43 | S4 second-line | `LAG-L43-doctor-voodoo-tophat__S4-second-line.jpg` | OK-note |
| 438 | L44 | S3 apothecary-raid | `LAG-L44-vudology-apothecary__S3-apothecary-raid.jpg` | OK-note |
| 439 | L44 | S4 the-reaction | `LAG-L44-vudology-apothecary__S4-the-reaction.jpg` | OK-note |
| 440 | L44 | S5 desert-bloom | `LAG-L44-vudology-apothecary__S5-desert-bloom.jpg` | OK-note |
| 446 | L45 | S1 the-banquet | `LAG-L45-fill-cup-velvet__S1-the-banquet.jpg` | OK-note |
| 456 | L46 | S1 desert-road-trip | `LAG-L46-riz-convertible-linen__S1-desert-road-trip.jpg` | OK-note |
| 458 | L46 | S3 sand-rally | `LAG-L46-riz-convertible-linen__S3-sand-rally.jpg` | OK-note |
| 459 | L46 | S4 worm-crossing | `LAG-L46-riz-convertible-linen__S4-worm-crossing.jpg` | OK-note |
| 466 | L47 | S1 sigil-ritual | `LAG-L47-chaos-magic-brocade__S1-sigil-ritual.jpg` | OK-note |
| 467 | L47 | S2 chaos-unleashed | `LAG-L47-chaos-magic-brocade__S2-chaos-unleashed.jpg` | OK-note |
| 468 | L47 | S3 gravity-flip | `LAG-L47-chaos-magic-brocade__S3-gravity-flip.jpg` | OK-note |
| 470 | L47 | S5 magic-aftermath | `LAG-L47-chaos-magic-brocade__S5-magic-aftermath.jpg` | OK-note |
| 476 | L48 | S1 the-choice | `LAG-L48-two-doors-desert-robe__S1-the-choice.jpg` | OK-note |
| 477 | L48 | S2 worm-of-stars | `LAG-L48-two-doors-desert-robe__S2-worm-of-stars.jpg` | OK-note |
| 478 | L48 | S3 door-guardians | `LAG-L48-two-doors-desert-robe__S3-door-guardians.jpg` | OK-note |
| 479 | L48 | S4 field-of-doors | `LAG-L48-two-doors-desert-robe__S4-field-of-doors.jpg` | OK |
| 486 | L49 | S1 block-concert | `LAG-L49-mic-street-signature__S1-block-concert.jpg` | OK-note |
| 487 | L49 | S2 worm-under-city | `LAG-L49-mic-street-signature__S2-worm-under-city.jpg` | OK-note |
| 488 | L49 | S3 street-battle | `LAG-L49-mic-street-signature__S3-street-battle.jpg` | OK-note |
| 489 | L49 | S4 desert-arrival | `LAG-L49-mic-street-signature__S4-desert-arrival.jpg` | OK-note |
| 496 | L50 | S1 the-final-ride | `LAG-L50-signal-mandala-finale__S1-the-final-ride.jpg` | OK-note |
| 497 | L50 | S2 signal-raised | `LAG-L50-signal-mandala-finale__S2-signal-raised.jpg` | OK-note |
| 498 | L50 | S3 final-duel | `LAG-L50-signal-mandala-finale__S3-final-duel.jpg` | OK-note |
| 499 | L50 | S4 rebuilding | `LAG-L50-signal-mandala-finale__S4-rebuilding.jpg` | OK-note |
| 500 | L50 | S5 walk-into-dunes | `LAG-L50-signal-mandala-finale__S5-walk-into-dunes.jpg` | OK-note |

Several hero picks are OK-note — strong compositions with a small drift (often a mirrored piercing); check the CSV note before using one as a close-up.

---
Questions about any image: look up its row in LEGEND-500.csv, open the zip named in `zip_name`, and check the contact sheet first.
