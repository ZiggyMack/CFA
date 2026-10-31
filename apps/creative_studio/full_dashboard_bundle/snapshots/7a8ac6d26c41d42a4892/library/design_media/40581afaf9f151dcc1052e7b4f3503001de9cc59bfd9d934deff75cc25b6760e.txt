# GROK-HD-DROP-20261009B: Hon Dolo handoff for Nova

From Ziggy to Nova. Built 2026-10-09 by Grok Bot. This drop covers everything made since the last drop (`GROK-HD-MASTER-20261009_part1of2.zip` / `part2of2.zip` in `/workspace/hd-sb/return/`).

> **Nothing in this drop is approved.** Every file has one of these statuses: **KEEPER-candidate (needs_user_review)**, **SUPERSEDED**, **DRAFT**, **REJECTED** or **PROPOSAL**. Ziggy makes the final calls.

## 1. How to unpack

The drop is split into 4 zip parts, each under 24 MB. Unzip all of them into the same folder and they combine into `GROK-HD-DROP-20261009B/`. Start with this README. `FILE_INDEX.csv` lists every file with its sha256, size, status, collection and zip part.

| Part | Contents |
|---|---|
| part1of4 | Docs (this README, PDF, FILE_INDEX.csv), benchmark kit part 1, grill refs, head anchors, earlier mouth tests, hand tattoo refs, identity inspiration |
| part2of4 | Benchmark kit part 2, outfit inventory (LOOKS.csv + contact sheets), superseded VIS-HD v001 |
| part3of4 | Benchmark kit refs update (MOUTH-LOCK-VIS-HD v003, 50 shapes), superseded VIS-HD v002 |
| part4of4 | **CURRENT mouth set VIS-HD v003 (50 shapes)** |

## 2. What happened today

1. **Benchmark kit.** We built `NOVA-IMG-BENCH-20261009` for Nova to run: a plan, prompts, Grok baselines, a scoring guide, a ledger and compare tools. It tests which image tool best holds the locked characters: face, small text tattoos, piercings, grill/teeth and which side props sit on. Its two zips are included unchanged. After those zips were made, the unzipped kit got a new `refs/MOUTH-LOCK-VIS-HD/` folder holding the v003 mouth set (50 shapes + manifest). That folder ships here as a separate update. Copy it into `NOVA-IMG-BENCH-20261009/refs/` after unzipping the kit.
2. **Why we did the mouth lock.** In ComfyUI, renders kept losing Hon Dolo's grill. Teeth came out natural, all gold or all silver. So we built a fixed mouth library: one close-up macro per mouth shape, all with a consistent grill. These become the reference that later head and body work is checked against.
3. **Ziggy's four-gold grill correction.** v001 used an older grill with two gold canines. Ziggy corrected it with his own reference (`03_GRILL_REF/GRILL-REF-4GOLD-ziggy.jpg`). The four-gold test `GRILL-LOCK-4GOLD-v2.jpg` passed his check and became the grill-lock reference. v002 was the first set made with the four-gold grill.
4. **12 shapes became 50.** v002 had 12 shapes. v003 keeps 6 of them unchanged (01, 02, 03, 09, 11, 12), regenerates 6 (04-08, 10) and adds 38 new shapes (13-50). Every v003 shape used one ref only: the grill master VIS-HD-03 AH (`2f74c026...e9a0`). Each shape got at most 2 rerolls.
5. **Head-library plan.** We tried head anchors r1-r6 and an iced-anchor proposal (see section 4). No head anchor for external_off is accepted yet. The head-library counts are in section 6.

## 3. Grill rule and grill states

**Grill rule (Hon Dolo):** exactly **four gold upper caps**: the lateral incisors and the **SHORT** canines. The two upper central incisors and the other upper teeth stay natural white. The lower row is silver. Piercings: **one hoop in each nostril** (no septum ring) and **two plain hoops, one at each bottom-lip corner**.

