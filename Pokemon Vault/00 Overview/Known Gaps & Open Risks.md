# Known Gaps & Open Risks

*What is verified, what is not, and what is deliberately left alone. Updated after the v0.32 audit pass.*

## ⚠️ Not verified — needs a human on a real screen

Everything below builds clean and passes the [[Test Suite]], but **no part of the Gen 2 import has been played**. The tests prove tables agree with each other; they cannot prove the game feels right.

| Risk | Why it matters |
|---|---|
| **Dex UI at 240 entries** | No hardcoded limits found (`wDexMaxSeenMon`, symbolic flag-array bounds), but scrolling/paging through 240 has never been exercised. |
| **Save/load with the new layout** | `MONS_PER_BOX` 20→19 and the grown dex arrays shifted the saved WRAM block. **Existing saves are invalid** — this needs a fresh game. |
| **Downscaled back sprites** | Gen 2 backs are 48×48, Gen 1 wants 32×32. NEAREST downscale keeps hard edges but has never been looked at in battle. Some may read poorly. |
| **Balance** | Base stats are Gen 2's with Sp.Atk/Sp.Def averaged. Nothing tuned against Gen 1's power curve or against [[Hidden Tier System]]. |
| **Encounter feel** | 55 maps rewritten. Rates are structurally correct (slot order) but the *experience* is untested. |
| **Oak's replacement Eevee** | Logic verified 5/5, but the scene has never been watched end-to-end. |

## 🟡 Known cosmetic gaps

- **Dex rating is meaningless above 150.** `engine/events/pokedex_rating.asm`'s last tier is `dbw NUM_POKEMON + 1`, so owning 150–240 species all yields the same text. Harmless; needs new tiers + gothic text to fix properly.
- **Learnsets are thinner than canon.** 70 Gen 2 level-up moves have no Gen 1 equivalent. Where filtering left a species under 3 moves it got a type-appropriate fallback kit — playable, but not designed.
- **Metronome can't roll the 5 new moves** (deliberate — vanilla's bound left byte-for-byte as shipped).
- **Zap Cannon paralyses at Gen 1's rate**, not Gen 2's guaranteed 100% (a true 100% variant needs a new effect handler).

## 🔴 Open latent bug class

**~30 remaining `ld a, ' '` sites** (see [[SGB Colorization Cleanup]]). Only the two feeding the title screen are fixed. Invisible on DMG; only surfaces once a screen's SGB palette colorizes shade 0/3 differently. **Don't fix speculatively** — wait for a reported artifact, then fix that one call site narrowly.

## ✅ Audited and clean (v0.32)

- No stone evolutions among the 89 new species → the removed Fire/Water/Thunder stones strand nothing
- `MonsterPalettes` and `MonPartyData` already included Mew → contiguous by dex
- All dex-flag consumers use symbolic bounds (`wPokedexOwnedEnd - wPokedexOwned`) → auto-adapt to 30 bytes
- No hardcoded species-count literals in code (only stale comments, now corrected)
- All 89 species obtainable by wild encounter or evolution — verified programmatically
- 19 empty ROM banks (45–63) remain for growth

## Deliberately out of scope
- No Gen 2+ mechanics (held items, breeding, new stats/types)
- Dark/Steel types → 10 species excluded
- Unown → 28-form subsystem with no Gen 1 analogue
- Legendaries single-location; fishing untouched

## Related
- [[Kanto Reborn - Overview]] · [[Test Suite]] · [[Table Alignment - The Two Index Systems]] · [[Roadmap & Ideas]]
