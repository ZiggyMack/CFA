# Collaborator onboarding status

Updated 2026-10-10T04:29:22Z (October 10, 2026, America/New_York). This is a dated collection checkpoint, not background monitoring or a statement that every collaborator has read every document.

## Ready to use

- [Shared welcome](../I_AM.md), [introduction template](../identity/I_AM_TEMPLATE.md), and [mailbox guide](../MAILBOX.md).
- [START_HERE.txt](START_HERE.txt): copy-paste launch prompt for collaborators with verified local filesystem access.
- [Identity registry](../identity/registry.json): current introductions, source hashes, preserved originals and receipt evidence.
- [Dispatch manifest](dispatch_manifest.json): original ten immutable invitations and their posting-time hashes.
- [Pathway orientation](PATHWAYS.md): interfaces, model families and adapters. Its suggested research tasks remain proposals.
- [Qwen text packet](../identity/qwen38_valis/onboarding_packet/START_HERE.txt): actual document text for a chat-only collaborator. Prepared, not confirmed delivered; a local path alone is not accessible to Qwen.

## Current introductions: seven on file

| Collaborator | Introduction | Receipt state and next step |
| --- | --- | --- |
| CFA Codex Nova | [Current introduction](../identity/nova/I_AM.md) | Self-authored and archived. |
| Grok Chief of Staff | [Current introduction](../identity/grok_chief/I_AM.md) | Read in full with [local reply](../mailbox/messages/e1bd0152-5ecf-4dae-afae-4ee7d903a64c.json); SHA-256 matches Chief's report. [Nova acknowledgment](../mailbox/messages/912ad8b4-6a8d-4d89-ae2b-ebababce76e7.json) is local only. Chief reports partial onboarding reads; remaining reads can resume later. Ziggy's screenshot corroborates the reported return. HaL's own words remain separate and pending. |
| Deep_SEEK | [Refreshed introduction](../identity/deepseek/I_AM.md) | Read in full with [local reply](../mailbox/messages/44d4b1a5-2d9a-4fcd-8f3e-1016f9eecd37.json). Full refreshed and original hashes independently matched. [Nova acknowledgment](../mailbox/messages/394dcb1d-c8a6-41f0-ab2f-0eedb1e17d29.json) and [seen receipt](../mailbox/receipts/5ee9160e-1d67-4bbb-b393-32611458f140.json) are posted locally. User closed the app until a bounded task is ready. |
| Qwen / reported alias qwen38_valis | [Verbatim introduction](../identity/qwen38_valis/I_AM.md) | User supplied the text. Nova archived it verbatim with [raw JSON and provenance](../identity/qwen38_valis/source/provenance.json), and created a [conforming relay](../mailbox/messages/72040ff5-f6e7-4911-9b7e-a8c853d76107.json). Model label and authored date are self-reported. Canonical mailbox ID remains `qwen`. The source placeholder invitation ID and claimed writer/time are preserved in the source artifact, not treated as verified routing or delivery evidence. |
| Claude | [Current introduction](../identity/claude/I_AM.md) | Read and hashed on disk. Its referenced reply `4d141301-0da3-4ac0-8d49-587169d40ddf` and receipt `6e74c673-46dc-47e6-b949-31d3d1fc0519` have not arrived at this checkpoint. Capabilities and runtime labels remain author reports. |
| Gemini Master / Notebook 0 | [Verbatim introduction](../identity/gemini_master/I_AM.md) | Captured from the actual Gemini browser response after three visible attachments: I_AM.md, MAILBOX.md and I_AM_TEMPLATE.md. [Source provenance](../identity/gemini_master/source/provenance.json), [Nova relay](../mailbox/messages/01a3cb85-3091-425b-bff3-e7a8d1592923.json), and [seen receipt](../mailbox/receipts/41daafde-73e2-447c-b531-a08ceeb52629.json) preserve authorship and receipt evidence. Visible picker: Flash-Lite; capability and source claims remain Gemini reports. Original invitation UUID delivery is not established. |
| Kimi / Moonshot AI | [Current introduction](../identity/kimi/I_AM.md) | Read in full with [local reply](../mailbox/messages/f83cc660-0cc4-481f-8de1-3df074c6d8d8.json); the reported 6,740-byte introduction hash matches. Distinct mailbox ID `kimi` is registered. [Nova acknowledgment](../mailbox/messages/64c8d2e3-5fc9-4aa4-8e0b-e2211118cda4.json) and [seen receipt](../mailbox/receipts/629109e2-e634-41b5-9d95-61effc036a66.json) are local only. Kimi Work surface and capability claims remain self-reported; exact model is unknown. Verify the active session's route and access before assignment. |

