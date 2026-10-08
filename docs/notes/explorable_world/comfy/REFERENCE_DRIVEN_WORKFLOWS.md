# Reference-driven images and video for the Observatory

**October 2 direction update:** the [video-first workflow map](index.html#video-first) now governs production. Ziggy selected source-video transformation with the original motion retained. The Godot study below remains a historical proposal; translating each result back into a playable world is no longer required. The video controls and review methods in this note now directly support the active work.

Reviewed September 12, 2026 from Ziggy's supplied 0:00–21:52 tutorial
transcript, attachment `52a043e2-ce83-4019-9a41-a6aced4feda9`.
Transcript SHA-256: `e1c56a45b35bc6ed7dcbf05af4f46e2c71283c64c9b2bdcf897c4aee8524db70`.
The canonical video URL, creator attribution and linked custom workflow
downloads have not been verified. The transcript declares NVIDIA sponsorship;
its hardware timings are not measurements of our environments.

**Decision: adapt the methods; discover dependencies before execution.**
This review produced no generation, model download or extension installation.
Pathfinder already covers setup routes, model roles, typed connections,
subgraphs and controlled comparisons. The [shared-methods map](../pathfinder_handoff/README.md#shared-methods-and-local-independence)
locates that curriculum. This note preserves the additional production steps.

## First use: render our world, then explore its appearance

At **19:22–19:57**, the presenter uses a low-poly 3D render for composition
and a realistic image for visual style. This is a promising way to explore
Ziggy's quality target using the Observatory's actual layout.

1. Capture one clean Godot view of the courtyard, without HUD. Preserve the
   camera transform, field of view, scene revision and source image hash.
   Start with the existing bench, archway, water and distant observatory.
2. Choose one style reference. Our [preferred guardian still](references/wolf_care_v001.intake.md)
   suggests soft forest light, believable surfaces and atmosphere. Record
   whether it guides lighting/materials or subject identity; those are
   different instructions. It does not supply a 3D wolf.
3. Discover a supported multi-reference editing template. The official
   [FLUX.2 Klein guide](https://docs.comfy.org/tutorials/flux/flux-2-klein)
   supplies base/distilled 4B and 9B editing recipes and Cloud entry points.
   It is a candidate, not a verified model in our account. Identify the exact
   variant and retain its encoder, VAE and sampling recipe. SDXL remains the
   default for new third-party still-image searches; this specific editing
   need can justify a different family.
4. Prepare one output at the template's supported modest dimensions. Request
   richer stone, wood, foliage and light while keeping the camera, building
   positions, horizon, paths and openings. Leave optional upscaling off.
5. Compare the source and edit. Reject attractive changes that relocate the
   arch, obstruct a route or invent another building. Record what improved
   and what drifted; preserve the graph and resolved inputs using [SOP 6](index.html#sop-6).
6. Translate the useful result into one **playable** improvement: replace a
   foliage asset, improve a material, or adjust scene lighting. Compare from
   the same camera, then walk around it and measure performance on the
   intended runtime. The [character showcase](../CHARACTER_SHOWCASE.md)
   remains the plan for a detailed resident or guardian.

The edited image is a visual study. It cannot establish matching geometry,
collision, lighting from another viewpoint or game performance. Keeping this
experiment to one view makes it a short aid to engine work.

## Video and dialogue checks to add to every borrowed recipe

**Preview wiring — 8:02–9:55.** Inspect the actual socket types inside a
subgraph. For a preview node expecting image frames, expose decoded `IMAGE`
and the matching `AUDIO`, or use a supported video-components conversion.
Do not connect a `VIDEO` object as though it were decoded pixels. Keep the
original save branch until the replacement produces a verified saved file.
An already adequate native preview needs no extension.

[VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite)
combines frames with optional audio; its output format, `frame_rate`,
`save_output` and format-dependent `save_metadata` settings matter. Check the
selected version's schema. For an ordinary review copy, use a supported MP4
codec instead of silently accepting GIF. Verify frame count, FPS, duration,
dimensions and audible synchronization in the actual file. Changing FPS
alone changes playback speed; it does not create intermediate frames.
An 81-frame sequence at 24 fps is about 3.375 seconds, not an eight-second
clip. Follow the exact model's valid frame counts and inspect the encoded
duration. Preserve editor/API JSON separately even when embedding metadata.

**Authored dialogue — 10:08–11:44.** A prompt enhancer can rewrite the intended
line before generation. Record both the entered text and effective prompt.
Use the recipe's supported enhancement toggle where available; bypass only
after checking the replacement connection. Text encoding and image
conditioning may still be required. Listen to the result: an unchanged
prompt does not guarantee correct speech or lip movement.
The transcript demonstrates newly generated speech/video; preserving an
existing shot while replacing dialogue is a separate test.

Current official [LTX union-workflow notes](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/2.5/LTX-2.5_ICLoRA_Union_Control_Distilled.json)
show an enhancement control and effective-prompt preview. This is a checked
2.5 example, not evidence that the transcript's 2.3 graph has identical nodes.
Our recovered guardian recipe also needs its own dependency/version check.

**Upscale after review — 13:45–15:57 and 18:21–19:04.** Save a baseline whose
composition, anatomy and motion work, then compare one upscale derivative.
Review changed faces, fur, text, edges, temporal flicker and sound/duration.
More pixels do not establish recovered original detail. Record the upscale
model, scale, settings and parent output; retain both files.

## Choose the environment before following installation instructions

| Environment | Apply the guide this way |
| --- | --- |
| Comfy Cloud at cloud.comfy.org | Discover supported templates, nodes and models. Use its supported import route for a missing model. Local Manager installs do not change this service. |
| Windows Portable | The tutorial's batch files, embedded Python and SDK installer steps concern that installation. This is not our selected production route on the HP Z210. |
| ComfyUI on a future Runpod Pod | A separately managed environment with its own OS, dependencies, models, storage and billing. Runpod authorization is verified; no Pod is provisioned. Select a compatible template and use its documented installation paths. See [Runpod setup](../RUNPOD.md). |

Comfy's [Cloud custom-node policy](https://support.comfy.org/articles/6791455062-custom-nodes-on-cloud)
describes the managed selection. Prefer a supported recipe before creating
another environment just to reproduce an optional convenience feature.

The likely “RG3” reference is [rgthree-comfy](https://github.com/rgthree/rgthree-comfy),
whose documented features include a progress bar and selective output
queuing. Treat it as optional; inspect which branches and seed controls
actually execute. The official [RTX node package](https://github.com/Comfy-Org/Nvidia_RTX_Nodes_ComfyUI)
requires an NVIDIA RTX GPU and lists `nvidia-vfx` in its
[requirements](https://github.com/Comfy-Org/Nvidia_RTX_Nodes_ComfyUI/blob/main/requirements.txt).
Verify the chosen host, driver, package and runtime before adopting the
tutorial's installation sequence. No local GPU purchase is implied.

Do not adopt universal “24 GB handles everything,” guaranteed speed, or
lossless-quality claims from the presentation. Memory depends on the exact
recipe, precision, dimensions and frame count. Cloning a node repository
also does not establish that model weights and runtime dependencies exist.

## Later candidates, when the experiment calls for them

The official [LTX repository](https://github.com/Lightricks/ComfyUI-LTXVideo)
lists versioned depth/edge/pose control and motion-track examples, worth
investigating if a shot must follow an authored camera or performance.
Its Dub-It example also describes dialogue rephrasing from an existing
video. That is a candidate for our later eight-second rewrite; it is not
the same as separately supplying replacement audio to a lip-sync system.
Availability, cost and preservation quality remain untested here. The October 2
video pivot promotes structural control to the first experiment; dialogue remains
a separate later route. Current LTX documentation keeps Dub-It on its validated
2.3 stack, separate from 2.5 visual-control workflows.

## October 3, 2026: supplied tutorials and the current Cloud template

The three supplied transcripts are archived byte-for-byte with SHA-256 hashes
in [their provenance record](references/user_transcripts_20261003.provenance.json).
They inform the work; they do not change the current task: a Comfy Cloud
FLUX.2 Klein two-reference still edit, using the Grok design for appearance,
pose and clothing and the intended likeness reference for facial identity.
Review that identity baseline before adding tattoos and a grill.

**[FLUX episode 08](references/flux_episode08_20261003.user_transcript.txt).**
The transcript covers FLUX.1 text-to-image, not Klein identity editing.
Loading example PNGs at 2:15-4:43 restores embedded workflow metadata; it
is not reference-image conditioning. Later style selectors concatenate
prompt text (8:15-10:58), and the realism LoRA comparison (25:16-27:34)
does not demonstrate face-reference mapping. Keep its useful methods:
fixed-seed comparisons, one change at a time, a simple exposed control
surface, and separate baseline/LoRA comparisons. Verify unique input
filenames and previews after the reported collision at 26:51-27:18.
Its FLUX.1 samplers, guidance settings and LoRAs are not Klein defaults.

**[MiniMax H3 tutorial](references/minimax_h3_20261003.user_transcript.txt).**
Treat this as a future video experiment. The creator describes ordered
image/video/audio references (7:14-8:02) and replacing an environment and
costume using image references (8:21-8:35). Assign separate roles to
appearance images, source-video performance/motion, and audio; write those
roles into the prompt and retain the input order. Reference use alone does
not establish exact motion or identity preservation: the creator also
reports appearance drift (6:55-7:12). Check the exact supported recipe
against the [Comfy H3 guide](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)
and [MiniMax announcement](https://www.minimax.io/news/minimax-h3-open-source)
before adopting its claims. This archive does not establish Cloud availability.

**[Video-model comparison](references/video_model_comparison_20261003.user_transcript.txt).**
Use its examples to define review criteria: natural motion, stable faces
and objects, prompt adherence, interaction and multi-reference separation.
Rankings are creator opinions, not our controlled benchmark; the estimates
at 24:13-24:56 are not current prices. Preserve the raw transcription rather
than silently treating its inconsistent model names as verified versions.

**Execution stays in Comfy Cloud.** Local checkpoint downloads, git/pip
installation, custom-node setup and hardware recommendations in these
transcripts do not provision the managed service. Discover supported Cloud
templates and dependencies before a later experiment; this review installs
no local nodes and downloads no weights.

## October 4, 2026: episode 07 prompt and style controls

The [episode 07 transcript](references/comfy_episode07_prompt_styles_20261004.user_transcript.txt)
is preserved unchanged and added to the existing [provenance record](references/user_transcripts_20261003.provenance.json).
At 1:06-1:20 and 9:57-10:26, the useful pattern is **instruction text +
optional style text -> string concatenation -> text encoder -> conditioning**.
This joins raw strings before encoding; `ConditioningConcat` operates on
already encoded conditioning and is a different operation. The colored
Easy Positive/Negative text nodes (2:20-2:44) are string inputs, not encoders;
node color and title do not establish socket type or model behavior.

Keep the core edit instruction visible, default optional styles to empty,
and inspect the complete combined prompt. The tutorial demonstrates several
style snippets (5:59-8:27; 10:32-11:07); add one at a time with a fixed seed,
checking that style changes preserve the intended likeness and design.
Its claim that earlier styles always matter more is not a universal rule.
Retain Klein's validated conditioning and sampling recipe; the tutorial's
SDXL negative-style branch is not evidence that the same branch is useful
in the current Klein workflow. Compact controls can expose the useful inputs
while preserving the inspectable graph (11:20-11:45).

The WAS/Easy Use installation and local styles CSV/config paths
(0:20-0:51; 4:46-5:56) do not install or configure Comfy Cloud. Verify supported
Cloud string controls before adopting that implementation; explicit editable
style text can express the same intent without an unverified local CSV path.
A combined-text display can show the effective prompt before generation.
An image preview displays supplied or already computed pixels; it cannot show
the future result of newly changed prompt/style controls until generation runs.
Keep input references, prior output and newly generated output clearly labeled.

## October 4, 2026: episode 06 styles and sampling controls

The [episode 06 transcript](references/comfy_episode06_styles_sampling_20261004.user_transcript.txt)
is archived with its source/hash in the existing [provenance record](references/user_transcripts_20261003.provenance.json).
It uses an SDXL workflow (0:51-0:59), joins separately encoded prompts with
`ConditioningConcat` (1:33-2:04), and later groups the interface (7:31-8:31).
That encoded-conditioning operation differs from episode 07's raw-string
concatenation before one text encoder; preserve this distinction when
adapting its style controls. The CSV loader's local installation and file
placement (0:28-0:48; 4:12-4:56) are not automatic Cloud configuration.

SDXL's `KSampler` bundles several controls. The current FLUX.2 Klein 9B
distilled recipe distributes them across `SamplerCustomAdvanced` and its
inputs: `KSamplerSelect` chooses the sampler, `Flux2Scheduler` supplies the
noise schedule and step count, `CFGGuider` sets guidance, and `RandomNoise`
sets the seed. Exposing these controls does not require replacing the
validated sampler graph. Keep the tested baseline of four Euler steps,
CFG 1 and seed 42 for comparisons. Do not copy 30 steps, CFG 7 or a Karras
schedule from another model's example without a deliberate compatibility
check; those values are not established Klein defaults or narrated settings
in this transcript.

Styles can overwhelm the requested subject (13:17-13:53). Start with no
style, add one optional style at a time, and review likeness, clothing and
composition before accepting a change.

**Episode 06 screenshot and source links.** Ziggy supplied the
[episode 06 video URL](https://www.youtube.com/watch?v=cmikc-Jo1gk) and previously
supplied the [episode 07 video URL](https://www.youtube.com/watch?v=Xsx-u0OMezw).
Both are recorded as user-supplied source URLs, not independently watched
video evidence. The episode 06 screenshot approximately matches the supplied
transcript's Chinese ink brush plus graffiti demonstration at **12:19-12:44**;
no exact playback timestamp is visible in the screenshot.

The screenshot shows two style CSV selectors, each emitting positive and
negative strings. Those strings feed separate positive/negative text
encoders; `ConditioningConcat` chains combine the encoded style and prompt
branches before `KSampler`. This is the SDXL conditioning-mix branch, distinct
from both episode 07's string concatenation and the current Klein reference
edit. Its visible sampler controls are seed **2024**, **fixed**, **30 steps**,
**CFG 7**, sampler **dpmpp_2m**, scheduler **karras**, and **denoise 1.0**.
These settings come from the supplied screenshot, not narration or an
independently fetched video. Preserve them as SDXL example evidence; they
do not replace the tested Klein defaults.

## October 4, 2026: episode 05 model comparisons

The [episode 05 transcript](references/comfy_episode05_sd3_comparison_20261004.user_transcript.txt)
is archived in the [provenance record](references/user_transcripts_20261003.provenance.json),
with the [video URL supplied by Ziggy](https://www.youtube.com/watch?v=q9ufjcMofI0).
This review used the supplied transcript, not independently watched video.
The tutorial compares SD3 Medium text-to-image packages with different
text-encoder contents/precision, then compares SD3 Medium with the SDXL
fine-tune Juggernaut X (10:07 onward). These are not source-image edits.

At 3:01-4:08 it changes the latent node and sampler settings for SD3:
`EmptySD3LatentImage`, 28 or 30 steps, CFG 4.5, `dpmpp_2m` and `sgm_uniform`.
Treat these as the tutorial's SD3 recipe, not transferable Klein defaults.
The reusable comparison method is shared raw prompt strings and an explicit
fixed seed (4:41-7:15), with separate model-specific encoders, latent setup,
sampling and decoding. Feed shared strings into each branch's own text
encoder; do not share encoded conditioning across incompatible architectures.
The same integer seed improves reproducibility within a fixed recipe but
does not establish identical latent noise or matched quality across model
architectures. Record each branch's full settings and evaluate the outputs.
Use distinct saved-image prefixes to identify the producing model (8:16-8:22).

The creator's quality preferences, hardware timings and proposed censorship
explanation for anatomical errors are historical opinions or hypotheses,
not established current findings for our account. Compare prompt adherence,
likeness, anatomy and preservation using our own outputs before choosing a
production route. In Comfy Cloud, discover supported models and compatible
nodes first; the tutorial's checkpoint downloads, local update and folder
placement instructions do not provision the managed service. Transcript
archival alone does not establish model availability.

The official [SD3 Medium model card](https://huggingface.co/stabilityai/stable-diffusion-3-medium)
confirms the illustrated packages share the SD3 image model and VAE while
bundling different text encoders/precision. They are not wholly different
image-model architectures. Our October 4 Cloud catalog query returned SD3.5
Medium/Large checkpoints and SD3.5 example/control templates; it did not
confirm the original SD3 Medium packages. Those SD3.5 hits have not been
dependency-tested or rendered, and are not a silent substitute for this guide.

**Applied to our existing reference editor:** the separate
[Civitai comparison](https://cloud.comfy.org/#1ee8615b-5586-42fd-bf3d-3d202b2377eb)
is now version 4, with A baseline and B Candid Film at 0.5. Shared reference
images, crop, assembled prompt and fixed sampling controls feed separate
matching Klein branches. Outputs have distinct A/B save prefixes. Server
conversion and dry-run passed without warnings; the compiled A branch equals
main editor version 6, and B equals A after its sole LoRA loader is bypassed.
This paired revision has not rendered. It adapts the tutorial's comparison
method to our tested Cloud recipe without importing local SD3 weights or
changing the main reference editor. See the [workflow library](workflows/README.md)
and [validation record](workflows/hon_dolo_reference_edit_v001.record.json).

## October 4, 2026: episode 04 single-image refinement and LoRA

The [episode 04 transcript](references/comfy_episode04_img2img_lora_20261004.user_transcript.txt)
is archived with its source/hash in the [provenance record](references/user_transcripts_20261003.provenance.json).
The [video URL](https://www.youtube.com/watch?v=xedwjtaPVzw) was supplied by Ziggy;
this review used the transcript, not independently watched video.

At 0:36-1:26, `LoadImage -> VAEEncode -> KSampler` replaces an empty latent
with an encoded starting image, using the checkpoint's matching VAE.
The denoise examples (1:36-4:16) illustrate a tradeoff: lower values generally
retain more of the input, while higher values allow larger changes. Denoise
is not a percentage of preserved pixels, an identity lock or a guarantee
that clothing, tattoos and facial features remain unchanged. Compare fixed
seeds and inspect the complete result. The image-size node at 4:19-6:48
resizes/crops pixels before encoding; it does not demonstrate a learned
super-resolution model or recovered detail. Preserve aspect ratio deliberately
and choose dimensions for the actual recipe rather than copying a universal
size/divisibility rule.

The tutorial adds LoRA to img2img at 15:12 onward. Check the exact base family,
recommended strength and documented trigger words (10:02-10:43). Its routing
at 12:05-13:21 sends the adapted MODEL to sampling and the adapted CLIP to
prompt encoding when the LoRA contains text-encoder weights; a model-only
LoRA does not imply the same CLIP changes. Keep a fixed-seed baseline with
the LoRA bypassed before assessing its effect.

This is single-input SDXL refinement, distinct from our two-reference Klein
identity edit. It does not automatically map a second person's face onto the
Grok design. Localized tattoo/grill changes need a separate mask/inpainting
workflow, and motion-preserving video needs a separate temporal workflow;
neither is built by this tutorial adaptation. Cloud availability and actual
execution must be established for the chosen graph. Local LoRA downloads
and folder placement do not provision the managed service.

**Cloud application:** the separate [Image Refinement SDXL recipe](https://cloud.comfy.org/#2a60a23f-f68a-4a66-92c6-0e30aa0d5e03)
adapts official `image_sdxl_simple` with a loaded-image latent and visible
denoise control. It deliberately uses available Juggernaut XL v9 instead of
the tutorial's Juggernaut X. Its 0.30 denoise is an exploratory starting value;
the main Klein identity route is unchanged. Version 2's server-converted graph
passed dry-run and resolved-input checks, but no image generation ran. The
[workflow record](workflows/hon_dolo_img2img_sdxl_v001.record.json) captures the
exact defaults and validation. Primary references are the
[ComfyUI img2img example](https://comfyanonymous.github.io/ComfyUI_examples/img2img/)
and the [Juggernaut v9 model card](https://huggingface.co/RunDiffusion/Juggernaut-XL-v9).

## October 4, 2026: episode 03 sampling and canvas operations

The [episode 03 transcript](references/comfy_episode03_sampling_canvas_20261004.user_transcript.txt)
is archived with its source/hash in the [provenance record](references/user_transcripts_20261003.provenance.json).
No canonical video URL was supplied and the video was not independently
watched. The supplied screenshot approximately matches connected paste at
16:50-17:09; no exact playback timestamp is visible.

A fixed seed supports controlled comparisons when the model, full inputs,
versions and runtime behavior are held constant; the tutorial's promise of
always identical pixels is too broad. An unchanged graph may reuse cached
results (3:27-3:39), which is not evidence of fresh inference. Steps, CFG,
sampler and scheduler are model-specific; additional steps or stronger CFG
do not guarantee better results. Promoting widgets to typed inputs
(6:13-7:17) lets one visible value feed multiple compatible branches, but
check the resolved execution values and seed's post-generation behavior.

A latent batch contains several samples within a run; queuing submits
additional jobs; independent output branches add computations to a graph.
These are different mechanisms and can increase Cloud usage and charges.
Check batch size, queued-job count, auto-queue state and reachable output
branches before running a comparison. The creator's RTX 4090 timing example
is not a Cloud cost or throughput measurement.

Grouping, collapsing or hiding controls changes the interface, not whether
a branch executes (12:31-12:49). Bypass can pass compatible inputs through
and is not a universal off switch; required inputs can become invalid.
Verify the actual executable branch/output selection instead of relying on
its group appearance.

For connected duplication, copy with `Ctrl+C`, then use `Ctrl+Shift+V` to
retain incoming connections from nodes outside the copied selection; see
the official [ComfyUI shortcuts](https://github.com/Comfy-Org/ComfyUI#shortcuts).
In the tutorial's basic SDXL graph, copy `KSampler`, `VAEDecode` and
`SaveImage` together (17:11-17:30) to create a complete additional saved-output
branch. Copying only a sampler does not create another saved image. Inspect
which upstream model, conditioning and latent links remain shared, then
use distinct output prefixes and deliberately vary only the intended input.
