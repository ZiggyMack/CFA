# Claude's bounded review of the cinematography R&D proposal and A/B pilot package — for discussion with Ziggy

Reviewer: Claude, lead writer. Date: 2026-10-12. Read in full: `collaborators/cinematography_rd_20261012/PROPOSAL.txt` (SHA-256 4fd9d1bd…, 8,762 bytes) and `PILOT_PACKAGE.txt` (f768ce4c…, 16,857 bytes), both hashes verified on D:, plus Nova's `NOVA_REVIEW_NOTES.json`. Status: review only. Nothing here assigns a candidate, ranks one, launches a comparison, renders, uploads or spends. Proposed status is preserved.

## 1. What the package gets right

- **Compare writing before rendering.** One frozen package, verbatim first responses with author, model, date and the exact inputs each candidate actually received; then one recommendation from Nova and me for Ziggy. This is the right order and the only fair one, since the candidates do not share access.
- **Two passes kept apart.** Pass A preserves A's camera movement and action and changes only the motivated practical lighting; Pass B is a separately declared camera treatment that may need regeneration and cannot be smuggled into Pass A. The proposed C prompt v2 is the single adapter for Pass A. I agree with Nova's caveat: the word "fixed-camera" in the proposal must be read as "preserve the source's existing camera movement," which the pilot package and the actual prompt already say.
- **Lineage and limits are honest.** A is a prepared excerpt of GEM-5A115C59, not a generation; B's job id, seed and cost are unknown; the 720p and nominal-rate caveats are stated; the three Civitai examples are archived stills, not verified motion; a path is not proof of viewing.
- **The method's rules are carried.** New scenes begin Preliminary; an accepted reference does not accept a new scene; dimensions stay separate; Ziggy judges motion, acting and the edit.

## 2. What the package says is missing, and what the writer lane can supply now (proposals)

The package itself states that the dramatic beat, the subject emphasis, the arrival and entry choreography and the storyboard scene-card id for the car scene have not been established, and asks candidates to name the minimum missing information. Those are writer questions. My proposals, for Ziggy to accept or change, so every candidate designs camera against the same beat:

- **Beat.** The car arrival is the prologue's junction between the drop and the cantina walk: Dolo arrives at the cantina landing at night to do business, the man who charges for everything stepping out to collect. In the cards it sits between P-6 (the drop) and P-7 (the cantina walk) as a proposed new shot, P-6b "the arrival." It is not inside the song.
- **Subject emphasis.** The man first, the door second. The car is the delivery, not the subject. Blue night with warm practicals at the door is the mood the cards already give that world (the neon city, wet landings, the cab's lamps).
- **Choreography.** The car settles, the door opens, he steps out, turns toward the door, walks out of frame toward it. That is what A already contains, so Pass A preserves it as is.
- **Sides, so Pass B is comparable across candidates.** The prologue's geography: the landing at screen-right, the vehicle settled at screen-left having arrived from screen-left, departures into depth, the cantina door at the far wall. A camera proposal that contradicts these needs to say why.
- **Identity caveat for Pass B.** A's performer is not lf_full and the silver jacket is not the locked brown-leather-over-off-white outfit; the pilot is a lighting diagnostic on a non-canon scene, which is fine for Pass A. For Pass B, a camera treatment designed only on A may not transfer; the stronger baseline for a regenerated camera test is a graded Grok frame of the same beat from the archives (the street landing N32, the cab landing N29, or the neon city E35, all preliminary) with the locked outfit, so the camera lesson lands on the shot it will actually serve. That choice is Ziggy's, and it changes no part of Pass A.

## 3. Additions I would make to the one-page expert return

- Ask each candidate to **name the beat they are serving and its screen sides** in one line, so camera designs can be compared on the same intention rather than on taste.
- Ask for **light stated as sources**: which emitters exist in A, what each lights, and what the proposed warm contribution does to falloff, occlusion, shadows and reflections; a response that proposes a look without naming a source is the yellow-wash failure in words.
- Ask each candidate to **declare their access level** at the top (text only, stills, video playback) as Nova notes; responses are then grouped by access before any ranking.
- Keep the **three examples bounded** as written; the cab-exit woman is the informant's inspiration, which ties it to the prologue's cab and makes it the most relevant of the three to this beat.

## 4. On the candidate pool

I hold no evidence to rank Gemini Master, Kimi, Qwen, DeepSeek or Nova on cinematography; the proposal is right that a stated preference and a coordination role are not earned grades, and that an operator role does not make Nova the lead by default. Two things will matter in the comparison more than fluency: whether a response separates observed cues in A from assumptions, and how much operator and repair burden its prompt would create for CFA. A small team is only worth it if the division of work is named (for example one candidate on lighting physics, one on camera and coverage) and it does not add coordination turns.

## 5. What I will do, and not do

I will read every candidate's first response against this review and the package and write, with Nova, one short recommendation for Ziggy. I will not assign, rank ahead of the responses, render, upload, or spend. Nothing in this review changes the Flow 002 dispositions (A and B: Scene, Preliminary, Needs fixes, no stars) or the proposed C prompt v2.

— Claude
