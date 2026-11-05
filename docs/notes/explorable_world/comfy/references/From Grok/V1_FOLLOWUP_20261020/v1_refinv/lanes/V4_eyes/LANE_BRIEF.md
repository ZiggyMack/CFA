# LANE BRIEF: V4_eyes (V_4, bot id 78934db1-dad1-4d94-9e44-828f71be65af), issued 2026-10-20 by Grok Chief of Staff
Your field: **Eyes: iris colour and glow level**. Coordinator: V_1 (96ead2b6-3f8a-4535-b179-30cd44123f8a). Read `/workspace/v1_refinv/COMMON_RULES.md` first; it binds you.
Inputs: `refs/` here (8 images, `refs/INDEX.tsv`), `REVIEW_HISTORY.md` here, and `/workspace/v1_refinv/CANDIDATES.tsv`. Related Chief queue entry: Queue item 3 (eyes) in `REF_DECISION_QUEUE_20261020.md` (copy in `/workspace/v1_refinv/`). That queue is Chief's preliminary view, and your visible evidence may overturn it.

## Candidates (shared IDs)
| cand_id | file | sha256 | stars |
|---|---|---|---|
| CAND-01 | CAND-01__LAG-LOCK-FACE-NATURAL.jpg | 602a9fd4021dc356086728a781aee985741811b3b401a52d9e85869652bb944f | 5 |
| CAND-02 | CAND-02__LAG-LOOK-V3-01.jpg | 63126392af1ccf8b6cd667998e169aeb2cd8fdf7ebaa79976b39730255677026 | 5 |
| CAND-03 | CAND-03__LAG-LOCK-FACE.jpg | cb183973ed1fc70ec906b762fb263b29c8866934a67f9608786b712579eaf056 | unrated |
| CAND-04 | CAND-04__LAG-BR-01_REST_front_v3_STANDARD.jpg | 1b60815fa2bb4f8f488ebcf123a6a71af4cba144d06667c73b2ceeb2de053c00 | unrated |
| CAND-05 | CAND-05__LAG-LOCK-ARM-SH13.jpg | 5c47f12190e9ba68f87f7c3f8d66f571400f8058baf9ff54ecfe406adf037567 | unrated |
| CAND-06 | CAND-06__LAG-FACE-NAT-A.jpg | ea096947b28c105000a87b430ad7964b7b28f9213e2aa341b396890479b66b36 | unrated |
| CAND-07 | CAND-07__LAG-FACE-NAT-B.jpg | e4442e4c0ea054d2a8fc01e1b407e32ec276bc26f3d5f1004fe8a9bfb2bf8262 | unrated |
| CAND-09 | CAND-09__Jet_Black_with_Lisan_user_reference.jpg | e2188aa3de4756017fa82d5b14757d24993033604de18625fd9a8a08044d3c1b | 5 |

## Per candidate, record
- Iris colour as it reads (name + rough hue).
- Glow: none / slight / strong emissive.
- Lighting influence (is colour explained by scene light?).
- Consistency between the two eyes.
- Distance from the rough/earlier reference (COMMON_RULES 9).
- Verdict for YOUR field only: SUPPORTS / MULTIVERSE (with drift comment) / HISTORY / NOT DETERMINABLE, plus one line of visible reason.
- Approval evidence for your field: HUMAN (path, date) or PROVIDER-only.

## Required outputs
1. `/workspace/v1_refinv/returns/V4_eyes_<UTC>_batch01_v001.md` + `.sha256`: the first 3 candidates in INDEX order (checkpoint).
2. `/workspace/v1_refinv/returns/V4_eyes_<UTC>_v001.md` + `.sha256`: all 8 candidates (batch 1 may be repeated verbatim or referenced by path+sha), then these sections:
   - `## Converged look (Eyes)`: one paragraph naming the single representative image (cand_id + sha256) that best anchors the field, and the exact feature description as seen in it.
   - `## Supporting images`: table cand_id | path | sha256 | role (anchor / supports / multiverse / history).
   - `## Unresolved fork`: AT MOST ONE choice you can't resolve from visible evidence, phrased as an A/B question for Ziggy, with the two cand_ids.
   - `## Out-of-lane notes`: one line each, for V_1.
   - `## Method`: tool/model used, viewing scale, any image not viewable.
3. Report path + sha256 + UTC of each file to Chief. Don't message other lanes directly; V_1 reconciles.

## Acceptance checklist (V4_eyes)
1. Header states lane, bot id, UTC, tool/model, and that pixels were seen (or exact blocker).
2. Every candidate in refs/INDEX.tsv has an entry keyed by cand_id + sha256 matching CANDIDATES.tsv.
3. Every check line above is answered or marked "not determinable at my scale".
4. Sides are given as HIS left/right, with direct/reflected noted.
5. Each verdict is one of SUPPORTS / MULTIVERSE / HISTORY / NOT DETERMINABLE; every MULTIVERSE has a drift diagnosis.
6. Distance-from-rough-reference noted per candidate.
7. Star prior shown per candidate; any disagreement with the prior stated with visible reason.
8. Approval evidence labelled HUMAN or PROVIDER with path; no nomination presented as approval.
9. Exactly one converged anchor image (or "none supportable", with reason); no composite or averaged person.
10. At most one unresolved fork.
11. No grades/scores/pass-fail; no forbidden paths opened; nothing generated.
12. batch01 and final files frozen with matching `.sha256` sidecars; no edits after freeze (corrections = _v002).
