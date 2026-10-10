# One detailed character in the Observatory

September 12, 2026. Proposed experiment; no character asset selected or imported.

## Ziggy's visual direction

The playable world proves exploration, but its current appearance is far from
Ziggy's realism reference. GTA6 is an aspirational quality reference. The
Ready Player One idea also allows deliberately different visual styles to
coexist: a detailed character in a simple or block-like environment could be
desirable. Uniform photorealism across the whole village is not a prerequisite
for the next useful result. The immediate need is visible evidence that a
substantially more convincing character can inhabit this playable world.

The screenshot shows angular foliage, repeated surfaces, simple distant
geometry and broadly uniform illumination. Current residents are procedural,
static figures using flat-color materials. More display pixels or a more
powerful GPU alone will not replace that geometry, surface design or motion.

## Identify what the favorite model actually contains

**Current first reference:** Ziggy subsequently selected
`10b936eb46c1e671b089bf26e0c551bb.mp4`. The
[preferred-reference intake](comfy/references/wolf_care_v001.intake.md)
records an eight-second image-to-video recipe recovered from that file.
Its representative still shows a woman touching foreheads with an enormous
wolf beside a stream: a concrete target for fur, clothing, atmosphere and
care expressed through posture. The original input `gf_24_a.jpg` was not
supplied. Only a still has been visually reviewed, not the full motion.
This is the primary direction for the showcase; the walking-wolf example
below remains secondary. Neither clip includes a playable character mesh.

Ziggy supplied [Civitai item 142373294](https://civitai.com/images/142373294)
and a screenshot of the [Favorite_1 collection](https://civitai.com/collections/17962709).
The screenshot establishes an art direction: believable fur and skin, forest
light, mythic creature scale, and gentle human/creature contact. That last
element gives care a visible expression before any dialogue is written.

Public metadata identifies the linked item as a 5.042-second, 1088 x 1920
video by Solricks, associated with the **LTX-2.5 Giant Fantasy** LoRA for
LTXV 2.5. The associated version describes text-to-video and image-to-video
support. It is a useful cinematic reference; the listing does not provide a
rigged game character. The [reference record](comfy/references/civitai_142373294.reference.json)
preserves verified IDs, source evidence, and remaining workflow unknowns.
The assistant has not authenticated into Ziggy's private collections or
verified this item's collection membership.

Ziggy subsequently saved the MP4, and its embedded Comfy editor/execution
graphs were recovered successfully. The [recipe intake](comfy/references/civitai_142373294.intake.md)
records a two-stage video-generation route and its remaining Cloud dependencies.
It contains no playable wolf mesh; this gives the cinematic experiment an
actual source recipe while the 3D showcase still needs an appropriate asset.

| Resource | Route into the game |
| --- | --- |
| Textured 3D character, preferably GLB/glTF; FBX is also supported | Inspect mesh, materials and any rig/animation, then import and stage in Godot. |
| Image-generation checkpoint or LoRA, such as an SDXL resource | Use to generate reference imagery; it is not a character body Godot can load. |
| Video-generation LoRA or finished clip, such as this LTXV reference | Study or reproduce appearance, movement and lighting in a cinematic workflow. A mesh, rig and real-time scene remain separate production work. |
| Character image or rendered promotional preview | Establish the desired appearance. A corresponding usable 3D asset must still be sourced or built. |

[Godot's import documentation](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)
recommends glTF and describes FBX support. Comfy's
[LoRA example](https://docs.comfy.org/tutorials/basic/lora) concerns generative
model adaptation. [Image-to-3D workflows](https://docs.comfy.org/tutorials/3d/hunyuan3D-2)
are a possible additional route, but their outputs, texture support and rigging
need validation. They do not guarantee an animated character matching a
reference image. The fastest first proof is likely an existing textured,
rigged game character with a supplied idle animation.

## Proposed implementation

1. Choose one human or creature against the supplied visual reference. The
   enormous forest guardian is a useful candidate for scale and emotional
   presence, but fur quality must be judged in the actual game renderer.
   Record source,
   exact version and permitted game use. Retain large originals in the existing
   cloud archive and only the selected runtime derivative in the game.
2. Import under `games/observatory/assets/characters/showcase/` and wrap it
   with `games/observatory/scenes/characters/showcase.tscn`. These paths are
   proposed and have not been created.
3. For a human resident, replace the existing visual child in `world_builder.gd`;
   preserve its parent, placement, collision, interaction and story state.
   For a creature, stage a separate showcase actor without replacing Mara's
   body or changing her story. Fit feet, forward direction and intended scale
   to the existing scene; oversized bodies need appropriate collision and
   enough space around the walking route.
4. Evaluate the imported materials in the actual renderer. Match light
   direction, exposure and ground contact. Different artistic styles can share
   believable physical placement. Imported preview lighting does not transfer
   automatically; skin, eyes and hair may need material work.
5. Use an included idle if available. Keep its movement anchored to the existing
   interaction. A static mesh can demonstrate shape and materials, but should
   not be presented as successful character animation or facial performance.
6. First compare in the existing courtyard. Then improve only the nearby light,
   ground and backdrop if that helps the composition. Keep the deliberate
   difference in style available for Ziggy to judge.

## Evidence and next decision

Capture the old and imported figures at the same conversation distance, then
walk around the imported figure to inspect front, side and back. Check both
resident placements if replaced, existing E interactions, collision, foot contact, shadows and any
included animation. Measure moving frame times and inspect texture/hair
artifacts on the local Compatibility build. A suitably optimized character may
work here; actual performance remains unknown until the asset is chosen and
tested. Use the cloud workstation for a separate richer-renderer comparison.

The result should answer two questions: does the character reach a convincing
visual standard in motion, and does its contrast with the surrounding world
feel interesting or accidental? Expand the successful treatment afterward.
The current chapter's story remains unchanged; facial acting and the separate
dialogue-rewrite experiment remain later work.
