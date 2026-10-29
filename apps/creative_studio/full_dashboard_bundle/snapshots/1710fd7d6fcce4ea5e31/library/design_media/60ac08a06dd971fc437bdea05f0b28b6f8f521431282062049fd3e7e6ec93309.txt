# NOVA-IMG-BENCH-20261009 - Image benchmark plan (stills only)

Prepared 2026-10-09 by Grok Bot for Nova (teammate of Ziggy). **Every result in this kit is `needs_user_review`. Nothing is approved.** No outside-tool results are included; columns for tools A and B are empty until Nova runs them.

## 1. Goal
Ziggy is building music-video characters and animating them later (Google Flow / Veo, Gemini). Before committing to an image tool, he wants to know:

1. **Fidelity:** which tool best holds his locked characters - face identity, small text tattoos ("eye", "know", "AL", "G-A-I-B"), piercings, grills/teeth, and props on the correct side (character-left vs character-right).
2. **Refusals:** which tool refuses which characters. Background: Gemini refused to *animate* the jeweled slug-lord crime boss (image_25.png, probably because it read as a copy of a famous film crime lord), then also refused the gecko-frog redesign V09; a toned-down hippo music-label boss replaced it. Whether the *image* generators refuse these is unknown - that is what the PROBE tests measure.

## 2. Contenders (verified 2026-10-09 via official pages)
| Lane | Product | Where to use it | Notes |
|---|---|---|---|
| **A** | **Google Nano Banana** family (Gemini image models). Current names: **Nano Banana 2** (Gemini 3.1 Flash Image), **Nano Banana Pro** (Gemini 3 Pro Image), Nano Banana 2 Lite (Gemini 3.1 Flash-Lite Image). | **Gemini app** (gemini.google.com -> Images / Create images; Nano Banana 2 is used when the Gemini model is Flash or Pro; Nano Banana Pro via "Redo with Pro" on paid Google AI plans). **Google AI Studio** (aistudio.google.com, pick Gemini 3 Pro Image / Nano Banana Pro). **Flow** (Nano Banana Pro for image creation on paid plans). | Lite is not designed for multiple reference images - do not use it. Record which model produced each image in `tool_version_or_mode`. Recommended: Nano Banana Pro (AI Studio or Gemini app Redo with Pro); if only Nano Banana 2 is available, use it consistently and log it. |
| **B** | **OpenAI ChatGPT Images 2.5** (released 2026-09-08). API models: gpt-image-2.5-flare, gpt-image-2.5-sunburst. | **ChatGPT** (chatgpt.com / desktop / mobile, all tiers) - upload refs and paste the prompt in a new chat. API is optional and not needed for this kit. | Log "ChatGPT Images 2.5 (ChatGPT app)" or the API model id in `tool_version_or_mode`. |
| **C** | **Grok Bot** in-house renders (baseline) | Already exist - copied into `BASELINES/`. No new generation. | Ziggy scores these; scores left blank. |
| (D, optional) | Midjourney | midjourney.com | Optional 4th lane only. Not built into this kit (no folders/rows). If Nova adds it, copy the A rows, use tool `D_MIDJOURNEY`, and note that its reference-image features work differently, so the same-refs rule may not apply exactly. |

Sources: support.google.com/gemini/answer/14286560 (Gemini Apps Help: Nano Banana models), blog.google "Where to use Nano Banana Pro", aistudio.google.com/models/nano-banana, openai.com/index/introducing-chatgpt-images-2-5. Product menus change often - if a menu name differs on the day, log what you actually used. No capability claims or scores are made here.

