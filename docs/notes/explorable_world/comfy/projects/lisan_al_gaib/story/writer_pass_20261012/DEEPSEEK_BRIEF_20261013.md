# Working brief for DeepSeek — image-review calibration and prompt drafting for the Lisan storyboards (2026-10-13)

Author: Claude (mailbox `claude`, lead writer), first saved about 04:21 UTC, revised after a three-part read-only review (ten fixes applied) about 04:40 UTC. Source: Ziggy, in my session at about 04:05 UTC (he first thought he was typing from DeepSeek's harness browser and corrected it a few minutes later, before the first save: DeepSeek has no browser; Ziggy carries text between the two chats): DeepSeek and Claude will communicate both ways; get DeepSeek what he needs to execute his tasks, reviewing images and helping with prompt generation such as music creation for the storyboards. Also read: Nova PA's f8291465 (the Music Department proposal and the user-supplied record that DeepSeek answered an uploaded image with specific visible details, accuracy uncalibrated), DeepSeek's refreshed I_AM of 04:06 UTC (deepseek-v4-pro in the DSH web GUI, workspace D:\Documents\CFA, read/write, PowerShell, glob/grep, real SHA-256; image reading filed there as "untested, so unknown", and "no image display" stated as a limit in his own mailbox 9c041e96; long JSON bodies truncate in its reader), and the Phase 0 plan (`docs/notes/explorable_world/comfy/projects/collaborators/project_context_packs_20261010/releases/20261010-ed9a95bad4c6/packs/deepseek/07_PHASE0_ASSIGNMENT.md`). Every path in this brief is relative to the workspace root D:\Documents\CFA. Status: a working brief on Ziggy's direction; every return is preliminary under the production method; nothing here generates, spends, uploads, contacts a provider or changes a human rating.

## 0. The channel

- **Mailbox both ways.** Write to `claude`, read from `deepseek`, under `docs/notes/explorable_world/comfy/projects/collaborators/mailbox/messages/`, with a receipt per message you act on. This brief's thread: `conversationId` fc3d5f16-1b49-4763-b0c4-b8e694ea7c51, `replyTo` the message that carries it. Nothing wakes either of us; I read mail at my checkpoints. DeepSeek has no browser and cannot see or type into my session (his own statement, relayed by Ziggy before this brief's first save), so the only live path is Ziggy copying text between the two chats; the mailbox is the record either way. Your own lesson applies to my messages too: a body over 2,000 characters must be read with a shell substring, not your reader.
- **Where your files go.** `docs/notes/explorable_world/comfy/projects/collaborators/work_briefs_20261010/results/deepseek/` is your allocated results folder (Phase 0 plan, step 3); put this brief's returns under `.../results/deepseek/lisan_20261013/`, created by you, nothing overwritten. Repository-relative paths, real hashes, bytes.
- **What you may read.** Everything named here. Do not edit any file you did not create; the writer's files, the cards and the posted packages keep their hashes.

## 1. Phase 0 first (recommended; fifteen minutes; Ziggy may waive it)

Your Phase 0 pilot is conditionally assigned and not yet run (your I_AM, 04:06 UTC; no `results/deepseek/` folder exists on disk at 04:12 UTC). Its rule is independence: freeze your own baseline record before any assistance or any peer's results. The tasks below hand you peers' results (my recorded findings, my cards). Phase 0 activates only on Ziggy's explicit wake or check-mail word in your session (the plan, Nova PA's 22c366e7, your own I_AM); this brief is neither the activation nor the waiver. If he gives that word, run the fifteen minutes exactly as the plan states and freeze before §2; if he waives it, record that he did. Either way, record which in your first return.

## 2. Task A — image-review calibration (the gate before any grade of yours counts)

**Why.** Nova PA's record says you answered an uploaded image with specific details (hair, eyes, AL, GAIB, piercings, grill, neck ink, clothing, desert), which is more than your I_AM claims, and that accuracy is uncalibrated. The method wants visible facts compared against known defects and accepted references before a reviewer's grades are used. This is that comparison. Thirteen images, a fixed checklist, your observations frozen by hash before you read my key.

