# Comfy video workshop

**Active direction, October 2, 2026:** create high-resolution, lifelike video in ComfyUI. Ziggy selected **change the look, setting, or characters while keeping the original motion** as the first test. Preserve the Observatory prototype for a later return; it no longer determines which media we produce.

<a id="video-first"></a>

**Video first: from supplied content to the right workflow**

**Actual production, clarified October 3:** a lifelike trap-rap music video starring **Hon Dolo** (Han Solo with face tattoos and gangster styling), with **Princess Leia, Chewbacca, Darth Vader, Boba Fett, and Jabba the Hutt**. The [casting brief v3](casting/casting_brief.txt) assigns Grok styling templates on a placeholder face, following its observed refusal to generate the actor likeness. The [Comfy still-edit handoff](casting/hon_dolo_still_edit.agent_handoff.txt) develops the intended likeness from selected references, saves a clean checkpoint, and finishes tattoos/grill before accepting an identity master. The [two-reference still workflow](workflows/README.md) has now produced a clean likeness candidate and a Civitai style comparison in Cloud; user acceptance, finishing and video remain pending. The woman-and-wolf experiment below is solely a capability test; it cannot establish rap lip-sync, human character replacement, tattoo consistency, or a finished music video.

The immediate goal is one convincing transformed shot. Keep its source performance and camera timing recognizable while changing a clearly specified visual element. Photorealism is judged through playback: stable faces, believable surfaces, natural motion, contact and consistent lighting. Resolution is a separate deliverable.