| Grill state | Meaning | Where it stands |
|---|---|---|
| `external_off` | No removable external grill. The base four-gold / silver-lower setup shows | VIS-HD v003 (50 mouth macros) is the keeper-candidate mouth set. **No external_off head anchor is accepted yet** |
| `external_iced_on` | Iced external grill worn over the teeth | Starting inspiration: r5 `eb5e80bb` (not final). Anchor proposal `HEAD-HD-ICED-ANCHOR-r1` (`8ab1485e`) is waiting on Ziggy: the fangs were shortened, maybe too much |

Known spec mismatch: the benchmark kit prompts and scoring guide (written earlier) say "two hoops in the RIGHT nostril". The current rule is one hoop in each nostril. The kit's PLAN.md already flags this for Ziggy to confirm. When scoring, note which spec you used.

## 4. Head anchors and earlier mouth tests

| Asset | Label | Status | Note |
|---|---|---|---|
| `d5405fd7` | HEAD-r1 | REJECTED | Head anchor r1: no tattoos |
| `dfe76372` | HEAD-r2 | REJECTED | Head anchor r2: eyebrow rings, reads too young |
| `203f5ce7` | HEAD-r3 | REJECTED | Head anchor r3: ears swapped, brow bar |
| `03406910` | HEAD-r4 | DRAFT | Head anchor r4: identity fixed, but iced grill and only one nostril hoop |
| `eb5e80bb` | HEAD-r5 | DRAFT | Head r5: Ziggy's STARTING INSPIRATION for the external_iced_on set. Not final |
| `26399aba` | HEAD-r6 | REJECTED | Head anchor r6: mixed grills, white lower row |
| `8ab1485e` | HEAD-HD-ICED-ANCHOR-r1 | PROPOSAL | Iced anchor proposal r1, waiting on Ziggy: fangs shortened, maybe too much |
| `46eb8f89` | MOUTHTEST | REJECTED | Early mouth test: face too zoomed-out. Superseded |
| `f7ef3d3c` | MOUTHTEST | REJECTED | Early mouth test: face too zoomed-out. Superseded |
| `5c924e75` | MOUTHTEST | REJECTED | Early mouth test: 6 gold teeth (rule is exactly 4). Superseded |
| `91ef0034` | GRILL-LOCK-4GOLD-v2 | KEEPER-candidate (needs_user_review) | The four-gold test Ziggy accepted. Same bytes as `03_GRILL_REF/GRILL-LOCK-4GOLD-v2.jpg`, so it is not copied twice. Superseded as a mouth test by the v003 grill master |

Identity inspiration photo: `08_IDENTITY_INSPIRATION/` (`9e2c260b...`, also in CFA as HD-DROP-71cad143227a / HD-PINSTRIPE-01-chest-up.jpg). Use it **only** for the face, the curls and the optional grill.

## 5. Mouth shapes: VIS-HD v003 (50, external_off)

All 50 are **KEEPER-candidate (needs_user_review)**. "Key" marks the **PROPOSED** 20 key states (PROPOSAL, Ziggy has not confirmed them). QA flags come from the v003 README/manifest.