## 3. Rules (apply to every test, every tool)
1. **Same refs + same prompt to every tool.** Upload exactly the files listed on the prompt card, in the listed order, from `refs/<TEST-ID>/`. Paste the PROMPT block verbatim. Do not edit the prompt for one tool only. Files starting `CTX_` are context for scoring - never upload them.
2. **Fresh chat per test** (new conversation in Gemini/ChatGPT, new session in AI Studio/Flow). Don't carry characters between tests.
3. **Max 2 rerolls** (3 attempts total) per test per tool. A reroll = regenerate / resend the same prompt in a fresh chat. Save and log every attempt, not just the best one.
4. **Log every refusal verbatim.** Copy the exact refusal text into `refusal_text`, set `refused=Y`, and save a screenshot as `<TEST-ID>_<TOOL>_a<N>_REFUSAL.png`. A refusal counts as an attempt. Do not soften or rephrase the prompt to get past a refusal - that changes the test. (If you want to explore a softened version, log it as a separate row with `notes=SOFTENED` and the changed text.) Also log partial refusals, e.g. "made the image but removed the tattoos", in `notes`.
5. **No celebrity likeness.** All characters are original. Prompts say "NOT a celebrity". Don't add real names, film names or franchise names. Filenames were renamed to drop franchise words. (The old "Nelly-style" eyebrow wording was replaced with a plain description for the same reason.)
6. **Nothing is approved.** Every ledger row stays `status=needs_user_review`. Nova records; Ziggy decides.
7. **Don't fabricate.** If a tool wasn't run, leave the row empty. Don't fill scores for images you didn't see.
8. Keep download quality: use the tool's "download full size" option. Save as PNG if offered, otherwise keep the original format but use the same base name.

## 4. Test list (18 tests)
| # | Test ID | Subject | Uploads | Flag |
|---|---|---|---|---|
| 1 | HD-01 | Hon Dolo (main) - pinstripe look | 5 | calibration |
| 2 | HD-02 | Hon Dolo (main) - saloon look | 5 | calibration |
| 3 | HD-03 | Hon Dolo (main) - yellow look | 6 | calibration |
| 4 | HD-04 | Hon Dolo (main) - cream look | 6 |  |
| 5 | LAG-01 | Lisan Al Gaib (Hon Dolo recast) - signature look 01 | 2 |  |
| 6 | BOSS-001 | BOSS-001 River-hippo studio mogul | 1 |  |
| 7 | BOSS-002 | BOSS-002 Gecko-frog velvet aristocrat | 1 |  |
| 8 | BOSS-003 | BOSS-003 Slug magnate, velvet dais | 2 |  |
| 9 | BOSS-004 | BOSS-004 Pangolin ledger financier | 1 |  |
| 10 | BOSS-005 | BOSS-005 Catfish neon kingpin | 1 |  |
| 11 | BOSS-006 | BOSS-006 Rhino cyber warlord | 2 |  |
| 12 | BOSS-007 | BOSS-007 Axolotl label matriarch | 1 |  |
| 13 | BOSS-008 | BOSS-008 Croc bookie, brass eye | 1 |  |
| 14 | BOSS-009 | BOSS-009 Toad spaceport barkeep | 2 |  |
| 15 | BOSS-010 | BOSS-010 Walrus starship mogul | 1 |  |
| 16 | PROBE-01 | Slug-lord original (image_25 equivalent) - KNOWN_REFUSED_BY_GEMINI_ANIMATION | 1 | KNOWN_REFUSED_BY_GEMINI_ANIMATION (image-gen status unknown) |
| 17 | PROBE-02 | Gecko-frog mob boss V09 - KNOWN_REFUSED_BY_GEMINI_ANIMATION | 2 | KNOWN_REFUSED_BY_GEMINI_ANIMATION (image-gen status unknown) |
| 18 | PROBE-03 | Hippo music-label boss (five-view set) - Gemini animation status unknown | 2 | Gemini animation status unknown (replacement for refused gecko-frog) |

## 5. Run order
1. **Calibration - HD-01, HD-02, HD-03** (Hon Dolo pinstripe, saloon, yellow) in both tools. Stop and look: are the uploads accepted, does the tool read "image 1/2/3" correctly, are sides being mirrored? Write any process issues in `notes`. Do not change the prompts - if something is broken in the kit, tell Ziggy before continuing.
2. **HD-04** (Hon Dolo cream).
3. **LAG-01** (Lisan Al Gaib signature look; natural white teeth, no grill).
4. **BOSS-001 ... BOSS-010** in order (round-1 boss candidates).
5. **Refusal probes last: PROBE-03 (hippo), PROBE-02 (gecko-frog V09), PROBE-01 (original slug-lord).** Run them last so a possible account warning can't block the fidelity tests. Expect refusals; that is data.

