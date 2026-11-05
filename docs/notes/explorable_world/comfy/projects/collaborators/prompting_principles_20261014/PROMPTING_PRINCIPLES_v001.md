# Prompting principles — the house style for scene generation across Flow, Gemini and Comfy (v001, 2026-10-14)

Author: Claude, lead writer and Pan_Handlers steward, recorded at about 04:57 UTC by the clock; nine evidence lines corrected at about 05:10 UTC after a read-only fact check against the prototype records (the first version overstated what the records show; every evidence line below now says what was measured and labels the rest hypothesis). Why now: Ziggy, in the session, in substance: we are going to outline for ourselves the global techniques one takes for prompting, whether through Gemini, Flow or Comfy; we have some starter things but we are learning we have to put down the specific styles we like; the one that started it was making sure the characters act as if they are not being filmed and just go about their normal day; this is the prompting side rather than the story side, global rather than local to a storyboard; DeepSeek's music recipes sit at the same higher level; Pan_Handlers is Claude's, so the global things come from this side; help out with ideas. His direction for future shots, verbatim as Nova PA relayed it (da73f3bc): **"life is happening and these characters don't know they're being filmed."** Nova PA's proposed implementation (interpretation, not his words): characters focus on their task, surroundings and each other; natural reactions and incidental gestures; believable physical motion; motivated lighting and camera movement; no gratuitous hero posing or looking into the lens unless an intentional performance shot calls for it; high image quality kept, not shaky cameras or grain; "starting gold" is confidence, not acceptance.

Status: a proposal for Ziggy and the team; principles with their evidence; nothing here changes a running job, a lock, a scope or a budget; prompt wording alone is not promised to overcome a model's limits. Evidence base: the four Lisan prototype runs of October 13 and 14 (SW-2 the rise on Flow; the Signal takes one and two on Flow; SW-2 on Gemini, preview only), the production method's lighting-as-sources finding, the prototype brief standard, the shot-direction card, DeepSeek's two cue drafts. The canonical copy lives here in CFA; whether a Pan_Handlers teaching copy follows the pathfinder handoff route after Ziggy's read and one rung of the ladder is open question 5.

## 1. The style in one sentence, and what it means for a prompt

Life is happening and these characters don't know they're being filmed. For a prompt that means five things at once: every character in the frame has a task; nobody looks at the lens unless the card names a to-lens shot; the world moves on its own and reacts to what happens; the light comes from things in the world and the camera gets no special light; and the camera is a witness that holds still or makes one motivated move. The audience watches busy people. A poster is a presentation; a scene is a moment someone did not stage for us.

## 2. The ten principles, each with a prompt pattern

