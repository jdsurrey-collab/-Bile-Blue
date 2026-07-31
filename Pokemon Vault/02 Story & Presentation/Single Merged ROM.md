# Single Merged ROM (No Version Exclusives)

**Status:** ✅ Done

## Summary
This fork only builds **one ROM** (`pokered.gbc`) — the `_BLUE` build path was removed from the Makefile entirely. All wild-encounter tables that used to branch on `IF DEF(_RED)`/`IF DEF(_BLUE)` were flattened into a single unconditional list per map, so species from both original versions are catchable in this one ROM.

## Key files
- `Makefile` — `_BLUE` build target removed
- `data/wild/maps/*.asm` — flattened wild-encounter tables
- `constants/pokemon_data_constants.asm` — `NUM_WILDMONS = 10` (the fixed slot count that had to be worked within)
- `data/events/prizes.asm`, `prize_mon_levels.asm` — Game Corner prize lineup (deliberately left as-is, see below)

## How it works
- Species pairs that used to be version-exclusive (Oddish/Bellsprout, Ekans/Sandshrew, Mankey/Meowth, Growlithe/Vulpix, Nidoran♂/♀, Scyther/Pinsir, etc.) now both appear in the same map's wild list.
- Since each map's wild list is a **fixed-size table** (`NUM_WILDMONS = 10` slots), there was no room to just add the missing half — duplicate filler slots were traded away instead. Most exclusive species show up at **reduced frequency** compared to their native version, not 1:1 rate parity with the original single-version game.
- **Game Corner prizes** were intentionally left on their Red-version selection (Nidorina, Scyther/Dratini/Porygon) — the Blue-side equivalents (Nidorino, Pinsir) remain obtainable via wild-caught evolution / Safari Zone, so nothing is actually lost.
- **Cosmetic-only `_RED`/`_BLUE` branches** that don't gate catchable content were left alone entirely and simply resolve to their Red-flavored asset now that only `_RED` is ever defined: Game Corner slot-reel graphics, the SGB border palette, the title screen's randomly-cycled Pokémon list, default player/rival name suggestions.

## Rule for touching this system
Any new entry added to `data/wild/maps/*.asm` just needs to keep the flat list at exactly `NUM_WILDMONS` (10) `db LEVEL, SPECIES` lines — `def_grass_wildmons`/`def_water_wildmons` assert this at build time, so a miscounted table is a hard build error, not a silent bug.

## Related
- [[Build & Versioning]] — confirms `make blue`/`make blue_debug` no longer exist as targets
- [[Victorian-Gothic Rewrite]] — the other big `text/*.asm`-adjacent, per-map data pass
