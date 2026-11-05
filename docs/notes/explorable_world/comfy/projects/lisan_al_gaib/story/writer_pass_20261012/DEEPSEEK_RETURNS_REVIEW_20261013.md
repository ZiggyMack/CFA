# Review of DeepSeek's first returns — Phase 0, the calibration blocker, the 22 prompt lines, the two cue drafts (2026-10-14)

Reviewer: Claude, lead writer and cue-card lead, recorded at about 00:30 UTC on October 14 (the returns were posted 2026-10-13 between 04:38 and 20:13 UTC; the session was down from about 14:45 UTC and restarted at about 00:15). Status: a reviewer's attributed notes under the production method; every return stays preliminary; nothing here accepts, generates, submits or changes a rating. Ziggy chooses the music; CFA Nova intakes nothing until he does.

## 1. What came back (hashes and byte counts of all five files verified on disk by me: the three 20:13 files at 00:20 UTC, the two 04:38 reports at 00:25 UTC)

| Return | Mailbox | File | sha256 | bytes |
| --- | --- | --- | --- | --- |
| Phase 0, executed and frozen (not waived) | e175d0ef, 04:38 UTC | `collaborators/work_briefs_20261010/results/deepseek/phase0_20261013T043602Z_e80435f1-ead1-4d22-b9ba-f3923f6c04d7.json` | f209727c2433c5fcb6daeab7cc652b0c951e957e6b9d51f6b2b1de334c4e7f2b | 4,536 |
| Task A, blocked at model level | 96937d59, 04:38 UTC | `.../results/deepseek/lisan_20261013/calibration_20261013T043745Z_64566cb1-5a92-498e-9f82-64ca3881cd88.md` | 5bd351bf6e2179c5e951ff0f586f23ddc499a88f0fb06369e2bf8887579284b1 | 3,845 |
| B1, the 22 prompt lines for LAG-COV-00 | 85ff3aa7, 20:13 UTC | `.../lisan_20261013/prompts_LAG-COV-00_20261013T201058Z.md` | 531b15e9690d19817099e4c10b83d5f0192d4be0fb85629ab4757cd6fd7c0ff8 | 9,789 |
| B2a, MD-LAG-SW-001 check, fixes, third direction | 92d2a79f, 20:13 UTC | `.../lisan_20261013/cue_MD-LAG-SW-001_20261013T201058Z.md` | 96725ff684426dde117c47a78d254d8ca1626aa99c17b7dcd99135d735ddad09 | 4,625 |
| B2b, MD-LAG-VAULT-002 full draft | 92d2a79f, 20:13 UTC | `.../lisan_20261013/cue_MD-LAG-VAULT-002_20261013T201058Z.md` | 32707afb21f13f43243ef1586b92347e4fde1baefefc7f0fd9abe57f2951d05d | 5,745 |

Dispatch of B1 and B2 was Ziggy's own (Nova's fb7cfdf6: a human relay at 20:09 UTC). The brief reached DeepSeek from disk before its carrying message was posted, which he recorded honestly (replyTo null).

## 2. Phase 0 and the calibration

- **Phase 0:** run as the plan directs, independent, frozen; the baseline read, parse and write all succeeded with his own tools; the report re-read and re-parsed. Nothing for the writer to grade; Nova verifies the bytes. Recorded as done.
- **Task A, the thirteen-image calibration:** blocked by an exact error from his surface: the model `deepseek-v4-pro` declares no image input, from a path or from an upload. He verified all thirteen hashes and byte counts (all match my table), filled no checklist field, and did not open the key, which is the order rule kept exactly. **Consequence, as the brief itself set it:** image review stays with the reviewers who can view; no grade of his counts, and none was given. The way to change that is Ziggy's: an image-capable model in the DeepSeek Harness, after which the same calibration runs unchanged. The user-supplied record that he once answered an uploaded image (Nova PA's f8291465, whose evidence record leaves the surface and the model null) must therefore come from a different surface or model than this session's; that is my inference, and Nova's note goes only as far as naming this deepseek-v4-pro session as the one that rejected image input.

## 3. B1, the 22 prompt lines (a draft for Nova's lane and HaL's; they use it or not)

**Verdict: usable as a draft, with two line fixes.** All 22 slots present, one line each, with angle, action, camera, key, fill, rim and carriers in every line; no franchise names, no coinages ("the tan suit", never the borrowed word), no second figure, no grill, the breather only in slots 17 to 19. The light model's statement is right for a turnaround (the sun fixed in the world and the camera orbiting, so the frontals are keyed from behind the camera and the back views are rimmed), but five lines do not obey it: see the second fix below.

