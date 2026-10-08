# Hon Dolo music video workflow plan

Reviewed October 4, 2026. We have enough creative direction to prepare **five reusable workflow families plus a timeline edit**. The song, selected designs and driving clips will determine which branches each shot needs. This is a research and selection plan, not five newly built or validated Cloud workflows.

## Creative brief and inputs

Hon Dolo leads a lifelike trap-rap video; Chewbacca is the MC/DJ. Leia, Vader, Boba Fett and Jabba complete the proposed cast. Hon Dolo's look remains open: the [received Grok collection](../casting/grok_intake_20261004/README.md) now contains 90 numbered lead concepts, eight early/face studies and eight supporting-cast studies, exceeding the original 12-option request. Grok continues tattoo/grill refinement. Grok images supply styling; intended-character references supply appearance. The clean still and first motion preview are candidates, not accepted character masters. See the [casting brief](../casting/casting_brief.txt).

The desired changes are likeness, tattoos, jewelry, wardrobe and setting. Once chosen, those features must remain consistent across shots. Where a source performance is used, its intended gestures, timing and contact need separate preservation checks. A human DJ reference supplies performance or styling; it does not establish Chewbacca's anatomy. The woman-and-wolf clip remains an unrelated capability test.

Available material includes Grok designs, intended likeness references, saved still recipes, one short I2V result and the supplied lyrics for **Hon Dolo - Strictly Business**. Its [project home](../projects/hon_dolo_strictly_business/README.md) preserves the unedited lyrics and a proposed 12-section story map with 21 shot cards. The MP3 and subtitle-bearing M4A have now been received and decoded; the MP3 is 233.480 seconds. Embedded section timings are provisional and the final subtitle overruns the audio. Audible alignment, an isolated vocal stem, selected driving performance and delivery framing remain open. The current planning assumption is a mixture of generated shots and transferred performances; this can change without rebuilding the whole library.

## Five workflow families

| Family | Job in this video | Starting recipe | Current evidence |
| --- | --- | --- | --- |
| 1. Character and shot stills | Combine design and likeness, approve the character, then prepare its shot-specific pose, costume and setting | Existing Klein Reference Edit; separate masked finishing branch when needed | Original still executed; current controls validated. Final likeness/design, tattoos and grill not accepted |
| 2. New shots from stills | Establishing shots, reactions, character entrances and simple Chewie booth movement | Existing native LTX-2.5 I2V Motion Test | One 4.04-second preview executed; sampled eye-closure and smile defects; acceptance pending |
| 3. Performance transfer | Give the selected character an existing performer's movement | Wan Animate 2 for a new setting; Wan2.2 Animate Mix when the source setting matters | Official recipes reviewed; current Cloud availability and compiled graphs unverified |
| 4. Rap performance and lip-sync | Match visible mouth movement to the recorded vocal, or generate a new shot driven by that audio | Sync over selected footage; LTX-2.5 audio-to-video as an alternative | Public recipes reviewed; no CFA lip-sync or audio-driven performance result |
| 5. Video finishing | Improve selected takes and check detail, timing and audio | Native SeedVR2 for general footage; optional MiniMax H3 Regenerate to 2K for qualifying H3 originals | Official recipes reviewed; current Cloud dependencies, execution and quality unverified |

These are five jobs, not a promise of exactly five graph files. Character finishing can warrant a separate masked editor; performance transfer has two conditional branches. The cast shares recipes. Input inspection and controlled comparisons remain supporting tools rather than mandatory passes on every shot.

```text
Grok styling + intended likeness -> character/shot stills -> approve the look
                                                    |
                          +-------------------------+-----------------------+
                          |                         |                       |
                      new motion             source performance      supplied vocal
                       via I2V                 via transfer          via audio-to-video
                          |                         |                       |
                          +---------- selected takes ----------------------+
                                             |
                         lip-sync where needed -> accept take -> upscale
                                             |
                              timeline edit + final music mix -> delivery
```

