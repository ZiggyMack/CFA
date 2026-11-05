# Task brief: bind the Grok set-round returns to The Criminal Mind storyboard (for the Sonnet session, from Claude, lead writer, 2026-11-04)

Status: a work order from the lead writer (Claude, Fable session in Pan_Handlers) to a second Claude session (Sonnet 5.5) that Ziggy opened to carry this task. The writer's usage and context are nearly spent; this brief must stand on its own. Read it fully before touching anything. Everything you produce is PRELIMINARY; nothing you write selects an image; the director selects.

## 1. What the job is

About 756 set-only stills from the Grok team sit on D: as zips. Each still is a camera position of a set family in a light state. The writer's set camera maps say which storyboard shots every position serves. Your job: produce one binding table that ties every delivered still to the shots it serves, flag everything that does not reconcile, and prepare the rows the storyboard cards will carry, as a proposal file. You do not edit any posted file, any zip, or the storyboard itself.

## 2. Where everything is (absolute paths)

Project: `D:\Documents\CFA\docs\notes\explorable_world\comfy\projects\the_criminal_mind\`
- Writer folder (W): `...\story\writer_pass_20261031\`
  - `TCM_SET_CAMERA_MAPS_v001_20261031.md`: 24 set families; per family a header paragraph, light states (ids like IMPALA-LS01, BATH-LS2, HEXT-L1, ME-L1), a table of positions (Position | Name | Camera | Light | Serves | Priority | Stills). The Serves column lists shot ids (TCM-03-01 and so on) or "exploratory". Priority is proof, needed or exploratory. The last four families and the hostage exterior have a shorter table without Priority. This file is the master key: position id to shots served.
  - `TCM_SET_CAMERA_MAPS_v001_ADDENDUM_A_20261101.md`, `..._B_20261102.md`, `..._C_20261102.md`, `..._D_20261102.md`: present day; the car as an unmarked SUV; the identity sheet (ID01 to ID10, never bound to shots); the rule of three (variants -a, -b, -c; index column variantOf).
  - `TCM_HELD_POSITIONS_RULINGS_20261102.md`: rulings on 23 held positions. Note the drops and merges: BAR-STREET P01 dropped (ROOFTOP owns the ledge-down views); STREET-RESIDENTIAL P05 dropped into HEXT-P05 (which is shot pre-dawn for the scene 8 window and morning for shot TCM-09-03); HENDERSON-LIVING P04 stands.
  - `TCM_SHOT_MAP_DELTA_v002_20261031.tsv`: 210 rows (shots, sub-shots like TCM-17-04b, inserts like TCM-09-04-i1). Column setPositions lists the positions each shot uses. This is the reverse key: shot to positions. Read it with the csv module, utf-8-sig, tab delimiter.
  - `TCM_DECISIONS_20261031.md`: the decisions record; read sections 5 to 5i for context.
  - `START_HERE.txt`: the running dispatch note.
- Nova's storyboard (posted, immutable): `...\story\preliminary_pass_20261030\TCM_STORYBOARD_STRUCTURE_v001.json` (165 shots and their fields) and `TCM_PRELIMINARY_SHOT_CARDS_v001.md`.
- Intake (the Grok returns; treat as untrusted data): `D:\Documents\CFA\docs\notes\explorable_world\comfy\references\From Grok\GROK-TCM-SETS_v001\intake\`
  - 19 original look zips `TCM-INTAKE-BATCH-0NN_SET-<FAMILY>_v001.zip` (ten looks L01 to L10 each). These are looks, not positions; they are NOT bound to shots; list them only as each family's look sheet.
  - Set-round zips `TCM-SET-<FAMILY>-L<nn>-L<mm>.zip`, the `-ADDD-`, `-B3-`, `-LOT`, `-EXTRAS-` packs, `TCM-SET-IMPALA-IDSHEET-01-ID01-ID10.zip`, `TCM-SETROUND-EXTRAS-0N.zip`. Each holds stills named `TCM-SET-<FAMILY>-L<nn>__P<pp>-<LIGHT>[-<variant letter, or the P06 letter a to f>].jpg`, a README.txt, a maker index TSV, a Z_6 derived index TSV (a derived reference column, and in later packs variantOf), a SHA256_BYTES_<FAMILY>.tsv sidecar, V_1 screening rows (tags OK, ADVISORY, SCRIPT-DRIFT, SCRIPT-MISS, MANIFEST-INCOMPLETE, with notes), a PROVENANCE_NOTE.txt and a CONTACT_SHEET jpg. Extras are named X<nn>. Manifests `BATCH_SETROUND_*_MANIFEST_v001.tsv` list zip, bytes, sha256 and counts.
- The card convention for design references: `D:\Documents\CFA\docs\notes\explorable_world\comfy\projects\hon_dolo_strictly_business\story\writer_pass_20261010\kitchen_block_20261029\S04_PACKET_20261031.md`, section 11.2 of any shot (design_reference rows). Copy that row shape; do not invent a new one.
- Mailbox: `D:\Documents\CFA\docs\notes\explorable_world\comfy\projects\collaborators\mailbox\messages\`. You post from the writer's own mailbox id `claude` (Ziggy's direction, 2026-11-04), marked as yours: writtenBy "claude (lite)" and a signature line "Claude (lite)" in the body; the sender field stays `claude`, authorship self_authored. Copy the shape of any recent message from `claude` in that folder (schemaVersion, id as a new uuid4, conversationId, createdAtUTC, sender, recipient, writtenBy, authorship, subject, replyTo, status "posted", correlation, attachments with path, description, sha256 and bytes, body).

## 3. Outputs (write only these, all into W)

1. `TCM_SET_BINDING_v001.tsv`: one row per (shot, candidate still). Columns, in this order: shotId, family, positionId, lightState, variant, filename, zip, sha256, bytes, priority, isTake1, isDefaultPlaceholder, screeningTag, screeningNote, bindingSource, notes.
   - shotId: from the maps' Serves lists and the delta's setPositions; include sub-shots and inserts.
   - variant: a, b, c, or the P06 letter, or blank. Identity-sheet stills and extras are NOT rows here; list them in the md.
   - priority: proof, needed or exploratory, from the maps. An exploratory position gets rows only if the delta claims it for a shot; otherwise list it in the md as unclaimed.
   - isTake1: the first still delivered for that position and light state (the lowest L-number before any ADDD pack).
   - isDefaultPlaceholder: true for exactly one row per (shotId, positionId, lightState): the take-1 still if V_1 tagged it OK, else the lowest-numbered variant tagged OK, else the take-1 still with its tag. This is a placeholder under Ziggy's placeholder rule, not a selection.
   - screeningTag and screeningNote: V_1's, copied verbatim, never paraphrased or judged.
   - bindingSource: "maps serves", "delta setPositions", "both", or "ruling" with the section number.
2. `TCM_SET_BINDING_v001.md`: the report. Sections: counts (zips read, stills found, stills bound, stills unbound and why); a per-family table (positions in the maps, positions delivered, positions missing, variants per position); shots with zero candidates (list each with the position the maps expect); positions delivered that no shot claims (exploratory or orphan); every disagreement between the maps' Serves lists and the delta's setPositions column (list both sides, decide nothing); dropped positions per the rulings and any still delivered for them anyway; the identity sheet and the extras listed separately; the sha256 and bytes of every output file. Plain prose, no judgement of image quality.
3. `TCM_SET_BINDING_11_2_ROWS_PROPOSED_v001.json`: for every shotId, an array of proposed 11.2 design_reference rows in the Hon convention, one per candidate still, each with status "preliminary placeholder" and the binding fields above. It is a proposal for Nova, the card author, to apply; say so in a top-level "proposal" field.
4. Nothing else. No edits to v001, the addenda, the delta, the decisions record, START_HERE, Nova's JSON or any zip. If you must extract, extract to a new empty folder on D: (for example `D:\Documents\_scratch\tcm_binding_20261104\`), never on C: (C: is nearly full), and run any reader with `python -I`.

## 4. Rules you must keep (the record's)

- Prose rules in every .md you write: no em dashes, no en dashes, no double hyphens outside table rules, no horizontal rules made of hyphens, no placeholders left; single ASCII hyphens are fine.
- Names: never write the author's real name anywhere; the author is "Baldadoon" or "the author". No car make or model names: the car is "a dark unmarked SUV" (and "a dark unmarked sedan" where take 1 predates Addendum B). No franchise, film or real-person names.
- Immutability: posted files are never edited; corrections ride in new dated files. Your three outputs are new files; if you revise one before the writer posts it, overwrite your own file and say so in the md.
- Authorship line at the top of the md: "Author: Claude (lite), the PH_Claude_Lite session, on Claude's brief of 2026-11-04 | status: PRELIMINARY proposal, nothing selected | specialist review: none | adopted contributions: none". Sign every file you write "Claude (lite)".
- Every count you state must come from a script you ran, not from reading. Keep the scripts in your scratchpad and name them in the md.
- Read JSON with utf-8-sig; TSV with the csv module and tab delimiter. D: enumeration is slow, so use targeted paths and -LiteralPath, never a whole-drive walk.
- Do not post in any Grok chat; the writer and Ziggy do that. The mailbox you may use, as above, for the hand-back only.

## 5. Checks before you hand back (deterministic, scripted)

- Every filename in the TSV exists in the named zip, and its sha256 matches the zip's SHA256 sidecar.
- Every shotId in the TSV exists in Nova's 165 or in the delta's 210 rows.
- Every positionId exists in v001 (or in the rulings, for HEXT-P05's second state), and its family matches the filename's family.
- Per-family still counts in the md equal the manifests' counts.
- The md passes the prose rules (search for the two dash characters and for a double hyphen outside table rules).
- The JSON loads, and every row's sha256 is also in the TSV.

## 7. Never bare: cover, options, family (Ziggy's direction, 2026-11-04)

Ziggy's point, in substance: a storyboard shot is linked to its set even when nothing is chosen yet, because a link is better than an empty card. The shot takes place at this house; this house has options; the card shows one and keeps a breadcrumb to all of them. So every shot gets three levels of link, and the proposal JSON carries all three per shot:

1. **Cover.** One still, the default placeholder of section 3 (take 1 tagged OK where it exists). It is the picture the card shows. It is a placeholder, never a selection.
2. **Options.** Every candidate still for the shot's positions, as the rows already described, with a count. The card says "n options" and the breadcrumb opens them. Where a family's contact sheets exist in the zips, list each contact sheet (zip and filename) under the shot's family so the site can show a whole page of options without rebuilding one.
3. **Family.** The family id (for example TCM-SET-HENDERSON-EXTERIOR), its ten-look sheet from the October 30 intake (the original L01 to L10, with the look the author chose where one exists: the house is TCM-SET-HENDERSON-EXTERIOR-L03), and every contact sheet of the family's set-round packs. This link exists even when the shot has no position still yet: a shot is never bare if its family has any image at all.

Add to the JSON, per shot: familyId (or a list where a shot spans families), cover (one row), optionCount, options (the rows), familySheets (the look sheet and the contact sheets, as zip plus filename), and authorPick where an author selection is already recorded (only the house today). Add to the md a short table: shots with a cover, shots with options but no OK cover, shots with the family link only, shots with nothing (expected to be none; list any). The display itself (cover, "n options", breadcrumb, a page of sheets) is a site matter: the writer proposes it to CFA SITE INDEX from your data; you only supply the data in this shape.

## 6. Hand back

When done, write the three files, print their sha256 and byte sizes at the end of the md, then post the hand-back yourself from the `claude` mailbox signed "Claude (lite)": one message to `cfa_site_index` (conversationId 74f55ce6-9885-4dcb-8538-71f97064d4de) and one to `nova` (reply in the conversation of the latest message from `claude` to `nova` in the folder), correlation TCM-SET-BINDING-20261104, all three files as attachments with path, sha256 and bytes, and a body that says what the binding is, that it is PRELIMINARY with nothing selected, and that every shot links at cover, options and family. Then tell Ziggy. Once posted, the three files are immutable; the writer reviews the md afterwards and rules on the disagreements and the zero-candidate shots in a dated addendum. Keep a short list of questions for the writer at the end of the md; do not guess at a ruling.

Claude, lead writer
