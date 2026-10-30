# Shot direction — the reusable structure for every storyboard shot (2026-10-14)

Author: Claude, lead writer, first saved 02:24 UTC by the clock, on Ziggy's direction relayed by CFA Nova in the session a few minutes before: each storyboard shot carries LIGHTING, CAMERA, CHARACTER DIRECTION and BACKGROUND ACTION, with their coordinated time beats and the resulting video-generation prompt; in his words, "background, rolling, lights, camera, action—we need it all." The writer runs point on the writing. Source lineage, technical settings, actual results and acceptance are carried separately and never merged into the creative sections; a good scene is never promoted into approved performance by the card itself.

## The card, section by section (every section present, "none" written where there is nothing)

0. **SHOT.** Id (SET-SHOT-TAKE), title, story place (episode, scene, card, panel), what the shot is for in one sentence.
1. **SOURCE LINEAGE.** The start frame by exact path, sha256 and bytes; variant and repair history; prior takes by file and hash; what in the frame is lock, what is inherited drift. Never edited after posting; new takes append.
2. **LIGHTING.** Emitters only: the key (what it is, where it is, its colour and softness), the fill (sky, haze, bounce), the rim, every practical (fire, lamp, console, lattice). How each behaves over the shot. No whole-frame washes; no light without a source. Sides stated as the character's and the viewer's, both, every time.
3. **CAMERA.** Height, distance, lens feel, move (locked, push, track, orbit) and when it starts and ends; the line (the axis between the character and what he faces) and which side of it the camera keeps; the frame's edges (what is in, what is off-screen and where).
4. **CHARACTER DIRECTION.** Who, what he does (one action, start to end), eyeline (one target, named as off-screen or in-frame, stated as character-left/right AND viewer-left/right, with up/down), face (brows, eyes, jaw, mouth; the mouth's rule), hands and body (which hand, how far, how fast; what does not move), breath, blinks. Ziggy's acting note verbatim when he gives one, marked as his. The read in one phrase (what the audience should understand), never an emotion label pasted into the prompt.
5. **BACKGROUND ACTION.** Everything that moves that is not him: creatures, vehicles, people, weather, dust, fire, debris, light changes; where each starts and ends; what must not happen (no second creature, no lunge, nothing reaching him).
6. **TIME BEATS.** One table, seconds as story design inside the route's native length, never accepted timing: for each beat, what LIGHTING, CAMERA, CHARACTER and BACKGROUND are doing at once, so that the four sections are coordinated and nothing is asked for that another section forbids.
7. **RESULTING PROMPT.** The copy-ready video-generation prompt, assembled from sections 2 to 6 in plain English: the scene, the character's action and face and eyeline, the background action, the light as sources, the camera, then the negatives. No franchise names, no coinages, no emotion labels, no words the generator over-plays ("dramatic", "epic", "signals", "gestures"); no sung or spoken words unless a card says to-lens and the song timing is accepted.
8. **TECHNICAL SETTINGS** (CFA Nova's; filled at run): route, model, mode, resolution, aspect, length, outputs, credits displayed, project and scene ids, the prompt as actually submitted if it differs from section 7.
9. **ACTUAL RESULTS** (CFA Nova's; filled on return): file, hash, bytes, duration, fps, resolution, whether audio is present and what it is, the frames sheet, the measured defects.
10. **ACCEPTANCE** (separate; Ziggy's gate is never written by the writer): Ziggy's verdict on the video; beneath it, clearly labelled, the writer's attributed preliminary grade (reviewer, date, L and S separate, a performance line: reads or not, which beat failed); nothing in sections 0 to 9 counts as acceptance.

## Rules the structure enforces

- The four creative sections are written together and reconciled in the beats table before the prompt is assembled; the prompt is derived from the card, never the other way round.
- One new variable per take against the prior take of the same shot; the card says which.
- Every side is written twice (character's, viewer's) in sections 2 to 6 so a correction like "up to your right" is never silently inverted; in section 7, the prompt, the approach to try next is directions in frame terms only with a landmark in the frame ("toward the top-left corner, past his raised palm"), a hand's motion as a frame direction with a limit ("a few inches, staying beside his head, never in front of his face"), and the mouth as a state after any source exception is stated exactly (a frame's parted lips close in the first half-second, then closed and still). Hypothesis from one result (LAG-SIGNAL-002, 2026-10-14): the generator may not resolve a character's left and right; untested until a take runs on it.
- The original of any take is preserved; a revision is a new take id beside it.
- The card changes only its own sections 8 to 10 after a run; a creative change is a new take, with the prior take's card kept.

— Claude
