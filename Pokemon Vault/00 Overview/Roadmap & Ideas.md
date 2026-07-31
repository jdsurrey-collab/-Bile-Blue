# Roadmap & Ideas

*Living document — update this whenever a thread opens or closes. Newest at top of each section.*

## In progress

- **[[Kanto Reborn - Overview]] — encounter overhaul + Gen 2 species import.** The current main effort. Phase 0 (species-index ceiling, [[Species Index Ceiling - GetName Fix]]) is ✅ done and verified in `Roms/v0.23`. Remaining: raise `NUM_POKEMON_INDEXES` and grow the species/dex tables, port + fold base stats, convert sprites, author movesets and the 5 approved new moves, write ~90 gothic dex entries, and rework every wild table. Full decision log lives in that note.

- **[[Industrial-Goth Score]] — rest of the soundtrack.** 5 tracks converted so far (Title Screen, Route 2/naming, Wild/Trainer Battle timbre-only pass, Pallet Town, Oak's Lab). Every other track in the game is still the bright vanilla original. Next candidates to consider: Gym theme, Route 1, Cerulean City, Pokémon Center — anything the player hears constantly.
- **[[SGB Colorization Cleanup]] — the remaining `ld a, ' '` blank-tile bug sites.** Confirmed present in ~30 more files (`home/window.asm`, `home/vcopy.asm`, `home/text.asm`, `engine/battle/core.asm`, `engine/battle/animations.asm`, `engine/gfx/hp_bar.asm`, `engine/battle/print_type.asm`, `engine/pokemon/status_screen.asm`, `engine/link/cable_club.asm`, `engine/items/town_map.asm`, `engine/menus/pokedex.asm`, `engine/menus/start_sub_menus.asm`, `engine/overworld/player_state.asm`, `engine/movie/hall_of_fame.asm`, `engine/movie/credits.asm`, `engine/movie/trade.asm`). Only the two feeding the title screen have been fixed. Don't touch these speculatively — this is a *latent* bug (invisible on real DMG, only visible once a screen's SGB palette colorizes shade 0/3 as different hues), so wait for an actual reported dotted-background complaint on one of these screens, then fix that one call site narrowly (per the [[Lessons Learned - Bug Patterns]] rule about not generalizing shared-function fixes).

## Discussed, not started

- **Graveyard / memorial system for permadeath'd Pokémon.** Conceptually placed at the **Pokémon Center** — reuses existing menu/PC infrastructure and the `home/pokemon.asm` `DEAD_BIT` scan logic already built for [[Permadeath Mode]]. No implementation started yet; this was a "what would you recommend next" conversation, not a committed plan. Worth revisiting once the soundtrack/SGB threads above are further along.

## Ideas raised, no decision yet

- Nothing currently queued beyond the two threads above. Add here as new "what should we do next" conversations happen.

## Explicitly decided against / out of scope

- No Gen 2+ mechanics (held items, breeding, new stats) — reaffirmed multiple times, most recently when scoping [[Smarter Trainer AI]]. The Gen 2 cartridge in the project folder is a reference/asset source only, never a mechanics import target.
- `Youngster`/`Cue Ball` trainer classes deliberately keep zero move-choice AI scoring — treated as intentional flavor, not a gap to close.
- Rival's 1st (lab) battle deliberately excluded from the AI kill-shot heuristic — stakes there are meant to be carried by the tier system alone, not sharper AI.

## Related
- [[Project Overview]]
- [[Version History]] — what's actually shipped per `Roms/vX.Y` snapshot
