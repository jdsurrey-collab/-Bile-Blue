# Hidden Tier System

**Status:** ✅ Done

## Summary
Every individual Pokémon secretly carries a power **tier from 1–10** (5 = neutral), applying a flat ±5%-per-step modifier to all 5 base stats. It's the project's answer to "every Pokémon of the same species should still feel a little different" without importing Gen 2+ mechanics like IVs/EVs. A small pixel-art badge shows the tier next to the level on the party status screen.

## Key files
- `constants/pokemon_data_constants.asm` — `MON_TIER` (an alias for the otherwise-vestigial `MON_CATCH_RATE` byte in the party/box struct)
- `engine/pokemon/tier_modifier.asm` — `ApplyTierModifier`, hooked into `CalcStat`'s base-stat read (`home/move_mon.asm`)
- `data/pokemon/tier_chances.asm` — `RollWildTier`'s weighting table
- `engine/battle/core.asm` — `InitWildBattle` (the actual roll site), `LoadEnemyMonData` (gym leader tier 6–8 rolls)
- `gfx/status/tier_numerals.png` — 10 hand-drawn glyphs (tally bars 1–4, V for 5, V+bars 6–9, X for 10)

## How it works
- **Storage**: `MON_CATCH_RATE` is copied into a new Pokémon's struct at creation but never read again for its original purpose (the real catch-odds math uses a separate battle-only copy, `wMonHCatchRate`/`wEnemyMonActualCatchRate`). Repurposed as `MON_TIER` — free storage, no struct resize.
- **Effect**: tier 1 = −20% to all 5 base stats, tier 10 = +25%, flat 5%-per-step in between, tier 5 = neutral (no change). Applied in `ApplyTierModifier`, called from `CalcStat`'s base-stat read.
- **Who rolls what tier**:
  - Wild Pokémon: rolled at battle-init time via `RollWildTier`, weighted toward low tiers.
  - Gym leaders (Brock through Sabrina, Giovanni): roll tier 6–8 live in `LoadEnemyMonData`.
  - Every other trainer/rival/Elite Four mon, and every gift Pokémon (starter, fossils, Eevee gift, Lapras, Hitmon*, Magikarp, Game Corner prizes, trades): stays neutral, tier 5.
- **Display**: a custom 1-tile badge (`gfx/status/tier_numerals.png`) shows next to the level on the party status screen's first page.

## Bugs hit & fixes

### The wild-tier roll was in the wrong function
Originally placed in `TryDoWildEncounter` (`engine/battle/wild_encounters.asm`) — but that function only runs for *ordinary* grass/water encounters. Fishing rods and scripted single-mon encounters (Snorlax on Route 12/16, the legendary birds, etc.) set `wCurOpponent`/`wCurEnemyLevel` directly and skip `TryDoWildEncounter` entirely, jumping straight into the shared `InitBattle → InitBattleCommon → InitWildBattle` chain. A caught Kakuna showing no tier badge at all is what surfaced this.

**Fix & lesson:** moved the roll to `InitWildBattle` — the one point *every* wild battle passes through regardless of trigger. General lesson: when several different trigger paths all eventually funnel into one shared function, put shared logic at the funnel point, not in one specific trigger's own code — rolling it any earlier will always miss some other path.

### `CalcStat`'s `hl` argument isn't a reliable struct pointer
Two of `CalcStat`'s call sites (`GetEnemyMonStat`'s scratch buffer, `LoadEnemyMonData`'s `battle_struct`-shaped `wEnemyMon`) use entirely different memory layouts than the party/box struct — so a `MON_TIER` byte can't be read at a fixed offset from `hl` reliably across all callers.

**Fix:** threaded the tier value through a dedicated HRAM byte, `hStatCalcTier`, that each caller sets immediately before calling `CalcStat`/`CalcStats`. A second HRAM byte, `hStatCalcBase`, round-trips the base-stat value itself — because `ApplyTierModifier` is invoked via the `homecall` macro, and `homecall`'s bank-restore `pop af` clobbers whatever `CalcStat` left in register `a`. (See [[Lessons Learned - Bug Patterns]] — this is the first of three occurrences of the "register value doesn't survive a bank-switching call" bug class this project hit.)

### Bank overflow from inlining
`ApplyTierModifier` was first attempted inline in `home/move_mon.asm` — but the fixed `Home` bank (shares ROM0 with `NULL`/`rst`/interrupt vectors and the header) had zero slack and overflowed by 9 bytes.

**Fix:** gave it its own floating `SECTION "Tier Modifier", ROMX` in `engine/pokemon/tier_modifier.asm`, included from `main.asm`, so the linker can bin-pack it anywhere with room instead of bloating an already-tightly-pinned section.

## Related
- [[Permadeath Mode]] — the other stakes-raising system
- [[Smarter Trainer AI]] — gym leaders' tier 6–8 roll and the AI's matchup scoring are independent systems, but both apply to the same battles
- [[Lessons Learned - Bug Patterns]] — the `hStatCalcBase`/`homecall` register-clobber bug, and its two later recurrences
