# Community workflow intake

Copy this sheet for a selected resource. This is a planning record, not an
executable graph, authorization gate, or completed-run record. Use the existing
run_record.json template when a real execution is submitted.

- Intended video/asset result and output type:
- Problem-to-recipe row selected and why it fits this material/preservation need:
- Relevant Panhandlers lesson or CFA fallback, source link/section and review date:
- Existing baseline graph/record path and exact version; outcome and limits reviewed:
- For video: source shot/time range; preserve motion, change appearance / replace character / localized edit / new action / dialogue / finishing:
- Must preserve versus may change: identity, action, camera, background, timing and sound:
- Source, generation, refinement and delivery dimensions recorded separately; aspect-ratio/crop decision:
- Source URL, creator, retrieval date, revision if known:
- Source kind: editor graph / API graph / metadata-bearing media / example only / node package
- Original file path and SHA-256, if retrieved:
- Named working copy:
- Execution environment and verified access: Comfy Cloud / local / Runpod Pod
  (connection alone does not establish an installed runtime):
- Graph stages and output branches:
- Core / frontend / connector versions (separate; unknown if unverified):

| Dependency | Exact class/model/version or file | Available here? Evidence/date | Adaptation or remaining work |
| --- | --- | --- | --- |
| Node / subgraph | | Unknown | |
| Model / text encoder / VAE | | Unknown | |
| Reference image / mask / video / audio | | Unknown | |

- Baseline settings: prompt, references, fixed seed/control, dimensions, steps,
  sampler, scheduler, CFG, denoise; duration/FPS where applicable:
- Queue repetitions and per-job batch size (record both):
- Required video frames or multiview counts (preserve structural requirements):
- Entered/effective prompt and any enhancement control; exact dialogue if needed:
- Preview/save socket types, generation/output FPS, audio handling, codec,
  persistent save and metadata settings; original output branch retained:
- Optional upscale stage and parent output; keep disabled for initial review:
- Automatic queuing disabled for the initial controlled comparison:
- Output destinations and any external/API operations:
- Cost exposure: native GPU / partner API / both; estimate and excluded costs:
- One proposed change, why it matters, and what result would support it:
- For a settings comparison: target node/stage, explicit candidate values,
  shared controls, active output branches, variant prefixes and stopping point:
- Source/model/asset attribution and usage terms:
- Browser handoff, only if needed: exact dependency, link, destination, expected
  filename, Cloud download size and purpose:
- Decision: adopt a small test / adapt the idea / defer / decline
- Evidence state: researched / available / validated without execution / executed / accepted
- Run record and observed result (leave unset before execution):
- Next decision:

## Decision and feedback

Use the [problem-to-recipe lookup](../workflows/README.md#choose-by-problem) to choose a starting point. The fields above form the decision record: what we want, which lesson informed the choice, which baseline we reuse, one deliberate change, and the observation that would support it. Record a reason for departing from the recommended baseline. Do not run a comparison merely to fill out this form.

If an actual job is submitted, use the existing [run record](run_record.json) without changing its schema:

| Decision or evidence | Existing run-record field |
| --- | --- |
| Question and baseline relationship | `question`, `parent_experiment_id`; keep the exact baseline path/version in this linked intake when no parent experiment ID exists. |
| Lesson, intake and rationale | `provenance.attribution_notes`: cite their paths/sections and review date. Keep upstream model/workflow provenance in `source`. |
| Actual graph and effective settings | `workflow`, `inputs`, including `inputs.resolved_parameters`. Preserve compiled values and hashes where available. |
| What actually happened | `evidence_status`, `job`, `outputs`, `usage`; leave unobserved values unknown. |
| Result, defects and next change | `review.observations`, `review.decision`, `review.cleanup_needed`, `review.next_change`. A completed job is not automatically accepted or better. |

For a dependency check or dry-run with no job, retain the intake/preflight record and its dated status; do not label it an executed run. The templates do not enforce permission or spending controls.

After review, add a short entry to [LESSONS.md](../LESSONS.md) with the problem, applied technique, result/defects, relevant record and next decision. Return only the reusable finding through [the Panhandlers ledger and feedback handoff](../../pathfinder_handoff/README.md); keep canonical graphs, media and run records in CFA. When evidence changes a recommendation, revise the relevant lookup entry and teaching task. If nothing was rendered or accepted, say so explicitly.
