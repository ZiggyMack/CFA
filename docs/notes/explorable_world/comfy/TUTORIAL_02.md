# Tutorial 2: reading and adapting someone else's workflow

Reviewed September 12, 2026 from Ziggy's supplied 0:00-23:24 transcript of
ComfyUI Tutorial Series, episode 2, nodes and workflow basics. A canonical video
URL was not supplied with this transcript. Pathfinder's current curriculum
records an Episode 2 URL; direct retrieval failed during the shared-methods
review, so a title/transcript match has not been independently checked here.
Timestamps below refer to the supplied attachment.
This is a source review and a read-through of our existing recipe, not a new run.

For the full learning curriculum, use Pathfinder's **ComfyUI guide → 07 /
Workflow lab**, which already provides seven Episode 2 practice milestones.
The [shared-methods map](../pathfinder_handoff/README.md#shared-methods-and-local-independence)
links its source and our local fallbacks. Keep this note focused on what changes
our Observatory procedure and the actual pump recipe; do not duplicate that lab.

## What carries into our work

At 0:33-2:22 and 11:26-17:50, the tutorial builds an understandable image graph:
load the model, encode instructions, prepare a latent input, sample, decode and
save. When studying an NKD or ZHO resource, locate these responsibilities before
changing prompts or adding nodes. Different model families can divide those
responsibilities among different loaders.

At 8:30-10:38, it follows connections to discover compatible operations. Follow
the **socket type and node schema**; colors and custom titles are visual aids.
At 13:21-13:40, two identical prompt encoders acquire positive/negative roles
from their destinations. A renamed node title does not change its function.

At 14:01-14:12, the demonstrated model's recommended settings guide sampling.
Preserve the specific release and recipe. At **11:41 the narrator identifies
Juggernaut X**, resolving Ziggy's earlier unnamed Version X reference. The
transcript does not establish an exact Civitai version ID or file hash. It does
not validate the reported X-versus-Hyper preference in our environment.

At 18:57-19:19, an omitted VAE connection provides a useful debugging example:
read the actual failing input and repair that connection. Do not respond to a
missing input by blindly changing seeds, reinstalling packages or buying a GPU.

At 20:15-23:08, reroutes, groups and collapsed nodes improve readability. After
the graph works, expose a small set of meaningful controls while retaining the
full graph for maintenance. Our [SOP 8](index.html#sop-8) carries this into App
mode where supported. Current UI labels and shortcuts may differ from the video.

## Qualifications for the current environment

| Tutorial simplification | Working rule here |
| --- | --- |
| Everything entering KSampler is latent | Its typed inputs include MODEL, positive/negative CONDITIONING and LATENT, plus settings. Only the sampled representation is latent. |
| Empty latent is a placeholder image | Core EmptyLatentImage creates a zero tensor of the requested size/batch; the sampler prepares seeded noise. Other architectures may need different latent nodes. |
| VAE works like compressing/uncompressing a file | It is a learned image/latent transform, not lossless ZIP storage. Keep original pixel images. |
| Save Image has no output, so processing must end | Branch the upstream IMAGE into saving and further processing. Current upstream SaveImage also has IMAGE passthrough; use it only if our deployed schema exposes it. |
| Save Image saves to your computer | It saves in the execution environment. In Cloud, preserving a local or Drive copy requires a separate output/archive step. |
| Save, Refresh, Reset View and Manager have fixed meanings | Current Save/Save As preserves workspace state; Export preserves an external graph. Reset View is navigation, not a way to reconstruct a lost graph. Cloud doesn't expose arbitrary local Manager installation. |
| Fixed seed reproduces an image | It supports controlled comparisons. Also preserve exact models, inputs, dimensions and settings; runtime/version changes can alter results. |
| 1024 is the universal image size | Use the selected release's supported dimensions/aspect ratios. SDXL guidance does not automatically apply to video, Z-Image or mesh workflows. |

Sources: [KSampler inputs and noise preparation](https://docs.comfy.org/built-in-nodes/sampling/ksampler),
[typed inputs](https://docs.comfy.org/custom-nodes/backend/datatypes),
[current upstream core nodes](https://github.com/Comfy-Org/ComfyUI/blob/master/nodes.py),
[autoencoder implementation](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/ldm/models/autoencoder.py),
[determinism caveat](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/cli_args.py),
[Cloud node policy](https://support.comfy.org/articles/6791455062-custom-nodes-on-cloud),
[current import/export actions](https://support.comfy.org/articles/2229074405-import-export-workflows).
Master-branch source was reviewed on this date; it is not a verified deployed
Cloud revision. The latest connection status remains separate from this review.

## Read the pump recipe we already executed

Our [recorded execution graph](workflows/pump_concept_v001.api.json) contains
ten nodes. These are inspected saved inputs from the earlier successful run,
not a fresh account-discovery result:

| Stage | Actual recipe |
| --- | --- |
| Diffusion model | UNETLoader loads z_image_turbo_bf16.safetensors; ModelSamplingAuraFlow applies shift 3. |
| Text encoder | CLIPLoader loads qwen_3_4b.safetensors with type lumina2; CLIPTextEncode processes the pump description. |
| Other conditioning | ConditioningZeroOut derives the sampler's negative input; this is not the tutorial's separate negative-prompt text box. |
| Starting latent | EmptySD3LatentImage requests 1024 x 1024, batch size 1. Its class name does not mean the whole graph is an SD3 checkpoint recipe. |
| Sampling | Seed 42, 8 steps, CFG 1, res_multistep, simple scheduler, denoise 1. |
| Visible output | VAELoader supplies ae.safetensors to VAEDecode; the resulting IMAGE feeds SaveImage. |

The tutorial's graph-reading method transfers to this recipe. Its Juggernaut
sampling settings and bundled checkpoint loader do not transfer automatically.
The saved editor graph has a randomize seed control: fix the control and seed
before attempting a controlled rerun. Actual current availability and cost
would need a production preflight.

## Apply this to the submitted resources

Use [SOP 2](index.html#sop-2) and the
[workflow intake sheet](templates/workflow_intake.md) for the next resource.
ZHO supplies recipes whose embedded model and grouped-node dependencies need
inspection. NKD supplies useful review/control operations; a package README or
GitHub Actions publishing run is not automatically a generation recipe.

Ziggy's Favorite_1 screenshot supplies a new visual reference: realistic
surfaces, atmospheric forest light, mythic creature scale and moments of care.
Its visible clip thumbnails do not establish downloadable 3D characters or
recoverable Comfy graphs. The [character showcase](../CHARACTER_SHOWCASE.md)
keeps the playable-asset test distinct from a cinematic image/video experiment.
Find actual recipe metadata where available before choosing a generation path.

### First favorite traced: LTX-2.5 Giant Fantasy

Public metadata for [item 142373294](https://civitai.com/images/142373294)
identifies a 5.042-second portrait video by Solricks, associated with the
LTXV 2.5 LoRA [LTX-2.5 Giant Fantasy, version 3313822](https://civitai.com/models/2928244?modelVersionId=3313822).
The [version API](https://civitai.com/api/v1/model-versions/3313822) describes
text-to-video and image-to-video support, names giantfantasy_ltx25.safetensors,
and supplies the trigger giantfx. It does not identify a complete base-model,
encoder, VAE, node and sampling recipe. SDXL remains our still-image default;
this video requires a workflow compatible with its own model family.

The item's prompt field says “Open this video in ComfyUI.” That is an
instruction, not the actual generation prompt. We checked the public page and
version metadata, then attempted a bounded original-video retrieval; the
download returned HTTP 403 before any media was saved. Ziggy then used the
browser's native Save video as menu successfully. The resulting MP4 contains
both the editor graph and a 72-node execution graph in its comment metadata.
Both were extracted and checked against the source file; see the
[recovered-recipe intake](references/civitai_142373294.intake.md) and
[reference record](references/civitai_142373294.reference.json). Video playback
and reproduction in our environment remain unreviewed.

**Decision:** retain the recovered graphs as source recipes and resolve their
actual Cloud dependencies before requesting any model import. Preserve a
separate working copy for any branch pruning or supported-node substitution.
Importing the LoRA alone is insufficient to execute this graph. This research
downloaded no model weights, used no paid generation and produced no new game
asset. It did establish a real example of workflow recovery from shared media.
