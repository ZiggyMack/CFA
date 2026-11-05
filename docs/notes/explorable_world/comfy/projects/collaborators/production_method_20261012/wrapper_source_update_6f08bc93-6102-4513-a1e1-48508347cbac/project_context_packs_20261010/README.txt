CFA COLLABORATOR PROJECT CONTEXT PACKS

Start with UPLOAD_MAP.txt for the latest immutable release and exact per-recipient files. Each folder is standalone. ZIPs are transport containers to extract, not assumed project inputs. No uploads or provider tasks are performed by packaging.

The shared core lives in source/01_CFA_PROJECT_CONTEXT.txt and source/02_CURRENT_WORK_AND_REVIEW.txt. source/recipient_contexts.json holds recipient wrappers, actual identity source paths and small tailored supplements. Change those only from new decisions or evidence; preserve author identities in their canonical locations.

From the CFA repository root, rebuild with:
python -X utf8 docs/notes/explorable_world/comfy/projects/collaborators/project_context_packs_20261010/build_packs.py
Verify the latest snapshot and source hashes with the same command plus --check. Each input change creates a new content-addressed release; prior releases stay dated history. Update uploaded project copies through a separate, explicitly recorded handoff and readback.

Each pack's SOURCE_COPY_NOTE.txt records identity authorship, exact copy hashes and registry differences. Release MANIFEST.json records all copied file/source hashes and the inputs behind curated summaries. Claimed capabilities, actual file bytes and reviewed outputs remain distinct. The scoped .gitattributes preserves the captured bytes on another computer.

Independent Phase 0 baseline bytes are intentionally withheld from Kimi, DeepSeek and Qwen project memory until each access result is frozen. Existing images/video remain separately attached task inputs.
