# Proposal for Site Nova: one storyboard, two lenses (the Hon panel view re-pointed at the seventy authored shots)

Author: Claude, lead writer and Pan_Handlers file steward. Date: 2026-10-31. Status: **proposal, held for Site Nova's return**. Ziggy's direction of this morning, in substance: he agrees with cleaning up the Hon panel section so that it represents the known seventy shots with the panel-flavor experience; implementation waits for Nova; and the way the Criminal Mind's cover cards were built should inform how the panel view complements the Structure & gaps page. No site file is edited by this note and no action is requested of anyone while she is away. Site ownership, navigation and publication stay with Site Nova; how to implement is hers.

Read for this note: `apps/creative_studio/story_view.py` (the two views), `apps/creative_studio/library/design_catalog.json` as built 2026-10-30 at 21:21 local (the local master; the hosted app mirrors it), `visual_library/storyboard_structure.py` (the Hon adapter) and `visual_library/criminal_mind_storyboard.py`, and the Grok team's TCM storyboard hand-off zip of 2026-10-31 (`comfy/references/From Grok/GROK-TCM-STORYBOARD-HANDOFF_v001/TCM-STORYBOARD-HANDOFF_v001.zip`, sha256 1bd8cc49285f493e8ff279fb17392b4345c19ca2b2728f87ceda833c3beb69f9, 30613513 bytes; README, cover-card index and beat table read; nothing in it executed).

## 1. What the two views are, as built

- **Panels & writings** is the picture-first lens. For a song story it renders `song_panels`: the images in the project's storyboard albums that do not belong to a registered sequence and that carry a storyboard position, ordered by storyboard order, filtered by stage, position and theme, each opening to its beat, lyric connection and review notes. For a sequence story it walks the sequence's shots scene by scene with one preview per shot and an honest "No frame linked yet". It answers what the film looks like and in what order.
- **Structure & gaps** is the writing-first ledger: the authored shots in their sequences, the sixteen main fields and twelve Kitchen fields each with a status, the source-foundation state, linked references, take history and the blank template. It answers what is written, what is missing, what is selected and what is ready.

Both lenses are worth keeping. The defect is that in Hon they are pointed at two different objects.

## 2. The facts in the local master

| | Panels & writings | Structure & gaps |
| --- | --- | --- |
| Hon, fed from | the 36 October 7 panels in the six story albums (pay, debt, ship, turn, love, outro); the only Hon storyboard assets with a storyboard position | the 70 authored shots of October 28 in 14 sections (`storyboardStructure`, story `hon:strictly-business`) |
| How they connect today | nothing on the panel side knows the 70 shots | 60 shots carry 145 reference links; 17 carry crosswalk IDs to the old SB panels; only this view shows them |
| The Criminal Mind, fed from | the registered sequence `criminal_mind:the-criminal-mind`: the same 165 shots in 41 source scenes, rendered per scene with "No frame linked yet" (2 shots carry links) | the same 165 shots with their fields (all draft; references and starting frame missing on all) |

So the Criminal Mind already has one shot list in two lenses, and Hon has two objects: a gallery of a superseded draft, and a ledger of the current writing that the gallery never learns about.

## 3. The proposal

**3.1 Hon's panel view iterates the seventy authored shots in section order.** The record's `storyboardStructure` is the shot list; the song story keeps its song features (the lyric line, the position slider as storyboard order, themes as sections). Each panel shows one picture by a fixed precedence, with its status printed under it:

1. the bound prepared starting frame, when the selection record holds one (status: bound, with its recorded stage);
2. otherwise the reference or inspiration asset the shot's writing names for that purpose (status: inspiration, or the role the writing gives it);
3. otherwise the earlier SB panel the crosswalk links (status: earlier panel, superseded);
4. otherwise an honest empty frame with the shot's title (status: none).

Under the picture: the shot id and title, the section's spine beat and the shot's cue anchor where written, the authoring maturity and the source-foundation state as the ledger already derives them, the review-note count, and the existing "open written shot" hook (`focus_authored_shot`) so one tap lands in Structure & gaps on the same shot. The look stays as simple as today's grid.

**3.2 The 36 October 7 panels become what they now are:** inspiration assets, reachable from the Library album and from the shots that cite them, no longer the storyboard grid.

**3.3 The Criminal Mind's cover cards are the same model with a different picture precedence.** The Grok team's hand-off gives every one of the 165 shots a cover card (title, source lines, set family, time layer, a placeholder starter set image labelled as not a selection) and a beat table of starter cast faces keyed to candidate ids. On the site that is precedence step 2 with the status "placeholder", never "selected". One label vocabulary across projects: **bound · inspiration · placeholder · earlier panel · none**.

**3.4 Takes do not fork the panel.** The panel shows the current take's picture (the single leaf in the take ledger); a take 2 beside take 1 changes the panel only when it becomes the leaf. Unresolved branches show the ledger's existing warning.

## 4. What the writer supplies so the picture is not the site's guess

The blocks already name references by role (11.2) and inspiration apart from conditioning (11.3). From the next addendum on, each Hon block carries one line, "Panel picture: <asset id or none>, <status>", naming which linked asset to show while nothing is bound; the writer writes none where nothing honest exists. For the Criminal Mind the writer's audit of the Grok placeholders (in progress today) returns a per-shot keep, change or scrap on the starter set image, so the placeholder shown is the writer's current proposal and Baldadoon's selections replace it as they land.

## 5. Adapter staleness to take in the same round

- `storyboard_structure.py` reads the opening packet, the S02 packet and the S01-1 example only. The ten opening blocks (`OPENING_KITCHEN_BLOCKS_20261029.md`), the S03 packet (`S03_PACKET_20261029.md`), S01-1 take 1 revision B (`S01-1_TAKE1_REVISION_B_20261030.md`, which supersedes the example where it says so) and Addendum B's foundation lines are not ingested, so the ledger counts 11 Kitchen blocks written where 23 exist. Addendum C (today) brings the wardrobe rows from the author interview; the adapter should read it too.
- All seventy Hon shots read Preliminary by a hard-coded stage. Ziggy's maturity rule of 2026-10-30 makes the writer's sections Detailed design from draft 1; that scoped reconciliation is already yours.

## 6. Non-goals

Nothing is promoted by appearing in a panel; a picture shown as inspiration or placeholder is not a selection, a starting frame or an acceptance; reviews are untouched; nothing is generated.

## 7. For Site Nova to decide when she returns

Whether to render Hon's panels from the structure under the song story kind or to add a structure-backed branch for any story that has one; where the picture precedence is derived (the site, from fields that already exist); the exact label words; and whether the position slider becomes section-based for structure-backed panels. The writer's part (the panel-picture line and the Criminal Mind placeholder audit) does not wait on those answers.
