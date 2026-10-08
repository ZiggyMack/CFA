# Hon Dolo Gemini video reference intake

Reviewed October 7, 2026 for [Hon Dolo — Strictly Business](../README.md). Ziggy selected **`gemini_generated_video_c0823c60.mp4`** as the best starting clip for Comfy experiments. Its opening close-up is the proposed first source excerpt. The earlier two clips remain useful cockpit and cantina staging references. The fourth clip, **`gemini_generated_video_58328bf1.mp4`**, is a user-directed candidate for S10A's dinner-with-Vader lyric; it does not replace the selected Comfy experiment source.

This intake records supplied media, full stream decoding and sampled visual review. It does not record a Comfy render, Cloud compatibility check, accepted final character or completed lighting refinement. Gemini is the user-stated provider; exact model/version, prompts, inputs and settings are unknown. All originals are unchanged.

## Media inventory and evidence

All four files are 1280 × 720 H.264 video at 24 fps, with **240 decoded frames and 10.000 seconds of picture**. Each contains AAC-LC stereo audio at 48 kHz; full audio decoding produces 10.005333 seconds. Container duration rounds to 10.01 seconds. Full audio/video decoding completed without errors for every file. The files have distinct SHA-256 hashes.

| Original file | Bytes | Role | Review sheet |
| --- | ---: | --- | --- |
| [gemini_generated_video_28961248.mp4](<../../../references/Gemini Video/gemini_generated_video_28961248.mp4>) | 6,513,730 | Cockpit and hyperspace performance montage | [16 sampled frames](contact_sheets/gemini_generated_video_28961248.contact_sheet.jpg) |
| [gemini_generated_video_2e361055.mp4](<../../../references/Gemini Video/gemini_generated_video_2e361055.mp4>) | 4,883,179 | Cantina reactions and toast | [16 sampled frames](contact_sheets/gemini_generated_video_2e361055.contact_sheet.jpg) |
| [gemini_generated_video_c0823c60.mp4](<../../../references/Gemini Video/gemini_generated_video_c0823c60.mp4>) | 5,307,098 | **User-selected experiment source**; four cantina performance shots | [16 sampled frames](contact_sheets/gemini_generated_video_c0823c60.contact_sheet.jpg) |
| [gemini_generated_video_58328bf1.mp4](<../../../references/Gemini Video/gemini_generated_video_58328bf1.mp4>) | 4,355,398 | **S10A dinner candidate, per user direction**; dinner/reaction and carbonite montage | [16 sampled frames](contact_sheets/gemini_generated_video_58328bf1.contact_sheet.jpg) |

The [manifest](manifest.json) contains complete source hashes, stream metadata, decode results, review evidence and reference roles. Review used 16 evenly spaced decoded frames per clip, selected full-size frames, and adjacent frames at the selected experiment clip's and fourth clip's cuts. **Normal-speed playback and audio listening have not been reviewed.** Lip-sync, lyric timing, flicker and uninterrupted prop contact are therefore not accepted findings. A decoded audio stream does not establish that it uses the supplied song.

## Selected clip and first excerpt

The selected `c0823c60` clip contains four shots. FFmpeg scene-change detection suggested the three transitions; inspection of adjacent frames confirmed each hard cut.

| Source frames, inclusive | Time range, end exclusive | Observed shot |
| --- | --- | --- |
| 0–59 | 0.000–2.500 s | Frontal face close-up with head and mouth movement |
| 60–118 | 2.500–4.958333 s | Medium performance with open-hand gestures |
| 119–179 | 4.958333–7.500 s | White-fur outfit, foreground partner and hands on shoulders |
| 180–239 | 7.500–10.000 s | Leather-jacket performance, hand/chain gesture and moving stage lights |

**Proposed first excerpt: frames 0–56 inclusive, 57 frames at 24 fps, lasting 2.375 seconds.** The last included frame has timestamp 2.333333 seconds; the trim's end-exclusive boundary is 2.375 seconds. This ends safely before the first cut and isolates face/head motion without hand contact, a second foreground subject or the strong late flare. The 57-frame count also satisfies an 8n+1 grid if the eventual recipe requires it; it is not a universal model setting. No trimmed derivative or new generation is claimed by this intake.

A later hand-gesture comparison could use frames 60–116, also 57 frames, after the simpler close-up is assessed. Keep the source timing and original soundtrack available separately. The planned lighting-refinement experiment must have its own graph, settings, result and comparison record; nothing here establishes that it has run.

## Character details and visible limits

The selected clip is closer to the [October 6 supplied design direction](../../../casting/grok_intake_20261006/README.md): `eye` appears image-left, `know` image-right; the image-right neck has a blaster motif; the chest has a ship; the inspected close-up shows nose/lip/ear jewelry, natural-looking upper incisors with gold canine caps and metallic lower teeth. These are sampled observations, not proof of exact continuity.

