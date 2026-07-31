# Eevee-Only Starter

**Status:** ✅ Done

## Summary
Professor Oak has **one** Pokémon to give, not three — every ball on the lab table yields Eevee no matter which is picked. The player no longer gets free evolution stones outright; instead [[Cultist Dream Sequence]] is what actually grants the single stone (and therefore the single eventual evolution) they'll have access to for that save. The rival gets Eevee too, and his rolls into one of the three Eeveelutions as the story progresses.

## Key files
- `scripts/OaksLab.asm` — the 3-ball choice, always resolving to `EEVEE`
- `data/pokemon/base_stats/eevee.asm` — Eevee's stats/moveset
- `RivalStarterOptions` table — rolls `wRivalStarter` once per save among `EEVEE`/`JOLTEON`/`FLAREON`/`VAPOREON`
- `data/trainers/parties.asm` — `Rival1Data`/`Rival2Data`/`Rival3Data`, resized from 3-way to 4-way
- `scripts/SSAnne2F.asm`, `PokemonTower2F.asm`, `SilphCo7F.asm`, `Route22.asm` (2nd table), `ChampionsRoom.asm` — every trainer-number lookup that branches on `wRivalStarter`
- `engine/battle/read_trainer_party.asm` — Champion's signature-move grant (Thunder/Fire Blast/Blizzard/Double-Edge matching the rival's final Eeveelution) and the lab-battle Sand Attack strip (below)

## How it works
- The 3 balls/map objects on Oak's lab table are still cosmetically present — picking any of them is identical, all resolve to `EEVEE`.
- The rival receives Eevee too, narrated with the same "claimed a ___!" text.
- `wRivalStarter` is rolled **once per save**, deciding what the rival's Eevee will have evolved into — but only **starting from his 2nd wave of battles** (SS Anne, Pokémon Tower, Silph Co., Route 22's 2nd battle, the Champion fight). His first 3 encounters (Lab, Route 22's 1st battle, Cerulean City) are always plain Eevee — no in-story time has passed for it to evolve yet.
- Every trainer-number/party lookup gated on `wRivalStarter` had to be resized from a 3-way branch (Bulbasaur/Charmander/Squirtle-style) to a 4-way branch (Eevee/Jolteon/Flareon/Vaporeon).
- The Champion's signature-move grant picks Thunder/Fire Blast/Blizzard/Double-Edge to match whichever Eeveelution the rival ended up with.
- The player starts with **no** evolution stones outright anymore — that's [[Cultist Dream Sequence]]'s job now.
- Title-screen mon cycling is untouched — still shows the vanilla Bulbasaur/Charmander/Squirtle, cosmetic only, doesn't reference "your starter."

## A tutorial-battle balance fix
Eevee's innate level-1 moveset is `TACKLE, SAND_ATTACK` (next learnset move, Quick Attack, isn't until level 27 — so there's no level threshold to dodge for either trainer's Eevee). At level 5 in the lab battle, both sides landing/missing on a coin-flip Tackle while Sand Attack stacks accuracy drops reads as unfairly swingy for a *tutorial-tier* fight.

**Fix:** the rival's (Gary's) Sand Attack is specifically stripped in `ReadTrainer`'s shared `.FinishUp` step, gated on `wCurOpponent == RIVAL1 && wTrainerNo == 1` — i.e. only the lab battle specifically, not his later Route 22/Cerulean City encounters, and not the player's own Eevee.

## Related
- [[Cultist Dream Sequence]] — what actually grants the player's one evolution stone now
- [[Smarter Trainer AI]] — explicitly excludes Rival1 (this lab battle) from its new kill-shot logic, on the reasoning that this fight's stakes are meant to be carried by the tier system alone
