# The music scoring department: how a brief is picked up by whoever is drafting

Author: Claude, lead writer and cue-card lead, 2026-10-28, recorded at about 05:56 UTC by the clock, at Ziggy's direction of the same hour (in substance: the scoring task is collaborator agnostic; this is the musical scoring department; Deep_SEEK happens to be helping for now, and if someone else were to do it they need to be able to understand it too, since Deep_SEEK may not be available). Status: a department page, not a role grant; nothing here assigns anyone new work beyond the drafter Ziggy named, generates audio, submits anything to a music service, spends, or changes any human rating. Ziggy is the final music author and the gate: nothing is accepted until he says so. Mode, cost and intake are CFA Nova's. Every return is preliminary. Reviewed once by three read-only reviewers (evidence, fit for a stranger, the standing lines) before posting; their findings are applied.

## 1. What the department is

A lane for the score songs: the pieces that run under the dialogue-free scenes of the Lisan Al Gaib series (the series plan's score-songs table) and, later, under any other production that wants one. Ziggy asked for it on 2026-10-13 through Nova PA (mailbox f8291465, correlation MUSIC-DEPARTMENT-CUE-CARDS-20261013): ready-made musical-style and lyric or instrumental options tied to panels and scenes, grouped when connected. The department's unit of work is the cue card: purpose, event arc, emitters, duration as story design, two or three contrasting directions each with a copy-ready prompt, quality checks, and what is open for Ziggy. Its unit of decision is Ziggy's one word per cue. Its unit of output, once he has chosen, is one generation per cue by whoever generates, listened to and graded like every other return. Nothing has been generated to date.

## 2. The seats, not the people

- **Author and selector: Ziggy.** Chooses the direction per cue, settles every open question, accepts or rejects what comes back. Nothing is accepted until he says so.
- **Cue-card lead: Claude (mailbox `claude`).** Writes or signs off the cue cards, writes the briefs, reviews the returns, keeps the decision record in the writer's folder.
- **Drafter: whoever Ziggy assigns.** Text work only: reads a brief and its sources from disk, returns a card. Deep_SEEK (mailbox `deepseek`) checked the sample's two sandworm directions, wrote their fixes and a third direction, and drafted the vault card in full on 2026-10-13; he is assigned brief 001 by Ziggy on 2026-10-28. Any collaborator with read access to the repository and the ability to write a few small files (one markdown return and two mailbox JSON files) can hold this seat; the brief never assumes a particular model, tool, browser or image input. If you can write the return but not the mailbox files, say so at the top of the return and stop; the cue-card lead posts the message, attributed to you.
- **Intake and execution: CFA Nova (mailbox `nova`).** Mode, cost and intake are hers. A generated cue enters the project through her intake as audio only; timing stays null until the audio lands (DECISIONS item 32).
- **Generator: unassigned.** Generation happens only after Ziggy chooses and says go, by whoever he names, with the prompt as the card gives it. The card is complete without audio.
- **Site: CFA SITE INDEX (mailbox `cfa_site_index`), not a seat.** The "CFA Site Nova" of Ziggy's word of 2026-10-28, the standing site maintenance owner, distinct from CFA Nova (mailbox `nova`). Ziggy asked on 2026-10-28 that the site be told brief 001 is in process, so that his dashboard's counter and metadata can be updated. What the site does with that is under its own standing mandate and CFA Nova's registry stewardship; this page assigns it nothing, and a display is not an acceptance.

## 3. How a drafter picks up a brief

1. Read the brief in this folder in full, then every source it lists, from disk, by path. Verify the listed hashes; a mismatch is a finding, not a stop.
2. Do the work the brief describes and nothing beyond it. Where the brief leaves a choice to Ziggy, prepare the default it names and keep any variant as a separate, unmerged line.
3. Return one markdown file under `returns/<your-registry-id>/`, named as the brief says, with the standard header (author, mailbox id, UTC time, the exact sources read with their hashes), a completion check, and a list of what is open for Ziggy. Your registry id is your `id` in `collaborators/mailbox/registry.json`, the same word the brief calls your mailbox id (for Deep_SEEK, `deepseek`). If you are not in the registry, use the id Ziggy's assignment gives you; failing that, a short lowercase name, and say in the header that you are unregistered.
4. Hash the return (sha256, bytes) and post one mailbox message to `claude` with the path, the hash and the bytes: `conversationId` set to the one the assignment message carries and `replyTo` set to that message's id, then a receipt for the assignment message. If no assignment message addressed to you exists in the mailbox, start a fresh `conversationId`, leave `replyTo` null, put the brief's file name in the subject, say in the body that you picked the brief up from disk, and post no receipt, since there is nothing to receipt. Say plainly anything blocked or unknown; a blocked result is a useful result.
5. Stop at the return. Do not generate, submit, upload, install, purchase, or edit any existing file.

## 4. The rules every cue carries

- **The scene's own sounds stay audible.** The iron's knock, a key's click, a relay's static: the music makes room for them and never replaces them, and a prompt never asks a generator to produce them.
- **Duration is story design, never timing.** The series plan's seconds are design; the cut's rhythm may follow the piece's sections, never its words; timing is null until the audio lands through CFA Nova's intake.
- **Score-song rules (the series plan).** A score song carries no lyric cue in the storyboard, so no panel is re-mapped to it; if a score song has words, the scene is cut so that no mouth on screen is singing them. The writer's default for the Story 01 cues is no voice at all.
- **Endings are the card's.** A held reveal, a release, a single note: the prompt says which, and "fade" is never a default.
- **One choice per cue; one variable per retry.** A choice names the direction whose prompt goes forward for one generation. A retry changes one thing and says which.
- **Nothing borrowed.** No borrowed melody, no borrowed lyric, no named artist to imitate, no book text, no song lyrics from any existing song. Original fragments, if any, are labelled as new and are Ziggy's to keep or discard.
- **Tool-agnostic words.** A brief, a prompt and a return name no music service, provider or tool. Where a source labels its prompt with a service's name, that label is the source's and is not repeated.
- **The house lines.** No franchise names ("the iron" in the writer's voice; "thumper" only as the archive's own word, never in a prompt); no coinage from the shamanic tradition's books; no name, place or plot from the game well behind the city; no real person named or implied anywhere; characters are characters.
- **Nothing accepted by a card.** A card, a brief, a return and a display are all proposals until Ziggy says otherwise.

## 5. Briefs in this folder

| Brief | Date | Target | Drafter assigned | State |
| --- | --- | --- | --- | --- |
| `MSD-001_STORY01_THREE_CUES_FINAL_PROMPTS_20261028.md` | 2026-10-28 | Story 01's three cues under Ziggy's chosen directions: final copy-ready prompts, the vault-to-tower rhyme, the tower on saxophone | Deep_SEEK, by Ziggy's word of 2026-10-28 | brief in this folder 2026-10-28; assignment message `46ebf08b-c335-454b-9ab1-9766657771ba` to `deepseek` in the mailbox the same hour, conversation `34d2e4f9-1ff3-4bbd-80d8-797ea8b59dc4`; no return yet |

Earlier department work, before this folder existed: Nova PA's sample card (`collaborators/team_integration_20261013/MUSIC_DEPARTMENT_SAMPLE_ebf32b6f-b7c4-4b4a-b1c6-4296084fe59b.md`, the sandworm card with directions A and B); Deep_SEEK's two returns of 2026-10-13 (`collaborators/work_briefs_20261010/results/deepseek/lisan_20261013/cue_MD-LAG-SW-001_20261013T201058Z.md`, his check of the sample with fixes and a third direction, and `cue_MD-LAG-VAULT-002_20261013T201058Z.md`, his full vault draft); the writer's tower card, direction sheet and cue map in `lisan_al_gaib/story/writer_pass_20261012/`. Those files stay where they are; this folder indexes them.

Claude, lead writer and cue-card lead
