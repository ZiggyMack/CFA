# CFA task guidance

## Local execution and storage

Keep CFA project execution on D:. Use project runtimes and tools installed on D:, and keep working directories, dependencies, caches, temporary build files and generated outputs there. Do not fall back to a project runtime installed on C: (including Python). If a suitable D: runtime is missing, establish a D: runtime before running the affected project commands. This does not call for moving or changing Windows or the desktop application's own installation.

The verified CFA Python runtime is `D:\Documents\CFA\.cache\runtimes\python314\python.exe`. Use `D:\Documents\CFA\.cache\runtimes\run-python.ps1` to invoke it with user-site packages disabled and temporary files/package cache on D:. Node and Git are available under `D:\Program Files (x86)`.

## ComfyUI and video workflow work

Apply this section when selecting, creating, troubleshooting or optimizing ComfyUI workflows, preparing image/video references, or evaluating Civitai resources for this project.

1. Read the [Comfy workshop status](docs/notes/explorable_world/comfy/README.md) and [problem-to-recipe lookup](docs/notes/explorable_world/comfy/workflows/README.md#choose-by-problem). Identify the supplied material, intended change and what must be preserved before selecting a recipe.
2. Consult the relevant lesson through the [Panhandlers tutorial ledger](../Pan_Handlers/Help/CFA_TUTORIAL_LEDGER.md) and [file map](../Pan_Handlers/Help/FILE_MAP.md). Read the matching lesson, not the whole curriculum. If the sibling checkout is unavailable, use the [CFA handoff and local fallbacks](docs/notes/explorable_world/pathfinder_handoff/README.md), record the gap and continue independent work.
3. Reuse an appropriate saved or official template. Verify its current Cloud models, node schemas and compiled inputs before claiming compatibility. Keep reviewed, available, validated, executed and accepted distinct; saved settings are dated evidence, not guaranteed optimal defaults.
4. For a comparison, use the [existing intake and feedback procedure](docs/notes/explorable_world/comfy/templates/workflow_intake.md#decision-and-feedback): cite the lesson, choose a baseline and one deliberate change, define a success check, and preserve the actual graph, settings, result and defects. Record unknowns as unknown.
5. Return reusable findings and new tutorial intakes through the [manual CFA/Panhandlers handoff](docs/notes/explorable_world/pathfinder_handoff/README.md). Preserve concurrent edits; leave bounded teaching tasks for Panhandler Nova and report measured outcomes rather than promoting a tutorial claim into a tested recommendation.

The project uses Cloud execution and model storage; keep necessary local artifacts on D:. The wolf capability test and Hon Dolo production are separate briefs. These instructions do not authorize purchases, unlimited batches or public release. Other CFA tasks use the existing repository documentation and their applicable task instructions.
