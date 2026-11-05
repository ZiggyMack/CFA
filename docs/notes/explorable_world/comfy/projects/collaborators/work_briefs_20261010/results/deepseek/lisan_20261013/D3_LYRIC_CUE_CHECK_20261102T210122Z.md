# D3 — lyric and cue mechanical check (Lisan only, no timing)

Author: Deep_SEEK, mailbox `deepseek`. UTC 2026-11-02T21:01:22Z. Text-level verification only; no timing, no vision, no generation. This closes the D3 item from Claude's starter suggestions (`SUGGESTIONS_FROM_CLAUDE_20261013.md`), held since 2026-10-13.

## Inputs read from disk, with hashes as I measured them

| Path (under `projects/lisan_al_gaib/`) | bytes | sha256 |
| --- | --- | --- |
| `lyrics_user_20261013/META_MIRROR_0_REMASTERED.lyrics.user.v001.txt` (set 1) | 4,167 | 57ca7406…f6ed |
| `lyrics_user_20261013/MM_0.lyrics.user.v001.txt` (set 2) | 4,373 | cab4d38d…0caa |
| `story/writer_pass_20261012/CUE_TO_LINE_MAP_20261013.md` | 9,636 | 25af90d3…3507 |
| `story/writer_pass_20261012/LYRIC_DIFF_20261013.md` | 7,283 | 48ed394c…e84f |

The two lyric files' hashes match the values recorded in `LYRIC_DIFF_20261013.md` and `DECISIONS_20261012.md`, so the lyric text is unchanged from when the map and diff were written.

## Result 1 — the ten listed differences: all ten confirmed

I re-derived each against both files, by hand at the string level.

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | L16 "of all" vs "of them all" | ✅ confirmed |
| 2 | set 1 `[BRIDGE]` header; set 2 unlabeled (L20–22) | ✅ confirmed |
| 3 | set 2 adds "Under the lies…" lead-in (L18) | ✅ confirmed |
| 4 | hook sung twice (set 1 L21–22) vs once (set 2 L22) | ✅ confirmed |
| 5 | Verse 1 header + blank line (set 2 L24–25) | ✅ confirmed |
| 6 | 4-line refrain stanza added (set 2 L29–32) | ✅ confirmed |
| 7 | Final Refrain whisper tail removed (set 2 L127) | ✅ confirmed |
| 8 | "I am the voice of y'all" added (set 2 L128) | ✅ confirmed |
| 9 | "Can you handle what you hand out? / Let the mirror talk back." (set 2 L134–35) | ✅ confirmed |
| 10 | "Little doubt. Big pride. / I kept pointin' at the devil— / Why he got my eyes?" (set 2 L137–39) | ✅ confirmed |

Arithmetic holds: 134 − 2 (header, repeated hook) + 11 lyric lines + 5 blank lines = 148.

## Result 2 — the fifty cue-to-line mappings: all fifty confirmed

I checked every row of `CUE_TO_LINE_MAP_20261013.md` against the set-1 file's actual line numbers and text; none is "not found", and the map's own exact/partial labels were reproduced, not re-scored. The verified set-1 line numbers per panel:

01→2–3 · 02→(no cue; 4–7 by position) · 03→8 · 04→10 · 05→11 · 06→12 · 07→14 · 08→16 · 09→19 · 10→20 · 11→21 · 12→25 · 13→25 · 14→25 · 15→26 · 16→26 · 17→26 · 18→26 · 19→28 · 20→28 · 21→30 · 22→31 · 23→37 · 24→42 · 25→42 · 26→43 · 27→45 · 28→47 · 29→48 · 30→51 · 31→52 · 32→53 · 33→58 · 34→61 · 35→65 · 36→76 · 37→78 · 38→78 · 39→80 · 40→82 · 41→87–88 · 42→92 · 43→93–94 · 44→96 · 45→97 · 46→99 · 47→100 · 48→102 · 49→108,110 · 50→127.

## Result 3 — the one discrepancy found

The map's headline says "**Fourteen** panels sit under a song header that differs from the guide's block name," but the enumerated panels total **fifteen**: 12–22 (eleven, Verse 1 ≠ "Bridge into V1") + 23 (one, Bridge 2) + 33–35 (three, Bridge 3 ≠ "Verse 2"). A headline count, not a substance error — the row-by-row data is correct. Flagged for Claude to reconcile if it matters.

## Limit

This is a string-level check of the map and diff against the lyric files. It establishes nothing about timing, vocal-lane alignment, or which set is canonical — those remain null and CFA Nova's. No grade, no acceptance, no change to any file.

— Deep_SEEK
