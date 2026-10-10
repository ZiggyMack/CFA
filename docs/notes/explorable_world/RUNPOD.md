# Runpod connection and Observatory experiment

September 12, 2026. Ziggy requested setup using Runpod's
[agent setup guide](https://docs.runpod.io/agent-setup.md), and asked whether
Runpod could be an alternative to Shadow.

## Verified setup

| Component | Observed state |
| --- | --- |
| Official marketplace | Added from `https://github.com/runpod/runpod-plugins-official.git` |
| Codex plugin | `runpod@runpod` version `1.2.0`, installed and enabled |
| Source revision | `4912d93e5ac4746acf6415ca395413eabf0564f4` |
| Bundled skills | Eight: `runpod`, `runpod-mcp`, `runpodctl`, `flash`, `companion-clis`, `runpod-usage`, `runpod-templates`, `runpod-migrate` |
| Hosted MCP | `runpod`, enabled, Streamable HTTP at `https://mcp.getrunpod.io/` |
| Authentication | OAuth completed successfully; Codex reports `o_auth` |
| End-to-end check | Passed: live `list_pods` with `includeClusterPods: true` returned `{"pods": []}` with no error |
| Cloud resources | This setup created no Pods, volumes or endpoints and submitted no paid jobs |

Installed through Codex's native, noninteractive commands:

```powershell
codex plugin marketplace add https://github.com/runpod/runpod-plugins-official.git --json
codex plugin add runpod@runpod --json
```

Verified using the same Windows account context that performed the installation:

```powershell
codex plugin list --marketplace runpod --json
codex mcp get runpod --json
codex mcp list --json
```

The installed package lives at
`~/.codex/plugins/cache/runpod/runpod/1.2.0/`; its skill and MCP files were
inspected locally. The version installed includes eight skills, superseding
the setup page's smaller inventory. Native plugin installation supplied the
skills together, so no duplicate global `npx skills` installation was needed.
The MCP server was registered by the plugin; no second registration was added.

Local `codex-cli 0.154.0-alpha.6.2` supports `plugin add`, allowing the assistant
to complete the install that the Runpod page describes as a UI step. Its MCP
syntax uses `--url`, not the page's `--transport http` syntax. If registration
is ever genuinely missing, verify local help before using:

```powershell
codex mcp add runpod --url https://mcp.getrunpod.io/
```

An initial sandbox-side check used a different Windows account context and
reported no installation. Verification under the installing account confirmed
both the enabled plugin and server. Do not reinstall or rewrite configuration
based solely on that sandbox mismatch.

The user-selected setup guide defers the Runpod CLI, Flash SDK and API keys
until needed. Follow that scope for this setup even though the bundled router
recommends a key for broader CLI work. OAuth authenticates the hosted MCP;
future CLI-only work may need separate setup. No Runpod CLI, SDK, local GPU
runtime, model weights or API key was installed or provisioned here.

## Connection verification and recovery

**Verified follow-up:** Ziggy's first screenshot showed a signed-in Runpod
website, while the Codex connection still reported `not_logged_in`. Started
`codex mcp login runpod` and opened its authorization URL in the browser.
Ziggy completed that separate consent flow; the CLI reported success, the
Runpod tools became available in this session, and a live Pod-list request
returned an empty list, including cluster members. Setup and read access are
now verified. No GPU or storage resource was created to perform the check.
Do not preserve temporary authorization URLs or callback values in this guide.

If reconnection is needed later:

In **Codex in VS Code**, open the gear menu, then **MCP servers**. Find
**runpod** and choose **Authenticate**, then complete the browser sign-in.
If the entry or new skills are missing, use **Restart extension** and reopen
the list. The installed skills should become available on a subsequent turn
after the client refreshes. The plugin does not need to be installed again.
[Codex MCP instructions](https://learn.chatgpt.com/docs/extend/mcp)

The assistant then verifies the tools are available and performs one read-only
Pod-list request. A successful empty list passes. An enabled configuration or
browser confirmation alone is not the end-to-end check. Do not create a Pod
merely to prove authentication. Record a failed connection accurately and
continue independent local work.
[Runpod MCP documentation](https://docs.runpod.io/get-started/mcp-servers)

## What this adds to our project

Runpod Pods supply Linux containers with GPU access. We can install and operate
our own ComfyUI, custom nodes and compatible model files there, instead of
depending on Comfy Cloud's available node catalog and model-import UI. That
would be a separate environment with its own storage, maintenance and billing;
our existing Comfy Cloud subscription does not run or pay for a Runpod Pod.
[Pod overview](https://docs.runpod.io/pods/overview)

For a **playable world**, Runpod documents a GPU-accelerated Ubuntu browser
desktop using Kasm/VNC. This is a possible Linux workstation for Godot, with
more setup than a ready-made Windows streaming desktop. Runpod's public Pods
documentation explicitly excludes Windows and UDP networking. Do not carry
the earlier Windows ZIP or Sunshine/Moonlight/Parsec assumptions straight into
this route. The desktop article's deployment link did not establish a specific
current template; inspect the actual template/image before provisioning.
[Desktop guide](https://www.runpod.io/blog/gpu-accelerated-virtual-desktop-runpod),
[networking](https://docs.runpod.io/pods/configuration/expose-ports)

Our Observatory uses GDScript; the inspected project has no C# project or
GDExtension. A Linux Godot executable can run its source project, while a
packaged delivery would need a Linux export and launcher. This is a portability
assessment, not a tested remote run. The current Compatibility renderer needs
OpenGL 3.3; Forward+ needs a suitable Vulkan environment.
[Godot requirements](https://docs.godotengine.org/en/stable/about/system_requirements.html)

GPU compute access alone does not prove accelerated desktop rendering. Check
the graphics/display driver capabilities and the renderer Godot actually
reports. CPU software rendering such as `llvmpipe` is not a successful GPU
workstation setup. Accelerated streaming encoding also needs the appropriate
video capability.
[NVIDIA container capabilities](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/docker-specialized.html)

## First proposed GPU test

1. Inspect live nearby GPU availability, a specific authenticated desktop
   template/image, the storage mount and the full hourly/storage quote. Prefer
   a graphics-capable RTX GPU for this test. Use Boston as the user location;
   earlier provider latency estimates do not measure Runpod's route.
2. Prepare one bounded on-demand test and its shutdown instructions, with the
   price and test duration concrete before seeking any needed spending approval.
   No GPU choice or paid deployment has been authorized by the agent-setup task.
3. Put only the required project/build files on persistent storage, install the
   matching Linux Godot version, and open the project in the desktop. Keep
   credentials and unrelated CFA material out of the transfer.
4. Test at 720p or 1080p: editor use, walking, relative mouse capture, Escape,
   an E interaction and audible water. Verify the GPU renderer and record
   rendering/streaming behavior separately. A visible desktop or successful
   `nvidia-smi` alone does not pass. KasmVNC documents a game cursor mode, but
   its behavior in our actual desktop remains to be tested.
   [KasmVNC client controls](https://www.kasmweb.com/kasmvnc/docs/master/clientside.html)
5. Save a small project change, stop/restart, and confirm it survives. Then
   compare richer rendering if the desktop and stream are usable. Review the
   result before adopting Runpod as the everyday play/development machine.

Container storage is disposable. A Pod volume survives stopping but is lost
when the Pod is terminated; a network volume has an independent lifetime and
ties placement to its data center. Verify the chosen desktop's actual mount
instead of assuming `/workspace` or `/home`. Persistent storage can remain
billable after GPU work stops. Keep the Google Drive archive and source-control
policy from [STORAGE.md](STORAGE.md); the local G: mount is not automatically
available in a Runpod container.
[Storage types](https://docs.runpod.io/pods/storage/types),
[network volumes](https://docs.runpod.io/storage/network-volumes)

Runpod is a strong candidate for a configurable asset workshop and an
experimental Godot desktop. Interactive play still needs this feasibility
test. [CLOUD_PLAY.md](CLOUD_PLAY.md) preserves the Shadow/AirGPU comparison;
no cloud gaming provider has been selected or benchmarked by this setup.
