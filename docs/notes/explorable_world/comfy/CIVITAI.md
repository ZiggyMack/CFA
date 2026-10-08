# Civitai access for The Observatory

**October 3 runtime result:** a Civitai-origin resource supplied by Comfy Cloud has now executed successfully: `flux-2-klein-9b-candid_film.safetensors`, through native `LoraLoaderModelOnly`, at strength 0.5 in the Klein 9B reference-edit comparison. See the [run record](workflows/hon_dolo_reference_edit_v001.record.json). The same-seed visual difference is subtle; no superiority over the baseline is established. Creator examples use the 9B base model, so this is one measured distilled-model test, not blanket adapter compatibility.

**Stored-key/import status remains unverified.** Live `owned:true` returned zero imported models and the Civitai-node search returned zero. Shared catalog entries use source `comfy-cloud`; their `repo_url` can still point to Civitai. No model-import or Secrets-test operation is exposed in MCP, and browser control failed kernel-assets initialization. The shared LoRA run did not exercise the saved provider key or Civitai/Buzz remote generation. [Comfy import instructions](https://docs.comfy.org/cloud/import-models) remain the route for a genuinely needed new model.

[Candid Film v2](https://civitai.com/models/2313101?modelVersionId=2757653), version 2757653/file 2644036, is publicly listed but its mini-version API reports `requireAuth=true`. Its original filename is `klein_candidfilm_v2.safetensors`; the Cloud catalog uses the alias above. File hash identity with Cloud's copy has not been checked. The optional [Klein Detail Slider](https://civitai.com/models/2334190?modelVersionId=2625692) is a later candidate only; its public download does not require authentication and would not prove the key. Neither import is needed to repeat the tested baseline.

Historical September 12 checkpoint: credential saved per report/screenshot; import and generation had not yet been tested. The October 3 update above supersedes the generation status.

**Ziggy's defaults:** SDXL 1.0 for new third-party still-image model searches, SafeTensor files, and highest-rated/most-downloaded shortlists. Our executed Z-Image pump recipe remains a preserved baseline. Video, speech, and mesh experiments need models appropriate to those tasks.

**Storage default:** import model weights directly into Cloud. Keep version references here; avoid local model downloads. Necessary media downloads go to D:. Follow the [project storage policy](../STORAGE.md).

Use Civitai to find resources for a specific scene or asset experiment. Keep the playable chapter in [games/observatory](../../../../games/observatory/README.md), recipes in [workflows](workflows/README.md), and generated originals in outputs/. Ziggy has delegated background prop choices; new model purchases and unlimited generation are separate decisions.

## File format and model family

SafeTensors stores tensor data without pickle's arbitrary-code deserialization behavior. Traditional pickle-based `.ckpt` files can carry that risk. This is a reason to prefer `.safetensors`; it does not establish artistic quality or compatibility. [SafeTensors maintainers](https://github.com/safetensors/safetensors)

**Checkpoint** describes the model resource; `.ckpt` describes a file format. A checkpoint can be distributed as `.safetensors`. Select **Checkpoint + SafeTensor** when looking for the main image model. Select **LoRA + SafeTensor** when looking for a smaller adaptation used with a matching base model. [Comfy's model guide](https://docs.comfy.org/tutorials/basic/text-to-image), [LoRA guide](https://docs.comfy.org/tutorials/basic/lora)

SD 1.5, SDXL, and SD3 identify different model families. Use **SDXL 1.0** as the base-model filter for our default search, then check any LoRA against the chosen checkpoint. A shared file extension does not make different architectures interchangeable. The tutorial screenshot is a guide to those controls, not evidence of today's popularity rankings.

## A practical filter preset

| Filter | Starting choice | How to use it |
|---|---|---|
| Sort | Most Downloaded, then Highest Rated | Build and compare two shortlists within our other filters. |
| Time period | All Time; then Month | Start broad, then investigate recent candidates. Check the site's period mode as explained below. |
| Model type | Checkpoint | Find the main image model. Switch to LoRA when seeking a specific style or subject adaptation. |
| Checkpoint type | All | Includes trained checkpoints and merges. This is not a quality ranking. |
| File format | SafeTensor | Keep our preferred weight format. |
| Base model | SDXL 1.0 | Our default image family. Evaluate Pony, Hyper, Turbo, Lightning, and other variants separately with their own instructions. |
| On-Site Generation | Leave unset for imports | Select when specifically seeking models usable by Civitai's generator. It says nothing about availability on Comfy Cloud. |
| Made On-Site | Leave unset | Refers to resources trained on Civitai; it is not a quality requirement. |
| Early Access / paid-access controls | No paid-access requirement | Check the selected version's access conditions before choosing it. |
| Hidden / Include Archived | Leave off | Start with ordinary available listings. |

The [official model API reference](https://github.com/civitai/civitai-developer-docs/blob/main/site/reference/models.md) documents sorting, model families, checkpoint types, generation availability, and platform-training filters. The actual [site filter implementation](https://github.com/civitai/civitai/blob/main/src/components/Model/Infinite/ModelFiltersDropdown.tsx) may differ from the tutorial screenshot.

**Time period needs context.** The API guide describes a window for sorting metrics. The reviewed site [schema](https://github.com/civitai/civitai/blob/main/src/server/schema/base.schema.ts) also defines a `periodMode` that defaults to `published`; the [model service](https://github.com/civitai/civitai/blob/main/src/server/services/model.service.ts) can restrict results by the latest version date. Do not describe Month as universally meaning only downloads received this month, or only models first released this month. Record the actual mode when visible; All Time avoids that cutoff while establishing the broad shortlist. This was a source review, not a live account UI test.

## Tutorial note: version X versus Hyper

Ziggy reports that the tutorial prefers a version called X over Hyper for quality, and clarified that SDXL is the comparison baseline. The newly supplied episode-two transcript explicitly names **Juggernaut X at 11:41**, resolving the previously unspecified model name. Its exact Civitai version/file/hash is still not identified by the transcript. Retain the quality comparison as a reported opinion, not our measured result or a universal preference. Start our new image-model searches with standard SDXL 1.0; evaluate accelerated variants separately when generation speed is useful. See the [annotated tutorial](TUTORIAL_02.md).

If Hyper refers to Hyper-SD acceleration, its [official model card](https://huggingface.co/ByteDance/Hyper-SD) describes distilled models and adapters intended for fewer sampling steps, with variant-specific guidance and scheduler settings. A later comparison should use each release's recommended recipe and assess scene detail, prompt adherence, and cost. No X-versus-Hyper experiment has been run here.

## Connect model downloads to Comfy Cloud

Comfy Cloud supports Civitai imports on Creator and Pro plans. For downloads requiring authentication:

1. In Civitai account settings, create an API key. Ziggy's screenshot places API keys under **Security & Apps**.
2. In Comfy Cloud, open **Settings → Secrets** and save that Civitai key. Give it a recognizable label, such as `Civitai Observatory`.
3. For a selected model version, copy its Download button's link. In Cloud choose **Models → Import**, paste the link, and select the appropriate model folder. Look under **My Models** when complete.

Public imports may not need a key. Cloud's importer accepts safetensors weights; the import selector determines supported folders. [Official import instructions](https://docs.comfy.org/cloud/import-models)

Enter credentials directly in Secrets, never in chat, screenshots, project files, or exported graphs. The exposed MCP tools have no Secrets editor or model-import operation, so this setup uses the browser. A secret stored there grants the importer access; it does not establish a separate authenticated Civitai connection for this assistant.

## What the GitHub package adds

[civitai-comfy-nodes](https://github.com/civitai/civitai-comfy-nodes) provides remote generation billed in Buzz. Its Model Selector's `air` output selects a model on Civitai's servers; `path` downloads weights for a conventional Comfy loader. The project is in early preview. These are additional routes to evaluate when they solve a production need.

Comfy Cloud manages its preinstalled nodes and currently disallows arbitrary user installations. Being in the Comfy Registry does not establish availability in our Cloud workspace. [Cloud node policy](https://support.comfy.org/articles/6791455062-custom-nodes-on-cloud)

The package's own authentication is separate from Cloud's import Secrets. Its [configuration source](https://github.com/civitai/civitai-comfy-nodes/blob/main/civitai_comfy_nodes/config.py) supports several credential paths and host-supplied context. Do not assume that context is supplied by cloud.comfy.org. No package was installed or authenticated in this review.

## First useful validation

**Ziggy's selection preference:** shortlist third-party models using highest-rated and most-downloaded rankings. Compare both where available, within the relevant task and compatible model family. Then inspect example outputs and the specific version before adopting it. Popularity guides discovery; the experiment establishes suitability here. Record the ranking period when it affects the selection.

Choose a resource for a named chapter need. Check its base model, required loader, trigger words, and usage terms; retain the exact model/version and file identifiers with the experiment record. An SDXL LoRA, for example, should not be treated as a drop-in addition to our existing Z-Image recipe.

After import, verify the model appears in the actual loader and inspect the resulting workflow before running it. Record the execution provider and its estimate separately: Civitai-hosted jobs use Buzz; native Comfy Cloud jobs use the Comfy budget. Keep actual cost unknown until a relevant usage record establishes it. Buying Buzz alone does not establish model compatibility or download entitlement.

## Current evidence and next step

### Model discovery and browser handoff

The assistant can research and shortlist models before import: inspect public model cards, compare download/approval counts, identify compatible versions, and prepare an exact file link and destination. Ziggy is not responsible for finding every model. With the current tools, the browser handoff is **once per new external model file/version added to Cloud**. Models already available in the shared catalog or previously imported can be reused in workflows without repeating that step. Comfy automatically reuses its saved provider key when needed.

**Standing handoff agreement with Ziggy, September 12, 2026:** the assistant owns the timing and preparation of these interruptions. Ask for the browser action when a selected model is needed for a concrete upcoming experiment and the import instructions are ready. First check whether the required model is already available in Comfy. A speculative candidate on the shortlist does not itself trigger an import request.

1. Prepare the scene/experiment purpose, exact model and version, direct import link, model type and destination folder, expected filename, and reported Cloud download size. Explain why this addition is needed. Include any actual source-access requirement; do not ask Ziggy to repeat an already completed account setup.
2. Send one concise **Import needed** interruption using the available asynchronous user-input channel. Give the browser steps and the completion signal: tell the assistant when the import appears under My Models, or report the import error. Bundle multiple already-justified dependencies for the same experiment when useful.
3. Continue independent preparation while waiting. Hold the dependent execution until Ziggy reports completion and a live catalog check establishes the imported model is available; silence or elapsed time is not completion.
4. Verify the imported entry and exact loader option, finish the workflow checks, and resume work within the existing authorization and budget. Record the resolved model/version in the experiment. Reuse the imported file for later compatible workflows without repeating the handoff.

The interruption supplies a concrete browser task, not a request for Ziggy to research models or approve individual background props. It does not expand authority for purchases, subscription changes, or public release. The optional Juggernaut example below remains prepared for a future comparison; no import is required merely to acknowledge this agreement.

On September 12, 2026, ordinary web retrieval of Civitai pages failed, but public Civitai API metadata reads through an authorized shell outside the sandbox succeeded. This provides direct public research access without reading credentials or downloading weights. It does not establish a signed-in Civitai session or access to private resources.

Two concrete SDXL candidates were checked against the public model API. Counts below are observations for the **whole model listing**, not the selected version, and do not establish a catalog-wide ranking:

| Model | Observed downloads / thumbs up | Selected version | Use in our project |
|---|---|---|---|
| [RealVisXL V5.0](https://civitai.com/models/139562?modelVersionId=789646) | 686,305 / 18,097 | V5.0 (BakedVAE), version 789646, file 703211; SDXL 1.0, FP16 SafeTensor | Start with the corresponding RealVisXL V5 checkpoint already discovered in Comfy's shared catalog; no new import is needed for that route. File-hash identity with the shared copy has not been checked. |
| [Juggernaut XL](https://civitai.com/models/133005?modelVersionId=456194) | 1,635,996 / 36,230 | Jugg_X_by RunDiffusion, version 456194, file 375666; SDXL 1.0, FP16 SafeTensor | Optional second checkpoint for a controlled atmospheric architecture comparison; project suitability is a hypothesis to test. |

Sources: [RealVis public metadata](https://civitai.com/api/v1/models/139562), [Juggernaut public metadata](https://civitai.com/api/v1/models/133005), [RealVis creator card](https://huggingface.co/SG161222/RealVisXL_V5.0), [Juggernaut publisher card](https://huggingface.co/RunDiffusion/Juggernaut-X-v10).

**Prepared optional import handoff:** paste `https://civitai.com/api/download/models/456194?fileId=375666` into Comfy **Models → Import**, then select **Checkpoint / checkpoints**. The selected filename is `Juggernaut_X_RunDiffusion.safetensors`, reported size 6,938,817.0625 KB (about 7.11 GB), SHA-256 `D91D35736D8F2BE038F760A9B0009A771ECF0A417E9B38C244A84EA4CB9C0C45`. The API reports Public availability. This is a Cloud import link, not an instruction to download the weights to D: or G:; a public import alone would not validate the saved Civitai credential. The download endpoint has not been fetched in this research.

The publisher's standard-model settings suggest a comparison starting at 1216 × 832, DPM++ 2M / Karras, 35 steps, CFG 6. This is an unexecuted recipe suggestion for the standard X version, not Lightning or Hyper. No model import, weight download, or new generation occurred during selection.

### Connection and import validation

Ziggy reports adding the Civitai API key to Comfy. The supplied screenshot shows a Civitai-provider secret named `COMFY_TEST_1` in Settings → Secrets. Its value was not inspected. This completes the reported browser setup step; an authenticated model import is still needed to validate the credential. The [Hugging Face guide](HUGGING_FACE.md) explains the other provider offered by that form.

Ziggy's supplied screenshots show Gold membership and separate Green and Yellow Buzz balances. They establish a screenshot observation, not a live balance check. This session has no authenticated Civitai tool connection.

The latest readiness check initially encountered `invalid_grant: refresh token reuse detected` again. A fresh `codex mcp login comfy-cloud` succeeded, followed by a responding production server reporting authenticated OAuth and 41 tools. The [connection notes](README.md) retain the recovery details; the recurring rejection's cause remains unknown.

Live catalog checks after recovery returned zero imported/uploaded models (`owned: true`, total 0) and zero nodes matching `civitai`. The shared SDXL 1.0 checkpoint search returned `realvisxlV50_v50Bakedvae.safetensors`. This establishes catalog availability, not a completed generation with that checkpoint.

The saved secret's name is valid: Comfy permits any label and automatically uses saved keys for protected imports. For a selected Civitai model version, use **Models → Import → paste its Download link → Continue → choose the model type/folder**, then wait for it in **My Models**. The current MCP inventory has no model-import or Secrets-editing operation. A public import can succeed without proving the saved key; an account-protected import is needed to establish its authenticated access. [Official import instructions](https://docs.comfy.org/cloud/import-models)

No model import, generation, or credit spend occurred in this readiness check. Our local game remains playable independently.