**P1. Task before face.** Give the character a thing to do that the scene needs, with hands and eyes on it. Not "he stands, powerful"; "he works the seized valve with both hands, leaning his weight into it." A face with nothing to do performs for the camera. *Evidence:* the Signal take one held still and read as static (Ziggy's feedback as relayed by CFA Nova root: the character was standing there without proper performance motion); whether a task in the hand would read differently is what rung 1 of the ladder would test.

**P2. The eyeline is on something in the world, named in frame terms with a landmark.** "His eyes are on the valve," "he looks up toward the top-left corner of the frame, past his raised palm." Never "looks at the camera" except in a to-lens shot; never "his left" or "his right" in the prompt (the character's sides live in the card; the prompt gives screen directions and landmarks). *Evidence:* take two of the Signal went to the wrong side on "his own right"; hypothesis from one result, the frame-term wording untested.

**P3. Two incidental tells, no more.** The things a person does without meaning to are what say "not filmed": wind in the curls, a squint against dust, one breath, a shift of weight, a glance down at the hands. Name one or two; three or more and the generator over-animates. *Evidence:* one result so far: the Signal take two asked for several simultaneous tells (brows, eyes, jaw, lips, breath, chin, head turn, two pushes) and the hand came back larger and busier than asked; the two-tell limit is a hypothesis from that one take.

**P4. The world keeps moving, written as its own paragraph.** Background action is stated separately from the character: extras do their own work and never watch him; the environment reacts to events (dust after the rise, sand off the worm's lip, a fire guttering as the rig goes under); nothing in the frame waits for him. *Evidence:* the shot card's background section; the worm action was present in all three Flow takes, but only take two wrote the background as its own paragraph (SW-2 and take one were single-paragraph prompts), so the paragraph form is a preference from one take, not a tested cause.

**P5. Light as sources, and the camera gets none.** Name the key, the fill, the rim and every practical, where each is and how it behaves; time of day as a source ("a high hazy sun," "the pump's dim lamps"); no washes, no light that has no source, no "cinematic lighting." *Evidence:* the production method's Flow 002 finding (a warm wash with no source reads as a grade, not a world); the haze key held across the Lisan takes when named as a source.

**P6. The camera is a witness.** State what it does, not how it should feel: height, distance, lens feel, locked or one motivated move and when. No "cinematic," "epic," "dramatic," "dynamic." No shake, no grain, no lens flare unless a source makes it; image quality stays high (Nova PA's interpretation of Ziggy's direction in da73f3bc, not his words). The first test of any shot is a locked camera; the move is the retry's variable.

**P7. Preserve by naming, in the prompt itself.** The identity carriers go into the generation text, not only the card: face geometry, hair, eye colour, every mark by name and place, jewelry by place, props by place, wardrobe; then "do not repair, add or change tattoos, piercings or clothing." *Evidence:* the SW-2 and Signal prompts that carried the carriers held them across eight seconds; the lineage section alone does not reach the generator.

**P8. States, not actions, for what must not move.** "Mouth closed, lips still," "the hand open and still, five fingers." Describing a transition ("the lips press closed") may invite the generator to keep performing it (a hypothesis from one result, LAG-SIGNAL-002, untested); state the source's exception once ("the first frame's parted lips close in the first half-second") and then the state. *Evidence:* take two's mouth reopened after a closing sentence; the SW-2 Flow take opened the mouth and showed teeth near the first second with "mouth closed" alone, so this is a tendency to manage, not a fix.

**P9. No emotion labels, no over-played words.** Not "concerned," "afraid," "heroic"; the brows, the jaw, the eyes, the breath, the hands. Not "signals," "gestures," "shouts," "dramatic," "epic"; the thing itself, small. A generator reads an emotion label as a cue to perform it at full size. *Evidence:* the Signal take two's face read as concern from brows and jaw alone; the hand, asked to "push forward," came at the camera.

**P10. One variable per take; the negatives as a closed list; silence declared and still recorded.** Change one thing between takes and say which. End every prompt with a do-not list specific to this shot (the second worm, the second hand, the look at the camera, the mouth opening, the camera moving). Say "silent, no speech, music or sound effects" and still expect an audio track and record whether it is there. *Evidence:* all three silent prompts on Flow returned an audio track: near silent once (Signal take one, peak -78.3 dBFS), substantial twice (SW-2, peak -7.7 dBFS; Signal take two, peak 0.0 dBFS).

## 3. The prompt skeleton (route-agnostic; 150 to 250 words; the order is the weight)

1. The start frame or the scene, in one sentence of what is where (screen terms).
2. Preserve: the carriers by name and place; do not change.
3. The character: the task; the eyeline (frame terms, landmark); the face as physical facts; the hands; the two incidental tells; states for what holds.
4. The background: what moves on its own; what reacts; what nothing does.
5. The light: sources, where, how they behave.
6. The camera: height, distance, lens feel, locked or one move.
7. Do not: the closed list for this shot.
8. The route prefix (CFA Nova's): length, aspect, resolution, silence, outputs.

## 4. Per route, what we have observed (labeled by evidence; not a ranking)

- **Flow, Omni 1.1 Flash, frames mode from a start frame:** holds identity and wardrobe well across 8 s when the carriers are named; adds an audio track despite a silence instruction; drifted the mouth open near the first second on SW-2; resolved a character-side direction the wrong way once and animated a hand "forward" as toward the camera once (both hypotheses from the same single result); kept the worm action in all three takes, with the separate background paragraph tried only in take two. Three takes of evidence.
- **Gemini (the identical SW-2 brief):** an 8-second 1280 by 720 preview exists beside error text; export timed out twice; no local file verified. Nothing to say about its prompting yet.
- **Comfy:** not yet run for Lisan; the Comfy report card is Nova's. The principles apply at the prompt node: P5 and P4 into the positive prompt, P10's list into the negative prompt, and P7's preservation through reference-image conditioning rather than words where the graph has it. Defer to the report card for the route's own grammar.
- **Image stills (Grok, the archives):** the same principles produced the poster frames we have; the coverage call already moves them toward P1 and P2 (a shot, not a portrait; eyeline off the lens).

## 5. The music parallel (DeepSeek's cue drafts, the same grammar)

The cue cards and the picture prompts share a shape: an event list as the arc (the thumper planted, the tracks converging, the rise, the held breath, the burst, the man on the dune), the scene's own sounds kept (the knock stays audible), sources carrying the mood ("a dry frame drum marks each step"; the drafts keep words like "dread" and "never triumphant" beside the sources), one copy-ready prompt per direction, a closed do-not list (no vocals, no pop structure, no imitation of a named artist, no borrowed melody), duration as design and not as timing. A prompt for sound and a prompt for picture are the same discipline: events, sources, negatives, one variable.

## 6. A test ladder for the style (proposal, not a request; each rung one variable; each from a graded still)

1. **A task shot:** Lisan at the valve (C18), both hands on the iron, eyes on the valve, one breath, the lamp as key. Tests P1 and P2 with the camera locked.
2. **A two-person shot:** Sassy setting Jet's cup at the edge of the firelight while Lisan sleeps; she never looks at him or the lens (C25). Tests P4 with a second figure who has her own task.
3. **A walking shot:** Lisan through the bazaar, the market busy and never watching him (C17). Tests P4 and P6 with one motivated move, the camera tracking at his pace.
4. **The signal, take three:** the frame-term eyeline (P2) as the one variable, if Ziggy wants it.

## 7. Open for Ziggy

1. Which of the ten are rules and which are preferences a card may break with a reason.
2. Whether to-lens is ever allowed outside the song's one chest-up panel and the mirror's whisper shots.
3. The house's position on slow motion (the mirror burst wants it; the style distrusts it).
4. Style words: none at all, or a short approved list.
5. Whether this becomes Pan_Handlers teaching after one rung of the ladder runs.

— Claude
