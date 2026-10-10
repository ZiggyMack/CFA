# First visual pass — September 12, 2026

Ziggy wants the world to look convincing before more story iteration. This
pass improves the existing playable chapter and prepares a modern-GPU preset;
the old workstation is no longer the intended ceiling for the project.

Open the [before/after comparison](../../docs/notes/explorable_world/visual_review.html).
All images are direct Godot captures. No AI image enhancement or cloud render
was used to make them look better than the running game.

## What changed

- Nine selected CC0 photo maps give stone and timber physical texture, normal
  detail and roughness. Metric UVs and mipmaps keep their scale consistent and
  reduce shimmer. Original files total 6,861,358 bytes; no model weights were
  downloaded. [Provenance and license](THIRD_PARTY_ASSETS.md).
- Curved masonry, dressed columns, cornices, window recesses, archive pergola,
  individual books and a courtyard inlay replace the bare architectural look.
- A shaped pump gains pipe bends, valve spokes, unions, hinges, bolts and a
  pressure gauge whose needle follows the existing water state.
- Residents gain shaped faces, hair, hands, clothing details and separate
  limbs, while retaining their original interaction and collision positions.
- Branching trees, individual leaves, garden plants and rocks, distant terrain,
  an observatory landmark and animated water improve the lakeside view.
- Directional shadows ground the structures and residents. Floating labels are
  smaller and limited to nearby distances. The terrain palette was corrected
  after actual captures revealed clipped highlights; distant scenery uses
  authored atmospheric shading.

The existing repair mechanics, two writing drafts, save data and walkable layout
continue to serve the same chapter. No further dialogue was written in this pass.

## Validation

The current geometry passed **36/36 world-access checks**, covering every
interaction in both resident configurations. Source startup smoke checks passed
all 11 interactions, floor availability and both story drafts. The rebuilt portable pack passed the same startup smoke check and confirmed
that private save/cache/test directories are absent. Its actual OpenGL courtyard
render was also inspected after packaging (16.66 ms mean / 17.65 ms p95). The earlier 388 functional checks belong
to the previous story pass; they were not all rerun for this visual change.

Five final stationary captures were reviewed at 1280x720 on the Quadro 2000,
Godot 4.7.2 Compatibility, driver 369.09, with the HUD and 60 fps cap. Each
sample contains 181 process-frame intervals after a 90-frame warmup:

| View | Mean ms | 95th percentile ms |
| --- | ---: | ---: |
| Courtyard | 16.67 | 18.08 |
| Pump | 16.67 | 17.78 |
| Lake | 16.67 | 17.86 |
| Archive | 16.67 | 17.92 |
| Repaired courtyard | 16.68 | 18.42 |

The baseline courtyard sample was 16.66 ms mean / 18.66 ms p95. These stationary,
capped samples do not measure the full walking experience, GPU headroom or
remote-stream latency. Other desktop applications were not closed for testing.
Raw capture metadata and image hashes are preserved in
[the visual record](../../docs/notes/explorable_world/visual_pass/record.json).

Godot emits the same Windows root-certificate-store warning seen in earlier
local checks; the game does not require network access to play.

### Local launch visibility

An agent-launched process can render successfully on `CodexSandboxDesktop`
while remaining absent from Ziggy's desktop and Alt+Tab. Process health and
render logs alone do not establish that Ziggy can see the game. On September
12, the two isolated game windows were closed gracefully, then `Play.cmd` was
launched through an approved normal-desktop invocation. A subsequent check
confirmed a responsive, visible game window on Windows desktop `Default`.
Future agent launches intended for Ziggy must verify that desktop and window
visibility, or give Ziggy the local `Play.cmd` to open directly.

## Cloud next

`Play_High_Quality.cmd` selects Forward+ at 1920x1080 with 4x MSAA, larger
shadows, SSAO, SSIL, SSR and restrained glow. It is an **untested remote/modern-GPU
candidate**, not a confirmed cloud result. `Play.cmd` retains local Compatibility
play. The high-quality launcher starts the current computer; it does not
provision a service or connect to a remote desktop.

The build script's `-CloudBundle` switch packages only seven portable application
and license files. The current ZIP is 99,888,290 bytes and its game pack is
13,765,920 bytes. Each ZIP member was checked byte-for-byte against the prepared
build. Local saves, logs and other repository data are excluded.
Follow the [cloud-PC test plan](../../docs/notes/explorable_world/CLOUD_PLAY.md)
for account, region, network and spending decisions.

This is still a stylized prototype. Terrain is distant scenery, the lake has
procedural ripples rather than a complete water simulation, and people do not
yet have skeletal animation or facial performance. The next visual milestone
should judge richer assets and lighting on the chosen remote GPU, before
resuming story revisions or the separate eight-second video experiment.
