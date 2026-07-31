# Permadeath Mode

**Status:** ✅ Done

## Summary
A Pokémon that faints in battle is **permanently marked dead**, not just "fainted." Dead Pokémon can never be revived by any normal means, and the party screen shows `RIP` instead of `FNT` for them. This is the mechanical backbone the rest of the project's stakes-raising features (hidden tiers, smarter AI) lean on — without real permanent loss, neither of those would matter as much.

## Key files
- `constants/battle_constants.asm` — `DEAD_BIT` (bit 7 of `MON_STATUS`, a bit vanilla status ailments never use)
- `home/pokemon.asm` — party screen display logic (`RIP` vs `FNT`)
- Pokémon Center / Revive / Max Revive item-use code — all check the flag before allowing any heal-from-faint action

## How it works
- `MON_STATUS`'s bit 7 is otherwise unused by vanilla Gen 1 (real status ailments — poison, burn, paralysis, etc. — only ever use the lower bits). Repurposing it as `DEAD_BIT` costs nothing structurally.
- When a Pokémon faints in battle, that bit gets set permanently on its struct.
- Every revival path (Pokémon Center heal-all, the `Revive`/`Max Revive` items) checks the bit first and refuses to act on a dead Pokémon.
- The party screen (`home/pokemon.asm`) prints `RIP` instead of `FNT` for any Pokémon with the bit set, so death reads as permanent at a glance, not just "currently fainted."

## Deliberately unchanged
- **The player's own blackout/whiteout behavior is untouched.** Whiting out (all Pokémon fainted) still just returns the player to the last-visited Pokémon Center exactly like vanilla Red/Blue — there's no separate "game over" state layered on top. Permadeath is per-Pokémon, not a run-ending condition.

## Related
- [[Hidden Tier System]] — the other stakes-raising system; tiers make individual Pokémon feel less interchangeable, which matters more once death is permanent
- [[Smarter Trainer AI]] — built explicitly *because* permadeath raises the real cost of every trainer battle, and vanilla AI barely reacted to the battle state at all
- [[Roadmap & Ideas]] — the discussed-but-unbuilt graveyard/memorial system at the Pokémon Center would be the natural next extension of this system
