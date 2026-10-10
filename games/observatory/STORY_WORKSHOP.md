# Story Workshop: the same place, another telling

Implemented and checked September 12, 2026. This completes a small story-iteration
milestone inside the playable Observatory. It changes written dialogue and found
text while retaining the world, repair rules and consequences. Voice performance
and footage/lip-sync editing remain separate, unexecuted experiments.

## Try it

1. If the old game is open, use **Save and leave**, then reopen
   [the portable launcher](builds/observatory/Play.cmd). Choose **Continue your
   visit**, or enter the courtyard if there is no save.
2. Press **Esc → Story workshop · compare the writing**.
3. Select **What we leave for others**, then **Back to the world**. Speak to Mara
   or Ivo, read the archive, or revisit an ending.
4. Switch back to **The practical repair** to compare the same moment. Your
   position, equipment, repairs and discoveries remain intact. The selected draft
   saves with your visit; old version-1 saves default to the original writing.

The original is direct about the work. The second draft gives the residents more
personal observations: Mara remembers the swallows she used to watch, Ivo keeps
the ropes ready, and the archive asks who was absent when a repair was called
finished. Both drafts explain how water carrying affects the crossing. Neither
adds a hidden care score, deadline, or new puzzle requirement.

For the next review, notice what makes you curious, whether you understand the
water problem, and which lines feel like people talking. Finish or defer the
repair and return before judging the consequence. This is an invitation to assess
the experience; the chapter's intended duration and movement comfort are still
unmeasured by a human play-through.

## Revise the writing

- [data/chapter.json](data/chapter.json) retains the original 17 entries.
- [data/drafts/curiosity.json](data/drafts/curiosity.json) contains the second draft.
- [scripts/story_state.gd](scripts/story_state.gd) declares the two allowed draft
  paths and validates complete replacements before applying them. Keep the same
  chapter ID and all 17 entry IDs, with nonblank title/text strings. Limits are
  160 characters per title, 12,000 per body and 512 KiB per file.
- [scripts/main.gd](scripts/main.gd) presents the workshop and stores the optional
  `draft` ID beside the existing version-1 save data. Draft selection does not
  emit a story transition or change puzzle state.

After editing a source draft, switch away and back in the **source** game to
reload it. Invalid or incomplete drafts leave the active text unchanged. Rebuild
the portable game to include edits in its PCK; changing source JSON does not
change an already exported pack. Start a fresh game process to use a rebuilt pack.
Adding a draft requires its ID/path in the story loader and a label in the menu.

## Validation from this pass

| Check | Observed result |
|---|---|
| Existing story / world / save suites | 108 + 36 + 56 checks passed again |
| Draft content and state isolation | 153 checks passed: both tools in both drafts, deferral/later repair, atomic rejection, no events/state changes, independent data |
| Actual scene menus and save integration | 35 checks passed: switching, position/look, progress, optional draft persistence, legacy/invalid metadata fallback, resumed repair |
| Source smoke | 11 interactions, floor and both bundled drafts passed |
| Packed smoke from an empty project directory | Same checks passed; `builds`, `.local` and `tests` absent from the packed resource filesystem |
| Visual review | Workshop, Mara's second draft and pause menu inspected at 1280 × 720; body text scrolls and buttons remain accessible |

Total: **388 functional checks**, plus the source/packed smoke checks and visual
inspection. The known Windows certificate-store warning appeared in offline
headless tests, whose exit codes were zero.

Reproduce the new suites from the CFA root after the commands in
[the original validation record](VALIDATION.md):

```powershell
$env:APPDATA = Join-Path (Get-Location) 'games/observatory/.local/osdata'
$cfaGodot = Join-Path (Get-Location) '.cache/godot-4.7.2/Godot_v4.7.2-stable_win64_console.exe'
& $cfaGodot --headless --path games/observatory --script res://tests/test_story_drafts.gd
& $cfaGodot --headless --path games/observatory --script res://tests/test_draft_menu.gd
powershell.exe -NoProfile -ExecutionPolicy Bypass -File games/observatory/build.ps1
```

Screenshots and interval samples are in ignored `.local/story-workshop-review/`.
These hidden-window captures ran while an older game instance remained open, with
some capture work overlapping export. Mean intervals were 54.64 ms (workshop),
68.33 ms (Mara) and 26.30 ms (pause), with 95th percentiles 179.83, 222.15 and
76.53 ms respectively. They document those capture conditions and **do not
establish current standalone play performance**. The earlier 60 fps samples
remain historical measurements, not a result of this pass.

The first export exposed two packaging issues: it included a save beneath the
build directory, and copying the unchanged engine failed because the old game was
open. The export now excludes build/user-data directories; the build script
reuses an existing runtime only when its SHA-256 matches the source executable.
The corrected pack passed the explicit directory-exclusion smoke check. The
running game was not terminated and its save file was not edited by these tests.

Comfy preflight again returned `invalid_grant: refresh token reuse detected`.
The normal browser login was started, but its callback timed out. No generation,
model import or cloud transfer was performed in this pass. This local workshop
does not require that connection.
