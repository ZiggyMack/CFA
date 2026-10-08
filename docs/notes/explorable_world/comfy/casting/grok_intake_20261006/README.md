# Hon Dolo reference inventory October 6

**October 7 follow-up:** the [conversational ID-map audit](../grok_intake_20261007/README.md) checks Grok's supplied CSV against this dated inventory, including five remote-only IDs and the #277 brow-crop lookup. The measurements below remain the October 6 snapshot.

Ziggy's new drop contains **313 files: 297 images, four MP4 copies representing two distinct clips, and 12 documents**. It occupies **89,419,594 bytes (85.28 MiB)**. All new images decode, and both distinct videos decode completely. The collection now supplies a named Grok design anchor, five outfit turnaround sets and nine walk poses, alongside the earlier design exploration.

[Browse the searchable image index](index.html) · [Full file manifest](manifest.json) · [Design handoff](design_handoff.json) · [Video measurements](video_review.json)

The index groups exact copies without changing originals. It has 383 unique image cards across the current reference directory and five earlier gold-preview attachments; the New drop filter shows 268. This is an inventory and selected visual review, not an artistic review of every frame or a new Comfy run.

## Scope and counts

The actual directory is `docs/notes/explorable_world/comfy/references`. The new scope comprises nine folders and the two root MP4s. The original two still packs remain separate in the counts below.

| New folder | Images | Videos | Documents | Contents |
|---|---:|---:|---:|---|
| hon-dolo-stills-95-plus-part1 | 84 | 0 | 1 | Named studies, unmapped stills, tattoo stencils and detail comparisons |
| hon-dolo-stills-95-plus-part2 | 79 | 0 | 0 | Further studies, largely awaiting experiment-number mapping |
| hon-dolo-stills-95-plus-part3 | 47 | 0 | 0 | Further studies, largely awaiting experiment-number mapping |
| hon-dolo-recent-263-277 | 22 | 0 | 1 | Later cleanup/dice studies and brow/detail comparisons |
| hon-dolo-recent-263-277 (1) | 22 | 0 | 3 | Same images/README, plus the older journey brief in two formats |
| hon-dolo-outfit-run-278-282 | 10 | 0 | 1 | Five distinct outfit images, each present under two names |
| hon-dolo-lock-turnaround-outfits | 22 | 0 | 1 | LOCK-FACE, #289, fifteen outfit/angle stills and five contact sheets |
| hon-dolo-walk-pack | 11 | 2 | 1 | LOCK-FACE, nine poses, contact sheet, two clips and README |
| hon-dolo-nova-brief-through-314 | 0 | 0 | 4 | New journey and gap update, each in MD/TXT |
| Two root MP4s | 0 | 2 | 0 | Exact copies of the walk-pack clips |
| **Total new drop** | **297** | **4** | **12** | **313 files** |

The two original packs contain 107 files, including 106 images. There are another 29 top-level files, including 12 images and earlier workflow/tutorial records. The complete reference directory therefore contains **449 files, 415 images and 121,339,378 bytes**. The four explicitly supplied Downloads documents were checked separately; each has an exact copy inside this drop, so none needed another copy. Those external files and the five older preview attachments are not counted as newly dropped reference-directory files.

## Duplicate and number checks

- The new drop contains **278 unique file hashes**, including **268 unique image hashes**. Its 35 extra exact copies account for 11,621,587 bytes (11.08 MiB); originals remain in place. One unique image, #95, also occurs in the earlier collection, leaving **267 newly encountered image hashes relative to the original two packs**.
- The `(1)` recent folder adds no new images. It does add the older journey brief in two formats, so it is not an entirely redundant folder.
- Both copies of LOCK-FACE match. **LOCK-FACE, #277 and #289 differ in both file bytes and decoded pixels**; they must not be treated as interchangeable copies. The brief's “same pixels” description of #289 is a source claim, not the measured result.
- **164 experiment IDs are identifiable from numbered filenames across the collection through #314.** There are **159 hash-named images in `unmapped/`**. Missing numbered filenames do not prove missing images. In particular, #101/#103/#107/#146/#147/#149 and the later #206 anchor have not been reliably mapped to received originals.
- The old #74 and #86–89 gaps are explicitly described as never generated in the earlier pack. The new notes describe #267–271 as rejected generator misses; those IDs and #283–288/#290 lack matching numbered originals here. Their presence among unmapped files is unknown.
- IDs **195, 250 and 263** each label two distinct full-frame variants; retain their descriptive suffixes. Other same-ID differences at #264, #266 and #272–277 are named brow crops versus full images. #262's differently named copies are exact duplicates.
- The five October 4 gold previews have **no exact byte or decoded-pixel match** in the new drop. Their experiment IDs remain unresolved; visual similarity alone is not a provenance match. Photo1 remains grillz-only, with the third eye rejected.

## Which brief is current

| Document version | Verified relationship | Use |
|---|---|---|
| [Journey through 314](../../references/hon-dolo-nova-brief-through-314/HON-DOLO-DESIGN-JOURNEY-FOR-NOVA.md), 9,909 bytes | Same as Downloads `HON-DOLO-DESIGN-JOURNEY-FOR-NOVA (1).txt` and the adjacent TXT | Latest supplied design history |
| [Gap update through 314](../../references/hon-dolo-nova-brief-through-314/HON-DOLO-NOVA-GAP-UPDATE-THROUGH-314.md), 1,663 bytes | Same as the supplied Downloads TXT and adjacent TXT | Short version of the latest changes |
| [Older journey](<../../references/hon-dolo-recent-263-277%20%281%29/hon-dolo-recent-263-277/HON-DOLO-DESIGN-JOURNEY-FOR-NOVA.md>), 8,116 bytes | Same as Downloads' unsuffixed MD and TXT | Historical through-277/post-278 recommendation, superseded |