**Working with the built-in Comfy Agent:** direct CFA access is restored through the local Codex app-server connection. The prepared [wolf handoff](workflows/wolf_care_union_control_v001.agent_handoff.txt) is an optional fallback, not a required manual upload. If used, explicitly select a separate wolf workflow; Ask gates runs but permits canvas edits, and Agent chat can consume credits. See [Comfy Agent documentation](https://support.comfy.org/articles/4013072355-comfy-agent). The handoff remains unsent.

**Where we left off.** The September work produced a playable Godot chapter and one Comfy pump still. Two video references have recoverable graphs, but no CFA video render, source-scene edit, or lip-sync result is recorded. The preferred [guardian MP4](references/wolf_care_v001.intake.md) is present: 1088 x 1920, 193 frames, 24 fps, 8.042 seconds. Its old recipe animates the missing `gf_24_a.jpg`; the clip itself can independently supply a new video-control experiment. Both recovered examples generated at 544 x 960 before 2x latent refinement. They are reference outputs, not our demonstrated native high-resolution generation.

This review covered the local Comfy handbook, tutorials, model guides, input/run templates, all saved workflow/reference families, storage/Runpod notes, and Pathfinder's scene, video and tutorial modules. Pathfinder remains an instructional reference, not an automatic workflow executor. The [shared-methods map](../pathfinder_handoff/README.md) locates it. Historical transcript URLs/attributions that CFA could not independently verify remain qualified; Pathfinder records Pixaroma episodes 1–4 and Max Novak's 2026 guide. Current primary documentation below was checked October 2; public documentation does not establish account availability.

**Choose by input and intended change.** These are recommended candidates to validate, not loaded or executed workflows.

| Your content and desired result | Workflow to prepare | What decides acceptance |
| --- | --- | --- |
| Existing clip; change look or setting, retain performance and camera timing — **selected first route** | LTX-2.5 Union Control; start with the source clip's depth guide. Official file: `LTX-2.5_ICLoRA_Union_Control_Distilled.json`.[^video-ltx] | Matching gesture, contact, framing and timing; intended appearance change; no distracting identity or texture drift |
| Character image plus a driving performance; create a new setting | Wan Animate 2, a distinct newer model using the driving video directly.[^video-wan] | Character likeness, performance, occlusions and camera behavior |
| Replace a character while retaining the existing background | Evaluate Wan2.2 Animate **Mix** with its reference image, source clip and mask/control preparation.[^video-wan-mix] | Subject/background boundaries and lighting hold through movement |
| Change only part of a clip | LTX-2.5 Inpaint with a mask; Wan2.1 VACE is a separate fallback candidate for masked/control editing.[^video-ltx][^video-vace] | Untargeted content remains acceptable; edited region stays coherent |
| Only a still image, or genuinely new action | LTX image-to-video/keyframe generation; this makes new motion, so it cannot prove preservation of a whole source performance | Action readability, identity and continuity |
| Replace dialogue later | Source video plus a dedicated lip-sync route; LTX Dub-It remains validated on 2.3, not 2.5.[^video-dubit] | Words, mouth movement, face stability and sound timing |

Structural controls guide generation; they do not lock every pixel or guarantee identity. Depth is the first candidate because the guardian includes a creature and scene geometry, rather than only a human skeleton. If depth also holds unwanted background structure too strongly, move to a masked edit or a task-appropriate pose/reference route. Change the route for that reason rather than repeatedly increasing prompt strength. Character replacement and background replacement should first be tested separately.

For a change covered by a specific edit adapter, also evaluate `LTX-2.5_V2V_ICLoRA_Single_Stage_Distilled.json`: it uses source RGB frames as guidance. Match the adapter's actual task; its shipped Instant Shave example is not a general relighting model.[^video-ltx]

**The supporting material, refocused.** The three supplied NKD/ZHO repositories remain useful, with different roles. Their READMEs and the VHS/RTX READMEs were rechecked October 2; earlier version and Cloud-catalog observations elsewhere in this handbook retain their September dates.

| Resource already in our material | Role now |
| --- | --- |
| [Comfy core](https://github.com/Comfy-Org/ComfyUI), [official templates](https://github.com/Comfy-Org/workflow_templates), [maintainer examples](https://github.com/comfyanonymous/ComfyUI_examples), [LTX nodes](https://github.com/Lightricks/ComfyUI-LTXVideo) | Baselines, exact node schemas, versioned video recipes and dependency checks |
| [VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite) | Video intake, frame/audio handling and saved review exports, when native nodes are insufficient |
| [NKD Preview Tools](https://github.com/Nekodificador/ComfyUI-NKD-Preview-Tools) | Optional timelines, scrubbing, frame extraction and comparison of takes |
| [NKD VFX Tools](https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools) | Optional lighting, lens, camera and control-map preparation; its still/viewport tools do not establish stable whole-clip processing |
| [ZHO workflow collection](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Workflows-ZHO) | Reference library including video and portrait examples; selectively adapt ideas after checking dependencies |
| FLUX.2 Klein, Qwen Image Edit, the executed Z-Image recipe, RealVisXL/Juggernaut references | Prepare a look or character still when needed. The SDXL preference remains a still-image default |
| Civitai, Hugging Face, [Civitai nodes](https://github.com/civitai/civitai-comfy-nodes) | Model/source discovery and selected imports. A hosted Civitai node is a separate service route, not required just to load a Cloud model |
| [NVIDIA RTX nodes](https://github.com/Comfy-Org/Nvidia_RTX_Nodes_ComfyUI) | Optional upscale comparison on a compatible RTX host after accepting a take |
| [rgthree](https://github.com/rgthree/rgthree-comfy), Registry and Manager | Optional workflow convenience and environment/dependency references |
| Hunyuan3D, its [wrapper](https://github.com/kijai/ComfyUI-Hunyuan3DWrapper), meshes, rigs and Godot/cloud gaming | Park the game work. Use 3D only if a particular shot needs previsualization |
| [LatentSync](https://github.com/bytedance/LatentSync), its [community wrapper](https://github.com/ShmuelRonen/ComfyUI-LatentSyncWrapper), saved Sync template | Retain as historically researched dialogue branches; not revalidated or required for this visual test |

The four tutorial reviews still supply useful methods: graph inspection and save/load; fixed comparisons and queue controls; image preparation/LoRAs; video handoff and finishing. Reuse those procedures without repeating the entire curriculum. See [Episode 2](TUTORIAL_02.md), [sampling/image edits](SAMPLING_AND_CONTROLS.md), and [reference/video methods](REFERENCE_DRIVEN_WORKFLOWS.md).

**First experiment: keep the performance, change the atmosphere.** This is the prepared experiment brief; no job is submitted.

1. Use the existing preferred guardian clip as the default available source, unless Ziggy selects another shot. Review its full motion and audio first; the previous visual review covered only a still. Select a continuous 4–8-second interval containing a clear gesture, retain its aspect ratio, and record time range, dimensions, frame count, FPS and hash. Split any multi-shot source at cuts before generation.
2. Make the first variation only a lighting/look change: the same encounter and composition in cool, overcast daylight, with believable skin, fur and fabric. Retain both subjects, their scale, positions, contact and camera movement. This proposed creative default isolates motion preservation before relocating the scene or replacing a character.
3. In the actual Cloud workspace, inspect the current official Union Control graph and its depth preprocessing. Resolve the exact model, encoder, VAEs, adapter and node versions against its model links and compatibility notes. Check source-video input and output handling, including every active subgraph. Save a separate working copy; leave original recovered graphs untouched. Keep 2.3 and 2.5 components separate unless the selected official recipe explicitly establishes compatibility.[^video-compat]
4. Prepare one modest-resolution take with the template's supported settings and a fixed seed; preserve source timing through documented resampling if the selected adapter requires another FPS. Record entered/effective prompt, resolved dimensions, control settings, estimated cost and exclusions. Keep optional finishing off, except refinement intrinsic to the chosen recipe. Use [SOP 7](#sop-7) for the bounded run and status/cost record once access and the experiment budget are established.
5. Compare source and candidate at the same timecodes and at normal speed. Check facial/animal anatomy, touch/contact, gesture timing, camera path, background stability, lighting and flicker. A pretty still with changed performance fails this test. Record specific defects before making one targeted revision. Keep source audio as a reference track; audition it and remux only if it fits the changed setting. Do not assume the selected video-control workflow carries it through.
6. After a take passes, make an HD review master and then one 4K delivery comparison. Keep both generation and finishing outputs and their recipes. A successful lighting test is followed by setting replacement, then character replacement if wanted; each changes one major constraint.

**Resolution and realism.** Proposed delivery targets are 1920 x 1080 and then 3840 x 2160 for landscape, or 1080 x 1920 and 2160 x 3840 for the guardian portrait. These are export targets, not claims about native model dimensions. A workflow may generate padded/model-aligned dimensions such as 1920 x 1088; choose and record a final crop or letterbox without stretching. Record source, first-stage, refined and exported dimensions separately. Keep the source's intended playback speed; changing an FPS field alone is not motion interpolation.

LTX's current shelf includes a Tiled Fusion V2V upscale workflow with FullHD/4K/8K options.[^video-ltx] That is a finishing candidate, not proof that our account runs it or that it restores true detail. Start with 4K only after the underlying performance works. Inspect skin, fur, hands, eyes, edges and temporal texture at full size. Reject an upscale that invents distracting detail or worsens flicker. HDR and higher frame rates are later, separate choices.

**What the eventual simple controls should show:** source clip and trim, what to preserve, what to change, optional character/look reference, preview quality and delivery size. The assistant selects the appropriate graph and explains that selection before loading it. The present table is a documented selector, not an implemented uploader or automatic router. [SOP 8](#sop-8) covers simplifying a graph after it has worked.

**Readiness and storage - October 3:** native Comfy tools now work. The two-reference still edit and Civitai-origin LoRA comparison have executed successfully; see the [run record](workflows/hon_dolo_reference_edit_v001.record.json). LTX/H3 video execution and new authenticated model imports remain untested. Keep model weights and execution in Cloud and necessary media on D:. C: was nearly full and caused intermittent local tool failures.

**Success for this milestone:** a playable source/result pair with the intended visual change and recognizable original motion, an inspected HD master plus optional accepted 4K derivative, measured media properties and actual cost, and retrievable source/input/workflow/output records. Our next practical step is current Cloud workflow/dependency discovery for this specific source-video task.

**Preserved September asset handbook**

The sections below retain the game-asset examples and dated connection history. The video direction above supersedes their earlier game-first priorities. The reusable SOPs still apply; acceptance now means acceptance for the selected media use.

Comfy helps develop the visual language and selected assets for **Water Before the Crossing**: a small place where restoring water changes what its residents have time to do. The first pump concept image is preserved. The [implemented game](../../../../games/observatory/README.md) supplies walking, repair interactions, and consequences using authored geometry; generated meshes remain a later experiment. The [chapter plan](../FIRST_PLAYABLE.md) defines the game scope.

This handbook combines researched procedures with an experiment system. Its recommendations are tailored to the existing Comfy Cloud subscription, the current HP Z210 workstation, and the Observatory's emphasis on curiosity and care. A procedure becomes proven here when its run record contains evidence from this environment.

**Storage rule:** keep model execution and bulk assets in the cloud; use D: for necessary local downloads. Git holds source, recipes, and asset records. The local game uses a small set of accepted derivatives. Follow the [storage policy](../STORAGE.md): the G: archive folder structure is confirmed online, streaming is enabled, and Drive confirms its cache at D:\appdata\Local\Google. Independent retrieval of the pump original remains pending.

**Provider update:** Ziggy saved a Civitai secret in Comfy; an authenticated import still needs validation. Public Civitai metadata research works. The [Hugging Face guide](HUGGING_FACE.md) covers additional model sources and token setup. The [Civitai procedure](CIVITAI.md) contains checked model candidates and the browser handoff agreement.

<a id="start"></a>

**Start here: what is established**

**Latest connection checkpoint ? October 3:** fresh browser authorization for the existing comfy-cloud connection succeeded. Live get_server_info and saved pump reads verified access; see the [connection proof](outputs/comfy_connection_20261003.proof.json). The older Story Workshop rejection below is historical. Initial empty CLI results came from the isolated sandbox profile, while the actual Windows profile had an OAuth refresh rejection. Renew in the real profile and verify live calls; a stored login alone is insufficient.

**Completed experiment:** the first pump concept completed through `run_template` with `image_z_image_turbo`. Job `cb835f1e-3b10-4972-860c-fb83fb0517c0` reached terminal completion; its [1024 × 1024 image](outputs/pump_concept_v001.png), [run record](workflows/pump_concept_v001.record.json), and [workflow files](workflows/README.md) are preserved. Ziggy accepted it as a starting direction and delegated background prop refinements; it is not an accepted game mesh. The usage report ended before the job, so actual cost is unknown.

The September 12, 2026 discovery checks returned authenticated OAuth, production version 0.57.0, and 41 tools. A later preflight failed with `invalid_grant: refresh token reuse detected`; the first browser callback timed out, then a fresh login succeeded and server information responded again without an IDE restart. This toolset has no live balance/status tool; its billing feed did not confirm the current balance. Ziggy's earlier screenshot remains the source for the Pro plan, 21,100 credits, and October 12 end date. These are local observations, recorded in the [learning record](LESSONS.md), separate from the documentation findings below.

Read [SOP 1](#sop-1) when restoring the connection, then [SOP 3](#sop-3) for the first image. Use [SOP 2](#sop-2) whenever a new GitHub recipe arrives. The [learning record](LESSONS.md) preserves corrections and experiment results between sessions. Future assistants should read this handbook and that record before choosing another workflow.

Our practical division of work is straightforward. Ziggy supplies creative direction and judges whether the place feels inviting and meaningful. The assistant researches dependencies, prepares inputs, operates available tools within the agreed task, inspects outputs, and records evidence. Cloud generation supplies candidate media. The implemented game supplies movement, mechanisms, resident behavior, and consequences. Ordinary background props are delegated to the assistant; reviews with Ziggy focus on the experience.

**When Ziggy's browser is needed:** the assistant prepares the model choice and exact import instructions, then gives a timely **Import needed** interruption for a concrete upcoming experiment. Include the link, destination folder, expected filename, Cloud download size, and purpose. Check existing model availability first; continue independent work while waiting; verify the imported entry and loader before dependent execution. Reuse it afterward. Ziggy explicitly accepts this division of work. Follow the [complete handoff procedure](CIVITAI.md#model-discovery-and-browser-handoff).

Comfy Cloud provides remote generation and browser access, so its model workloads do not require local model installation. The resulting assets still need to fit the device that renders the game. Cloud GPU specifications do not establish frame rate on the Z210.[^cloud]

<a id="graph"></a>

**Reading the graph**

A workflow connects operations through typed inputs and outputs. In a basic diffusion image graph, the model supplies generation behavior, the text encoder converts the prompt into conditioning, the sampler works on a latent representation, and the VAE decoder produces a visible image. A save node writes the result. Models can package these functions differently.[^basic]

| Term | Working meaning |
|---|---|
| Workflow | The recipe: operations, connections, and settings |
| Model | Learned parameters used by one or more operations |
| Custom node | An additional operation supplied by a package |
| Template | A starting workflow with an intended task and inputs |
| Seed | A recorded sampling input useful for controlled comparisons |
| Steps / sampler | Settings for the sampling process; follow the chosen model's recipe |
| Reference image | A concrete design constraint supplied to a compatible workflow |
| MCP | The connection through which this assistant can discover and invoke Comfy operations |

These distinctions prevent a common detour: a workflow collection is useful even when some dependencies are unavailable, while a preview extension cannot supply a missing generation model. More nodes are useful when they solve a specific production problem.

**Tutorial 2 applied.** Ziggy supplied a nodes/workflows transcript, including an SDXL recipe explicitly named Juggernaut X at 11:41. The [annotated tutorial notes](TUTORIAL_02.md) explain the transferable method and walk through our ten-node executed pump graph. The transcript identifies the model name, not its exact version ID or weights.

Read actual socket types: a standard KSampler accepts MODEL, CONDITIONING and LATENT inputs, plus settings. The latent representation is not the only kind of data entering it. Positive and negative prompt encoders can be the same node class; their destinations give them their roles. VAE decoding reconstructs pixels from a learned representation and should not be described as lossless file decompression.[^ksampler][^core-nodes]

Save Image writes in the execution environment, so a Cloud save does not automatically create a D: archive. Branch an IMAGE output when both saving and further processing are needed. Current upstream SaveImage also exposes IMAGE passthrough; the deployed Cloud schema must establish whether that socket is available. The tutorial's older no-output layout is not a universal rule.[^core-nodes]

**Why GitHub also says “workflow.”** In GitHub Actions, a workflow automates repository work such as publishing software. The NKD VFX Actions page lists 11 runs of one publishing workflow. Those entries are publication history. A ComfyUI workflow is the graph used to create or process media.[^vfx-actions]

| Where it appears | What to inspect | What it tells us |
|---|---|---|
| GitHub Actions, such as publish.yml | Automation definition and run history | How the developer publishes or checks the package |
| A Comfy recipe, usually a JSON graph or an image with graph metadata | Nodes, links, model/input dependencies, parameters | How a media-generation task is assembled |
| A package README and node documentation | Capabilities, schemas, requirements, examples | Which operations could help build a recipe |

A public repository link is normally enough to follow its readable files and related sources. Individual run logs, private resources, and some GitHub views may be inaccessible from the research tools. A screenshot or excerpt is useful when a specific page cannot be retrieved; copying every link is unnecessary. This review read the VFX Actions index directly, but retrieval of its individual run/workflow view failed. The supplied screenshot shows the publishing definition; detailed execution logs were not inspected.

<a id="resources"></a>

**The resource shelf**

For third-party models, Ziggy's preference is to shortlist by highest rated and/or most downloaded. New still-image model searches default to SDXL 1.0 and SafeTensor files; preserve the executed Z-Image recipe as a baseline. Compare rankings within the relevant task and compatible model family, then inspect versions and examples. The [Civitai procedure](CIVITAI.md) explains the filters, setup, and validation steps.

The following is an adoption order, not an installation list. Availability must be checked in the actual Cloud workspace. Sources were reviewed September 12, 2026; branch links remain mutable unless an immutable revision is recorded in an experiment.

Use official guides to understand a recipe, the live Cloud schema to establish available inputs, and the official core source to investigate implementation. Match upstream code to the deployed core version when that version is known. The observed MCP server version identifies the connector; it does not establish the ComfyUI core or frontend version. The core README describes those components' separate release paths.[^core]

| Resource | Why it belongs here | Current decision |
|---|---|---|
| ComfyUI official core repository | Upstream node implementations, graph execution, server code, and API examples.[^core] | Primary implementation reference when documentation needs clarification |
| Civitai and its official Comfy node package | Additional resources for asset experiments; see the [Civitai procedure](CIVITAI.md) | Public metadata discovery verified; provider key saved in Comfy; first authenticated import pending; civitai node search returned no matches |
| Comfy's official workflow templates | Searchable starting recipes and reusable subgraphs.[^templates] | First place to select a supported baseline |
| ComfyUI examples | Maintainer examples for learning image graphs and their variations.[^examples] | Study when a graph needs explanation |
| Z-Image-Turbo official guide | Provides a Cloud image workflow in the model family visible in Ziggy's screenshot.[^zimage] | First pump-image candidate |
| Qwen-Image-Edit-2511 official guide | Describes editing and material/design changes from image inputs.[^qwen] | Candidate after accepting a reference |
| Hunyuan3D 3.0 official partner guide | Describes image/text-to-mesh and related texture/topology workflows.[^hunyuan] | Candidate for the later static housing |
| NKD Preview Tools | Image and media review utilities.[^nkd] | Optional; not found in our exposed Cloud catalog on September 12 |
| NKD VFX Tools | Lighting, camera, perspective, and 3D placement controls.[^vfx] | Optional; not found in our exposed Cloud catalog on September 12 |
| ZHO workflow collection | Community examples spanning editing, generation, and 3D.[^zho] | Study and selectively adapt |
| Registry and ComfyUI-Manager | Package identification/version information and tools for managed installations.[^registry][^manager] | Dependency references; no local installation needed |
| VideoHelperSuite | Video loading, sequence assembly, and preview utilities.[^vhs] | Promoted to video support for the October pivot; verify the chosen runtime |
| Hunyuan3DWrapper | A separate custom-node route around Hunyuan3D-2, with additional environment dependencies.[^wrapper] | Defer; distinguish it from the 3.0 partner route |

**NKD Preview Tools: review of the first submitted link.** The pack documents floating image previews, references, video/audio timelines, video viewing, and frame extraction. Mask Painter has moved into the author's separate Basic Tools pack. Its software license is MIT. It provides no documented mesh inspection or 3D generation node.[^nkd]

For this project, its strongest potential use is comparing pump silhouettes and material changes. That is an adoption hypothesis. There is also a concrete documentation discrepancy: the popup guide describes an image output, while the inspected node source defines no output sockets. The target environment's actual schema must determine wiring; these mutable pages may reflect different versions.[^nkd-popup][^nkd-source]

The package metadata observed during review says version 3.10.5. That is neither an installed version nor a tested compatibility result. One open issue reports a crash with video input; it is an unverified report, not a reproduced defect here.[^nkd-package][^nkd-issue] Native previews and saved images are sufficient for the first comparison.

**ZHO workflows: review of the second submitted link.** This is a broad collection of recipes. Its README's newest dated changelog entry is December 20, 2024; that observation does not prove when every repository file last changed. The repository identifies GPL-3.0 as its license. The Sketch to 3D example lists a sketch tool, background removal, and TripoSR dependencies. The sequence is useful to study, but those dependencies need separate Cloud checks.[^zho]

Inspection of the FLUX.1 DEV JSON shows explicit model filenames and a grouped workflow node. A successful download therefore does not establish that this graph will execute in the current environment.[^zho-flux] Our first adoption should preserve a useful idea, such as isolating an object before reconstruction, in a currently supported recipe. Record the source and changed dependencies; do not label an adaptation as the original author's tested setup.

**NKD VFX Tools: the additional repository.** This is a separate package from Preview Tools. Its README describes lighting, lens, perspective, and 3D placement operations and says example workflows are still being prepared.[^vfx] Preview 3D accepts GLB/GLTF and other supported 3D inputs, with image, mask, depth, and camera-related outputs.[^vfx-3d] A possible later use is placing an accepted pump mesh into a courtyard reference to guide composition. That would be a shot-design experiment; engine behavior and performance still require their own tests.

The latest run listed on the inspected Actions index is version 1.7.4 at commit f9e8cdad8941fde6356b33edc4c15bca9f407eb1.[^vfx-actions] This identifies that publishing run, not an installed package in our Cloud account. Check the actual node inventory before adopting this route.

Comfy Cloud currently supplies a maintained set of preinstalled custom nodes and does not support directly installing arbitrary packages. The Nodes sidebar is the place to check. A listing on another service that calls itself “ComfyUI Cloud” is not evidence of availability on cloud.comfy.org.[^cloud-nodes]

<a id="sop-1"></a>

**SOP 1 — Establish the working connection**

Use this when beginning a production session or recovering an absent connection. The output is a short evidence entry stating which account and operations are available.

1. Read the [connection README](README.md) and latest learning record. Reuse the configured connection. The recorded successful OAuth setup is not a reason to register a second server.
2. Inspect this session's tool inventory. If Comfy is absent, record that limitation and reload the client connection. Continue briefing, research, or workflow inspection while access is being restored. Do not describe documentation examples as executed tool calls.
3. Once exposed, use the documented server-information and billing checks. Search templates and inspect the selected template's schema and prompting guide. Use model/node discovery where dependencies need resolving.[^mcp]
4. Record the check time, available template/model identifiers, and any uncertainty. An account screenshot can inform the record, but live results determine the next operational step.
5. Hand off to a specific experiment: one image, one input edit, or one mesh. Keep its intended output visible before submitting it.

The useful evidence states are **researched**, **available in this account**, **executed here**, and **accepted for game use**. Advancing one state does not imply the others. An imported workflow can still fail during execution.[^execution]

In the observed version 0.57.0 toolset, billing access is through get_billing_activity and get_usage_report; get_billing_status is absent. A successful billing-history call does not establish the current credit balance. Use the actual exposed tools and the account UI for information they do not return.

If tools are exposed but a call fails with an OAuth refresh rejection, recover authentication before submitting a job. Our September 12 preflight reported `invalid_grant: refresh token reuse detected`; its cause was not established. Use `codex mcp login comfy-cloud` to start fresh browser authorization for the existing server. Do not register another server or copy tokens into a workflow. Once login completes, verify a read-only server-information call; if the running IDE connection still rejects authentication, reload its connection and recheck. Record this as a preflight failure, separate from any generation job. A submission timeout is different: reconcile job status before attempting another submission.

**Completion:** actual tools respond and the selected task has supported inputs. If tools remain absent, connection discovery is still pending; the rest of this handbook remains usable for preparation.

<a id="sop-2"></a>

**SOP 2 — Inspect, adapt and reuse a community workflow**

Use this before adding a community workflow to the production shelf. The output is an adoption decision with a source, dependency inventory and one controlled experiment. Copy the [workflow intake sheet](templates/workflow_intake.md); use the [tutorial read-through](TUTORIAL_02.md) as a worked example. This applies to GitHub recipes and workflows recovered from shared media.

1. Identify the object: workflow JSON, custom-node package, model, tutorial, or connector. State which chapter asset or review problem it helps.
2. Read the author's README and the relevant workflow/source files. Record the URL, observed date, and revision when obtainable. If a commit cannot be verified, say so rather than inventing a pin.
3. List required node classes, model identifiers, input files, and any service calls. Inspect grouped/subgraph dependencies as well as the visible canvas. Mark whether cost comes from Cloud GPU activity, a partner service, or both.
4. Name the target environment: managed Comfy Cloud, local installation, or a separately managed Runpod Pod. For Cloud, discover the required nodes and models through its catalog. A Runpod connection alone does not provide a Comfy installation. Preserve the original file before adapting names or connections; follow the selected host's installation procedure.[^cloud-nodes]
5. Record repository attribution and the model/asset terms linked by the provider. A repository's software-license label alone does not document the terms of every model or asset used by a workflow. Preserve the applicable source links for later release review.
6. Choose **adopt a small test**, **adapt the idea**, **defer**, or **decline**, with a concrete reason. Unknown Cloud availability means “pending discovery.”

**From an adopted idea to an executable working copy:**

1. Obtain the actual graph, not just its screenshot or attractive output. Open editor JSON through File → Open or drag/drop. A supported original image may carry workflow metadata, but a screenshot, recompressed copy or downloaded clip may not. If only a prompt and model list survive, record a reconstruction rather than claiming the author's exact recipe.[^import][^format]
2. Export/preserve the original before editing. Trace loaders, preparation, sampler/processing, decoder and every output branch. Inspect subgraphs and bypassed sections; record external service calls and output destinations. Identify a node by its class and schema, not its user-editable title or socket color.
3. Match model family, text encoder, VAE, LoRAs and latent nodes. Use the specific release's dimensions and recommended settings. A filename substitution does not establish compatibility. On Comfy Cloud, check existing resources first; invoke the agreed browser-import handoff only for a genuinely missing supported model. There, a missing custom node requires an available substitute or a different supported recipe; a local Manager installation does not change the Cloud catalog.[^cloud-nodes]
4. Prepare one baseline execution within the existing task/budget. Use one queue submission, the smallest supported output batch, and disable automatic queuing for this first comparison. For a simple still-image recipe, that normally means batch size one; preserve required frame/view counts in video or multiview graphs. Use a fixed seed/control and retain the author's other resolved settings where supported. Record any required batch, dependency or setting change as an adaptation rather than an exact reproduction.
5. Inspect validation errors before submitting. Fix the named missing input, model or node rather than randomly changing parameters. Use a single informative job and record its ID/output/cost through SOP 7. Unchanged graph branches may be cached; quick completion alone does not prove new sampling.[^execution-cache]
6. Preserve the baseline result. Change one relevant factor, rerun within scope, compare and record whether it improved the intended asset. Keep seed, input media, dimensions, model versions and all sampling settings in the run record; a fixed seed alone cannot guarantee identical results across runtimes.[^determinism]
7. Organize the working graph into labeled stages with notes, reroutes and groups, then consider App mode after it is useful. Preserve editor JSON for maintenance and API JSON where execution requires it. Reuse the tested recipe and dependencies for subsequent assets, rather than asking Ziggy to repeat model imports.[^import][^format]

Prefer a simple official workflow when it can answer the same experiment question. Add an extension when there is evidence of a specific benefit: a comparison view, a needed input operation, or an output format. Popularity alone does not establish compatibility or asset quality.

**Completion:** another person can explain why this resource belongs in the project and what remains unverified. Record the decision in [LESSONS.md](LESSONS.md). No blanket cloning or local environment changes are required for this evaluation.

**Current visual use:** the proposed [character showcase](../CHARACTER_SHOWCASE.md) and Ziggy's Favorite_1 references focus our selection. A cinematic image/video workflow can establish appearance and atmosphere. A playable character additionally needs a usable mesh, materials and any animation; a successful clip does not prove that asset exists.

**Recovered example:** the [Giant Fantasy intake](references/civitai_142373294.intake.md) demonstrates this SOP on an actual browser-saved MP4. Its editor graph and 72-node execution graph survived in metadata and are preserved with hashes. Dependencies and disabled branches still need Cloud validation; extracting a recipe is separate from executing it.

**Settings and branch comparisons:** follow the compact [sampling procedure](SAMPLING_AND_CONTROLS.md). Count active output branches as well as submissions and samples, retain required video frames, and record which stages share primitive controls. Hidden widgets remain active; bypass can leave required connections invalid. Export and inspect the resulting graph before a controlled comparison. Disabling automatic submission does not establish that pending/running jobs were canceled.

**Video previews and prompt rewriting:** the [reference-driven workflow note](REFERENCE_DRIVEN_WORKFLOWS.md) adds typed subgraph outputs, matching frame rate/audio, persistent output and metadata checks. Preserve the original save branch until its replacement is verified. Record the effective prompt after any enhancement, especially when dialogue must remain exact; use a supported toggle before attempting a bypass. Preview extensions and upscalers are optional dependencies, selected for a specific need.

<a id="sop-3"></a>

**SOP 3 — Produce the first pump concept**

Use the [asset brief](pump_brief.json) and [prepared prompt](pump_concept_prompt.txt). The deliverable is one saved reference image plus its workflow and run record. It is an art-direction experiment, before any mesh generation.

The pump should communicate practical care: an accessible service panel, a replaced fitting, paint preserved where possible, and a stable stone base. Its form should suggest that residents maintain something useful. An ornate monument would serve a different scene purpose. This interpretation comes from the chapter's design, rather than a provider's model recommendation.

1. Start with a supported image template. Z-Image-Turbo is the first candidate; its official guide supplies a Cloud workflow. Preserve its model-specific defaults for the first run and inspect the live inputs. Do not transplant sampler settings from an unrelated model tutorial.[^zimage]
2. Duplicate/name the working recipe for the Observatory pump. Replace the demonstration subject with our prepared prompt. Use one isolated object on a plain background, with the whole housing in frame. Leave model and workflow identifiers unknown in the record until actually selected.
3. Set one output and record the chosen dimensions, seed, prompt, and resolved settings. A square 1024-pixel image is our starting composition suggestion if supported by that template. Record the actual settings rather than assuming the screenshot's values remain selected.
4. Apply [SOP 7's cost check](#sop-7), then submit once through the available interface and retain the returned job identifier immediately. Observe that job through completion. A missing preview or interrupted client connection calls for checking the existing job before another submission.
5. Download the result and inspect it at full view and at a small on-screen size. Is the silhouette recognizable? Can the player find the service area? Are fittings coherent? Does the image convey use and maintenance without distracting scenery?
6. Mark **keep**, **revise**, or **reject** with one sentence. If revising, identify the main defect and one change to test. Preserve the unsuccessful result when it explains a decision.

The first run's value is partly operational: can we follow the recipe, retrieve its output, explain its cost, and reconstruct its inputs? A pleasing image without its recipe is an incomplete experiment.

**First observed result:** the downloaded PNG confirms the exact prepared prompt, seed 42, eight steps, CFG 1, `res_multistep` sampler, `simple` scheduler, denoise 1, shift 3, and batch size 1. The general prompting guide suggested `euler`; we retained the selected template's actual `res_multistep` setting. The lake-green, brass, and stone palette, service panel, and silhouette read clearly. The housing is too pristine and tall/slender for the brief; its repair patch and replaced coupling are not obvious, and the lever socket is ambiguous. Review the concept with Ziggy before selecting a focused revision. No mesh or engine acceptance follows from this image.

**Completion:** one output opens locally, its source/settings are recorded, and a design decision is attached. Image quality is still a judgement to make from the actual result.

<a id="sop-4"></a>

**SOP 4 — Refine a design through controlled edits**

Begin with a reference accepted under SOP 3. Preserve it unchanged and link its record into the next experiment.

1. State the change in ordinary language: “replace the corroded coupling with a practical brass repair” or “reduce the decorative ridges while retaining the service panel.” Specify the features that should stay recognizable.
2. Choose an available editing template. Qwen-Image-Edit-2511 is a candidate because its official guide covers image editing and material/design work.[^qwen] Confirm the actual input count and image handling before wiring it.
3. Make one substantive change. Keep camera, palette, and proportions stable where the task permits. Record the reference file's hash, prompt, and settings.
4. Compare the edit with its parent. Inspect both the requested change and collateral changes: a moved pipe, altered panel, invented text, or changed proportions can matter more than attractive texture.
5. Keep the variant only if it serves the chapter. Record its relationship to the parent, then name the next question.

For different views, seek evidence that they describe the same object. Separately generated front and rear pictures can disagree; a plausible pair of images is not a geometry check. Inspect panel positions, footing, pipe connections, and dimensions before treating views as reconstruction inputs.

Start with native side-by-side image viewing. NKD becomes useful if it is available and a small test confirms its comparison behavior. A video timeline adds little to a two-image material decision.

For world appearance, the [one-view procedure](REFERENCE_DRIVEN_WORKFLOWS.md#first-use-render-our-world-then-explore-its-appearance) uses an actual Godot render as layout reference and a separate image for style. Compare camera, paths and major forms, then carry the useful material, asset or lighting decision into Godot. Review the base result before optional upscaling. An edited still is visual direction; the changed game scene needs its own viewing and performance check.

**Classic image-to-image:** the [Episode 4 production notes](SAMPLING_AND_CONTROLS.md#image-to-image-and-loras) cover `Load Image → Resize → VAE Encode → KSampler → VAE Decode → Save Image`, with the required model/conditioning and compatible VAE connections. Preserve the prepared input's dimensions, aspect/crop choices and hash. Compare denoise values from that same parent and fixed settings; feeding each output into the next run is a separate sequence of edits. Lower denoise generally preserves more of the starting image, but cannot guarantee unchanged layout.[^img2img]

**LoRA comparison:** first establish the image-to-image baseline, then compare a compatible adapter off/on while preserving the prompt, seed and denoise. In the standard loader, route its MODEL to the sampler and CLIP to both prompt encoders; record both model and CLIP strengths. Keep any required trigger phrase unchanged between comparison runs. Applying a downloaded LoRA uses learned adjustments; it is not training a new model. Verify the selected loader and family, and use our Cloud import procedure only for a missing supported dependency.[^lora]

**Completion:** the revision has an explicit improvement and an accepted relationship to the reference. A “care state” visual should convey a specific condition, such as a replaced coupling, without implying a character's virtue from weathering alone.

<a id="sop-5"></a>

**SOP 5 — Convert one reference into a usable static prop**

Begin after accepting the pump's form. The deliverable is a reviewed static housing and an engine test record, with moving parts and behavior handled in the game project.

Hunyuan3D 3.0's documented partner workflows include image-based generation, optional multiple views, texturing, UV work, parts decomposition, and topology processing. These are candidate capabilities to discover and price; the guide's existence is not evidence that our output will meet a game's asset needs.[^hunyuan]

1. Choose a supported image-to-3D workflow and inspect its output options. Start from the accepted isolated reference. Supply additional views only if their geometry is consistent and the selected workflow supports them.
2. Keep this experiment to the exterior housing. Leave the moving lever, collision, water effects, and repair logic as separately authored components. Evaluate whether generated panel and mounting details leave room for them.
3. Save the original output before cleanup. Inspect the full object from front, sides, rear, and below. Look for floating pieces, holes, merged fittings, inaccessible openings, inverted surfaces, and a distorted base.
4. Record mesh counts, material slots, texture sizes, orientation, scale, and missing components where the inspection tool exposes them. Use measured findings to choose cleanup. Do not use a provider's “game ready” description as an acceptance result.
5. Prepare an engine copy. For the planned Godot evaluation, glTF 2.0 / GLB is a suitable interchange target; Godot explicitly recommends glTF and supports binary GLB.[^godot] Confirm which format the selected generator actually exports.
6. Place it beside a simple scale reference in the target scene. Test collision and interaction separately, and measure frame time on the intended PC. The [chapter plan](../FIRST_PLAYABLE.md) proposes an initial 720p/30-fps target; no result has established it yet.

If cleanup costs more effort than a simple authored housing, keep the generated image as reference and build modest geometry from it. That is a valid experiment outcome. The first prop should help establish a repeatable art pipeline while keeping the chapter achievable.

**Completion:** the asset is visibly acceptable from relevant viewpoints, imports with its materials, and has observed performance in the intended scene. A downloadable mesh alone completes the generation stage only.

<a id="sop-6"></a>

**SOP 6 — Preserve the work and reproduce an experiment**

Use the [run record template](templates/run_record.json). It is a project record, not an executable Comfy workflow or an enforced spending control. Duplicate it for each actual experiment and replace unknown values with observations when they become available.

Comfy's Save/Save As keeps work in its account/workspace. Export produces a local file; import supports drag-and-drop or the Comfy icon's File → Open action. Moving a JSON between environments does not supply its missing models or nodes.[^import]

1. Preserve the editor workflow under workflows/ with a descriptive versioned filename. Where automation uses a different representation, retain its exact execution JSON too. Editor JSON preserves canvas layout; API JSON focuses on executable inputs/connections and omits layout.[^format]
2. Record the source revision or retrieval date, template and model identifiers, input files, entered/effective prompts, seed, dimensions, and other resolved parameters. For video, include frame counts, generation/output FPS, audio handling and observed duration. Record upscale derivatives against their parent output. Use `inputs.resolved_parameters` and `outputs` in the existing record template. Save hashes for files we possess. Unknown remote revisions should remain explicit unknowns.
3. Record the job ID before waiting. On completion, associate every output with that run. Download assets promptly; hosted MCP output URLs expire, and some submitted workflows' outputs may lack embedded workflow metadata.[^mcp]
4. Keep bulk originals in cloud storage, with a verified persistent archive for accepted results. Download only necessary references and derivatives to outputs/ on D:, separate from edited game assets. Record stable remote identifiers, sizes, hashes, and retrieval evidence; ignore rules and temporary links do not provide backup. Follow the [storage policy](../STORAGE.md).
5. Keep credentials and transient signed URLs out of retained records. Preserve the nonsecret execution inputs exactly, with original attribution and source links. Review private input data before sharing; clearly identify any redacted shareable version.
6. To reproduce, reopen the saved editor file or use the saved execution recipe with its required dependencies. Check resolved settings before running. Compare the new result and record differences; a fixed seed alone is not a cross-version reproducibility guarantee.

**Observed archive path:** `pump_concept_v001.png` contained both `workflow` (editor JSON) and `prompt` (API JSON) metadata. These were extracted directly into the corresponding files under workflows/, without manual graph conversion, and checked against the intended settings. The embedded editor graph exactly matches apply_slots output. The original template editor graph is retained separately. Inspect each future output for metadata; this result does not guarantee that other PNGs or download paths preserve it.

The same editor recipe is saved privately in Cloud as **Observatory - Pump Concept v001** (`observatory-pump-concept-v001.json`), without overwriting another recipe or publishing a shared snapshot. Refresh Cloud's Workflows sidebar to find it. Its saved seed control remains randomize: the recorded job used seed 42, but a controlled UI rerun requires setting 42 again or selecting a fixed seed control.

**Completion:** a future session can locate the recipe, original inputs, outputs, decision, and remaining uncertainty. It should not have to infer a workflow from a screenshot.

<a id="sop-7"></a>

**SOP 7 — Observe cost and recover from failures**

Comfy currently documents Cloud GPU usage at 0.266 credits per active GPU second and a conversion of 211 credits per US dollar. Partner Nodes consume the same balance at model/parameter-dependent rates. For scale, 60 active GPU seconds would be about 15.96 credits at that rate; that is not a quote for a particular image or partner job. Recheck pricing when choosing the actual recipe.[^credits]

The live estimate for image_z_image_turbo returned zero paid-API-node credits while explicitly excluding GPU runtime and other costs. Its total run cost remains unknown. Preserve that distinction when reporting estimates.

1. Record the live balance and the intended output count. Capture an estimate if the selected interface supplies one; otherwise label the cost unknown and use the smallest informative calibration task within the agreed scope.
2. Begin calibration with one job at a time. Record reported usage as well as before/after balance. Concurrent activity or reporting delay can make a balance difference an unreliable measure of a single job.[^credits]
3. If the client loses contact, look up the existing job. A timeout in our client does not establish that the remote job failed. The documented MCP job operations include status, waiting, output retrieval, and cancellation; use the available schema.[^mcp] If the selected job should be stopped, request its cancellation, then verify its terminal status and observed usage. Cancellation does not establish that no credits were used.
4. If execution fails, record the failing node, message, and approximate time. Check missing nodes/models, incompatible inputs, and environment assumptions before changing settings. Separate configuration failures from dissatisfaction with an otherwise successful image.[^execution]
5. Inspect usage before retrying. Failed or partially executed generations can still consume credits.[^charges] Make a concrete repair to the recipe or mark the failure unresolved. Avoid automatic repetition of an unchanged failure.
6. Record the decision and any remaining partial outputs. A project spending target is an operating agreement; do not describe it as a server-enforced ceiling unless the actual interface provides that guarantee.

The subscription month gives us a practical review point. Monthly credits do not roll over, while purchased top-ups have a different expiry policy.[^expiry] Preserve accepted assets and recipes as we work, and use remaining time to finish useful experiments rather than enlarging the asset list merely to consume credits.

**Completion:** the result or failure has a cost observation and an evidence-based next action. A run record can be complete even when a candidate is rejected.

<a id="sop-8"></a>

**SOP 8 — Make a proven workflow comfortable to use**

Once a recipe produces repeatable useful results, evaluate Comfy's App mode. Its builder lets a workflow expose selected inputs and outputs through a simpler interface. The documented sequence is choose inputs, choose outputs, preview, and set the default view.[^app]

For our pump recipe, expose the subject description and any supported reference/material controls that have proved useful. Keep technical settings at the tested defaults unless changing them serves an experiment. Show the image output and preserve the underlying graph for maintenance.

Save the workflow, reopen it, and check that the simplified controls resolve to the expected graph values before running a small verification. Saving an App view is a usability milestone. It does not add game behavior or prove that the generation result belongs in the chapter.

**Completion:** Ziggy can find the relevant creative controls and recognize the result, while the full recipe remains recoverable. App mode is documented capability; no Observatory App has been created or tested yet.

<a id="learning"></a>

**How the project accumulates expertise**

The useful learning loop is **a question → a small experiment → an observed result → a changed procedure**. Research supplies candidates. A run supplies evidence. The handbook retains the procedure, and the learning record retains why it changed. This is how future sessions can build on prior work.

**Learning with Pathfinder.** Ziggy shares resources with PanHandlers Nova as well. Consult its fuller lessons before duplicating general tutorial material here. Our [shared-methods map](../pathfinder_handoff/README.md#shared-methods-and-local-independence) identifies the workflow lab, save/load practice and Cloud checklist, with local fallbacks for each. CFA retains the concise operating steps, exact recipes, environment-specific decisions, recovery instructions and evidence needed to continue if Pathfinder is unavailable. Record the source/date and any adaptation; return reusable production findings through the existing handoff. Neither this handbook's build nor the game requires the other checkout.

Each note should include the claim, evidence status, source/run, consequence for our next action, and what would invalidate it. “This model is good” is too broad. “This isolated pump design imported with two materials; its rear pipe needed rebuilding” provides a reusable lesson once actually observed. That sentence is an example of the intended detail, not a result achieved here.

| When | Update |
|---|---|
| A new repository is proposed | Identify its purpose, dependencies, and adoption decision |
| A workflow is discovered | Record actual availability and schema |
| An experiment finishes | Complete its outputs, usage, and design review |
| A failure is resolved | Preserve the failing condition and the successful correction |
| A model/node version changes | Mark affected recipes for a targeted recheck |
| A work session ends | Leave a short next action and unresolved questions in the learning record |

Our first asset sequence is one image, one deliberate edit, one static mesh, and one engine import/performance check. The game project's first movement-and-interaction scene can proceed independently with placeholder geometry. The [project map](../README.md) places the proposed engine project at games/observatory/ relative to the CFA root; accepted media will feed its assets/ directory. Advance according to evidence rather than a promise to use every available model. Video, sound, style training, and additional node packs can earn a place when the first chapter needs them.

The prototype succeeds when a visitor can understand the water problem, choose how to engage with it, and see the residents' changed circumstances. Generated assets support that experience. They do not replace its design.

<a id="sources"></a>

**Sources and review boundaries**

Primary documentation and author repositories were reviewed September 12, 2026. Many pages are continuously maintained and have no fixed publication date. The ZHO date above is its README changelog date; Preview Tools' version is observed package metadata. No immutable commit was verified for Preview Tools or ZHO. The VFX Actions index identifies the specific publishing revision recorded above, but its detailed run logs were not retrieved. The initial source review installed no third-party code and submitted no generation. The subsequent pump-image run validates connection recovery, one native template execution, local output retrieval, and metadata archiving; editing, 3D generation, engine import, and actual cost reporting remain unverified.

[^cloud]: Comfy Org, [Comfy Cloud overview](https://docs.comfy.org/get_started/cloud), continuously maintained; accessed September 12, 2026. Remote generation and browser output handling.
[^basic]: Comfy Org, [Text to Image Workflow](https://docs.comfy.org/tutorials/basic/text-to-image), accessed September 12, 2026. Introductory diffusion graph operations; its SD1.5 recipe is not a settings prescription for every model.
[^core]: Comfy Org, [ComfyUI core repository](https://github.com/Comfy-Org/ComfyUI), master branch/README reviewed September 12, 2026. Core source, API examples, and component release boundaries; consulted as a reference without installation.
[^templates]: Comfy Org, [workflow_templates](https://github.com/Comfy-Org/workflow_templates), main branch reviewed September 12, 2026. Official template repository. [Browsable templates](https://comfy.org/workflows/).
[^examples]: comfyanonymous, [ComfyUI_examples](https://github.com/comfyanonymous/ComfyUI_examples), accessed September 12, 2026. [Readable examples](https://comfyanonymous.github.io/ComfyUI_examples/).
[^zimage]: Comfy Org, [Z-Image-Turbo workflow](https://docs.comfy.org/tutorials/image/z-image/z-image-turbo), accessed September 12, 2026. Cloud workflow and model-specific setup; advertised timing is not an account benchmark.
[^qwen]: Comfy Org, [Qwen-Image-Edit-2511](https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit-2511), accessed September 12, 2026. Editing and industrial-design/material use cases.
[^hunyuan]: Comfy Org, [Hunyuan3D 3.0 partner workflows](https://docs.comfy.org/tutorials/partner-nodes/hunyuan3d/hunyuan3d-3-0), accessed September 12, 2026. Generation, views, textures, and topology options.
[^nkd]: Nekodificador, [ComfyUI-NKD-Preview-Tools](https://github.com/Nekodificador/ComfyUI-NKD-Preview-Tools), main branch reviewed September 12, 2026. Node inventory and Mask Painter relocation; [MIT license](https://github.com/Nekodificador/ComfyUI-NKD-Preview-Tools/blob/main/LICENSE.txt).
[^nkd-popup]: Nekodificador, [Popup Preview documentation](https://github.com/Nekodificador/ComfyUI-NKD-Preview-Tools/blob/main/docs/popup-preview.md), accessed September 12, 2026. Documented preview behavior; compare with actual node schema.
[^nkd-source]: Nekodificador, [nodes.py](https://github.com/Nekodificador/ComfyUI-NKD-Preview-Tools/blob/main/nodes.py), accessed September 12, 2026. Inspected output definition differs from popup documentation.
[^nkd-package]: Nekodificador, [pyproject.toml](https://github.com/Nekodificador/ComfyUI-NKD-Preview-Tools/blob/main/pyproject.toml), accessed September 12, 2026. Observed version 3.10.5, not an installed version.
[^nkd-issue]: ComfyUI-NKD-Preview-Tools, [Issue 4](https://github.com/Nekodificador/ComfyUI-NKD-Preview-Tools/issues/4), opened August 10, 2026; accessed September 12, 2026. User-reported video crash, not independently reproduced.
[^zho]: ZHO-ZHO-ZHO, [ComfyUI-Workflows-ZHO](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Workflows-ZHO), reviewed September 12, 2026. README changelog latest dated entry December 20, 2024; workflow dependencies and repository license label.
[^zho-flux]: ZHO-ZHO-ZHO, [FLUX.1 DEV 1.0 workflow JSON](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Workflows-ZHO/blob/main/FLUX.1%20DEV%201.0%E3%80%90Zho%E3%80%91.json), main branch inspected September 12, 2026. Explicit model filenames and grouped workflow node.
[^registry]: Comfy Org, [Registry overview](https://docs.comfy.org/registry/overview), accessed September 12, 2026. Package discovery and version information.
[^manager]: Comfy Org, [ComfyUI-Manager](https://github.com/Comfy-Org/ComfyUI-Manager), accessed September 12, 2026. Installation/environment-management tooling; separate from Cloud package availability.
[^vhs]: Kosinkadink, [ComfyUI-VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite), accessed September 12, 2026. Optional video operations.
[^wrapper]: kijai, [ComfyUI-Hunyuan3DWrapper](https://github.com/kijai/ComfyUI-Hunyuan3DWrapper), accessed September 12, 2026. Hunyuan3D-2 integration and additional dependencies.
[^cloud-nodes]: Comfy Org, [Custom nodes on Cloud](https://support.comfy.org/articles/6791455062-custom-nodes-on-cloud), accessed September 12, 2026. Preinstalled selection and current installation limits.
[^mcp]: Comfy Org, [Comfy Cloud MCP](https://docs.comfy.org/agent-tools/mcp), public-beta documentation accessed September 12, 2026. Discovery, schemas, jobs, expiring downloads, and output-metadata limitations. Tool names are documented, not invoked in this review.
[^execution]: Comfy Org, [Workflow execution issues](https://support.comfy.org/articles/8229866129-workflow-execution-issues), accessed September 12, 2026. Missing dependencies and environment/configuration diagnosis.
[^godot]: Godot Engine, [Available 3D formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html), stable documentation accessed September 12, 2026. Recommended glTF interchange and GLB support.
[^import]: Comfy Org, [Import & export workflows](https://support.comfy.org/articles/2229074405-import-export-workflows), accessed September 12, 2026. Save versus export and portability limitations.
[^format]: Comfy Org, [Workflow API format](https://docs.comfy.org/development/api-development/workflow-api-format), accessed September 12, 2026. Editor and execution representations. Exact menu wording varies between current official pages; use the matching export action in the installed UI.
[^credits]: Comfy Org, [How credits work in Comfy](https://support.comfy.org/articles/5846341390-how-credits-work-in-comfy), accessed September 12, 2026. Published GPU rate, conversion, shared balance, and reporting delays. Rates require a fresh check for production runs.
[^charges]: Comfy Org, [Unexpected credit usage and charges](https://support.comfy.org/articles/1116676382-unexpected-credit-usage-charges), accessed September 12, 2026. Partial/failed runs can incur usage.
[^expiry]: Comfy Org, [Credit expiry: monthly vs top-up](https://support.comfy.org/articles/5040699374-credit-expiry-monthly-vs-top-up), accessed September 12, 2026. Monthly credits do not roll over.
[^app]: Comfy Org, [App mode guide](https://docs.comfy.org/interface/app-mode), accessed September 12, 2026. Configurable inputs/outputs, preview, default view, and saving.
[^vfx-actions]: Nekodificador, [VFX Tools Actions index](https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools/actions), accessed September 12, 2026. Eleven runs of the publishing workflow. Individual run details were supplied as conversation screenshots; direct retrieval of those views failed.
[^vfx]: Nekodificador, [ComfyUI-NKD-VFX-Tools](https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools), master branch reviewed September 12, 2026. Art-direction operations and example-workflow status.
[^vfx-3d]: Nekodificador, [Preview 3D documentation](https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools/blob/master/docs/preview-3d.md), accessed September 12, 2026. Supported inputs and preview/control-map outputs; no Cloud compatibility test performed.
[^ksampler]: Comfy Org, [KSampler](https://docs.comfy.org/built-in-nodes/sampling/ksampler), accessed September 12, 2026. MODEL, CONDITIONING and LATENT input roles and seeded noise preparation.
[^core-nodes]: Comfy Org, [current core nodes.py](https://github.com/Comfy-Org/ComfyUI/blob/master/nodes.py), master branch reviewed September 12, 2026. Empty latent, VAE and SaveImage implementations; SaveImage currently returns IMAGE. This is not a verified Cloud revision.
[^execution-cache]: Comfy Org, [server execution overview](https://docs.comfy.org/custom-nodes/backend/server_overview), accessed September 12, 2026. Graph execution and caching.
[^determinism]: Comfy Org, [CLI arguments](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/cli_args.py), master branch reviewed September 12, 2026. Deterministic mode explicitly does not guarantee determinism in all cases.
[^img2img]: Comfy Org, [Image-to-image workflow](https://docs.comfy.org/tutorials/basic/image-to-image), accessed September 12, 2026. Reference input and denoise; the page's SD1.5 example is not our selected SDXL recipe.
[^lora]: Comfy Org, [LoRA workflow](https://docs.comfy.org/tutorials/basic/lora), accessed September 12, 2026. MODEL/CLIP application and strengths; see current core implementation for zero-strength bypass behavior.
[^video-ltx]: Lightricks, [LTX-2.5 workflow shelf](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/2.5/README.md), reviewed October 2, 2026. Union Control, inpaint, generation and tiled finishing are separate recipes. Mutable upstream examples; not account tests.
[^video-wan]: Comfy Org, [Wan Animate 2](https://docs.comfy.org/tutorials/video/wan/wan-animate-2), reviewed October 2, 2026. Reference image plus driving video with a newly generated background and camera controls; not the same model as Wan2.2 Animate.
[^video-wan-mix]: Comfy Org, [Wan2.2 Animate](https://docs.comfy.org/tutorials/video/wan/wan2-2-animate), reviewed October 2, 2026. Mix and Move have different inputs and purposes.
[^video-vace]: Comfy Org, [Wan2.1 VACE](https://docs.comfy.org/tutorials/video/wan/vace), reviewed October 2, 2026. Control video and masked edits; a new fallback reference for this audit, not an existing executed recipe. The page flags ongoing template/documentation changes.
[^video-dubit]: Lightricks, [Dub-It beta](https://docs.ltx.io/open-source-model/feature-guides/audio/dub-it-beta), reviewed October 2, 2026. Validated on LTX-2.3; LTX-2.5 support remains in development.
[^video-compat]: Lightricks, [Workflow & Asset Compatibility](https://docs.ltx.io/open-source-model/reference/workflow-asset-compatibility), reviewed October 2, 2026. Match exact workflows and adapter cards instead of substituting model generations.
[^video-cloud]: Comfy Org, [Custom nodes on Cloud](https://support.comfy.org/articles/6791455062-custom-nodes-on-cloud), rechecked October 2, 2026. Current managed-node restriction; account inventory not inspected.
