# Run the Observatory on a cloud PC

September 12, 2026. Ziggy clarified that the current PC should not set the final
world's visual ceiling. Improve the world before further story iteration, and
prepare to run the game on a remote GPU.

**Current status:** the game and an optional modern-GPU launcher are prepared
locally. The [prepared test ZIP](../../../games/observatory/builds/Observatory-cloud-test.zip)
is about 100 MB, with an adjacent SHA-256 manifest. No cloud PC has been purchased, provisioned, connected, or benchmarked.
Comfy OAuth also needs a separate recovery; it is not required to run the game.

**Runpod alternative, September 12:** Ziggy requested the official agent setup.
The Runpod Codex plugin and eight bundled skills are installed. Hosted OAuth
sign-in and a live Pod-list check passed; the account returned no Pods,
including cluster members. [Runpod setup and proposed test](RUNPOD.md) covers a Linux GPU
desktop route and the differences from the Windows plan below. No Runpod
compute or storage was provisioned. Evaluate interactive streaming before
choosing it as the everyday workstation.

**Current recommendation: Shadow PC Gaming, Power, month to month.** Ziggy
confirmed that the AirGPU OS dropdown offers only BYOL and that no separate
Microsoft OS license is available. AirGPU is therefore set aside for this
experiment. The [US offers page](https://shadow.tech/us/shadowpc/offers/)
advertises **Power at $54.99/month** and **Power Lite at $43.99/month**.
Power is the proposed choice for sustained world-building sessions and more
included storage; neither plan has been purchased or activated.

The [official Gaming specifications](https://support.shadow.tech/hc/en-us/articles/31001157820049-Shadow-PC-Gaming-Offers-Hardware-Specifications)
list **Windows 11 included, RTX A4500 with 20 GB VRAM, 28 GB RAM and 512 GB SSD**
for Power. Current limits are **210 hours/month**, **six hours per session**,
and **30 minutes idle before shutdown**. Power Lite uses the same GPU/RAM but
has 256 GB storage, 120 hours/month and four-hour sessions. The recommendation
is for the consumer Gaming offer; checkout must confirm the US region, actual
availability, included Windows, final price and current limits. Our web check
did not complete a US checkout, and the displayed public price is not an order.

**Next handoff:** Ziggy runs the official
[Washington D.C. speed test](https://speedtest.uswdc01.shadow.tech/) from the
actual PC/connection before subscribing. Use the Shadow Windows application
for the first stream. The prepared Windows ZIP and Godot project can be used
on that remote desktop; provider-specific setup replaces the earlier
AirGPU/Moonlight instructions below.
Boston is in the [published continental-US service area](https://support.shadow.tech/hc/en-us/articles/33563634214161-Frequently-Asked-Questions-FAQ).
Shadow [normally assigns the data center](https://support.shadow.tech/hc/en-us/articles/34401117134481-Requesting-a-Datacenter-Migration-for-Your-Shadow-PC)
according to location and availability. Washington D.C. is our first test
endpoint, not a confirmed allocation; AirGPU's 22 ms estimate does not transfer.

## Boston connection and first test settings

Ziggy supplied the following Speedtest result on September 12, 2026. Use
**Boston, Massachusetts** as the connection location. These are user-supplied
measurements to a Boston test server, not a measured cloud-PC route.

| Measurement | Reported result |
| --- | ---: |
| Download | 96.32 Mbps |
| Upload | 38.35 Mbps |
| Idle latency | 16 ms |
| Download-loaded latency | 175 ms |
| Upload-loaded latency | 316 ms |

The available throughput is promising for a 1080p test. Latency rises when the
connection is busy; avoid simultaneous bulk Drive transfers or downloads during
the initial play test. This result alone does not locate the bottleneck or
measure jitter, packet loss, decoding time, or cloud input-to-display latency.

**Earlier AirGPU comparison, now set aside: RTX A5000,
US East (New York II).** Ziggy's
September 12 AirGPU configurator screenshots show that option at **22 ms**,
versus A10G/Northern Virginia at 33 ms, the selected RX 9060 XT/Charlotte at
44 ms, and L40S/Ohio at 47 ms. These are provider-displayed connection estimates,
not our measured input-to-display latency. The A5000 offers a promising balance
of rendering capacity and the lowest displayed latency. A10G/Northern Virginia
is the fallback if the A5000's actual quote or availability is unsuitable.

The earlier screenshot's Ryzen/8-vCPU/16-GB configuration belonged to the
selected AMD option and did not establish an A5000 quote. It showed **200 GB
storage at $10/month ($0.333/day)**. These are retained comparison details,
not active provisioning instructions.

**License requirement:** Ziggy confirmed that no separate Microsoft OS license
is available. The latest screenshot selects **Windows 10 (Bring your own
license)**; switching from the earlier Windows 11 BYOL option has not resolved
this. Ziggy then checked the dropdown and confirmed **BYOL is the only option**.
No separate license purchase is proposed to continue this experiment.

The latest screenshot quotes **$1.85/hour plus $0.23/day storage**, excluding
VAT, with **8 vCPUs / 48 GB RAM**, a stream ceiling of **4K60 / 50 Mbps**, and
**100 GB at $7/month**. The selected GPU is outside the screenshot, so this
cannot yet be attributed to the recommended A5000. This is a quote, not a
purchase or a measured result.

Start with **1920x1080, 60 fps, H.264, 20 Mbps**, preferably over Ethernet.
Use the available Shadow client settings to start with this target. The
AirGPU screenshot's stream ceiling does not configure a Shadow session.
These are our test settings, not measured performance. Compare 720p60 if
decoding is slow, and 1080p30 if needed to distinguish decoder limits from
host rendering or network delay. Keep the world running on the remote GPU.

**Earlier AirGPU client research (not required for Shadow): Moonlight.** Its
[current v6.1.0 requirements](https://github.com/moonlight-stream/moonlight-qt/releases/tag/v6.1.0)
specify 64-bit Windows 10 1809/Server 2019 or newer. The
[setup guide](https://github.com/moonlight-stream/moonlight-docs/wiki/Setup-Guide#moonlight-client-setup-instructions)
describes hardware H.264 decoding and older-device limits. Its legacy Windows
7 wording should not override the current release notes. Parsec's
[published client minimum](https://support.parsec.app/hc/en-us/articles/32381568346644-Hardware-and-Software-Compatibility)
is newer than the i7-2600/Quadro 2000, so do not promise that client will work
well on this PC. No streaming client was installed during this review.
The local OS check returned **Windows 10 Pro 22H2, build 19045, 64-bit**, which
meets that Moonlight release's OS requirement; hardware decoding remains untested.

For Shadow, its official
[Washington D.C. network test](https://speedtest.uswdc01.shadow.tech/)
can check the route before subscribing. Its
[testing guide](https://support.shadow.tech/hc/en-us/articles/32731862190609-How-to-Troubleshoot-Your-Internet-Connection-for-Shadow-PC)
calls 30 ms or less ideal and also checks jitter. That result would apply to
Shadow's test endpoint, not prove AirGPU connectivity or end-to-end play quality.

## How the pieces fit

| Component | Job |
| --- | --- |
| Comfy Cloud | Generate candidate images, video, and other supported assets |
| Cloud Windows PC | Run the Godot editor, asset tools, and playable world on a remote GPU |
| Ziggy's existing PC | Display the stream; send mouse, keyboard or controller input |
| Git | Version source, workflows, provenance and selected runtime assets |
| Google Drive | Archive original media and selected builds |

Streaming the desktop moves real-time rendering off the local GPU. The local
machine still needs to decode the stream, and connection latency/jitter affect
control response. A normal browser export of the game would still render on
the browser's local GPU; it would not accomplish this offload.

More compute supports richer lighting, denser models, animation and larger
environments. It does not create those assets automatically. The same Godot
project can continue; moving to a cloud PC does not require rewriting it in
another engine.

## Two candidates checked

| Service | Fit | Verified details and limits |
| --- | --- | --- |
| [Shadow PC](https://shadow.tech/us/shadowpc/offers/) | Current recommendation: Power for a month of world-building and streaming tests | Included Windows 11; public price $54.99/month. Actual regional availability, checkout total and network route remain unverified. |
| [airgpu](https://airgpu.com/) | Set aside: the available OS requires a license Ziggy does not have | Own software and Parsec/Moonlight streaming were suitable; supplied quote was $1.85/hour plus storage, excluding VAT, with the selected GPU offscreen. No purchase performed. |

My recommendation is one month on the included-Windows Power offer after the
network test and checkout review. No spending has been authorized for a
specific cloud-PC plan. The first session should establish streaming comfort
and actual Forward+ rendering before committing to longer use.

Shadow's [published requirements](https://support.shadow.tech/hc/en-us/articles/33563634214161-Frequently-Asked-Questions-FAQ)
recommend at least 15 Mbps down and 5 Mbps up, and caution that some devices
from 2012 or earlier may have problems. The actual HP/decoder/network path
therefore needs a stream test. Prefer Ethernet and a nearby data center.

## First session

1. Use Boston and the Shadow network test above. Review the US Power offer,
   available data center, included Windows, total charges and session limits
   before provisioning. Ziggy handles account/payment and streaming login.
   Install the Shadow Windows application for the initial connection.
2. Copy only the prepared cloud ZIP or its whitelisted portable files to the
   remote desktop. It excludes local saves, logs, API keys, and the wider CFA
   repository. Installing a remote editor/assistant is a later step; this
   local session does not automatically gain control of that desktop.
3. Run **Play.cmd** remotely first. Test camera movement, an interaction, and
   save/reopen at 1080p. Record the host GPU, frame timing, stream latency,
   visible artifacts and Ziggy's comfort. Lower the stream resolution if
   decoding or bandwidth is the problem.
4. Run **Play_High_Quality.cmd** on that modern GPU. It selects Forward+ at
   1920x1080, 4x MSAA, larger shadows, screen-space ambient occlusion, indirect
   lighting and reflections, plus restrained glow. The actual remote render
   is **untested**; tune it from captures, rather than calling it validated.
5. Compare the same courtyard and pump views. Keep improving the actual models,
   materials, vegetation and lighting toward the desired atmosphere.
6. Save work and shut down the cloud PC after the session. Stopping a Shadow
   machine does not cancel its monthly subscription; review renewal separately.

The ordinary launcher remains available for local checks. The new launcher
starts whichever computer it is run on; it does not connect to a cloud service.
Its effects use Godot's documented
[Environment settings](https://docs.godotengine.org/en/stable/classes/class_environment.html).

## After visual direction is convincing

Resume story feedback and the separate eight-second dialogue-rewrite experiment.
PanHandlers Nova's review was read: an already available Cloud model should be
reused when suitable; needless imports and credentials are not prerequisites.
The requested original clip → replacement audio → lip-sync output → critique
is still an unexecuted experiment, not a result supplied by this visual pass.
