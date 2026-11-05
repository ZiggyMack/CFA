LAG-1K duplicate pass - delivery v001 (2026-10-21, ET)
=======================================================
What this is: the frozen result of the Lisan al-Gaib LAG-1K duplicate pass.
Everything here is PENDING ZIGGY. It was a tag-only pass: no image was moved,
renamed or deleted.

How it was made
- HaL grouped the 997 LAG-1K drafts by image similarity (64-bit dHash, within
  10 bits, same category only): 192 images in 43 lookalike clusters, 805 with
  no close match. -> DUP-CLUSTERS-v001.tsv
- V_1's team (V_2..V_5) judged and tagged every clustered image under Ziggy's
  rule: lighting, FX, backdrop, landmark and expression changes all count as
  different (VARIANT). Batch stamp 20261021T053554Z.

Headline
- 192 clustered images, 0 true duplicates: 128 VARIANT, 47 KEEP-IDEA-FIX-FACE,
  11 NOT-A-DUP, 5 DRIFT-MULTIVERSE, 1 DUPLICATE-KEEPER.
  The pass mostly confirmed variety rather than shrinking the pile.
- Fix list (47, redo from the locked anchor, face only). Top reasons: chin
  reads GAB (11), eye disc wrong (9), reads as a different man (8), chin
  misread/misplaced (5), AL wrong (5), broken worms (4).
- Open question for Ziggy: LAG-1K faces read younger, clean-shaven and slimmer
  than the CAND-01 target (C33 is the exception). Accept as baseline or treat
  as drift?

Files
- V1_dedup_LAG1K_summary_20261021T053554Z_v001.md  - read this first
- V1_dedup_LAG1K_rollup_20261021T053554Z_v001.tsv  - one row per image, tags
- V1_dedup_LAG1K_fixlist_20261021T053554Z_v001.tsv - the 47 fix-face rows
- *.sha256                                          - sidecar hashes
- DUP-CLUSTERS-v001.tsv (HaL) sha256
  ecea3ded6d0dcb43e4201a466782660dd2559c2fa3b369ee22ec49946c6240b3
- dedup_sheets\  - 12 comparison/flavor sheets (+ .sha256 sidecars) for
  picking favourites

Checked by Chief before delivery: all sidecar hashes match; tag counts match
the summary; all 192 rows map 1:1 to HaL's cluster file (same cluster,
category and sha256); the fix list equals the 47 KEEP-IDEA-FIX-FACE rows.
