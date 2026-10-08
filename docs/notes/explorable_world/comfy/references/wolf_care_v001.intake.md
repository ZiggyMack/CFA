# Preferred reference: the woman and the forest guardian

September 12, 2026. Ziggy selected `10b936eb46c1e671b089bf26e0c551bb.mp4`
as the reference to use first. The earlier walking-wolf clip remains secondary.

## What we have

- [Preserved MP4](../outputs/references/preferred_10b936eb46c1e671b089bf26e0c551bb/10b936eb46c1e671b089bf26e0c551bb.mp4): 9,397,638 bytes, 1088 x 1920, 24 fps, 193 video samples, 8.042 seconds, with an audio track.
- [Representative still](../outputs/references/preferred_10b936eb46c1e671b089bf26e0c551bb/representative.png): a kneeling woman and enormous gray-brown wolf touching foreheads beside a forest stream. Detailed fur, worn clothing and warm backlighting establish the desired visual direction. Only this still has been visually reviewed; its timestamp is unknown. Motion and audible content remain unreviewed.
- [Editor workflow](wolf_care_v001.editor.json) and [execution graph](wolf_care_v001.api.json): both recovered from this MP4's comment metadata. The editor has four top-level nodes and eight subgraphs; the execution graph has 72 nodes.
- [Reference receipt](wolf_care_v001.reference.json): source/output hashes, settings, model filenames, dependency gaps and review limits.

The MP4 was relocated from game materials to ignored Comfy reference storage
on D:, with its hash unchanged. It is not yet an accepted runtime asset or a
verified cloud archive. The source creator, Civitai item and exact published
model version are unknown for this file; the earlier clip's attribution does
not establish them.

## What the recovered recipe does

This is **image-to-video**: `use_image` is enabled and the starting image is
`gf_24_a.jpg`. The supplied MP4 does not include that input file, and a scoped
search of CFA's `games/` and `docs/` found no matching image. A video frame
could become a new input for an adaptation, but would not recover the original
image or prove an exact recreation.

Recorded settings include seed 42, nominal eight seconds, 544 x 960 initial
sampling followed by 2x latent enlargement and refinement, CFG 1, and
`euler_ancestral`. It references LTX-2.5, a distilled LoRA and
`giantfantasy_ltx25.safetensors` at strength 0.8. The receipt inventories all
nine referenced model filenames; presence in a source graph does not establish
which files our Cloud environment supports or which optional branches execute.
An external MP3 and empty API-key inputs also remain in the preserved source.

Keep these recovered exports unchanged. Before a replay, work on a copy:
resolve the source image, inspect selected image/audio/API branches, check
Cloud node/model availability, and validate the output path and cost. The
[workflow intake procedure](../index.html#sop-2) and
[sampling comparison procedure](../SAMPLING_AND_CONTROLS.md) apply. No graph
execution, model import or paid generation was performed for this inspection.

## What reaches the game

| Desired experience | Additional work |
| --- | --- |
| Show the finished scene as a cinematic or on an in-world display | Prepare a game-supported video asset and implement playback, presentation and sound. The viewer sees a recorded camera view. |
| Generate a variation of this scene | Adapt and validate the recovered Comfy recipe, supplying its missing inputs and compatible dependencies. The result is still video. |
| Walk around and interact with the guardian | Source or create a textured 3D body, prepare its rig/animation as needed, then implement materials, placement, collision and behavior in Godot. The clip supplies appearance and atmosphere. |

A Civitai generative model or LoRA contains learned weights, not a playable
character mesh. A GLB/glTF/FBX character supplies geometry and may include
materials, a rig and animations, but still needs an engine test. The next
visual proof remains [one detailed character in the Observatory](../../CHARACTER_SHOWCASE.md),
with this quiet guardian encounter now the primary reference.
