# Sampling experiments for Observatory assets

Initial review September 12, 2026 from Ziggy's supplied continuation transcript,
0:21–20:34. It covers KSampler controls, batches and graph organization; its
episode number and canonical URL have not been verified. These timestamps
must not be attached to Pathfinder's Episode 2 URL by assumption.

Pathfinder already teaches the general concepts in **07 / Workflow lab →
Control guide / Practice path** and **03 / Workflow anatomy → Size & sampler /
Controlled experiment**. The [shared-methods map](../pathfinder_handoff/README.md#shared-methods-and-local-independence)
locates those sources. This note retains only their production implications.

| Passage | Rule for our experiments |
| --- | --- |
| 0:44–4:16: seed, queue and cached reruns | Fix seed and its control while comparing one change. Record actual submitted values. Identical cached work is not a fresh speed benchmark; fixed seed alone does not ensure identical pixels across environments. |
| 4:20–6:10 and 8:15–9:55: steps, guidance and sampler | Follow the specific model and recipe. More steps or CFG do not guarantee improvement; CFG is not a contrast control. The presenter's Juggernaut ranges do not replace our Z-Image or LTX settings. |
| 6:13–8:12: primitive/shared controls | Expose controls where the deployed interface supports it. Record which stages share a value so changing one comparison branch does not silently change the baseline too. |
| 9:58–10:55: image batches | Count queued jobs, samples per job and active output branches separately. Preserve required video frames/views. The presenter's RTX 4090 timing is not our Cloud timing or cost; batching also changes memory demand. |
| 11:27–13:47: grouped interface | A frame, reusable subgraph and hidden widget have different roles. Hiding a control does not disable its value. Current subgraphs and legacy group-node commands can differ. Preserve the full export. |
| 13:50–20:12: bypass and copied branches | Check the actual connections and enabled outputs after duplication or bypass. Required data can be lost; a branch that looks inactive may still need validation. Extra samplers are not a guarantee of parallel execution. Give outputs distinct prefixes tied to their variants. |

## Small, controlled comparisons

1. State one visible question, such as whether a chosen setting improves fur
   detail without losing the gentle expression. Fix a baseline graph and inputs.
2. Name one control and its target node/stage. Record a short explicit list of
   values within the supported recipe, the expected outputs and stopping point.
   Use separate baseline/candidate controls unless sharing is deliberate.
3. Start with one submission and the smallest supported batch. Leave automatic
   queuing off. If stopping a sweep, check pending and running jobs separately;
   disabling automatic submission alone does not establish cancellation.
4. Record actual parameters and output/variant mapping in the run record's
   `inputs.resolved_parameters` and `outputs` fields. Keep cached versus newly
   sampled results distinguishable when evaluating time or cost.
5. Compare the intended improvement and collateral changes. Organize or expose
   simpler controls after the recipe works; retain hidden values in its export.

The executed pump still remains seed 42, eight steps and CFG 1. The recovered
LTX recipes use two advanced sampling passes with explicit sigma sequences,
not the tutorial's single KSampler step control. Preserve each pass and its
purpose before varying settings. Recovery of a recipe is not a completed run.

Primary checks: [KSampler inputs](https://docs.comfy.org/built-in-nodes/sampling/ksampler),
[node modes and bypass](https://docs.comfy.org/basic-concepts/nodes#mode),
[current subgraphs](https://docs.comfy.org/interface/features/subgraph),
[execution/cache behavior](https://docs.comfy.org/custom-nodes/backend/server_overview),
[determinism limits in core](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/cli_args.py).
This is documentation review. No sweep, workflow conversion or Cloud run was
performed while incorporating the transcript.

<a id="image-to-image-and-loras"></a>

## Image-to-image and LoRAs: Episode 4

Additional review September 12, 2026: supplied transcript identifies itself
as Episode 4 and runs 0:00–17:16. Canonical video URL and downloadable graph
are unverified. Attachment `d80051c7-f869-41d9-8a23-9aede833ac84`, SHA-256
`cae0e978292ed6c56eb6632d3c7194407df1f519c01d60880a3b95c182ee392a`.
No model download, import or generation was performed for this review.

Pathfinder already covers **03 / Workflow anatomy → VAE paths → Start from
an existing image**, **Size & sampler**, and **02 / Setup routes → Models &
files**. Reuse those explanations; the production additions follow here.

### Prepare the image, then vary denoise

**0:09–6:48.** In the demonstrated classic SDXL graph, the image path is:

```text
Load Image → Resize → VAE Encode → KSampler latent_image
                                      ↓
                                 VAE Decode → Save Image
```

The compatible VAE feeds both encode and decode; the sampler still needs its
model and positive/negative conditioning. Its starting dimensions come from
the encoded image, subject to the VAE's size handling. This is not the same
wiring as every modern instruction-edit or multi-reference model. Use the
selected template, rather than replacing inputs in our Z-Image or LTX graph.
[Comfy image-to-image guide](https://docs.comfy.org/tutorials/basic/image-to-image).

Preserve the original and the prepared input separately. Record actual
width/height, resize method, crop/padding choices and file hashes. The core
`ImageScale` node, displayed as Upscale Image, can also shrink an image.
Choose dimensions that preserve the intended aspect ratio; disabling crop
does not prevent stretching when the specified ratio differs. Preview the
prepared image before VAE Encode. Use the model recipe's supported sizes;
1024-square and multiples of 64 are not universal requirements for all
architectures. [Core image sizing implementation](https://github.com/Comfy-Org/ComfyUI/blob/master/nodes.py).

A fourfold increase in both dimensions means sixteen times as many pixels.
If memory fails, identify encoding, sampling or decoding as the failing stage.
A tiled VAE does not reduce the selected sampling resolution. Do not use
the presenter's timings as our Cloud cost/performance estimate.

For our [courtyard appearance study](REFERENCE_DRIVEN_WORKFLOWS.md#first-use-render-our-world-then-explore-its-appearance),
test denoise alone from one unchanged prepared image, seed, prompt and recipe.
For a compatible SDXL recipe, 0.30 / 0.50 / 0.70 are illustrative comparison
values, not approved jobs or preservation guarantees. Start with one result
within the experiment's scope; compare whether richer surfaces retain the
arch, paths, horizon and camera. Keep a smaller supported change if layout
drifts. Consider a controlled editing or inpainting recipe when a feature
must stay fixed; denoise alone cannot lock geometry or identity.

Lower denoise generally retains more of the source; higher permits more
change. The transcript's 0.6 starting point is one example. Denoise is not an
opacity blend or a percentage of pixels to preserve: the current standard
[KSampler implementation](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/samplers.py)
selects a noise schedule from it. Full denoise can largely overwhelm the
starting image; other reference-conditioning paths can still matter.

**6:48–7:43.** Clipboard reuse is convenient where supported, but every input
must still be saved and identifiable. Comparing three denoise values from
the same parent is different from feeding each result into the next run.
For intentional successive edits, record every parent/child relationship;
otherwise accumulated drift confounds the comparison.

### Add a compatible LoRA as a separate experiment

**7:47–17:16.** A LoRA supplies learned adjustments for a compatible base
model. Loading one applies existing weights; it does not train a new adapter
during generation. Confirm exact family/version, file, any required trigger
phrases and recommended strengths. Not every LoRA requires a trigger.
The cloud/fire examples are demonstrations, not selected Observatory assets.
[Comfy LoRA guide](https://docs.comfy.org/tutorials/basic/lora).

In the classic `LoraLoader` route, connect checkpoint `MODEL` and `CLIP` to
the loader, its `MODEL` to the sampler, and its `CLIP` to both prompt encoders.
The VAE keeps its encode/decode role. Record both `strength_model` and
`strength_clip`; setting only the former to zero does not necessarily remove
the adapter's entire effect. Some adapters contain no text-encoder changes
or use a model-only loader; inspect the actual recipe.

Compare adapter off/on with the same prepared input, trigger text, seed,
denoise and other controls. With the standard loader, both strengths at zero
provide a bypass baseline; verify the active path in other loaders. Establish
that difference before testing strength changes. Follow the specific model's
recommendations, rather than making the tutorial's 0.3–1 range a project rule.
[Loader implementation](https://github.com/Comfy-Org/ComfyUI/blob/master/nodes.py).

Use the [Civitai procedure](CIVITAI.md) to check existing Cloud availability
first and supply the exact import handoff only if needed. A local
`models/loras` directory does not populate Comfy Cloud. A Runpod installation
would have its own storage and loader inventory. The tutorial's SDXL adapters
cannot be assumed compatible with the guardian's LTX-2.5 recipe.
