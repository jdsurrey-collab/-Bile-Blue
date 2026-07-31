# Version History

*Maps the `Roms/vX.Y` build snapshots (see [[Build & Versioning]]) to the git commits and features that produced them. Update this whenever a new snapshot is cut.*

## Fork-specific commits (newest first)
These are the commits that make this project "Pokémon Purple" rather than plain pret/pokered — everything before `fae9cb4b` is unmodified upstream history.

| Commit | Summary | Systems touched |
|---|---|---|
| `f537d629` | Add smarter trainer AI, title screen palette fix, and cultist dream text fixes | [[Smarter Trainer AI]], [[SGB Colorization Cleanup]] (PAL_TITLEMON), [[Cultist Dream Sequence]] |
| `dde89c34` | Fix title screen dot texture, cultist dream text overflow, and menu popup cleanup | [[SGB Colorization Cleanup]], [[Cultist Dream Sequence]], [[Victorian-Gothic Rewrite]] (line budget) |
| `769ed42d` | Fix wild-tier coverage gap, cultist dream freeze, and SGB border dot palettes | [[Hidden Tier System]] (`InitWildBattle` fix), [[Cultist Dream Sequence]], [[SGB Colorization Cleanup]] (border) |
| `07e1a747` | Add hidden Pokémon tier system, Eevee-only starter with cultist dream stone choice, and dark musical rework | [[Hidden Tier System]], [[Eevee-Only Starter]], [[Cultist Dream Sequence]], [[Industrial-Goth Score]] |
| `fae9cb4b` | Merge Red/Blue into one ROM, rebrand as Pokémon Purple with gothic intro | [[Single Merged ROM]], [[Purple Rebrand & Gothic Intro]] |
| `7dc6b43f` | Rewrite all remaining flavor/NPC text in Victorian-gothic tone, skip intro | [[Victorian-Gothic Rewrite]] |
| `6a47cc43` | Add hardcore permadeath mode and Victorian-gothic story rewrite | [[Permadeath Mode]], [[Victorian-Gothic Rewrite]] |

Everything at `405b6246` and older is unmodified upstream pret/pokered history (kept for reference — see `upstream` remote in [[Build & Versioning]]).

## `Roms/vX.Y` snapshots on disk
`v0.1` through `v0.22`, sequential, one per completed fix/feature round (not all of them 1:1 with a git commit — some snapshot mid-round debugging states). Not yet pushed to git — see `.gitignore`'s `/Roms/` entry.

**Not yet reverse-mapped in detail to specific commits** — if precise version-to-fix mapping becomes important, cross-reference build timestamps against `git log --format='%ai %h %s'`.

## Open question
The user has not yet confirmed whether `Roms/v0.22`'s `ClearScreen`/`TitleClearScreen` regression fix (see [[SGB Colorization Cleanup]]) actually resolves the "weird grays during battle"/"blurry artifacts" report in their own hands-on testing.

## Related
- [[Build & Versioning]]
- [[Roadmap & Ideas]]
