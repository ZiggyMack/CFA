# Common rules for every lane (V_1 to V_5, and V_6 if added)
1. Scope: existing candidate refs only, in `/workspace/v1_refinv/lanes/<your lane>/refs/` (and `/workspace/v1_refinv/candidates/`). Use ONLY these images.
2. Forbidden: `/workspace/v1_calib/` (pilot blind images and frozen return), `/workspace/v1_push/`, `/home/box/chief_private/`, any PRIVATE_MAP / alias map / answer key, and any blind-to-original mapping. Don't hash-match candidates against pilot files. No pilot rerun or second pilot.
3. No generation or renders, no spending, no new agents or sessions, no production grades, no gold promotion, no release/hold changes, no site edits, no contacting generators.
4. View every image you report on with your image-reading tool (state the tool and model). If you can't see pixels, report the exact blocker and leave the fields blank. Never fabricate sight.
5. Report against the SHARED IDs in `/workspace/v1_refinv/CANDIDATES.tsv` (cand_id + sha256). Never invent IDs.
6. Gold is per field. Judge only your lane's field(s). Note anything else in one line under "Out-of-lane notes" for V_1.
7. Star priors: ≥3★ = candidate pool; ≤2★ = history only; "unrated" = unknown, NOT rejected. Your visible-evidence corrections beat stars or popularity, so say so explicitly when you disagree with a star prior.
8. Representative existing images only. Never describe or propose an averaged or composite person.
9. Distance check: for each candidate, note how far your field sits from the rough/earlier reference (CAND-03 lock era, plus the history text). Uniform drift can hide an off-centre feature, so describe direction and size (for example "AL 1 brow-height above the brow line").
10. Multiverse = worth keeping but maybe not the main look. When you tag a candidate Multiverse, add a comment diagnosing which feature drifted.
11. Sides: "his left/right" = the subject's own side. In a frontal view his right = image left. Record whether you see the face directly or reflected.
12. Approval evidence: mark each claim HUMAN (dated Ziggy decision or verbatim relay, with path) or PROVIDER (agent spec or nomination). A nomination alone is not approval.
13. Rolling batches: batch 1 = the first 3 candidates in your INDEX.tsv order. Write `<lane>_<UTC>_batch01_v001.md` and freeze it (rule 14). V_1 checks it against your acceptance checklist. If it passes, continue with the rest into the final return without waiting. Clear cases sort forward. Uncertain ones go in your "For Ziggy" section, never guessed.
14. Freeze: after writing a return, compute sha256 and write it to `<same name>.sha256` (format: `<sha256>  <filename>`), then never edit that file. Corrections go in a new file ending `_v002.md` (then `_v003`…) that says what it corrects. Report path, sha256 and UTC to Chief.
15. UTC stamp format in filenames: `YYYYMMDDTHHMMSSZ`.