| # | Shape | Key state (PROPOSAL) | QA |
|---|---|---|---|
| 01 | REST | KEY | ok: good |
| 02 | MBP | KEY | ok: good, both nostril hoops |
| 03 | AH | KEY | ok: good, grill master |
| 04 | EE | KEY | ok: good grill; lips moderately wide |
| 05 | OH | KEY | ok: good grill; open oval more than tight O (r1 5937a023 rejected: 6 gold) |
| 06 | OO-W | KEY | ok: good |
| 07 | F-V | KEY | weak: upper teeth rest on lower lip; lip not fully tucked |
| 08 | L-TH | KEY | ok: good, tongue tip at upper teeth |
| 09 | S-T-K | KEY | ok: good |
| 10 | CH-SH | KEY | weak: grill good; lip funnel weak (r1 01329c40 rejected: 6 gold) |
| 11 | GRIN | KEY | ok: good |
| 12 | SHOUT | KEY | ok: good |
| 13 | KISS-PUCKER | KEY | ok: good |
| 14 | BLOW-KISS |  | ok: good |
| 15 | BITE-LOWER-LIP |  | ok: good |
| 16 | BITE-UPPER-LIP |  | FAIL: FAIL: lip bite not achieved and gold laterals/canines rendered silver; both tries failed (r1 0e9e4b9a all-silver) |
| 17 | LIPS-PRESSED-THIN |  | weak: lips closed but not very thin |
| 18 | LIP-ROLL-IN |  | weak: weak: lips closed, not rolled in |
| 19 | SMIRK-LEFT | KEY | ok: good |
| 20 | SMIRK-RIGHT |  | weak: weak: almost neutral |
| 21 | SNEER | KEY | ok: good |
| 22 | SNARL |  | weak: grill good; snarl weak (upper lip not pulled high) |
| 23 | GRIMACE |  | ok: good grill; moderate grimace |
| 24 | CLENCHED-JAW |  | ok: good |
| 25 | JAW-DROP | KEY | ok: good |
| 26 | SMALL-O |  | ok: good |
| 27 | BIG-LAUGH | KEY | ok: good |
| 28 | CHUCKLE |  | ok: good |
| 29 | CLOSED-SMILE | KEY | ok: good |
| 30 | HALF-SMILE |  | ok: good grill; lower teeth hidden |
| 31 | POUT |  | ok: good |
| 32 | FROWN |  | weak: mild frown |
| 33 | LIP-LICK |  | weak: weak: tongue sweeps inside mouth, not across upper lip |
| 34 | TONGUE-OUT | KEY | ok: good |
| 35 | TONGUE-IN-CHEEK |  | weak: weak: tongue pokes between lips instead of cheek bulge |
| 36 | WHISTLE |  | ok: good |
| 37 | PUFFED-CHEEKS |  | weak: weak: cheeks not visibly puffed (r1 72bbaa25 rejected: one nostril hoop, no stubble) |
| 38 | TSK |  | ok: good |
| 39 | YAWN |  | ok: good |
| 40 | WHISPER-SH |  | weak: grill good; lips not rounded forward |
| 41 | R-SOUND |  | weak: grill good; lip rounding weak |
| 42 | Y-SOUND |  | ok: good |
| 43 | RAP-MID-WORD | KEY | weak: grill good; shape symmetric, not lopsided |
| 44 | YEAH-ADLIB |  | ok: good |
| 45 | GRIT-LIPS-BACK |  | ok: good |
| 46 | KISS-TEETH |  | FAIL: DRIFT: visible side teeth natural white where gold laterals/canine should show |
| 47 | CHAIN-BITE |  | ok: good |
| 48 | EXHALE |  | weak: grill good; only one nostril hoop in frame |
| 49 | HUM |  | ok: good |
| 50 | SING-VOWEL |  | ok: good |

**Proposed 20 key states (PROPOSAL):** 01 REST, 02 MBP, 03 AH, 04 EE, 05 OH, 06 OO-W, 07 F-V, 08 L-TH, 09 S-T-K, 10 CH-SH, 11 GRIN, 12 SHOUT, 13 KISS-PUCKER, 19 SMIRK-LEFT, 21 SNEER, 25 JAW-DROP, 27 BIG-LAUGH, 29 CLOSED-SMILE, 34 TONGUE-OUT, 43 RAP-MID-WORD.

Note: 3 of the proposed key states have weak picks right now: 07 F-V, 10 CH-SH and 43 RAP-MID-WORD. They may need a reroll before head batches use them.

## 6. Counts (keep these collections separate)

| Collection | Count | Notes |
|---|---|---|
| Mouth macros (VIS-HD) | 50 | Separate collection. v003 exists for external_off |
| Head baseline, per grill state | 130 | 50 fronts (one per mouth shape) + 4 extra views x 20 key states (80) |
| Head pitch expansion, per grill state | +40 (130 -> 170) | Pitch up + pitch down for the 20 key states. **Tracked separately** from the 130 |
| Head totals, both grill states | 260 baseline / 340 with pitch | 2 x 130 / 2 x 170 |
| Prop-mouth shots | 50 | Separate collection. Not started |
| Outfit looks | 70 | Tier A 17 + Tier B 18 = 35 proposed core (to regrill). Tier C 35 are outfit text only. PROPOSAL |

## 7. Hand tattoo refs (Princess Leigh card)