- **His flag, resolved:** slot 1 to-lens is correct. The brief he read from disk carried a blanket "no to-lens" check that my review struck before the brief was posted at about 04:40 UTC; the posted brief (9bded34a) reads "eyeline off the lens in every slot except the chest-up frontal". He followed the card, which is the right call, and flagged the difference instead of hiding it.
- **Fix, lines 6 and 14 (3QBL, chest-up and full body), carriers:** with the camera behind his left shoulder, his left side is the near side, so the left ear hoop is visible near, not "peeking at the far edge", and the nostril hoop is hidden by the turn of the head. Rewrite the carriers as: the left ear hoop near, the curls, the cloak's line, the chain at the nape; no nostril hoop.
- **Fix, lines 6, 7, 14, 15 and 19 (every three-quarter-back slot), the key:** each reads "Key: high hazy sun from the camera side", which the call's fixed sun forbids once the camera is behind his shoulder; at that angle the sun is on his far side, so the key is the rim on his far edge and the haze is the only fill on his near side. Rewrite the light in those five lines as: key the high hazy sun from behind him on his far edge; fill the hazy sky and sand bounce on the near side; no key from the camera side. (The review audit found this; I had passed the lines on carriers alone.)
- **A delta to the coverage call, to file before LAG-COV-00 dispatches:** rule 7 says "Nothing to-lens" while the LAG-COV-00 set keeps the chest-up frontal on the lens; the rule should read "nothing to-lens except where a set names the slot". Recorded here and in DECISIONS item 48; the posted call keeps its hash.
- **Not verifiable by text:** "the striped coiled worm on his left forearm" (lines 10 and 12) describes the arm art from the lock's text; whether the art reads that way is a viewing question for the reviewers who can view.

## 4. B2a, MD-LAG-SW-001 (the sandworm beat)

**Verdict: the audit is right, and the third direction is the one I would try first.** He found what my own refinement found (the tail missing: the man on the dune) and two more that the sample's prompts never name: the tracks converging, and the sand burst with his surfacing. His deltas to A and B are correct and keep each direction's character. Direction C, a ritual processional (a dry frame drum marking each step; the knock answered from the horizon by a converging thud; the rise as tectonic weight rather than impact or shimmer; the burst swallowing the motif; a beat of silence; one held low tone on the man on the dune) is unlike A's pulse and B's light, keeps the knock audible, has no vocal hook, and ends on the held reveal rather than a fade, which is the beat's actual shape. The rules check holds.

- **Cue-lead note for Ziggy's choice:** C fits the score-song idea best (the scene drives and the music walks with him); B is the second choice; A reads most like a trailer. Recorded as the writer's preference, not a decision.
- **His sources line is right where mine was wrong:** events 1 to 5 from the scene card, the tail from Story 01 scene 4 and the series plan's score row. The sample card never named the tail at all; my 15ccd720 attributed it to the scene card, which lacks it; the brief's §3 B2 carries the correction, and his line matches it.

## 5. B2b, MD-LAG-VAULT-002 (the vault under the storm clock)

**Verdict: complete in the sample's format and usable as the second cue card's musical section.** All ten events placed in order; the build's peak on the door (event 6) and the release on the breath and the lamps (8 and 9), exactly as the skeleton asked; emitters respected and no colour invented for the lattice; two directions that are actually different (the machine breathing; the vault's silence); copy-ready prompts within the rules; an original four-line fragment that quotes nothing ("Forty years the door kept still, / Grit to the elbow, iron and will. / The storm threw itself against the stone, / And the vault drew one clean breath alone."); the vocal note keeps the series rule (no mouth on screen sings; any voice off-screen and optional).

- **Craft note, both directions:** the "storm clock" in the story is the brown sky crossing the desert toward the cliff, not a clock; a clock-like tick or pulse is a device that can come out of the generator as a cliché. Keep the dread as weather (a drone that rises as the sky browns) and use the tick only if the generation needs a grid. A preference for the prompt's next pass, not a rule.
- **Cue-lead note for Ziggy's choice:** A for the first try (the work sounds carry the scene's own actions, which is what a score song wants); B if the cut runs quieter than the story design.

## 6. D3, offered

He reports D3 (the lyric and cue mechanical check) done on his side with one finding, the cue map's headline count (fourteen stated, fifteen enumerated), which Nova independently confirmed. The file is welcome whenever he is next active; this note starts nothing.

## 7. For the record

DeepSeek's first task as a mailbox batch started by Ziggy: three text returns in one session, each with paths, hashes, bytes, sources read and limits stated; one honest blocker; one correct deviation flagged rather than hidden. That is the standard. The image lane needs a different model; the text lane is open.

— Claude
