# The Observatory — Water Before the Crossing

**Project status, October 2, 2026:** active development has shifted to [lifelike video creation in ComfyUI](../../docs/notes/explorable_world/comfy/index.html#video-first). This playable prototype is preserved for a later return. The visual and story priorities below describe its September checkpoint.

A first playable 3D chapter: enter a lakeside courtyard, meet the people carrying water, borrow a tool, repair the supply or leave it for later, and return to see what changes. The upper path and archive stay open. The repair can still be finished after a deferred visit.

**Play on this PC:** double-click **Play.cmd** in this folder using File Explorer. It opens the game directly. The prepared portable engine lives in the repository's ignored `.cache/godot-4.7.2/` folder. No Comfy connection is needed while playing.

**Storage:** this is the small local play/test project on D:. Keep model weights and bulk generation in the cloud, and bring in only selected game assets. Engine downloads, generated builds, and runtime caches are ignored in Git. See the [project storage policy](../../docs/notes/explorable_world/STORAGE.md); cloud-streamed gameplay is not configured. The [cloud-PC plan](../../docs/notes/explorable_world/CLOUD_PLAY.md) prepares that next step so local hardware need not set the final visual ceiling.

| Control | Action |
|---|---|
| WASD | Walk |
| Mouse or arrow keys | Look |
| E | Speak or inspect the object you are looking at |
| Shift | Walk faster |
| Tab | Journal |
| Esc | Pause, resume, or close a conversation |
| M | Toggle sound |
| F3 | Show frame timing |

Approach a station until the E prompt appears. At the workbench, choose either tool. Conversations and tool choices use buttons with mouse or keyboard focus. Longer text scrolls while the choices remain visible. The pause menu includes a return to the entrance if movement becomes awkward. A new visit asks before replacing an existing save.

Progress saves after story changes, periodically while walking, and on exit. Source-project saves are in `.local/visit.json`; the portable build has its own `user_data/visit.json`. These are local to the PC. There is no hidden deadline or care score.

**What to review first:** the world's appearance, atmosphere, model shapes and materials. Ziggy has put further story iteration on hold while visual quality improves. Open the [visual comparison](../../docs/notes/explorable_world/visual_review.html) and [visual pass record](VISUAL_PASS.md).

**Modern GPU / cloud PC:** `Play_High_Quality.cmd` requests Godot Forward+ at 1080p with additional lighting effects. Run it on a suitable modern GPU; it has not been rendered or measured on a cloud PC yet. It does not establish a remote connection. Keep using `Play.cmd` for the current local machine.

**New: compare two story drafts in the same visit.** Press **Esc → Story workshop**
and switch between **The practical repair** and **What we leave for others**.
The second draft adds personal observations and quieter questions; the repair
and consequences remain the same. Switching preserves your position and progress,
and your selected draft saves with the visit. If an older game is already open,
save and leave, then reopen it to load the rebuilt pack. Follow the
[Story Workshop guide and current validation](STORY_WORKSHOP.md).

**The reusable scene and its editable story**

| File | What can change here |
|---|---|
| [data/chapter.json](data/chapter.json) and [data/drafts/curiosity.json](data/drafts/curiosity.json) | Two dialogue/archive drafts; preserve entry IDs and switch away/back in the source game to reload edits |
| [scripts/story_state.gd](scripts/story_state.gd) | Tool rules, conditions, branches, journal, and save-state validation |
| [scripts/world_builder.gd](scripts/world_builder.gd) | Courtyard, buildings, props, residents, and visible world changes |
| [scripts/player.gd](scripts/player.gd) | Movement, collision body, and looking |
| [scripts/main.gd](scripts/main.gd) | Interaction selection, menus, persistence, sound, and scene orchestration |

Changing dialogue does not require rebuilding geometry. Changing the meaning of an action or introducing a new consequence requires corresponding story-rule changes and tests. Current performances are written dialogue with simple resident figures; voice acting, lip sync, and cinematic performance are later work. The game has no dependency on temporary Comfy URLs or ignored generated-image files. Its pump is authored geometry informed by the first concept, including a repair plate and newer coupling.

**Portable development build**

`builds/observatory/Play.cmd` launches the prepared game pack with its own engine binary. Keep that folder together when moving it. It runs without the source tree, editor UI, account, or internet connection. It currently packages the standard Godot editor binary as its runtime; a smaller release-template export is a later packaging task. Generated builds are ignored in Git.

To rebuild from the repository root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File games/observatory/build.ps1
```

The execution-policy setting applies only to that build process. It does not change the machine's policy. Add `-CloudBundle` to create a ZIP containing only the seven portable application/license files, excluding local saves and logs. The script exports a PCK and copies the already downloaded engine when needed, reusing a byte-identical runtime. It excludes build/user-data directories from the pack and does not fetch dependencies or publish anything.

For a new checkout, obtain the standard Windows x86_64 portable **Godot 4.7.2** from the [official archive](https://godotengine.org/download/archive/4.7.2-stable/) and extract it into `.cache/godot-4.7.2/` at the CFA repository root, or pass its console executable to `build.ps1 -EnginePath`. This prototype uses the [Compatibility renderer](https://docs.godotengine.org/en/stable/about/system_requirements.html). The current engine is `4.7.2.stable.official.ed1daf0bf`; its MIT license is included in [GODOT_LICENSE.txt](GODOT_LICENSE.txt).

**Validation and limits**

See [VALIDATION.md](VALIDATION.md) for the original evidence and commands, and
[STORY_WORKSHOP.md](STORY_WORKSHOP.md) for this pass's 388 checks, package checks
and visual review. The first visual pass adds authored detail and selected photo materials; it remains a stylized prototype rather than the final visual target. Puzzle steps currently use station interactions, and residents change placement at the return transition; detailed tool animation, facial performance, roaming NPC schedules, controller support, and the full scenario lobby are not implemented. A human assessment of pacing and movement comfort is still needed.
