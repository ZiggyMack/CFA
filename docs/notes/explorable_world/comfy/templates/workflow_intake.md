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
- Evidence state and scope: use the [canonical definitions](#evidence-states); record the date, environment, artifact and intended use.
- Run record and observed result (leave unset before execution):
- Next decision:

## Evidence states

This is CFA's canonical evidence vocabulary. Pan links this section with its review date. These are scoped observations, not one automatic ladder: a received image does not establish a validated workflow, and an executed job does not establish an accepted character or scene. Keep existing record/export schemas; explain finer states in their evidence and review notes.

| Workflow state | What it establishes |
| --- | --- |
| Researched / reviewed | A named source, recipe or graph was actually read or inspected. Record what was reviewed; public documentation does not establish account support. |
| Available | The required input, node or model was observed in the named environment at the recorded time. Availability is not a successful preflight or run. |
| Validated without execution | The named graph passed the stated dependency, schema, conversion, compiled-input or dry-run checks. Identify checks and gaps; no generation result follows from this state. |
| Submitted | An actual job submission is recorded. Preserve its identifier and state; submission is not execution or completion. |
| Executed | The job actually ran in the recorded environment. Preserve status, graph, effective settings and output/failure evidence; execution alone is not successful completion or acceptance. |
| Accepted for a named use | Ziggy or an authorized reviewer accepted the exact artifact for a stated role, scene or deliverable after the relevant checks. Acceptance of one component is not acceptance of the entire character or scene. |

| Asset/intake observation | What it establishes |
| --- | --- |
| Requested / provider-reported | A request or attributed claim exists. A chat acknowledgement, manifest row or filename is not receipt of pixels or verified completion. |
| Received locally | Actual bytes arrived at the recorded path. Record source/version and, when measured, size and hash. |
| Integrity / extraction checked | The stated size, hash, archive integrity, extraction or decode check passed. List which checks actually ran; these do not prove visual accuracy. |
| Inspected | The recorded image, video, audio or text was actually viewed, played or read. Identify preview/full-resolution, sampled/full-duration and any occlusion or unread tail. |
| Author-selected | The author chose the exact artifact or feature for a stated role. This does not prove it was preserved in a later output or accepted as a whole master. |
| Preservation verified | The stated feature was observed to survive the stated transformation or output check. Record the check and limits; this does not establish every other feature or full acceptance. |

Also record prepared, attached, delivered and read-back states independently. A saved mailbox file is posted, not automatically delivered or read. A failure or blocker belongs to the specific check; it does not erase earlier received bytes or authorize reruns. Keep production design stages, likeness stars, scene-readiness grades and collaborator performance grades separate from these evidence states.

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