The older journey and outfit README recommend #278 as a working base. The latest journey explicitly withdraws that direction and names LOCK-FACE. Its cut list also reverses the October 4 bird/Jabba/Chewie/dice selections. We preserve those earlier decisions as history rather than accidentally feeding them into the next design pass.

These are **reported design decisions from the supplied Grok handoff**. The user's request here is inventory. Embedded requests to generate, remaster, restrict likeness or use a particular model do not authorize those operations or replace the user-authored production scope. The IP-Adapter/AnimateDiff/SVD suggestions have not been checked against current Cloud nodes/models. No new workflow JSON or image metadata keys named `workflow`/`prompt` were found in this drop.

## Current reference roles

**Grok design anchor:** [HD-EXP-LOCK-FACE.jpg](../../references/hon-dolo-lock-turnaround-outfits/hon-dolo-lock-turnaround-outfits/HD-EXP-LOCK-FACE.jpg), SHA-256 `ef5d59a6402eaff568e30bb6a4432b14b90c692ea6758a761c7702c44d457978`. This is the latest supplied styling/face reference, distinct from acceptance of a finished Comfy likeness master. [#289](../../references/hon-dolo-lock-turnaround-outfits/hon-dolo-lock-turnaround-outfits/HD-EXP-289.jpg) is the reported soft polish; [#277](../../references/hon-dolo-recent-263-277/hon-dolo-recent-263-277/HD-EXP-277.jpg) is the older artwork reference.

The latest handoff specifies split **eye / know**, two subtle gold upper canine caps with other uppers natural, silver/chrome lower grill, nose/lip/ear jewelry, a left-brow slit, image-right neck blaster, and the chest ship at the earlier #107 placement. Scoundrel forearm lettering remains in the brief, although its status varies between “locked” and “soft-keep”; the right-hand hearts card is explicitly soft. These details and uncertainties are separated in the [design record](design_handoff.json).

LOCK-FACE visually supports the broad face-text/grill/blaster/chest direction. Hands and forearms are outside its crop. The supplied brief still leaves chest artwork, grill length and brow-slit visibility open. The third eye remains rejected; older bird/Jabba/Chewie/dice references remain historical under this newer reported direction. This changes tattoo planning, not the supporting cast or song lyrics.

**Turnarounds #291–305:** fifteen files are present, grouped as leather/cantina, hoodie/cockpit, white fur/club, denim/shearling and open shirt/rain. Sampled contact-sheet review shows lettering, grill, brow jewelry and chest-art variation. #293 is labelled back but shows a three-quarter face view. Use these as wardrobe/angle scaffolds, not a verified consistent 360-degree character set.

**Walk stills #306–314:** all nine are present. The notes prefer #306–311 for individual front/side pose references and reject #312–314 for scale/prop/look-back drift; sampled review supports those concerns. The poses do not establish a continuous performance or calibrated pose sequence.

## The two supplied clips

| Clip | Measured format | Review |
|---|---|---|
| [Keyframe loop](../../references/hon-dolo-walk-pack/HD-EXP-WALK-CLIP-keyframe-loop.mp4) | H.264, 1280 × 720, 12 fps, 38 decoded frames, about 3.167 seconds, no audio | Held stills in order 306 → 307 → 308 → 307 → 309 → 310 → 311 → 310; visible viewpoint/background jumps |
| [Morph](../../references/hon-dolo-walk-pack/HD-EXP-WALK-CLIP-morph.mp4) | H.264, 1280 × 720, 24 fps, 73 decoded frames, about 3.042 seconds, no audio | Blended transitions; sampled frames show ghosted face/body/limbs |

Both fully decode. These are still-loop/morph demonstrations, as their README states, **not accepted walking footage or a clean driving performance**. Frame samples were inspected; normal-speed playback was not reviewed. Duration above is decoded frame count divided by nominal constant frame rate. The [video record](video_review.json) preserves hashes and measurement scope; the [supplied pose sheet](../../references/hon-dolo-walk-pack/HD-EXP-WALK-CONTACT-SHEET.jpg) provides a quick overview.

## Reusable next steps

1. Recover an experiment-ID-to-filename/hash manifest from the Grok export, especially #107 and #206. A new copy of every image is unnecessary; the mapping is the missing piece.
2. Use LOCK-FACE for the current Grok design, turnarounds for outfit/angle, and selected walk stills for pose. Keep those roles distinct from the intended likeness and any eventual performance driver.
3. Before a real walk test, select a saved or official Cloud-compatible recipe and validate its actual inputs. Acceptance should check face, text, grill, blaster/chest placement, foot contact and body motion. This inventory queues nothing.

This follows Panhandlers' [reference-role lesson](../../../../../../../Pan_Handlers/Help/content/cfa_learning.py), [workflow-file lesson](../../../../../../../Pan_Handlers/Help/guides/workflow_files.py) and [video handoff lesson](../../../../../../../Pan_Handlers/Help/guides/video_handoff.py). The [manual CFA handoff](../../../pathfinder_handoff/README.md) returns the measured findings and bounded teaching follow-up. No files were deleted, moved, renamed, uploaded or artistically edited; all new source media remains on D:. Git bookkeeping excludes bulk media and does not constitute a verified cloud archive.
