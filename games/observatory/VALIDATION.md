# Observatory prototype validation

Observed September 12, 2026. This record concerns the first authored chapter, not the full proposed game.

| Check | Result |
|---|---|
| Story state | 108 checks passed: both tools, sequencing, deferral and later repair, inspection without mutation, save invariants |
| World access | 36 checks passed: real player movement, connected walking space, all 11 interactions selectable in both states, resident relocation and visual reset |
| Scene save/menu integration | 56 checks passed: Windows save replacement, repeated load, player/story/sound restoration, reset confirmation/cancellation, missing and corrupt files |
| Main scene smoke | All 11 interactions construct their dialogs; player settles on the floor |
| Packed game smoke | Exported PCK loads without the source project; the same 11-interaction/floor smoke check passes |
| Rendering | Native OpenGL 3.3.0, NVIDIA driver 369.09, Quadro 2000; Godot Compatibility renderer |
| Engine | Official portable Godot 4.7.2, `4.7.2.stable.official.ed1daf0bf` |

The geometry test flood-fills a 0.5 m walking grid using the player capsule and swept collision checks. It then uses the main scene's interaction distance, facing, and occlusion rules. All open sampled cells were connected to the spawn region: 2,456 while hauling, 2,455 at the crossing. This is a useful accessibility check, not a substitute for how movement feels to a person.

**Short rendered samples at 1280 × 720**

Each sample measures 181 wall-clock process intervals after a warmup, with the frame cap at 60. UI is included. The camera is stationary. These results do not establish performance throughout a full human play-through.

| View | Mean interval | 95th percentile |
|---|---|---|
| Pump workshop | 16.667 ms | 18.402 ms |
| Tool dialogue | 16.676 ms | 16.992 ms |
| Courtyard after repair | 16.669 ms | 17.994 ms |

Local screenshots, JSON metrics, and logs are in `.local/` and are ignored in Git. The first courtyard capture used Godot's supplied frame delta; later captures above use wall-clock intervals and are the reported measurements. Screenshots were inspected for scene composition, the repaired pump, changed resident locations/water, and visible dialogue choices. Longer text now scrolls independently of the choices.

**Reproduce checks**

From the CFA root in PowerShell, use the console engine extracted into `.cache/godot-4.7.2/`. Keep test user data inside the workspace:

```powershell
$env:APPDATA = Join-Path (Get-Location) 'games/observatory/.local/osdata'
$cfaGodot = Join-Path (Get-Location) '.cache/godot-4.7.2/Godot_v4.7.2-stable_win64_console.exe'
& $cfaGodot --headless --path games/observatory --script res://tests/test_story.gd
& $cfaGodot --headless --path games/observatory --script res://tests/test_world_access.gd
& $cfaGodot --headless --path games/observatory --script res://tests/test_visit_save.gd
& $cfaGodot --headless --path games/observatory -- --smoke-test
& $cfaGodot --path games/observatory --rendering-method gl_compatibility --resolution 1280x720 -- --capture --pump
```

The save suite uses unique test files and never writes the real `visit.json`. Headless runs skip audio playback; audible mix and comfort still require human review. Rendered runs load and play the synthetic ambience. The sandbox reports an inability to read the Windows root certificate store; these offline checks still finish successfully. That warning does not indicate a Comfy connection failure.

**Remaining experience work:** human movement/pacing feedback; more physical tool animation and resident activity; art, voice and sound direction; a second narrative draft; mapping selected lobby settings into supported rules. The current build implements one calm configuration and simple station-based mechanisms. It does not implement movie-footage rewriting, voice cloning, lip sync, combat, multiplayer, or a large simulated population.
