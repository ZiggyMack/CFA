# Storage and cloud execution

**Standing instruction from Ziggy, September 12, 2026:** use cloud processing and storage wherever practical. Use D: for necessary local downloads. Keep source, design, and reproducible instructions in Git, and keep the local working set small enough for this PC.

## Where each part belongs

| Material | Default home | What stays in Git |
|---|---|---|
| Game code, scenes, story, documentation, prompts | CFA repository on D:, synchronized with its Git remote when committed and pushed | The files themselves |
| Workflow JSON, model/version references, asset records | CFA repository; saved working recipes also in Comfy | Sanitized recipes, stable identifiers, hashes, sizes, and retrieval records |
| Checkpoints, LoRAs, encoders, and other model weights | Provider model library and Comfy Cloud imports | Source and exact version references; no local model collection |
| Generated originals, high-resolution textures, video, large meshes | Cloud production workspace plus a persistent cloud asset archive | Asset records; small previews only when useful |
| Assets needed by the active playable chapter | Optimized derivatives in games/observatory/assets/ on D: | Small accepted assets; evaluate Git LFS for larger versioned game assets |
| Engine downloads, temporary files, caches, packaged builds | Ignored directories on D: | Download/build instructions and required licenses |

Comfy supports importing model files directly from Civitai or Hugging Face into Cloud. Use that route without first downloading the weights to this PC. [Cloud import documentation](https://docs.comfy.org/cloud/import-models)

GitHub stores our shared source history, but a local clone still occupies disk space. Ordinary GitHub repositories reject files above 100 MiB; bulk model and media storage belongs elsewhere. Git LFS stores references in Git and separate binary objects, which still occupy local space when retrieved. It is an option for selected game assets, not a reason to mirror a model catalog. [Cloning](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository), [large files](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), [Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)

## Local paths and working practice

- Repository: `D:\Documents\CFA`.
- Necessary downloaded outputs: `D:\Documents\CFA\docs\notes\explorable_world\comfy\outputs`.
- Disposable downloads or tool caches: `D:\Documents\CFA\.cache` (create task subfolders as needed).
- Agent-authored helper scripts, diagnostic exports, and temporary downloads also belong in a task subfolder of `.cache` on D:. Give subprocesses an explicit D: output/temp destination when supported; do not assume the Windows default temporary directory is on D:.
- Active game and its accepted derivatives: `D:\Documents\CFA\games\observatory`.
- Runtime state: the game's existing `.local` directory, or the portable build's `user_data` directory, both on D:.
- Google Drive content cache: `D:\appdata\Local\Google`, confirmed by Drive's relocation notification supplied by Ziggy. Drive manages this directory; it is separate from disposable project scratch.

Preview and compare in the cloud where possible. Download only selected references or derivatives needed by the current chapter or a concrete inspection. Before a substantial download, check the destination's free space and allow for extraction, conversion, and temporary copies. Use explicit D: destinations; manual browser downloads should use Save As to the appropriate D: folder. Browser/OS caches have not been globally relocated.

Keep one active working set and create portable builds when needed for delivery or validation. The local game remains a small client for play and interaction testing; image/video generation and model execution stay remote. Full cloud rendering or streamed gameplay would be a separate engine-hosting task and is not configured here.

The scoped ignore files exclude model-weight suffixes even when accidentally placed beside a workflow or game asset. Existing rules exclude generated output, engine cache, and build directories. Ignore rules prevent ordinary accidental staging; they neither upload files nor free disk space.

## Preserve results without keeping every local copy

**Google Drive archive preparation:** use `G:\My Drive\CFA Observatory`. Ziggy's September 12 browser screenshots confirm the project folder and its Originals, Approved Assets, and Builds subfolders reached Drive online. They show 672.49 GB of 2 TB used. The pump files match locally; their online contents and independent retrieval still need verification. The earlier `D:\Google Drive` destination appears to be an older archive. Comfy's production workspace and temporary download URLs are not evidence of an independently recoverable archive. Its published retention policy does not establish a permanent backup guarantee. [Comfy retention policy](https://docs.comfy.org/support/data-retention)

For each retained original, record provider, stable asset/job identifier, object version where available, byte size, hash, and the date retrieval was verified. Use the storage fields in the [run-record template](comfy/templates/run_record.json). Keep credentials and expiring signed URLs out of Git. A pointer without a retrievable object is not a backup.

When a cloud archive is connected, prefer provider-to-provider transfer when supported; otherwise use a bounded D: staging copy. Verify the stored result before retiring its only local copy. The existing pump PNG remains on D: because its independent backup is unverified. No assets were deleted during this storage pass.

## Google Drive archive setup

`G:\My Drive` is accessible through the local filesystem outside the sandbox. Ziggy identified it as the live Drive mount. The initial `D:\Google Drive` copy did not appear online, so the project now uses G: and preserves the earlier D: copy. There is still no authenticated Drive API/connector in this session. Local mount access does not prove an upload completed.

Created **G:\My Drive\CFA Observatory** with **Originals**, **Approved Assets**, and **Builds**. The first test is **Originals\pump_concept_v001**: six content files totaling 929,950 bytes plus an [archive receipt](comfy/workflows/pump_concept_v001.drive_archive.json). They contain the original PNG, run-record snapshot, editor/execution/template graphs, and prompt. Every content file matches its source SHA-256 and size; the receipt matches its project copy. No existing files were overwritten and the source PNG remains in place.

The receipt records confirmed G: mount access, matching local copies, and browser-confirmed synchronization of the project folder structure. File-content upload and independent retrieval remain unverified: the screenshots show the three immediate subfolders, not the pump files. Its previous-attempt entry preserves the D: result and Ziggy's correction. The archived run record is a snapshot whose relative paths refer to the CFA repository; its backup-verification field remains null.

**Next check:** confirm **CFA Observatory → Originals → pump_concept_v001 → pump_concept_v001.png** appears in Drive's web interface, then independently retrieve a copy for hash verification before retiring the only project original. Ziggy's screenshots confirm **Stream files** and the cache relocation to `D:\appdata\Local\Google`. Recheck account capacity before substantial uploads; do not mirror the Git checkout into the asset archive.

Drive for desktop is configured for **Stream files**, confirmed in Ziggy's screenshot. Drive's subsequent notification confirms its local cached files are now stored at **`D:\appdata\Local\Google`**. This replaces the earlier suggested `D:\GoogleDriveCache` path; the actual D: location meets the project storage preference. Keep it separate from the streaming mount and any mirrored folder. The external drive must remain available. [Stream/mirror behavior](https://support.google.com/drive/answer/13401938?hl=en), [cache settings](https://support.google.com/drive/answer/13470231?hl=en)

The September 12 Manage Offline Files screenshot shows **0 bytes offline** and **913 KB cached**, with a **Clear cache** control. The Settings screenshot shows **Limit cache size** unchecked and explicitly states the limit excludes files awaiting synchronization and files made available offline. Recommended starting cap: **10 GB**, if the field permits it; this is a project preference, not an observed or applied setting. Keep the streaming mount on G: when changing the separate cache location. There is no need to clear the current small cache as part of setup.

### Free local space while keeping the cloud archive

With streaming, G: is a virtual view of Drive. Files can remain listed there while their contents live primarily in the cloud; accessed files may be cached locally. The virtual G: mount is separate from the physical cache directory now configured on D:.

- **Inside G:** keep the file and remove its **Available offline** pin if enabled. On Windows this setting is under the file's right-click **Offline access** menu. Drive manages the remaining cache; removing the pin does not guarantee immediate disk reclamation. [Offline access](https://support.google.com/drive/answer/2375012?hl=en)
- **Do not use Delete in a synced folder to clear local storage.** Deletion propagates to Drive and other synced devices. [Drive deletion behavior](https://support.google.com/drive/answer/2375102?hl=en)
- **Separate D: staging copies:** after upload and independent retrieval are verified, an unneeded working copy outside every synced or backed-up folder can be removed without deleting the cloud archive. Confirm the folder is unsynced first. Keep the assets needed by the active game.

The Drive cache can contain edits awaiting upload; do not delete it manually as project scratch. A synced folder alone does not establish independent backup against propagated changes. The G: copy is ready for Ziggy's browser check; the original project files and earlier D: archive have been retained.

## Measured starting point

### October 4, 2026 cleanup

C: reached **0 bytes free** during the Comfy work. Removed **2,909,687,922 bytes (2.71 GiB)** across **3,776 disposable download-cache files** older than 24 hours:

| Cache | Removed bytes |
|---|---:|
| VS Code cached extension download packages (`CachedExtensionVSIXs`) | 1,906,116,212 |
| pip HTTP downloads and wheel cache | 634,453,976 |
| npm package download cache (`_cacache`) | 369,117,734 |

Immediately after cleanup, C: had **2,894,303,232 bytes (2.70 GiB)** available. This remains limited headroom; running applications can change the figure. Deletion was restricted to resolved, inspected cache paths, excluding reparse points and files changed after inspection. No deletions were skipped or failed. The candidate manifest and per-file results are retained outside Git under `D:\Documents\CFA\.cache\storage_cleanup`.

Installed extensions/runtimes, active VS Code update installers, Codex sessions, attachments, credentials, databases, project files, and Drive-managed data were preserved. The actual Codex data directory was about 1.97 GiB; the sandbox profile's Temp directory was empty. The cleanup did not relocate application-managed caches or change system/user environment variables. Future extension/package downloads may repopulate their caches.

The two small Comfy diagnostic directories removed earlier on October 3 are recorded separately in `REPO_LOG.md` and are not included in these totals.

### September 12 baseline

Read-only observations on September 12, 2026; sizes will change:

| Area | Observed size |
|---|---:|
| C: available space | 14.36 GiB |
| D: available space | 382.29 GiB |
| Repository .cache, including Godot executable and ZIP | 257.83 MiB |
| games/observatory, including its portable build | 183.90 MiB |
| docs/notes/explorable_world before this document | 1.22 MiB |
| New game/design files eligible for Git at audit time | 1.34 MiB across 51 files |

The three local project areas total about 443 MiB. Most is the engine, its ZIP, and the portable build's engine copy. The entire repository's committed HEAD file contents measured 236.27 MiB, including preexisting media; this does not measure Git history or all local CFA files. Disk availability came from .NET DriveInfo; PowerShell drive counters were unavailable in the sandbox.

This pass documents the policy and updates local protections. It does not establish that new source files have been committed/pushed or that a cloud backup has been created. No bulk upload, model download, subscription change, or history rewrite was performed.