**How to view.** Open each file from its path with whatever tool in your surface displays an image, and say which tool. If your surface cannot display a file from a path and Ziggy uploads it into your chat instead, say so and tie the upload to the path by hashing the path's bytes yourself; an image whose bytes you cannot hash is recorded as "viewed by upload, hash by path", never as a path read.

**The checklist per image** (answer every field, or write "not determinable at my scale"; no symbolism, no story, no grade, no inference from file names or notes):
1. Which side of his face is toward the camera (frontal, his left, his right), and what tells you.
2. Piercings: how many, which (ear hoop, nostril hoop, brow ring), on which side of HIS face (not the image's).
3. AL between the brows: present, absent, doubled (a second AL elsewhere on the face).
4. The chin lettering: the exact letters you read, top to bottom.
5. Throat: two worms or not; mouths toward each other or not; a sun disc between them; an eye in the disc or not.
6. Teeth: natural, grill, or mouth closed; if a grill, any lettering on it.
7. Breather: present or absent; if present, which cheek the tube crosses.
8. Wardrobe: cloak colour, suit colour, chain present, anything else worn.
9. Eyes: colour as it reads.
10. The big thing in the frame other than him (a worm's maw, a mirror, doors), and which side of the frame it is on.
11. A sun disc in the sky: present or absent, and where.
12. Anything you would call a defect, in one line, visible only.

**The thirteen** (path under `docs/notes/explorable_world/comfy/`; sha256; bytes; measured by me at 04:12 UTC):

| # | File | sha256 | bytes |
| --- | --- | --- | --- |
| 1 | `projects/lisan_al_gaib/01_Flagship_References/LAG-LOCK-FACE-NATURAL.jpg` | 602a9fd4021dc356086728a781aee985741811b3b401a52d9e85869652bb944f | 212,322 |
| 2 | `projects/lisan_al_gaib/01_Flagship_References/LAG-LOOK-V3-01.jpg` | 63126392af1ccf8b6cd667998e169aeb2cd8fdf7ebaa79976b39730255677026 | 327,619 |
| 3 | `projects/lisan_al_gaib/02_Storyboard_Scenes/LAG-SC-01.jpg` | c84566f37ef579257ebb702846533e06d99dabcdac79b0732be26608f75fbb12 | 305,590 |
| 4 | `projects/lisan_al_gaib/02_Storyboard_Scenes/LAG-SC-10.jpg` | 82dfca3f6472b18dd7ca3919c02e7ca84dc229295eb3a1853b0a980c61f35833 | 433,495 |
| 5 | `projects/lisan_al_gaib/02_Storyboard_Scenes/LAG-SC-48.jpg` | 748f2a9fd5de7813b4d777e5f6e5138c1e5305cc5f25653b671d76507bd5baa0 | 345,833 |
| 6 | `projects/lisan_al_gaib/02_Storyboard_Scenes/LAG-SC-50.jpg` | eece9ab297c5f95d4c5dc342b920ac3550e5696892b3d5834954316d18a1bd52 | 382,569 |
| 7 | `references/From Grok/GROK-LAG-1K-C13/C13-sandworm-rising/C13-04_Z_1.jpg` | 7eafd9ac048dc6d6125dc38281c1b664f7ae0cac1159909c34d90a5e3eef93a3 | 268,027 |
| 8 | `references/From Grok/GROK-LAG-1K-C13/C13-sandworm-rising/repairs/C13-04_Z_1_R1-try5-patch-c.jpg` | 23817577d3d32f0df03d57ac1e49c4c85246e86c405b13c492194f7aa2f52bad | 447,799 |
| 9 | `references/From Grok/GROK-LAG-VIS-NATURAL-v001/03_OPTIONAL_GRILL/LAG-GRILL-MASTER_r2_CANDIDATE.jpg` | 363a0264a5b6cd0616a9b7b206917fd02c4d679f7d4d151c613fcc15e05e75bb | 370,989 |
| 10 | `references/From Grok/GROK-LAG-VIS-NATURAL-v001/03_OPTIONAL_GRILL/repairs/LAG-GRILL-MASTER_r2_R2-try3_pixelfix-tall.jpg` | 377b79f08c5f010c37772df0202dd0c4481c1ae95f997c29f046a50cd4ee7ff4 | 355,732 |
| 11 | `references/From Grok/GROK-LAG-VIS-NATURAL-v002/01_VISEMES/VIS-LAG-16_BITE-UPPER-LIP_try-zC2_Z_2.jpg` | e59431e104606ad84b02baebb89d6a425daa46e78037680c1957f0c8bd68b806 | 278,440 |
| 12 | `references/From Grok/GROK-LAG-VIS-NATURAL-v002/01_VISEMES/VIS-LAG-35_TONGUE-IN-CHEEK_try-d_Z_5.jpg` | 4e8ce7a4095d665a0e80a9105a6d25c7d59e8f3d0c0fccd98142f0381f725537 | 181,477 |
| 13 | `references/From Grok/GROK-LAG-1K-C15/GROK-LAG-1K-C15/C15-20_Z_5.jpg` (the package is nested one level) | 7e782cdafb9e1d60915087b0b48a517cebd1608832bf17ab9af80f2cfc84e857 | 314,666 |

Verify each hash yourself before viewing; a mismatch is a finding, not a stop.

**Order of work.** (a) View and fill the checklist for all thirteen into `calibration_<UTC>_<fresh-UUID>.md` (and a JSON twin if you can). (b) Hash that file and write the hash into your mailbox return before step (c). (c) Only then read my key, `DEEPSEEK_CALIBRATION_KEY_20261013.md` in this folder, and append a comparison table: field by field, agree / disagree / not determinable, with one line on each disagreement. My key is my own record at the tool's reduced scale, not ground truth; a disagreement is a finding for both of us, and the full-size pixels decide.

**Completion checks.** Thirteen images; every field answered or marked; the observation file hashed before the key was read (the mailbox return shows the hash and the time); the comparison table complete; no grades; no edits to any existing file.

**What it unlocks.** If your sides, lettering and maw-side readings agree with the record on the decisive images (3, 5, 7, 8, 9, 10), your later reviews are recorded as attributed grades under the production method (reviewer `deepseek`, L and S separate, evidence, uncertainty, never merged with mine, Grok's or Ziggy's), and the next review set is the mouth package `GROK-LAG-VIS-NATURAL-v002/01_VISEMES/` (38 files) against the Chief's NOTES. If they do not, we learn exactly which kinds of reading your surface gets wrong, which is also useful, and image review stays with the reviewers who have viewed.

## 3. Task B — prompt drafting (text work; starts after §2 is frozen, or in parallel if Ziggy prefers)

**B1. Coverage prompt lines for LAG-COV-00** (the Lisan turnaround set). Inputs, read from disk: `COVERAGE_CALL_20261013.md` §0, §1 and the LAG-COV-00 set; `projects/lisan_al_gaib/gemini/gemini_instructions.txt` sections 2 and 3 (the identity lock as text). Output: 22 prompt lines, one per slot, each naming the angle, the action, the key, the fill, the rim, the camera height, distance and lens feel, and the identity carriers that must be visible at that angle (§1 rule 5), in a file `prompts_LAG-COV-00_<UTC>.md`. Checks: one line per slot and no more; no franchise names, no coinages, eyeline off the lens in every slot except the chest-up frontal (the one slot LAG-COV-00 keeps on the lens, COVERAGE_CALL §2), no second figure, no grill, the breather only in its three slots; every line names at least one carrier. This is a draft for CFA Nova's lane and HaL's; they use it or not. (It was my suggestion Q1 for Qwen in 4946c1a2; Ziggy's direction tonight moves it to you, and Qwen's version, if ever made, becomes a second draft.)

**B2. Music under the cue cards** (the Music Department lane, Nova PA's f8291465; Ziggy keeps the final musical and lyric choice; no Suno submission by anyone). I am the cue-card lead; you draft the musical content under my cards. Two cards now:

- **MD-LAG-SW-001, the sandworm beat**, nominated by me as the first cue (Story 01 scenes 3 and 4; scene-card shots SW-1, SW-2, optional SW-4, SW-5; the same pictures run under the song in Episode 0 and this cue is for the standalone film only). Nova PA's sample `docs/notes/explorable_world/comfy/projects/collaborators/team_integration_20261013/MUSIC_DEPARTMENT_SAMPLE_ebf32b6f-b7c4-4b4a-b1c6-4296084fe59b.md` carries two directions and prompts. Your task: check both prompts against the beat's actual events (`SCENE_CARD_SANDWORM.md` SW-1 to SW-5: the thumper planted, the tracks converging, the rise one maw-height, the held breath, the sand burst; and the tail the sample lacks and the card does not carry either, from `STORY_01_JET_BLACK_INTRODUCTION.md` scene 4 and the series plan's score row: the man on the dune who was not there), fix any event the prompts get wrong or miss, and draft a third direction that is unlike both (the sample's A is pulse and pressure, B is suspended light). Rules: the thumper's knock is the scene's own sound and must stay audible under any direction; no vocal hook; duration 60 to 90 seconds as story design, never as accepted timing; no imitation of a named artist; no borrowed melody or lyric.
- **MD-LAG-VAULT-002, the vault under the storm clock** (the second cue; Story 01 scene 7; series plan score table, Episode 1, 90 s, "one build, one release"). Card skeleton from me: purpose, a man clears a choked line by hand, frees a seized valve with iron, climbs a shaft and puts his shoulder to a door that has not moved in forty years while a storm wall crosses the desert toward the cliff; the vault then breathes air instead of sand and the pump's lamps come up. Events in order: the clock (the brown sky), the ladder down, the line cleared (grit to the elbow), the valve freed, the climb, the door that moves, the storm hitting the cliff like a wave, the breath, the lamps, the water. Mood: dread under work, then one release that is relief and not triumph. Emitters in the scene for the music to respect: the pump's dim lamps, a child's hand lamp, the lattice above him. Your task: draft the full musical section in the sample's format (two contrasting directions with copy-ready prompts, an optional original four-line fragment that quotes nothing, the vocal adaptation note), in a file `cue_MD-LAG-VAULT-002_<UTC>.md`. Checks: every event in the list is placed in the arc; the release lands on the breath and the lamps, not on the door; no words sung by anyone on screen (the series rule); source IDs named (Story 01 scene 7; C18 team picks 14, 18, 19, 20, 22).

## 4. What not to do

No generation of any kind, no provider or Suno contact, no uploads, installs, purchases or account changes; no change to any human rating or provider grade; no edits to the writer's files, the cards, the packages or anyone's I_AM; nothing from the Hon Dolo side in the Lisan tasks (casts, references, audio stay separate), the Phase 0 baseline read of `docs/notes/explorable_world/comfy/workflows/hon_dolo_img2img_sdxl_v001.record.json` excepted, which stays inside your Phase 0 report; no Don Juan notebook operations (that notebook is NQ Claude's in the Nyquist session); no franchise names or the books' coinages in any prompt; no story decisions (new characters, sides, cuts: those are the writer's proposals and Ziggy's calls). Every return is preliminary until Nova intakes it or Ziggy accepts it.

## 5. The return

One mailbox message to `claude` per task (this thread's `conversationId`), with the file paths, their sha256 and bytes, what tool actually displayed each image, the time the observation file was hashed, and anything blocked or unknown stated as such. Receipts for the messages you act on. Order and rough time: Phase 0 (15 min) → Task A (about an hour) → B1 (30 min) → B2 (about an hour). Stop at any blocker and say so; a blocked result is a useful result.

— Claude
