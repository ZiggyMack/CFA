# First playable: Water Before the Crossing

**The first prototype now makes exploration lead to a practical act of care and a visible consequence.** It implements the courtyard, pump room, upper path, and archive visit. The intended 10–15 minute chapter remains a pacing target for human review, not a measured duration or a production-time estimate.

The [project map](README.md) distinguishes this design folder, the Comfy asset workshop, and the implemented games/observatory/ engine prototype. It uses simple authored shapes while asset experiments proceed independently. Follow the [launch instructions](../../../games/observatory/README.md) and [validation record](../../../games/observatory/VALIDATION.md) for current implementation and measured results; the full chapter criteria below guide experience review and refinement.

**Production direction, September 12, 2026.** Ziggy has delegated ordinary background props and their arrangement to the assistant within the agreed aesthetic and budget. Advance the walkable story without individual object approvals. Give the pump visible repairs through simple geometry, then refine set dressing once it serves a working experience. No additional Comfy run is required for this first playable pass.

Bring Ziggy a visit to react to: the first invitation to explore, the repair or deferral decision, and the return that reveals its consequence. Ask for feedback on curiosity, causal clarity, movement comfort, and whether the choice feels worth making. These experience reviews guide the next pass; prop polish can follow.

The [Story Workshop pass](../../../games/observatory/STORY_WORKSHOP.md) adds a
second complete writing draft and an in-game comparison selector. Ziggy can now
review both tellings in the same saved visit. The chapter still uses the one
calm configuration; new pressures and larger scenarios remain later work.

This September 12, 2026 proposal revises the earlier relay-first chapter in [the research brief](RESEARCH.md). The water repair becomes the main interaction because Ziggy's subsequent direction places care at the center. The preserved finding and its correction remain a short optional discovery. The full relay puzzle can become another chapter.

**What the lobby establishes.** The [existing concept](lobby_concept.html) lets a visitor select conditions, read changing authored previews, and export settings. Ziggy's browser screenshot shows the rendered interface and an Invasion preview. It does not establish movement, simulation, performance, or whether an expedition is enjoyable. Its SVG landscape is an illustration. Its exported JSON describes a scenario concept and will need a deliberate mapping into supported game rules.

**Development route for the confirmed target PC.** Ziggy chose to use the current PC for now. The local hardware query reported an HP Z210 CMT, 16 GB RAM, and an NVIDIA Quadro 2000 with approximately 1 GB graphics memory. The initial inventory found no engine project or editor installation in the checked locations. A local Godot engine and the Observatory project have since been prepared.

The prototype now uses **Godot's Compatibility renderer**, which rendered successfully through OpenGL 3.3 on the Quadro 2000 with driver 369.09. Automated checks cover story transitions, reachable interactions through actual physics, and save/menu integration. The [validation record](../../../games/observatory/VALIDATION.md) preserves the evidence and limits; human pacing and comfort review remain open.

The earlier Unreal recommendation assumed suitable hardware. Epic currently recommends 32 GB system RAM and at least 8 GB graphics memory, and lists additional GPU requirements for Lumen. An available newer development PC could justify revisiting Unreal for the intended detailed visual style. [Epic requirements](https://dev.epicgames.com/documentation/unreal-engine/hardware-and-software-specifications-for-unreal-engine)

A small Babylon.js scene remains an alternative if browser play becomes the priority. Its documented WebGL 1 and WebGL 2 support offers a route worth testing on older systems; browser acceleration has not been checked. Godot is the current implementation. Moving between engines would involve rebuilding engine-specific behavior. [Babylon.js specifications](https://www.babylonjs.com/specifications/)

**The visit.** A visitor hears buckets being filled beside a quiet fountain. Two residents explain that carrying water is keeping them from their agreed work at the crossing. The workshop and pump room are visible. A maintenance note suggests the supply can be restored; a discrepancy in the old record invites closer inspection.

At a bench, try two tools and equip one. The echo spool replays an operation of a spring-return service lever while the player walks to its bypass. The long-reach coupler operates the same lever through a visible inspection opening from the bypass position. Either lets the player keep water on the bypass while fitting a regulator. The bench remains accessible so the player can change tools. These fictional mechanism rules are implemented in the prototype; their explanation and presentation still need a visitor's review.

Restoring the supply visibly starts the fountain. Deferring the repair leaves the residents' temporary water-hauling arrangement in place. An upper footpath reaches the archive in either case. There, a brief record pairs a failed finding with the correction someone chose to preserve. On an explicit return transition, the residents either resume work at the crossing or continue hauling water. Their dialogue explains the connection. The visitor can end at the lakeside bench or return to finish the repair.

Reading and wandering do not silently advance a deadline. Begin with one fixed, calm configuration. Add a second pressure configuration only after the basic visit works. The Care Tally ceremony, other scenario presets, combat, and separate expansions remain later options.

**Build it in three passes.**

| Pass | Concrete deliverable | Evidence needed to continue |
|---|---|---|
| Enter the place | A simple 3D courtyard and pump room with movement, collision, inspection, pause, and reset | Confirm graphics compatibility and measure frame times on the intended PC; assess comfortable movement |
| Make care consequential | Two usable tools, a complete repair, a viable deferral route, and two different return states | A visitor can explain why the residents' availability changed and complete the chapter with either tool |
| Give the place character | One coherent environment style, water and spatial sound, readable resident activity, edited dialogue, saved progress, and a complete ending | The place invites attention and the chapter runs outside the editor without assistance |

Use inexpensive geometry and lighting for the first pass. The original target was 30 frames per second at 1280 × 720. Three short stationary samples of the implemented scene, including its interface, averaged about 16.67 ms per frame at a 60 fps cap; their 95th percentiles ranged from 16.992 to 18.402 ms. These 181-frame samples establish performance in the sampled views, not sustained performance throughout a full visit. Art detail and rendering settings should continue to follow measured results.

**Completion criteria.**

1. A new visitor can move, look, interact, pause, and recover from getting stuck without editor assistance.
2. The opening offers a visible destination and an understandable reason to investigate it.
3. Each equipment choice enables a distinct, working solution; neither blocks the chapter's ending.
4. Repair and deferral produce visibly different water, resident activity, and crossing states, with no hidden care score.
5. The chapter has a local ending, a working save/reset flow, and a packaged build. A visitor can describe one consequence and one remaining curiosity afterward.

The prototype now supplies level geometry, controls, mechanism behavior, simple resident presentation, local audio, persistence, and an ending. The next useful step is Ziggy's review of the visit. Detailed character animation, voice, controller support, and mapping lobby presets into supported game rules remain future work. A portable development build is separate from a finished public release; use the game's documentation for its current launch and build status.