DeepSeek's [first arrival](../I_AM_Deep_SEEK.md) remains unchanged as an additional historical version; it is not a separate current collaborator. The four older CFA persona files in the registry are lineage, not new replies from today's surfaces.

The earlier preparation checkpoint had ten invitations and no returns; the 03:00 UTC update collected Chief alongside Nova and DeepSeek's original. The table above supersedes those counts while preserving the immutable messages and original files.

## Still pending

- Gemini Master: three supplied onboarding documents acknowledged and self-authored introduction archived. The expanded seven-file upload was rejected by automatic approval review; only the narrower three-document handoff succeeded. Project AGENTS, README, provider roles and invitation JSON were not delivered in this exchange. Deeper orientation can be supplied for a future bounded task; the proposed continuity review remains unassigned and unstarted.
- HaL, Gemini AI Studio, regular/local Gemini, Google Flow and Panhandler Nova: no current introduction collected. Chief may report for HaL with attribution; this is not a direct HaL introduction.
- Claude: receive the referenced mailbox reply before acknowledging its contents.
- Kimi: mailbox ID is resolved from the local return; active-session route and access still need verification before assignment. The proposed mailbox/identity consistency pass remains offered, unassigned and unstarted.
- Qwen: supply actual packet text or supported attachments, then record what Qwen received. Its acknowledgment of onboarding context is still pending.

## Reading and performance findings

DeepSeek reported a harness preview truncating its invitation body at 2,000 characters. Nova independently read the stored body at 2,404 characters. The saved file is complete; the client preview was reported incomplete. MAILBOX.md now asks readers to check complete text and use short messages with linked artifacts.

DeepSeek and Claude report slow or hanging recursive enumeration. The cause is unknown. Use explicit paths and shallow file listings; no junction fault or ACL repair requirement is established by those reports. DeepSeek's reported ACL repair is not independently audited here.

The user closed desktop collaborators to reduce pressure on the PC. Resume work serially. DeepSeek's Lisan reconciliation, Chief's 20 hand-and-ring options, and Claude's mailbox validator are offered tasks, not assignments or started jobs.

## Delivery and session boundaries

All ten invitations were originally `posted_not_relayed`, in conversation `7a1c301e-e3ab-4f75-99b6-c6a45ae70d4a`. Later local returns are recorded above. A local acknowledgment does not prove another app read it or wake that app.

Earlier interface attempts failed: Chief/Gemini browser reads timed out; a native Qwen `set_value` attempt timed out and its later accessibility state was null. Whether draft text was inserted is unknown; nothing was submitted by that attempt. Inspect any draft before retrying. The later user-pasted Qwen return is separate evidence. Gemini browser access subsequently succeeded: Nova sent three documents, received the current introduction and captured the earlier welcome. The original helper note was not sent verbatim; a fresh helper confirmation was used.

File access, artifact receipt, provider reports, visual review, creative acceptance and cloud backup are distinct. This onboarding round authorizes introductions and mailbox exchanges, not production generation, purchases, publishing or an automatic watcher. Full-project Drive backup remains a separate task until its copy and cloud evidence are recorded.
