# Hon Dolo conversational ID map — October 7

The new [Grok CSV](<../../references/From%20Grok/HD-EXP-ID-TO-FILENAME.csv>) and [consolidation handoff](<../../references/From%20Grok/NOVA-CONSOLIDATION-AND-ID-MAP.txt>) add a reusable lookup between conversational experiment IDs, file hashes and proposed reference roles. The [row-by-row audit](id_map_audit.json) checks them against the [October 6 measured manifest](../grok_intake_20261006/manifest.json) and [design handoff](../grok_intake_20261006/design_handoff.json). Both supplied files remain unchanged.

## What the map establishes

- The CSV contains **170 rows: 169 numeric experiment IDs plus LOCK-FACE**, with no duplicate IDs or malformed SHA-256 values.
- **164 numbered rows plus LOCK-FACE** match received image hashes. This preserves the previous locally identifiable ID set; it does not increase local numbered-image coverage to 169.
- **#285–288 and #290** have reported Grok filenames/hashes but no matching asset in the received October 6 inventory. These are remote-only records, not newly supplied images.
- **All 159 hash-named stills remain unmapped.** The CSV resolves none of them. In particular, **#101, #103, #107 and #206** still have no proven ID-to-file association. Chest and forearm component references cannot be recovered by guessing from file order.
- The two JSON companions mentioned in Grok's text — `HD-EXP-ID-TO-FILENAME.json` and `UNMAPPED-HASH-FILES.json` — were not supplied. The received CSV covers numbered IDs and LOCK-FACE, not the promised unmapped-file list.

`canonical_path_on_grok_box` uses Grok's `/workspace` paths. `n_paths_on_box` counts copies there; it is not a count of copies on D:. Use the audit's `local_hash_matches` to locate received files. The `REF-184`, `REF-186` and `REF-95` alias filenames mentioned in the handoff are absent here; their numbered originals are already present.

## Preserve variants when resolving an ID

The CSV's **#277 canonical row selects `HD-EXP-277-brow-zoom.png`**, an 880 × 720 detail crop. The existing artwork-map reference is the **1280 × 720 `HD-EXP-277.jpg`**. Both are legitimate received files with different hashes; a simple CSV lookup must not silently replace the full artwork map with its crop.

| Reference | SHA-256 | Intended record role |
|---|---|---|
| [LOCK-FACE](../../references/hon-dolo-walk-pack/HD-EXP-LOCK-FACE.jpg) | `ef5d59a6402eaff568e30bb6a4432b14b90c692ea6758a761c7702c44d457978` | Current Grok design anchor reported in the supplied handoff |
| [#277 full image](../../references/hon-dolo-recent-263-277/hon-dolo-recent-263-277/HD-EXP-277.jpg) | `9d3f828d43530f43dec589ea64e0a68f3b397ca39786c9bc87a97100f55fd75e` | Older artwork map |
| [#277 brow crop](../../references/hon-dolo-recent-263-277/hon-dolo-recent-263-277/HD-EXP-277-brow-zoom.png) | `9635449c3f0bc2f9532a3fb184f5290a90d0d83097a2084e85b93b5829766024` | Detail inspection; CSV's chosen canonical file |
| [#289](../../references/hon-dolo-lock-turnaround-outfits/hon-dolo-lock-turnaround-outfits/HD-EXP-289.jpg) | `4836234de5b3a94f3cd9e4407870c88e7cfbc2a1db65ea09695a24699d63c0d7` | Optional related soft polish |

The CSV also chooses brow crops for **#266 and #272–276**. Preserve the local variant lists for these IDs and for distinct full-frame variants #195, #250 and #263. A canonical filename is a lookup choice, not proof of the best production reference.

LOCK-FACE, full #277 and #289 remain distinct in bytes and decoded pixels, as measured on October 6. The new handoff explicitly corrects its earlier “same pixels” claim for #289. No accepted Comfy identity master is established by this map.

## Proposed organization, without moving sources

Grok proposes an active pool, archive/history, identity exclusions and unmapped holding. These are useful **index roles**; this intake performs no deletion, renaming, moving or quarantine, and changes no character locks. Preserve the source recommendations separately from measured file identity.

The proposed roles keep LOCK-FACE as the design anchor, #289 optional, full #277 as the older artwork map and #259 as neck-placement history. #291–305 remain outfit/angle scaffolds; #306–311 remain individual pose scaffolds. Their presence does not establish a consistent turnaround or walking performance. The rejected/drifted variants, earlier tattoo explorations and still-loop/morph clips remain available as history. Supporting-cast images belong to their own production roles and should be excluded from **Hon Dolo identity inputs**, not discarded from the project.

The next useful export is evidence that connects unresolved IDs to exact existing hashes, especially #107 and #206. No bulk recopy is needed. Workflow suggestions in the supplied text remain unverified Cloud proposals; this mapping audit performs no generation or submission. Any independent Comfy experiment has its own run record.