Audio-to-video and post lip-sync are alternatives for suitable shots. A generated silent reaction, helmeted performance or DJ insert need not pass through a human-mouth model.

## Character finishing

Reuse [Klein Reference Edit](https://cloud.comfy.org/#dd649394-dae2-4831-8eb0-3c90527b0fc8) for design-plus-likeness work. Retain the original design, clean likeness checkpoint and finished character separately. Approve the look before spending on more angles or motion. The existing [workflow index](README.md) and [still-edit brief](../casting/hon_dolo_still_edit.agent_handoff.txt) retain the current reference roles and controls.

For local tattoo/grill corrections, investigate official `flux_fill_inpaint_example`: image plus painted mask, its own FLUX.1 Fill model/encoders/VAE, and a localized prompt. It is a separate model recipe, not extra mask wiring assumed to work inside the Klein graph. The documented dependencies are `flux1-fill-dev.safetensors`, `clip_l.safetensors`, `t5xxl_fp16.safetensors` and `ae.safetensors`; their current availability here is unknown. Review lettering, mouth anatomy, mask boundaries and areas meant to remain unchanged. Exact tattoo placement may need compositing/tracking later if generation cannot retain it. [Official Fill guide](https://docs.comfy.org/tutorials/flux/flux-1-fill-dev), [template](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/flux_fill_inpaint_example.json).

Start optional style LoRAs only after a useful baseline exists. Civitai supplies model resources, not an extra required video stage. Match the exact architecture and variant, verify import access and compare one strength change. Our shared-catalog film-LoRA run did not prove a fresh authenticated Civitai import or a quality gain. The paired comparison remains validated but unrendered.

## New shots and transferred performances

Reuse [Hon Dolo Motion Test](https://cloud.comfy.org/#bfe78175-2366-4a28-bb76-518c89bef525), derived from `video_ltx2_5_i2v`. Its [record](hon_dolo_motion_v001.record.json) preserves 960 x 512, 24 fps and 97 frames. This demonstrates new motion from a still, not preservation of an existing performance. Its intrinsic latent refinement is part of generation, not proof of final HD/4K finishing.

Choose the performance route by what the shot must preserve:

| Shot requirement | Candidate and input contract | Specific preflight finding |
| --- | --- | --- |
| Transfer gestures into a newly designed scene | `video_wan_animate2`: character image + driving video + scene/camera prompt | Official graph uses `WanAnimate2ToVideo` and `WanAnimate2Cache`; no external skeleton extraction in this recipe |
| Replace a performer while retaining the source setting | `video_wan2_2_14B_animate`, Mix branch: image + video + face/pose preparation + tracked subject mask | Current upstream includes SAM2 segmentation, KJNodes PointsEditor, DWPose and a relight LoRA; checking the main Wan weight alone is insufficient |
| Reinterpret whole-scene structure | LTX-2.5 Union Control with depth/edge/pose controls | Our chosen wolf depth branch lacks three Video Depth Anything classes; unchanged graph cannot run there |
| Try richer combined reference control after a named failure | `video_minimax_h3_r2v` | Public starter connects two appearance images; video/audio reference slots are empty. It is not already wired for a driving performance |

[Wan Animate 2 guide](https://docs.comfy.org/tutorials/video/wan/wan-animate-2) and [graph](https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_wan_animate2.json); [Wan Mix guide](https://docs.comfy.org/tutorials/video/wan/wan2-2-animate) and [graph](https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_wan2_2_14B_animate.json); [Union Control](https://docs.ltx.io/open-source-model/feature-guides/structural-control/union-control); [H3 guide](https://docs.comfy.org/tutorials/video/minimax/minimax-h3-native) and [graph](https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_minimax_h3_r2v.json). Public graph inspection was performed October 4; these mutable upstream links are not pinned execution evidence.

Wan Animate 2 also needs its model, text encoder, CLIP vision encoder, VAE and acceleration LoRA. Mix adds `DownloadAndLoadSAM2Model`, `Sam2Segmentation`, `sam2_hiera_base_plus.safetensors`, `yolox_l.onnx`, `dw-ll_ucoco_384_bs5.torchscript.pt` and `WanAnimate_relight_lora_fp16.safetensors`. Check all exact names against the selected graph in Cloud. Mix's inspected source-FPS output is unconnected; its export uses a separate FPS control showing 16, while source audio is connected. Inspect compiled timing and resample deliberately before claiming audio or motion preservation.

H3 R2V requires the `ref2va` family, its Qwen3VL encoder and separate audio/video VAEs; T2V/I2V `fl2va` is a different role. Keep H3 as a challenger if a measured limitation warrants it. Existing [H3 discovery](minimax_h3_20261003.discovery.json) establishes dated catalog presence only.

For Chewie, first judge the design and a simple head/arm gesture. Then test one visible hand touching a deck or fader. Fur, muzzle, hand anatomy, equipment contact and a larger silhouette need their own review; a human replacement mask may be too small. Human-rap success would not validate those details.

## Song timing and mouth movement

The first candidate for exact recorded vocals over selected footage is `api_sync_so_lip_sync_video`: `LoadVideo + LoadAudio -> SyncLipSyncNode -> SaveVideo`. The [retained upstream graph](upstream/api_sync_so_lip_sync_video.json) selects `sync-3` and defaults to `bounce` for unequal durations. Supply matching trims and inspect that setting so a short performance is not silently reversed to fill audio. Current public schema and local graph are research evidence; account support, compiled inputs, cost and execution remain unverified. Sync is a paid partner operation; check its quote and run authorization before submission. [Official template](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/api_sync_so_lip_sync_video.json), [node implementation](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_api_nodes/nodes_sync_so.py).

Prefer one isolated lead-vocal stem, preserve its silences and song timecodes, and retain the full mix for editing. Use a visible face and a continuous shot with suitable mouth motion. Fast rap, teeth/grill stability and nearby tattoos remain project-specific tests. [Sync input guidance](https://sync.so/docs/compatibility-and-tips/improving-lip-sync-quality).

For a new performance, LTX's `LTX-2.5_A2V_Two_Stage_Distilled.json` accepts fixed input audio and an optional first frame. It generates the movement; it does not retain another clip's exact gestures. Its documented BF16 components differ from our executed quantized I2V recipe, so reuse of that success is not dependency validation. Check audio trim, actual frame count and rounding of duration. Cloud catalog ID is not yet established. [Audio-to-video guide](https://docs.ltx.io/open-source-model/usage-guides/audio-to-video), [official graph](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/2.5/LTX-2.5_A2V_Two_Stage_Distilled.json).

Documented Dub-It takes rewritten dialogue text and synthesizes speech; its current validated family is LTX-2.3. Reserve it for an optional spoken cameo rather than treating it as the recorded-song path. [Dub-It guide](https://docs.ltx.io/open-source-model/feature-guides/audio/dub-it-beta). Chewie/Jabba mouth support is unproven; Vader/Boba helmet shots can use physical performance without visible mouth synthesis.

## Finishing and assembly

**October 4 MiniMax addition:** official `api_minimax_h3_max_r2v` includes an optional H3 Regenerate to 2K branch. It retains the unmodified H3 original and the effective prompt/reference inputs. This is a conditional provider-specific alternative, not established support for our LTX/Wan footage. Apply regeneration before post lip-sync, trimming or re-encoding. The [song project](../projects/hon_dolo_strictly_business/README.md#minimax-as-an-alternate-finishing-route) and [shot-plan contract](../projects/hon_dolo_strictly_business/shot_plan.json) record the source requirements, public evidence and comparison checks. No Cloud validation or new run is claimed. This branch is an exception to the general post-lip-sync upscale order in the earlier diagram.

Evaluate `utility_seedvr2_3b_int8_upscale_video` after accepting a take. The official native example uses `seedvr2_3b_int8_convrot.safetensors` and `seedvr2_ema_vae_fp16.safetensors`; current account support is unknown. Begin with one HD derivative and compare it with the original for tattoo lettering, grill, fur, edges and flicker. Retain timing/audio, measure encoded dimensions, and inspect normal-speed playback. Attempt 4K only after that comparison; larger dimensions alone do not establish better detail. [SeedVR2 guide](https://docs.comfy.org/tutorials/utility/seedvr2), [native template](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/utility_seedvr2_3b_int8_upscale_video.json).

The final timeline is an editing project: sequence accepted shots against the full song, cut to musical phrases, match color/exposure, add titles and deliberate sound effects, then verify delivery. Comfy's clip export is useful, but it does not decide the music video's edit. Keep generated ambience separate from the final mix. Editor and delivery format remain undecided; no extra product purchase is needed for this research.

## Next proof tests

These are proposed tests, not an authorized batch. Each waits for appropriate input selection and Cloud preflight.

1. **Hon Dolo performance:** one 3–4-second clip with a visible face, modest head turn and one unobscured gesture. Use Wan Animate 2 if a fresh setting is acceptable; Mix if source-setting preservation matters. Compare source/result at matched timecodes for pose, contact and timing, and compare likeness to the chosen reference. Test movement before adding lip-sync.
2. **Hon Dolo vocal:** one 4–6-second phrase containing fast syllables and a pause. Compare the accepted input shot with one Sync result, or choose A2V if generating the performance. Inspect mouth closures, grill, tattoos, facial proportions, audio alignment and retiming. Do not score an A2V result as an exact-motion-preservation test.
3. **Chewie DJ:** after a simple movement preview, test one deck contact. Compare hand position, contact duration, fur and controller geometry. Keep camera movement modest for this first contact check.
4. **Finishing:** compare one accepted short take with one upscale at the same playback rate. Reject invented detail or increased flicker; record the result before considering 4K.

For every comparison, retain the original source, exact trims, intended changes/preservation, actual graph, compiled settings, prompt, model/version, seed where applicable, output, usage/cost, defects and next decision. Use the existing [decision and feedback procedure](../templates/workflow_intake.md#decision-and-feedback). A still's approval does not approve its motion; execution does not imply acceptance.

## Evidence and resumption

The latest read-only Cloud checks in this investigation returned **authentication required**, including server info and template searches. Earlier successful authentication and the saved artifacts remain historical evidence; no cause for the renewed failure is established. No new generation, model import, purchase or Cloud workflow save occurred during this investigation.

After reconnection, verify server info and a known saved-workflow read, then check only the chosen next candidate: template revision, every required model/node, source inputs and compiled graph. Keep heavy official video templates intact and inspect their exposed controls rather than rebuilding their internals by hand. Save the exact graph and metadata when a candidate is adopted for testing. Unknown support, price and quality stay unknown until measured.

## Pathfinder breadcrumbs

The relevant existing lessons are [video routes](../../../../../../Pan_Handlers/Help/content/video_routes.py), [H3 reference roles](../../../../../../Pan_Handlers/Help/content/h3_candidate.py), [video and audio handoff](../../../../../../Pan_Handlers/Help/guides/video_handoff.py), [image editing](../../../../../../Pan_Handlers/Help/guides/image_edit_lab.py) and the [tutorial ledger](../../../../../../Pan_Handlers/Help/CFA_TUTORIAL_LEDGER.md). If the sibling checkout is absent, this plan, the local workflow index and the linked official sources provide the production fallback.

Bounded follow-up for Panhandler Nova: add the distinction between recorded audio, generated dialogue and final music mix; link this five-family plan from the current video route lesson; preserve reviewed/validated/executed/accepted labels. The newer LTX-2.5 A2V candidate, Mix segmentation/FPS findings and H3's empty performance slots are research updates, not tested recommendations. Leave app schema changes and CFA graph execution out of that documentation task. Return adopted teaching changes through the [manual handoff](../../pathfinder_handoff/README.md).
