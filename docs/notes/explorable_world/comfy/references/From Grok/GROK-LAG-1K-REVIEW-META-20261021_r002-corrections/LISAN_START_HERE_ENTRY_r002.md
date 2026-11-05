# Lisan START_HERE entry (CFA-META-20261021 r002, "Lisan r002 corrections")

- **Dataset:** Lisan Al Gaib (LAG-1K originals + repairs; LAG-VIS-NATURAL chin-fix set)
- **Authoritative:** r001 (base, frozen) + r002 corrections; r002 wins on the fields it lists
- **Readiness:** r001 READY per Chief receipt CFA-META-20261021 r001. r002 PREPARING until the Chief confirms it on D:.
- **Metadata verification:** r001: 208/208 SHA256SUMS_r001.txt entries match on D:. Chin-fix folder: 14/14. r002: see SHA256SUMS_r002.txt and the Chief receipt.
- **Media availability (separate statement):** 997 originals + 70 repair versions all resolve to matching bytes on D: (Codex read-only check: 1,067/1,067). 3 rows are DECLARED_NOT_ON_DISK placeholders (set declared as 1,000, 997 drafts exist); no file, hash or ID invented. VIS chin-fix set: 14/14 current fixes on D: (10 in v003-redo\01_VISEMES, 4 in the chin-fix folder).
- **Scores:** Only V Team verdicts are VALIDATED (fix scope only). HaL / Z bot / Chief scores are PRELIMINARY. Dedup/multiverse tags PRELIMINARY pending Ziggy.
- **Source-root mapping (box -> D:):** exact per-file D: paths are in r001 `D_PATH_MAP_r001.tsv` (joined by full sha256, not filename). Summary:
  - /workspace/lisan-al-gaib/LAG-1K/<category>/<frame>.jpg -> D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\GROK-LAG-1K-C01..C45, GROK-LAG-1K-G1, LAG1K_Z1, LAG-1K (exact per-file paths: D_PATH_MAP_r001.tsv in r001)
  - /workspace/lisan-al-gaib/LAG-1K/<category>/*-fix*.jpg -> D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\GROK-LAG-1K-FIXES-20261021\<category>\ (47 final fixes) and r001 media\repairs\<category>\ (all 70 versions)
  - /workspace/lisan-al-gaib/LAG-1K/C13-sandworm-rising/repairs/ -> r001 media\repairs\C13-sandworm-rising\
  - /workspace/lisan-al-gaib/GROK-LAG-VIS-NATURAL-v003-redo/01_VISEMES/ -> D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\GROK-LAG-VIS-NATURAL-v003-redo\01_VISEMES\
  - /workspace/lag-meta/GROK-LAG-VIS-NATURAL-v003-redo_chinfix-v005-v006/ -> D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\GROK-LAG-VIS-NATURAL-v003-redo_chinfix-v005-v006\

## Folders (also as `LISAN_START_HERE_ROWS_r002.tsv`, Z_6's START_HERE columns)

| revision | D: root | manifest | manifest sha256 | files | authoritative | media |
|---|---|---|---|---|---|---|
| r001 (Lisan LAG-1K review metadata) | `D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\GROK-LAG-1K-REVIEW-META-20261021\` | SHA256SUMS_r001.txt | 695dc063578f72c4d16fa9339e4d21a1071f20a6c4610ea595a204d88731802d | 209 | yes | ALL |
| r002 (Lisan r002 corrections) | `D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\GROK-LAG-1K-REVIEW-META-20261021_r002-corrections\` | SHA256SUMS_r002.txt | SELF (this row sits inside the manifest; sha given in the Pent H | 11 | yes | NONE (metadata-only supplement; all media referenced by hash in r001 and the folders below) |
| chin-fix folder v005-v006 | `D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\GROK-LAG-VIS-NATURAL-v003-redo_chinfix-v005-v006\` | FOLDER_SHA256SUMS.txt | 711ade6158df63a06ce3f5d452529e7cd3d80d1bbb2d080d85582cd96a22d42b | 15 | yes | ALL |
| GROK-LAG-1K-FIXES-20261021 (media: 47 final fixes) | `D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\GROK-LAG-1K-FIXES-20261021\` | SHA256SUMS | f4ed0bb9f3a06c859d08b9ec78d93870bb34a3010f69575501c902814ce4d522 | 74 | yes | ALL |
| GROK-LAG-1K-FIXES-20261021 (FIX_INDEX.tsv / README lineage and verdict text) | `D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\GROK-LAG-1K-FIXES-20261021\` | SHA256SUMS | f4ed0bb9f3a06c859d08b9ec78d93870bb34a3010f69575501c902814ce4d522 | 74 | superseded | n/a |
| GROK-LAG-VIS-NATURAL-v003-redo (current parts) | `D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\GROK-LAG-VIS-NATURAL-v003-redo\` | SHA256SUMS | 17ab4c95dc95aaa91a258341a2b028f9450b41fcd7ccaf8c96ffe8dcce35e284 | 39 | yes | ALL for the current parts |
| GROK-LAG-VIS-NATURAL-v003-redo (superseded parts) | `D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\GROK-LAG-VIS-NATURAL-v003-redo\01_VISEMES\` | SHA256SUMS | 17ab4c95dc95aaa91a258341a2b028f9450b41fcd7ccaf8c96ffe8dcce35e284 | 39 | superseded | n/a (kept as history, do not ingest as current) |

Frame-family join: dataset + frame_family -> root_original_sha256 / version_sha256 / base_sha256 + donor_sha256s (r002 LINEAGE_CORRECTIONS) -> D: path (r001 D_PATH_MAP) -> selected candidate and scoped status (r001 index final_passed_version + r002 STATUS_UPDATES). "Final version" means the latest V_3-passed version for the fix scope, not Ziggy acceptance.
