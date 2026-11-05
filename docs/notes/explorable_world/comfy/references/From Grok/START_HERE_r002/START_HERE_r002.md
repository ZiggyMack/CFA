# START_HERE r002 — CFA handoff index (Falcon, Lisan, video test)

Status: **PREPARING**. Nothing has been sent to Nova or posted. The TSV is the machine-readable index; this page explains it.

12 rows: 4 Falcon (v001 and v002 superseded, v004 authoritative, resolver r001), 1 video test (Chief's row, verbatim), 7 Lisan (HaL's LISAN_START_HERE_ROWS_r002.tsv, sha 99f271d7cdf7b9ac104d61990367f3187080aabd7baffd7f7a7f96c96ad8d5bf, merged verbatim except that the r002 manifest cell SELF was replaced with c123b2bb...598546, as stated in that row's note).

Rules: metadata verification is separate from media availability. Only rows with authoritative=yes are ingested. Superseded rows are history and must not be ingested.

Falcon: authoritative metadata = FALCON-METADATA v004 (a47d04cd), read together with FALCON-META-RESOLVER r001 (65838b8a). Counts after the resolver copies: RESOLVED locally = 1,224 originals + 68 repairs; UNRESOLVED = 0 originals + 144 historical repair versions; 5/5 version-only bases resolved; 3 final-version pointers unresolved, a subset of the 144, none a current pass.

| # | dataset | package | revision | authoritative | manifest sha256 |
|---|---|---|---|---|---|
| 1 | GROK-HD-FALCON-1000 | FALCON-METADATA | v001 | superseded | n/a (main table FALCON_METADATA_v001.tsv = 43c0bae69478074fcceb2 |
| 2 | GROK-HD-FALCON-1000 | FALCON-METADATA | v002 | superseded | n/a (main table FALCON_METADATA_v002.tsv = 5410474f7fad5390dcd07 |
| 3 | GROK-HD-FALCON-1000 | FALCON-METADATA | v004 (FALCON-META rev v004) | yes (authoritative metadata; read with FALCON-META-RESOLVER r001) | a47d04cd439f72d6d75924a90c94aa87301e46b15144432829a4f38d132e50ad |
| 4 | GROK-HD-FALCON-1000 | FALCON-META-RESOLVER | r001 (supplement to v004) | yes (supplement; does not replace v004) | 65838b8aba722567d684558fa84964de01d152d8fac07650bca2de3f05363fb8 |
| 5 | video-test | GROK-VIDEO-TEST | v001 | yes | d764aef124f1dbe597d20602d13c6b0afe1c5efe18370afaa17cbac941eb9949 |
| 6 | LAG-1K | CFA-META-20261021 | r001 (Lisan LAG-1K review metadata) | yes | 695dc063578f72c4d16fa9339e4d21a1071f20a6c4610ea595a204d88731802d |
| 7 | LAG-1K + LAG-VIS-NATURAL | CFA-META-20261021 | r002 (Lisan r002 corrections) | yes | c123b2bbd3ac60416d5496fa2605962b404b83e23a8b5d0e3bd0e66c7b598546 |
| 8 | LAG-VIS-NATURAL (chin-fix set) | CFA-META-20261021 | chin-fix folder v005-v006 | yes | 711ade6158df63a06ce3f5d452529e7cd3d80d1bbb2d080d85582cd96a22d42b |
| 9 | LAG-1K | CFA-META-20261021 | GROK-LAG-1K-FIXES-20261021 (media: 47 final fixes) | yes | f4ed0bb9f3a06c859d08b9ec78d93870bb34a3010f69575501c902814ce4d522 |
| 10 | LAG-1K | CFA-META-20261021 | GROK-LAG-1K-FIXES-20261021 (FIX_INDEX.tsv / README lineage and verdict text) | superseded | f4ed0bb9f3a06c859d08b9ec78d93870bb34a3010f69575501c902814ce4d522 |
| 11 | LAG-VIS-NATURAL | CFA-META-20261021 | GROK-LAG-VIS-NATURAL-v003-redo (current parts) | yes | 17ab4c95dc95aaa91a258341a2b028f9450b41fcd7ccaf8c96ffe8dcce35e284 |
| 12 | LAG-VIS-NATURAL | CFA-META-20261021 | GROK-LAG-VIS-NATURAL-v003-redo (superseded parts) | superseded | 17ab4c95dc95aaa91a258341a2b028f9450b41fcd7ccaf8c96ffe8dcce35e284 |
