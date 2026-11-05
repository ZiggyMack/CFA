# Benchmark: lip-bite mouth shapes (known limitation)
Closed by Ziggy 2026-10-15 as a benchmark for future models.

Shapes: 15 (upper teeth biting lower lip), 16 (lower teeth biting upper lip), related 07 F/V.
Best stand-ins: 07 try-zB_Z_2 (L5 S3), 15 zA_Z_2 (L5 S3), 16 zC2_Z_2 (L5 S3) / zE07_Z_3 (L4 S3).

Failed methods: face-ref prompts (ref mouth copied), text-only, lip-mechanics wording,
hardest-detail-first ("inside out"), underbite, bulldog jaw, upside-down face, animation frame,
plain face with no tattoo and no ref (5/5 failed, so the tattoo is not the cause),
real-photo mouth swaps. Closest: pixel edits and flipped-15 composites.

## Cross-model test (run the same prompts on any other image/video model)
A. Plain: "Extreme close-up, front-on, of a young man's mouth. His upper front teeth press down into his lower lip, folding it inward. Soft even light."
B. Plain reverse: "...his lower front teeth press up into his upper lip, folding it inward..."
C. Lisan base prompt (breather v3 face, look 01, no breather, natural teeth) + A, then + B.
Score each L/S 1-5, 3 tries per prompt; log model, date, scores here.
| model | date | A | B | C-A | C-B | notes |
|---|---|---|---|---|---|---|
| Grok Bot image tool | 2026-10-14 | fail | fail | fail | fail | baseline |
