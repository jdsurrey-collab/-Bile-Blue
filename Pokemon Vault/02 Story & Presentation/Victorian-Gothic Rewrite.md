# Victorian-Gothic Story Rewrite

**Status:** ✅ Done

## Summary
Every NPC/sign/menu text in `text/*.asm`, plus the opening monologue, has been rewritten in a darker, Victorian register — archaic diction, mourning/funeral imagery, class-conscious cruelty — while preserving the original substance (same information conveyed, same script beats). Each location got its own unique despair-flavored treatment rather than one generic "gothic filter."

## Key files
- `text/*.asm` — one file per map, matching `scripts/*.asm`
- `data/text/text_2.asm` — the opening monologue
- `macros/scripts/text.asm` — the `text`/`line`/`cont`/`para`/`done`/`prompt` DSL all of this is written in

## Gym Leader themes
Each Gym Leader carries a distinct thematic flavor, layered into their dialogue specifically:

| Leader | Theme |
|---|---|
| Brock | stone / tomb |
| Misty | drowning |
| Lt. Surge | war veteran |
| Erika | beauty and rot |
| Koga | plague |
| Sabrina | madness |
| Blaine | ash / ruin |
| Giovanni | cold menace |

## The hard constraint: line budget
The display box is 20 tiles wide. Every `text`/`line`/`cont`/`para` segment has to hold to **~18 visible characters per line** — this matches the longest lines found in the original shipped/checksum-verified game. The box does **not** reject overlong lines; it silently wraps mid-word at the character boundary and cuts the rest. This isn't a build-time-caught error — it only shows up as a corrupted-looking wrap in an actual screenshot.

This bit the project directly in [[Cultist Dream Sequence]] (lines like "and I shall whisper" at 20 chars wrapped mid-word, only caught from a user screenshot showing "whisp"/"r" split) — worth remembering any time new dialogue is added anywhere, not just in that scene.

## Rules for touching this system
When touching dialogue in `text/*.asm`:
- Keep to the Victorian-gothic despair tone established per-location.
- Respect the ~18-visible-character-per-line budget.
- Preserve the existing macro skeleton — same count of `line`/`cont`/`para`/`done`/`prompt` — so box paging behavior doesn't change.

## Related
- [[Cultist Dream Sequence]] — the line-budget bug's most recent concrete occurrence
- [[Single Merged ROM]] — a separate, non-text change to the same wild-encounter/Game-Corner data layer
