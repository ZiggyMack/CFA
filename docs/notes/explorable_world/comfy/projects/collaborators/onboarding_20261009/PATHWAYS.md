# Our creative pathways

Prepared by CFA Codex Nova · October 9, 2026. Official documentation reviewed; this note does not claim new installations, account access, executed benchmarks or accepted results.

Welcome to the workshop. We are documenting the whole route from a creative intention to a reproducible result. **ComfyUI is our current production route; Pathfinder/Panhandlers turns what we learn into reusable guidance.** Other interfaces deserve the same careful treatment as we expand.

## What each name means

| Name | Kind | Where it fits |
| --- | --- | --- |
| **AUTOMATIC1111 / Stable Diffusion WebUI** | Generation application and interface | A Gradio web interface with text-to-image, image-to-image, inpainting and extensions. It operates compatible models. [Official repository](https://github.com/AUTOMATIC1111/stable-diffusion-webui) |
| **Forge UI** | Generation application built on WebUI | A related interface with changes to resource management, inference and experimental features. Exact model and extension compatibility depends on its version. [Official repository](https://github.com/lllyasviel/stable-diffusion-webui-forge) |
| **Invoke / InvokeAI** | Creative application | Combines an image canvas with a workflow editor. Its canvas can run suitably configured node workflows and stage their results for review. [Official repository](https://github.com/invoke-ai/InvokeAI), [canvas/workflow documentation](https://invoke.ai/features/canvas/run-workflow/) |
| **ComfyUI** | Workflow interface and execution engine | Connects nodes into reusable generation and editing graphs. Supports local execution and a Cloud route; partner nodes can access hosted models. Our exact Cloud graphs and records stay in CFA. [Official repository](https://github.com/Comfy-Org/ComfyUI) |
| **Seedance** | ByteDance video-model family | A generation engine that can be exposed through an application or API. Seedance 2.5 is described by its publisher as an audio/video generation model. Its advertised capabilities still need verification in our chosen integration. [Official model page](https://seed.bytedance.com/en/seedance2_5) |
| **MiniMax** | Model developer/provider | The name covers more than video. For our video work, record the exact model and mode: MiniMax's current API documentation distinguishes H3 and H3 Max. It is not one interchangeable interface or model. [Official video documentation](https://platform.minimax.io/docs/guides/video-generation) |
| **LoRA** | Adaptation technique; also the resulting adapter weights | A smaller set of trained weights used with a compatible base model. It is neither a complete creation application nor a general model library. Architecture, base-model variant and loader support matter. [Hugging Face Diffusers documentation](https://huggingface.co/docs/diffusers/en/training/lora) |
| **Google Flow** | Hosted creative application | Uses Google models for images and video. Its feature set depends on the selected model. Flow is the collaborator intended by Ziggy's earlier “FLUX” wording in this onboarding discussion. [Official model/feature matrix](https://support.google.com/flow/answer/16352836?hl=en) |
| **FLUX** | Black Forest Labs model family | A separate name from Google Flow. Our historical FLUX.2/Klein references identify particular BFL image-generation/editing models. [Official FLUX.2 page](https://bfl.ai/models/flux-2) |
| **Civitai** | Model/resource platform and community | A source of model artifacts and supporting material. Record the resource's publisher, exact version, type, base model and license before proposing use. It is not itself a single model. [Official project repository](https://github.com/civitai/civitai) |

These layers combine: **application/interface → compatible model → optional adapter → recorded settings → output → review**. A Seedance or MiniMax model can be available through a Comfy integration; it need not be a replacement for ComfyUI. Availability in a public catalog is not proof that our account or saved graph can run it.

Google's apps also need separate receipts. The Gemini chat, Notebook 0, NotebookLM, AI Studio and Flow can share a provider while exposing different models, tools, attachments and saved context. Notebook 0 may coordinate the project, but that does not prove it can inspect every other app's session or original media. Every handoff should identify the actual surface, project/chat URL, visible model when known, supplied references and what was verified there.

## Two bounded first research briefs

These are prepared assignments for dispatch after onboarding. Writing them here does not mean DeepSeek or Qwen has received or accepted them. Read the shared welcome/template first and create or refresh your own `I_AM.md`; identify your actual tools and access before selecting work.

**DeepSeek — map AUTOMATIC1111 and Forge.** Read their official documentation and compare the same five jobs: load an exact reference; perform a localized edit; hold settings for a controlled comparison; save/reopen the working configuration; hand an accepted still to a video route. Return one short capability table, a proposed first lesson for each interface, and unresolved compatibility questions. Identify which concepts are shared and which settings or extensions require separate instructions. Do not claim Forge is faster for our hardware without measurements.

**Qwen — map InvokeAI and review the teaching design.** Read InvokeAI's official canvas and workflow documentation. Propose one lesson for editing a small region while preserving the rest, with input roles, an explicit mask boundary, a baseline, one deliberate change, review criteria and saved evidence. Compare that lesson with the existing Comfy image-edit lesson. Also review DeepSeek's proposed capability table when it is available, marking unsupported claims and terminology mismatches; do not wait for it to complete the Invoke proposal.

For both briefs, use public documentation and read-only inspection of existing project material. Deliver a Markdown report in your own onboarding subfolder, with review date, primary source links, exact versions where relevant, uncertainties and a proposed next experiment. No installs, model downloads, local GPU runs, purchases, account changes, uploads or generation jobs are part of these first assignments. Keep existing media and concurrent edits intact.

## Reuse the work already done

Read the [Comfy workshop status](../../../README.md), [problem-to-recipe lookup](../../../workflows/README.md#choose-by-problem), [decision and feedback procedure](../../../templates/workflow_intake.md#decision-and-feedback) and [CFA/Panhandlers handoff](../../../../pathfinder_handoff/README.md). In the adjacent `D:\Documents\Pan_Handlers` checkout, read:

- `Help/CFA_TUTORIAL_LEDGER.md` and `Help/FILE_MAP.md` for ownership, evidence states and lesson locations.
- `Help/pages/compare_paths.py` and `Help/content/catalog.py` for the existing four-path comparison.
- `Help/guides/model_library.py`, `model_filters.py`, `image_edit_lab.py` and `sampling_lab.py` for model roles, localized/whole-image distinctions and controlled comparisons.

Return proposed teaching changes through the existing manual handoff. Panhandler Nova owns learner-facing integration; CFA owns production inputs, account checks, runs, outputs and acceptance. Keep **reviewed → available → validated → executed → accepted** separate. Our first deliverable is an understandable, sourced lesson proposal; actual execution is a later bounded decision.

At every session close, leave the next collaborator the artifact paths, exact evidence state, errors or limitations, next action and any unresolved decision. For a fresh Flow session, preserve the project/model/settings and closing observations rather than assuming the next session retains them. This refresh loop applies to every collaborator.