For each test, do tool A then tool B (or alternate the order per test to avoid bias - note it).

## 6. Naming and saving returned files
- Nano Banana: `RETURNS/A_NANOBANANA/<TEST-ID>_NANOBANANA_a<N>.png`
- ChatGPT: `RETURNS/B_CHATGPT/<TEST-ID>_CHATGPT_a<N>.png`
- `<N>` = attempt 1, 2 or 3. Example: `HD-01_CHATGPT_a2.png`.
- Refusal screenshots: `<TEST-ID>_<TOOL>_a<N>_REFUSAL.png` in the same folder.
- One row per attempt in `LEDGER.xlsx` (or `LEDGER.csv`). Attempt 1 rows are pre-filled; insert rows for attempts 2-3.
- Grok Bot baselines are already in `BASELINES/<TEST-ID>_GROKBOT.jpg` (some tests have a second `_GROKBOT_B.jpg`).

## 7. How to score
- Fill the score columns in `LEDGER.xlsx` using `SCORING_GUIDE.md` (0-5 scales, Y/N checks, NA where a feature doesn't apply - NA is pre-filled).
- Use `COMPARE/COMPARE.html` (open in a browser) or `python3 COMPARE/build_compare_sheets.py` to see ref | Grok Bot | Nano Banana | ChatGPT side by side.
- Summarise per tool: count of refusals (by test), mean of each score column across the HD/LAG tests (fidelity) and across bosses (character hold). Sides (tattoo_placement_correct, prop_side_correct) should be reported as a pass rate, not averaged into "overall".
- Send the filled ledger + RETURNS folders back to Ziggy. Status stays `needs_user_review`.

## 8. Known caveats (honest notes)
- **Boss tests:** the Grok Bot baseline IS reference image 1 (the round-1 proof). So boss tests measure how well A/B hold an existing character in a new shot, plus whether they refuse it; the Grok row is the target, not a competitor score.
- **HD outfit refs** (image 3) carry old drift (e.g. full gold grills). The prompt says to take outfit/scene only from image 3 and locks from images 1-2.
- **Nostril hoops:** spec says two hoops in his RIGHT nostril (character-right = viewer-left). In HD-EXP-LOCK-FACE.jpg one hoop sits on each side of the nose; Ziggy should confirm which is canon. Score against the written spec and note it.
- **LAG-01:** image 2 (LAG-LOCK-FACE.jpg, as requested) still shows the retired iced grill; the prompt tells the tool to ignore its teeth. Current guidance (`LAG-NOVA-GUIDE`) uses LAG-LOCK-FACE-NATURAL.jpg as identity truth (image 1) and signature outfit LAG-LOOK-V3-01 (used as the baseline). LAG-LOOK-01.jpg (original look 01) is included as context only because it carries the old eye/know/grill spec.
- **PROBE-01:** no file named `image_25.png` exists on the box. The slug-lord original is `side-lord/REF-lord-source.jpg` (the source image the side-lord redesign was based on; matches the description: jeweled slug lord on a throne with background dancers). Treat it as the image_25 equivalent and have Ziggy confirm. Its Grok baseline is the closest existing in-house slug render (an early supporting-cast still), not a re-render of image_25; BOSS-003 is added as `_GROKBOT_B`.
- **BOSS-009** tattoo: baseline shows option B (requested A); prompt uses option B so A/B can be compared with the baseline. BOSS-006 baseline put the tattoo on the chest; prompt asks for the planned right-neck spot.
- Baseline PNGs were converted to JPEG (q93) to keep the kit small; original paths + sha256 are in `BASELINES/baselines_manifest.csv`. Refs are byte-identical copies (sha256 in `refs/refs_manifest.csv`).
