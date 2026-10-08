# Hugging Face for The Observatory

Reviewed September 12, 2026. **Researched; no Hugging Face account connection, import, or paid execution tested here.**

Use Hugging Face as an additional model source. Preserve Ziggy's SDXL 1.0/SafeTensor defaults for new image work and the cloud execution/D-drive storage policy. Google Drive is our preferred candidate for the asset archive; it still needs connecting.

## What it adds

| Resource | Possible use in our project | Primary example |
|---|---|---|
| Publisher model releases and model cards | Understand the original model, files, settings, and limitations; record a specific revision | [Stability AI's SDXL 1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) |
| 3D generation models | Investigate turning an accepted concept into a textured prop | [Tencent Hunyuan3D-2](https://huggingface.co/tencent/Hunyuan3D-2) |
| Audio-driven video models | Explore a future character performance from an image and audio | [Wan2.2-S2V](https://huggingface.co/Wan-AI/Wan2.2-S2V-14B) |
| Spaces | Try browser demos and prototypes before adopting a workflow | [Spaces overview](https://huggingface.co/docs/hub/en/spaces-overview) |

These examples establish what the publishers offer, not compatibility or successful runs in our Cloud account. The Comfy template, nodes, model format, and dependencies must match. A generated mesh also needs engine cleanup and testing. Audio-driven video is a separate production experiment from our current written game dialogue.

Hugging Face also provides hosted inference through providers; supported tasks, quotas, and billing depend on the service. Storing a model-download token in Comfy does not provision that compute. [Inference Providers](https://huggingface.co/docs/inference-providers/index)

## Minimal Comfy setup

1. Start with a free Hugging Face account; no paid upgrade is needed just to create a download token.
2. In [Access Tokens](https://huggingface.co/settings/tokens), create a token for Comfy with read access to the needed repositories. Prefer fine-grained permissions for the selected resources. Model downloads do not need repository write access. [Token documentation](https://huggingface.co/docs/hub/en/security-tokens)
3. For a gated model, complete its access request or terms on the model page. The token can only use access already granted to its account. [Gated models](https://huggingface.co/docs/hub/en/models-gated)
4. Add the token directly in **Comfy Cloud → Settings → Secrets**, choosing Hugging Face as provider. Keep it out of chat, project files, and workflow exports.
5. Check whether Cloud already has the required model. If an import is needed, supply the supported model file's download link in **Models → Import**. The transfer goes to Comfy Cloud; do not download the weights to this PC first. Public resources may not need authentication. [Cloud imports](https://docs.comfy.org/cloud/import-models)

The first validation should confirm the imported file appears in the intended loader. Saving a secret alone is not a successful import or generation.

## Storage and connection boundaries

Hugging Face offers public/private [Storage Buckets](https://huggingface.co/docs/hub/storage-buckets) for artifacts, but they have no Git history. They are an optional future tool, not an additional storage setup required now. Spaces runtime disks are temporary; a demo's disk should not be used as our archive. [Spaces storage](https://huggingface.co/docs/hub/spaces-storage)

The intended division is: Git for source and asset records; Civitai/Hugging Face for model sources; Comfy for generation; Google Drive for retained originals; D: for the active game and necessary local copies. The [storage policy](../STORAGE.md) records the archive connection status and next steps. A token entered into Comfy enables that importer; it does not authenticate this assistant separately to Hugging Face or Google Drive.
