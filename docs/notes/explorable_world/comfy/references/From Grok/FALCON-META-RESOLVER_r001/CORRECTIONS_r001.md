# CORRECTIONS_r001 — versioned wording corrections to FALCON-META rev v004

Supplement to frozen FALCON-META rev v004 (MANIFEST_v004.sha256 = a47d04cd439f72d6d75924a90c94aa87301e46b15144432829a4f38d132e50ad).
No v004 file is overwritten. Where the wording fix touches a Markdown file, a corrected copy named `*_r001-corrected.md` is in this folder. The JSON and TSV stay frozen; read them with the corrections below.
None of these corrections changes a count, status, verdict, hash or decision.

| # | v004 file | Location | v004 text | Corrected text | Copy |
|---|---|---|---|---|---|
| 1 | README_v004.md | line 10 | `MANIFEST_v004.sha256`: checksums for every v003 file. | ... checksums for every v004 file. | README_v004_r001-corrected.md |
| 2 | SCHEMA_FIELD_DICTIONARY_v004.md | line 6 | package_rev: Always "FALCON-META rev v003". | Always "FALCON-META rev v004". (The TSV itself already carries v004 in package_rev.) | SCHEMA_FIELD_DICTIONARY_v004_r001-corrected.md |
| 3 | EXCEPTIONS_COVERAGE_v004.md | line 77 (C04-battle-light-008) | v003 records v007b | v004 records v007b | EXCEPTIONS_COVERAGE_v004_r001-corrected.md |
| 4 | EXCEPTIONS_COVERAGE_v004.md | line 84 (C04-battle-light-006 hash) | ...but v003 original identity is 35398903a8f1 | ...but the v004 original identity is 35398903a8f1 | EXCEPTIONS_COVERAGE_v004_r001-corrected.md |
| 5 | FALCON_EVIDENCE_v004.json | conflicts[] entry for C04-battle-light-006 (hash) | "chest audit scanned sha 16c5b38527e0 but v003 original identity is 35398903a8f1" | read as "...but the v004 original identity is 35398903a8f1". Resolved by Chief's ruling: original = 35398903 (before_C04-battle-light-006.jpg); 16c5b385 = repair; V_5's pass on b90e0f6c is STALE; Z_9 rebuilds. | JSON frozen; correction recorded here only |
| 6 | EXCEPTIONS_COVERAGE_v004.md | line 7 (blocker 2) | "5 repair file(s) have appeared since v003" | Clarification: the 5 files listed are new to v004's repair index. That is not a claim that all 5 were created after v003 was built. Each one still has no verdict. | note only |

Checked and left as is: FALCON_EVIDENCE_v004.json "Pent House relay quoted in the v003 brief" refers to the v003 build brief, so it is correct. The many `..._v003.tsv` / `Z_3_v003-fix` strings are real source and image filenames, not revision labels.
