# FALCON r002 SUMMARY — FALCON-META rev v004 + resolver r001

Status: **PREPARING**. Nothing sent to Nova and nothing posted. Supplement folder: `FALCON-META-RESOLVER_r001/` (box: /workspace/falcon1000/_nova_metadata_v001/FALCON-META-RESOLVER_r001/; intended D:: `D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\FALCON-META-RESOLVER_r001\` once Chief pushes it).

## Revisions
- **FALCON-METADATA v004** (MANIFEST_v004.sha256 a47d04cd439f72d6d75924a90c94aa87301e46b15144432829a4f38d132e50ad, 5 files) is the **authoritative metadata**. Read it with resolver r001.
- **FALCON-META-RESOLVER r001** (this folder) is a supplement: D: path map, intended deliverables that were missing, root/base/donor lineage, wording corrections, and a bundle of evidence sheets. It does not change any v004 verdict, status or decision.
- FALCON-METADATA v001 / v002 on D: are **superseded** by v004. Do not ingest them. v003 was box-only and was never pushed.

## Metadata verification vs media availability (separate)
- Metadata verification: Site Index PATH_AUDIT verified the 5/5 v004 manifest files on D: with 0 failures.
- Media availability is listed per media record in FALCON_D_PATH_MAP_r001.tsv. Every record was matched on its FULL SHA-256, never on filename alone.

## Count labels (Site Index wording; recomputed after the resolver copies)
Before copies (PATH_AUDIT): RESOLVED locally = 1,223 originals + 62 repairs. UNRESOLVED = 1 original (C04-006 original, 35398903) + 150 historical repair versions. All 5 version-only bases resolve once matched by hash. The 9 unresolved final-version pointers are a SUBSET of the 150 (6 of them are current scoped passes), not extra files.

**After the resolver copies (r002 labels):**
- **RESOLVED locally: 1,224 originals + 68 repairs** (1,223 originals + 62 repairs on D:, plus 1 original + 6 repairs in resolver media/, which reach D: when Chief pushes).
- **UNRESOLVED: 0 originals + 144 historical repair versions** (HISTORY_ONLY_DEFERRED, retrievable from the box path in the map).
- Version-only bases: 5/5 RESOLVED (C22-022-v001, C24-019-v001 and C24-020-v001 sit on D: under their unversioned names in GROK-HD-FALCON-1000).
- Final-version pointers: 63 in total. 54 are on D:, 6 are in resolver media/ (all 6 current scoped passes), and **3 remain UNRESOLVED**. Those 3 are a subset of the 144, and none of them is a current pass: C04-battle-light-008-v007b (not passed, FIX), C41-cockpit-ext-004_Z_3_v003-fix (Ziggy pick) and C69-hyperspace-exit-012_Z_3_v002-fix (Ziggy pick).
- Availability: DELIVERED 1,290 / NOT_DELIVERED_INTENDED 7 (all copied here) / HISTORY_ONLY_DEFERRED 144. Total 1,441 media records.

## Copied deliverables (byte copies, hash-verified, existing filenames)
| frame | file (media/) | sha256 | why |
|---|---|---|---|
| C04-battle-light-006 | C04-battle-light/before_C04-battle-light-006.jpg | 35398903a8f11bb5a850a21fe13c0b3d0894a511f6e5d2808104211cd152c9da | true original (Chief ruling) |
| C05-lurch-grin-002 | C05-lurch-grin/C05-lurch-grin-002_grill-v002-s444.jpg | b0645d7473a872d92478c0c5b7b1ffcaec2231cbbe4f5ceeef77175dda366158 | current scoped pass (grill) |
| C05-lurch-grin-004 | C05-lurch-grin/C05-lurch-grin-004_grill-v002-s444.jpg | e91ff8cb7b520492a949b8d0be8f2438884e74f18bbfe68dd08292fab2e5b982 | current scoped pass (grill) |
| C05-lurch-grin-007 | C05-lurch-grin/C05-lurch-grin-007_grill-v001-s444.jpg | 340306c59572da1a10d27fa598d2fb377a79d08586664d54188c776dd81cbfd8 | current scoped pass (grill) |
| C05-lurch-grin-009 | C05-lurch-grin/C05-lurch-grin-009_grill-v001-s444.jpg | 2b01ee3832c7256614c1ef815784ff203563cef6e218bc1a0793e896395f5a7d | current scoped pass (grill) |
| C05-lurch-grin-014 | C05-lurch-grin/C05-lurch-grin-014_grill-v001-s444.jpg | 3ca9a3b71b3316db3e66608464ce3b4fc0c827b783d592abd68250afb3d38281 | current scoped pass (grill) |
| C41-cockpit-ext-002 | C41-cockpit-ext/C41-cockpit-ext-002-v002.jpg | 695fab2875dbfb644c7b8166c94c4fe89441c6aa35a06c0a81b30e8f4c1e7430 | current scoped pass |

## D: roots (source-root map /workspace -> D:)
- /workspace/falcon1000/<category>/ -> `...\From Grok\GROK-HD-FALCON-1000\<category>\` for C01-C28 and C41+. **Anomaly:** C29-C40 (180 originals) sit directly under `...\From Grok\<category>\`, not inside GROK-HD-FALCON-1000. Both locations are hash-verified, and nothing was moved.
- Chest repairs: `...\From Grok\HD-FALCON-CHEST_v001\` (49 records), `...\From Grok\HD-FALCON-CHEST_v002_supplement\` (8 records).
- Resolver media: `FALCON-META-RESOLVER_r001\media\<category>\` (7 files), after Chief's push.
- Every exact D: path is in FALCON_D_PATH_MAP_r001.tsv, taken from a read-only full-hash rescan made on 2026-10-21 plus PATH_AUDIT.

## Lineage (LINEAGE_r001.tsv, 212 repairs)
root_original_sha256 = the v004 family original (C04-006 -> 35398903). base_parent_sha256 = the recorded edit input; it is **unknown for 91** repairs where no source records it, and no chain was inferred from filenames. donor_sha256s = unknown for all 212, because no Falcon source records patch donors per file.

## Evidence (EVIDENCE_SOURCES_r001.tsv, 128 v004 source_inventory paths)
125 sheets are BUNDLED byte copies in evidence/. 4 of those live sheets changed after v004 was built (ROLLUP.md, Z8_CHEST_v001.tsv, Z9_CHEST_v003.tsv, Z10_CHEST_FULLSCALE_v001.tsv), so the bundle has the current bytes and the table records the v004-cited sha. The v004-time bytes of those 4 can't be recovered. 3 are EMBEDDED_ONLY: 2 stencil reference PNGs, plus the C04-006 original, which is copied under media/ instead.

## Still open (not packaging-complete)
- Chief to push this folder to D: and issue a READY receipt.
- 3 unresolved final pointers (above). They were not copied because none is a current pass. Copy on request.
- v004 packaging blockers that still stand: repairs keep landing (chest rebuilds to the C04-010 v011 scale), V-Team validation backlog, Ziggy's 20 dup groups plus chest variants.