- `64af4db6...`: hearts sheet. `00da907b...`: spades sheet. `00b6dd3f...`: hand-photo example (hearts, card-in-tattoo layout, gold rings, white fur).
- Ledger default: **CHARACTER-RIGHT hand**.
- Hearts vs spades, and the two layouts (sheet vs card-in-tattoo), are **separate exploration options**. Do not combine them. Ziggy still has to pick the side and the suit. All PROPOSAL.

## 8. Pending

1. **external_off head anchor.** None accepted yet. Needed before head batches start.
2. **Iced anchor fang length.** Ziggy to decide on `HEAD-HD-ICED-ANCHOR-r1` (`8ab1485e`): are the fangs too short?
3. **Head batches.** 130 per grill state, plus the 40 pitch shots tracked separately. Not started.
4. **35-look regrill.** Tier A + Tier B from LOOKS.csv, redone with the four-gold grill. Not started.
5. **50 prop-mouth shots.** Separate collection. Not started.
6. **Hand tattoo side/suit.** Default is CHARACTER-RIGHT. Ziggy picks hearts or spades and a layout.
7. **Key states.** Ziggy to confirm or adjust the 20 proposed key states.
8. **Nostril spec.** Confirm that the benchmark kit should use one hoop per nostril (see section 3).

## 9. Known failures and weak spots

- **VIS-HD-16 BITE-UPPER-LIP: FAIL.** The lip bite never happened, and the gold laterals/canines came out silver. Both tries failed (r1 `0e9e4b9a` was all silver).
- **VIS-HD-46 KISS-TEETH: grill drift.** The visible side teeth are natural white where the gold laterals/canine should show.
- **Weak poses (grill mostly fine, shape is weak):** 07 F-V, 10 CH-SH, 17 LIPS-PRESSED-THIN, 18 LIP-ROLL-IN, 20 SMIRK-RIGHT, 22 SNARL, 32 FROWN, 33 LIP-LICK, 35 TONGUE-IN-CHEEK, 37 PUFFED-CHEEKS, 40 WHISPER-SH, 41 R-SOUND, 43 RAP-MID-WORD, 48 EXHALE (only one nostril hoop in frame).
- In v003 generation, gold-count drift (6 gold) was caught and rerolled on 05 and 10. 37 r1 was rejected for having one nostril hoop and no stubble.
- The v003 README calls the grill lock "Ziggy approved". That means Ziggy signed off on the grill rule. It does not approve any image: every v003 file is still needs_user_review.
- ComfyUI losing the grill is the root problem. Check the grill on every new render against `03_GRILL_REF/`.

## 10. Status of every file

Paths are relative to `GROK-HD-DROP-20261009B/`. The 50 MOUTH-LOCK update images are collapsed into one row here; FILE_INDEX.csv lists each one.

