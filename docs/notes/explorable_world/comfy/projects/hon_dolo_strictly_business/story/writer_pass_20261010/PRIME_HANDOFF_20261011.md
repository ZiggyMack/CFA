# Prime master handoff — October 11, 2026

Recorded by Claude, lead writer, from Ziggy's handoff in the active session (2026-10-11, about 13:55 America/New_York, 17:57 UTC by the files' timestamps). This is a writer's capture for the record and for CFA Nova's music intake; it is not the intake itself.

## 1. The files, as received

| File | Path (project folder) | Bytes | SHA-256 | Written (UTC) |
| --- | --- | --- | --- | --- |
| Prime audio | `hon_dolo_strictly_business/Hon_DoLo.mp3` | 5,366,974 | `d2283a49caf57d35f01eedf6f26036609c7c51e93dd0771edbf3a37948915532` | 2026-10-11 17:57:08 |
| Prime lyric text | `hon_dolo_strictly_business/Hon_DoLo.txt` | 3,746 | `4d8f867b525ad8cc05d5a78a1ac129ed1a9f46acb288c0698c7646dc35af918b` | 2026-10-11 17:57:39 |

Ziggy's description: the finalized Prime, "the ringer," the version you would hear on the radio today: the trap cut, the second iteration after the trap element was added. It supersedes the October 7 working master for every timing purpose.

## 2. What I measured

Measured with the ffmpeg CFA already bundles (`.cache/hon_dolo_i2v_20261004/python_packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe`), decode only, no file written:

- Decoded audio length: **3:52.76** (about 232.76 s, ffmpeg's progress resolution). Windows metadata rounds it to 3:52 at 182 kbps.
- Audio stream: MP3, 48 kHz, stereo.
- A second stream is an embedded 360 × 360 cover image, not moving video.
- Not measured: BPM, section boundaries, silences, waveform comparison with the earlier masters. Those belong to the intake and the listening pass.

For scale: the October 7 working master was 234.960 s and the October 4 master 233.480 s. Prime is about 2.2 s shorter than the October 7 file. Nothing from either old timebase transfers.

## 3. The lyric text is a new master

`Hon_DoLo.txt` differs from `lyrics.user.v002.txt` in five of twelve sections (details in `STORYBOARD_UPDATE_20261011.md`, section 2). The substantive change is the first bridge, rewritten to the second bridge's wording with "punch it" added and the 88 / light-speed line removed; the rest are small deliveries. Recommendation: register `Hon_DoLo.txt` as lyric master v003 with its hash, keep v001 and v002 as history, and recount the shot plan's section line ranges against it. Card text does not change; cards refer to sections.

## 4. Holds, until the intake and the listening pass are done

- No timing, phrase alignment or lip-sync preparation against any file except `Hon_DoLo.mp3`.
- No card carries a timecode until the timed lyric map exists and its section boundaries and the beat stop have been spot-checked by someone with the recording in front of them.
- The old masters are not deleted; they are dated evidence of the other flavors and may become their own productions later.

## 5. The rescoring request (for Google AI Studio, or any capable listener)

Ziggy proposes that Google AI Studio review the track, as it dissected the inspirational video (`collaborators/video_studies/lil_vader_MwHocQFlw_c_20261009/`; the study folder records the session URL https://aistudio.google.com/prompts/1Oys2niEp9fADle8kUcI5LIeWx5jxbNLl, which showed the title "Visual Analysis of Lil Vader" when I opened it on October 11). His crux: the track has core lyrics, echoes and ad-libs, and mouth matching has to tell them apart. The upload and the run are an operator action for Nova (browser relay) or Ziggy; this folder prepares the request only. Suggested request text, to be sent with `Hon_DoLo.mp3` and `Hon_DoLo.txt` attached:

> You are given a 3:52.76 stereo MP3 and the exact lyric text with its section headers. Produce a timed lyric map for lip-sync planning. (1) Section boundaries: start and end times for each header in the text, in order, from the audio. (2) Line timestamps: start and end for every lyric line within each section, keeping the text's wording exactly. (3) Lane labels: tag every timed line, and where needed every word, as LEAD (the main vocal), DOUBLE (a second take of the same words sung in unison or near-unison, as in the doubled chorus chant) or AD-LIB (echoes, repeated tails, interjections and the trailing "I know" lines). (4) The beat stop: the exact time and length of the stop after the line "Man, don't start." (5) Tempo: BPM and whether the groove sits in a half-time feel; mark the two "punch it" hits. (6) Rests: audible rests longer than a beat after punchlines. Report what you could not resolve as unknown. Return a table with columns: section, line text, start, end, lane, note. Do not paraphrase the lyrics.

Whatever comes back is a provisional map (a model's timestamp is a report). The spot-check before any card gets a time: the twelve section starts, the beat stop, and the two "punch it" hits, against the recording.

## 6. For CFA Nova

Please run `Hon_DoLo.mp3` and `Hon_DoLo.txt` through the music-intake procedure used on October 4 and 7 (hashes, full decode, duration and sample counts, waveform comparison against the two earlier masters, same-words check against v002 with the diff above), point `shot_plan.json` at the new master and lyric file, and record the holds above. Nothing in this folder performs those steps.

— Claude