**Dice remain above the image-right eyebrow.** The latest handoff says dice were dropped, alongside the earlier Chewie lettering, bird and Jabba motifs. Selecting this video for experiments does not reinstate those retired details. Its brow marking should remain an explicit source-versus-target difference, not silently become part of the current design.

The second shot's hands are partly cropped or blurred in reviewed frames. The white-fur shot shows tattooed hands on the lead's shoulders, apparently belonging to the foreground partner; card/lettering ownership and placement need review before that scene can establish character continuity. The final shot contains motion blur and a strong flare near the sampled 9.292-second frame. These more complex moments are useful later tests, after the opening close-up.

## Other reference roles

**`28961248`: cockpit performance.** The sampled sequence changes from a medium pilot view to face close-ups, side-console operation and a frontal two-handed yoke grip. Pink/cyan beams, light strokes across the face and a late bright flare complicate detail inspection. The inspected grip frame has no obvious extra digit, but sampled frames cannot establish stable contact or ring detail. Proposed use: cockpit performance, travel energy and control inserts. The whole montage is unsuitable as one uninterrupted motion reference; select a single shot first.

**`2e361055`: cantina personality and toast.** The performer turns, smiles and later raises a glass amid neon bar lighting. Inspected toast frames show a plausible grip without an obvious extra finger. Glass pickup, rim/liquid behavior, jewelry and hand continuity remain unreviewed in motion. Proposed use: cantina swagger, a reaction cutaway or a toast insert. Camera changes/cut boundaries need separate review before choosing its excerpt.

Both earlier clips visibly retain the older **Chewie forehead text, cheek/neck dice, large cheek bird, Jabba-like neck mark and broad gold upper grill**. They are staging/performance references, not replacements for the current design anchor or accepted identity masters.

## Fourth clip: dinner with Vader candidate

Ziggy associates `58328bf1` with **“Dinner date with Darth Vader? — I ain't order this shit.”** Record this against **S10A, Dinner with Vader**, in the [shot plan](../shot_plan.json). This is a user-directed scene candidate, not an accepted take or verified lyric timing. The existing S10A draft places Vader at the far end of a table; this reference instead seats Hon Dolo beside him and supplies a reaction close-up. The shot plan has not been silently rewritten.

The fourth clip contains five shots. Scene-change detection followed by adjacent-frame inspection confirmed the boundaries below; the chamber entry at frame 120 includes strong radial blur.

| Source frames, inclusive | Time range, end exclusive | Observed shot and candidate role |
| --- | --- | --- |
| 0–59 | 0.000–2.500 s | Hon Dolo holding a wineglass beside Vader at an ornate dinner table; S10A establishing candidate |
| 60–119 | 2.500–5.000 s | Hon Dolo's changing reaction across Vader's shoulder; S10A reaction candidate |
| 120–177 | 5.000–7.416667 s | White-fur outfit, vapor-filled chamber and apparent lowering relative to the rim |
| 178–208 | 7.416667–8.708333 s | Face/shoulder close-up in an orange-lit pool |
| 209–239 | 8.708333–10.000 s | Finished carbonite slab; possible S10C visual reference, a reviewer inference |

**The first five seconds are a two-shot dinner sequence, not one continuous motion driver.** Either 2.5-second shot could be considered separately after playback and song alignment. No exact trim, song placement or take has been accepted by this intake.

The inspected dinner close-up retains the `eye`/`know` words, ship chest motif, facial jewelry and **retired brow dice**. A sampled smile has natural-looking upper incisors, gold at the canines and metallic lower teeth; these details need continuity review across expressions. Frame 0 shows a plausible ringed wineglass grip without an obvious extra digit, but glass/liquid behavior and continuous hand contact have not been reviewed.

The later chamber setup has **two human hands resting on the white-fur shoulders beneath chains, without a visible connected owner** in inspected frames. This may be intentional staging or a generated contact/anatomy problem; it remains unresolved. The montage also changes wardrobe from leather to white fur. The final slab retains facial markings and gold-colored teeth, with differently posed hands. The pool-to-slab cut supplies no evidence of a coherent transformation. These caveats do not prevent the dinner shots serving as scene references, but the full montage is not an accepted identity or motion-continuity master.

## Reuse and next evidence

The intake follows the existing distinction between appearance, performance and audio references taught in Panhandlers' `Help/guides/video_handoff.py`. Its `Help/guides/workflow_files.py` explains why saved media alone does not supply an executable graph or model dependencies. Apply the [workflow decision and feedback procedure](../../../templates/workflow_intake.md#decision-and-feedback) when choosing the subsequent edit recipe.

The originals and derived contact sheets are local media on D:, excluded from Git; the README and manifest preserve the audit. Remaining checks are normal-speed playback, listening against the song, acceptance of an exact source excerpt, current Cloud dependencies/compiled inputs, and a bounded edit with before/after comparison. Reference review is distinct from compatibility validation, execution and acceptance.