| Path | What it is | Status | Part |
|---|---|---|---|
| `NOVA_README.md` / `NOVA_README.pdf` | This handoff doc | PROPOSAL | 1 |
| `FILE_INDEX.csv` | Path, sha256, size, status, collection, part for every file | PROPOSAL | 1 |
| `01_BENCHMARK_KIT/NOVA-IMG-BENCH-20261009_part1of2.zip` | Benchmark kit part 1 (plan, prompts, baselines, ledger, compare tools, HD/LAG/PROBE refs), included as-is | PROPOSAL | 1 |
| `01_BENCHMARK_KIT/NOVA-IMG-BENCH-20261009_part2of2.zip` | Benchmark kit part 2 (BOSS-001..010 refs), included as-is | PROPOSAL | 2 |
| `01_BENCHMARK_KIT/UPDATE_refs_MOUTH-LOCK-VIS-HD_v003/VIS-HD-01..50_*.jpg` (50 files) | Kit refs update: v003 mouth shapes (same bytes as v003 01_VISEMES) | KEEPER-candidate (needs_user_review) | 3 |
| `01_BENCHMARK_KIT/UPDATE_refs_MOUTH-LOCK-VIS-HD_v003/manifest.csv` | Update to kit refs/MOUTH-LOCK-VIS-HD: manifest (v003, 50 shapes) | KEEPER-candidate (needs_user_review) | 3 |
| `02_MOUTH_VISEMES/GROK-HD-20261009_VIS-HD_v003.zip` | CURRENT mouth viseme/expression set v003, 50 shapes, external_off, four-gold grill; README has drift notes; includes 02_REJECTED rerolls + 9 contact sheets | KEEPER-candidate (needs_user_review) | 4 |
| `03_GRILL_REF/GRILL-REF-4GOLD-ziggy.jpg` | Ziggy's own four-gold grill reference (input) | KEEPER-candidate (needs_user_review) | 1 |
| `03_GRILL_REF/GRILL-LOCK-4GOLD-v2.jpg` | Four-gold grill test that Ziggy accepted as the grill-lock reference (= asset 91ef0034). As a mouth test it is superseded by the v003 grill master | KEEPER-candidate (needs_user_review) | 1 |
| `03_GRILL_REF/GRILL-MASTER_VIS-HD-03_AH_2f74c026c40fdc16aea74c9abd8a0943d3bccf8f99a591a3f915230e6d93a9e0.jpg` | Grill master used as the only ref for v003 (= VIS-HD-03 AH) | KEEPER-candidate (needs_user_review) | 1 |
| `04_HEAD_ANCHORS/HEAD-r1_REJECTED_d5405fd7bf894f98f622bfd2df6c083a53ddd9b335172e30837658ee39ba37e9.jpg` | Head anchor r1: no tattoos | REJECTED | 1 |
| `04_HEAD_ANCHORS/HEAD-r2_REJECTED_dfe763724b08c1145e4ba211740f1be0d7c8d4243393ab74e664743d0b9e8629.jpg` | Head anchor r2: eyebrow rings, reads too young | REJECTED | 1 |
| `04_HEAD_ANCHORS/HEAD-r3_REJECTED_203f5ce7b9c29638095537cb85cef8a6e1be7e8e154fd5490de93400697d5b30.jpg` | Head anchor r3: ears swapped, brow bar | REJECTED | 1 |
| `04_HEAD_ANCHORS/HEAD-r4_DRAFT_03406910c793808373b66cfc32c8f140096730b616d414da46eac31aba53d607.jpg` | Head anchor r4: identity fixed, but iced grill and only one nostril hoop | DRAFT | 1 |
| `04_HEAD_ANCHORS/HEAD-r5_DRAFT_eb5e80bb7a9209cb6276985aba6578ea2a7bf4f0ef84574509988c7cf8eb7f56.jpg` | Head r5: Ziggy's STARTING INSPIRATION for the external_iced_on set. Not final | DRAFT | 1 |
| `04_HEAD_ANCHORS/HEAD-r6_REJECTED_26399aba6d079d8104dd6f7aba233bb42801cc24113a5c3748862c0de4e8933c.jpg` | Head anchor r6: mixed grills, white lower row | REJECTED | 1 |
| `04_HEAD_ANCHORS/HEAD-HD-ICED-ANCHOR-r1_PROPOSAL_8ab1485e479abc0a3b181df59aa754fc3eaf751edce8507cd3379d193cd77e0c.jpg` | Iced anchor proposal r1, waiting on Ziggy: fangs shortened, maybe too much | PROPOSAL | 1 |
| `05_MOUTH_TESTS_SUPERSEDED/MOUTHTEST_REJECTED_46eb8f89afc0ef39af6866f1cb8555c6125ebd328bba8facf785799ea9c6f76b.jpg` | Early mouth test: face too zoomed-out. Superseded | REJECTED | 1 |
| `05_MOUTH_TESTS_SUPERSEDED/MOUTHTEST_REJECTED_f7ef3d3c26a64d8d48e91c09a58f4749281855c62fb112f8ace6775c2d5773ed.jpg` | Early mouth test: face too zoomed-out. Superseded | REJECTED | 1 |
| `05_MOUTH_TESTS_SUPERSEDED/MOUTHTEST_REJECTED_5c924e75f1ed10f9f7e6e65974ed347649bf8a8f8ebfe9bc08672f855aec3389.jpg` | Early mouth test: 6 gold teeth (rule is exactly 4). Superseded | REJECTED | 1 |
| `06_OUTFIT_INVENTORY/LOOKS.csv` | Outfit inventory: 70 looks (Tier A 17 + Tier B 18 = 35 proposed core; Tier C 35 outfit-text only) | PROPOSAL | 2 |
| `06_OUTFIT_INVENTORY/_inv/b_full.jpg` | Outfit inventory contact sheet (b_full) | PROPOSAL | 2 |
| `06_OUTFIT_INVENTORY/_inv/drip_a.jpg` | Outfit inventory contact sheet (drip_a) | PROPOSAL | 2 |
| `06_OUTFIT_INVENTORY/_inv/drip_b.jpg` | Outfit inventory contact sheet (drip_b) | PROPOSAL | 2 |
| `06_OUTFIT_INVENTORY/_inv/drip_u.jpg` | Outfit inventory contact sheet (drip_u) | PROPOSAL | 2 |
| `06_OUTFIT_INVENTORY/_inv/early_0.jpg` | Outfit inventory contact sheet (early_0) | PROPOSAL | 2 |
| `06_OUTFIT_INVENTORY/_inv/early_1.jpg` | Outfit inventory contact sheet (early_1) | PROPOSAL | 2 |
| `06_OUTFIT_INVENTORY/_inv/early_2.jpg` | Outfit inventory contact sheet (early_2) | PROPOSAL | 2 |
| `06_OUTFIT_INVENTORY/_inv/early_3.jpg` | Outfit inventory contact sheet (early_3) | PROPOSAL | 2 |
| `06_OUTFIT_INVENTORY/_inv/other.jpg` | Outfit inventory contact sheet (other) | PROPOSAL | 2 |
| `06_OUTFIT_INVENTORY/_inv/rollout_a.jpg` | Outfit inventory contact sheet (rollout_a) | PROPOSAL | 2 |
| `06_OUTFIT_INVENTORY/_inv/rollout_b.jpg` | Outfit inventory contact sheet (rollout_b) | PROPOSAL | 2 |
| `07_HAND_TATTOO_REFS/TATTOO-HAND_hearts-sheet_64af4db643488299457b5a22424a8dd82a92abf39db29ea120e1bbb19ae12c66.jpg` | Princess Leigh card hand tattoo ref: HEARTS sheet. Exploration option only, not combined with the others | PROPOSAL | 1 |
| `07_HAND_TATTOO_REFS/TATTOO-HAND_spades-sheet_00da907bf9fdabfb7fba309bbd8b8fe96c35bdaddba9d81878aa164bb36bc90e.jpg` | Princess Leigh card hand tattoo ref: SPADES sheet. Exploration option only, not combined with the others | PROPOSAL | 1 |
| `07_HAND_TATTOO_REFS/TATTOO-HAND_hand-photo-hearts-card-in-tattoo_00b6dd3ff9a6193380994005a10715aec327e7d3466a974a0be4457c03aeaa4e.jpg` | Princess Leigh hand-photo example: hearts, card-in-tattoo layout, gold rings, white fur. Exploration option only, not combined with the others | PROPOSAL | 1 |
| `08_IDENTITY_INSPIRATION/IDENTITY-INSPIRATION_9e2c260bfe137683aa276a3d484f94a895f02939db5bcf598db8da698a301209.jpg` | Identity inspiration photo (input; also in CFA as HD-DROP-71cad143227a / HD-PINSTRIPE-01-chest-up.jpg). Use for face, curls and optional grill only | KEEPER-candidate (needs_user_review) | 1 |
| `90_SUPERSEDED/GROK-HD-20261009_VIS-HD_v001.zip` | Mouth set v001 (12 shapes), old two-gold-canine grill | SUPERSEDED | 2 |
| `90_SUPERSEDED/GROK-HD-20261009_VIS-HD_v002.zip` | Mouth set v002 (12 shapes), first four-gold grill; replaced by v003 | SUPERSEDED | 3 |

### Not in this drop (by design)

- Loose v001/v002/v003 contact sheets sitting next to the zips in `return/`: the zips already contain their sheets (v001 CONTACT, v002 and v003 SHEET pages).
- Build scripts (`hd-sb/vis_v003/`, `hd-sb/regrill/build_looks.py`) and `/workspace/cosmic-avatar/` (a separate project).
