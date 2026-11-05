# LAG-1K duplicate pass: lane assignments (V_1), 20261021T052447Z
Source: /workspace/lisan-al-gaib/LAG-1K/DUP-CLUSTERS-v001.tsv (sha256 ecea3ded6d0dcb43e4201a466782660dd2559c2fa3b369ee22ec49946c6240b3, by HaL). There are 43 clusters with 192 images in total. The other 805 images have no close match and are not part of this pass.
Each cluster has one owner. Before you start, claim your clusters by writing returns/CLAIMED-<lane>_dedup.txt.

## Assignments
- V_2 (49 images): LAG-DUP-006, LAG-DUP-009, LAG-DUP-013, LAG-DUP-020, LAG-DUP-022, LAG-DUP-024, LAG-DUP-031, LAG-DUP-033, LAG-DUP-037, LAG-DUP-042, LAG-DUP-043
- V_3 (47 images): LAG-DUP-001, LAG-DUP-010, LAG-DUP-014, LAG-DUP-019, LAG-DUP-023, LAG-DUP-025, LAG-DUP-032, LAG-DUP-035, LAG-DUP-038, LAG-DUP-039
- V_4 (48 images): LAG-DUP-002, LAG-DUP-004, LAG-DUP-007, LAG-DUP-011, LAG-DUP-015, LAG-DUP-016, LAG-DUP-021, LAG-DUP-026, LAG-DUP-027, LAG-DUP-028, LAG-DUP-036
- V_5 (48 images): LAG-DUP-003, LAG-DUP-005, LAG-DUP-008, LAG-DUP-012, LAG-DUP-017, LAG-DUP-018, LAG-DUP-029, LAG-DUP-030, LAG-DUP-034, LAG-DUP-040, LAG-DUP-041

## Rules (from Ziggy, 2026-10-21)
- Tag only. Never delete, move or edit an image.
- Cluster by shot: same scene, same view, same framing. The tool's clusters are candidates, not confirmed. Split the large ones (12-20 images) by eye. On min_dhash_dist, 0-4 means near-identical and 8-10 means a similar layout only.
- Give every image one tag:
  VARIANT: same shot with a meaningful change in lighting, explosions/FX, action or pose. Keep it.
  DUPLICATE-KEEPER: the best and most on-model copy of a redundant shot.
  DUPLICATE: redundant with the keeper and nothing meaningful changed. Archive it; nothing is deleted.
  DRIFT-MULTIVERSE: same shot, but the character has drifted. Write a drift note naming the feature that drifted.
  NOT-A-DUP: the tool grouped it wrongly.
- When a sub-shot has 3 or more close versions and no clear keeper, mark it ZIGGY-PICK. V_1 builds one comparison sheet per sub-shot for Ziggy.
- Judge the keeper against current Lisan calls:
  Throat worms: style c02 (LAG-WORMSEG-c02) is Ziggy's call.
  Build: the CAND-01 lean-natural, semi-athletic frame is Ziggy's call.
  Teeth: natural by default.
  Still open: piercings and eye glow. Don't use them as keeper tiebreaks.
- Return file: returns/<LANE>_dedup_LAG1K_<UTC>_v001.tsv with these columns: cluster_id, sub_shot, path, sha256, tag, keeper_reason_or_drift_note, ziggy_pick(Y/N). Freeze it with a .sha256 sidecar.
- Post in V Team only when you're done or stuck. If you're stuck, say what you tried.
