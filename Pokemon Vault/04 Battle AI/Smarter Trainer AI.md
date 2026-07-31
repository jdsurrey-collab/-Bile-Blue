# Smarter Trainer Battle AI

**Status:** ✅ Done — implemented, and empirically verified via a PyBoy direct-function-call test harness (not just a clean build)

## Summary
Permadeath (see [[Permadeath Mode]]) raises the real stakes of every trainer battle, but vanilla Gen 1's AI barely reacts to the battle state at all. This is a scoped set of fixes/additions to the two existing AI subsystems — **no held items, no new stats, nothing structurally Gen 2**. Built under [[Roadmap & Ideas]]'s "what next, without adding new-gen mechanics" prompt; full plan preserved at `C:\Users\jdsur\.claude\plans\mutable-whistling-newt.md`.

## Scope decisions (locked in with the user before building)
- Kill-shot logic is a **heuristic** (HP fraction + type effectiveness), not a real damage-formula estimate — lower risk, easier to verify in Z80.
- **Rival1** (the lab battle) excluded — lowest-level, lowest-information fight; its stakes are meant to be carried by the tier system alone.
- **Youngster** and **Cue Ball** (the only 2 classes with zero move-choice scoring at all) deliberately left as-is — intentional flavor, not a gap to close.
- Regular trainer classes get **no new move-choice logic** — only the universal switch-in fix applies to every trainer. Sharper move-choice logic is reserved for the roster that already gets hand-written item-use AI (gym leaders, Elite Four, Cooltrainers, Giovanni, Blackbelt, Agatha, Lance, rival's 2nd/3rd battles).

## Key files
- `engine/battle/trainer_ai.asm` — move-choice modifications, `CooltrainerFAI` gate fix, new Modifications 4 & 5
- `engine/battle/core.asm` — `GetTypeMatchupMultiplier` (new), `AIGetTypeEffectiveness` (rewritten), `AIChooseBestSwitchIn` (new, replaces `EnemySendOut`'s old scan)
- `data/trainers/move_choices.asm` — per-class modification wiring
- `ram/wram.asm` — new WRAM scratch bytes for both new functions

## The two existing AI subsystems (as they were before this work)
1. **Move-choice scoring** (`AIEnemyTrainerChooseMoves`) — a 4-byte score array modified by numbered "modification" functions listed per-trainer-class. Only 3 modifications existed before this work; a 4th slot was dead code.
2. **Per-class item-use/switch AI** (`TrainerAI`) — most regular classes have zero logic (`GenericAI` is a no-op); only gym leaders/Elite Four/rival/a few named classes have hand-written healing/switching routines.

## What changed

### Dual-type effectiveness fix
`AIGetTypeEffectiveness` used to stop at the **first** matching `TypeEffects` row instead of considering both of the defender's types (pret's own comment already flagged this). New `GetTypeMatchupMultiplier` (attacking type in `d`, defender type1/type2 in `b`/`c`, 16-bit multiplier out in `hl`, `EFFECTIVE`(10)=neutral, up to 40 for a real 4x weakness) mirrors the real damage-calc's own type-matchup walk but stays read-only so it's safe to call from AI scoring. A mono-type defender is handled correctly (one matching row applied once, not squared).
**Incidental second fix**: the old function initialized its result to hex `$10` (16) with a comment saying it should've been `EFFECTIVE` (10) — and `AIMoveChoiceModification3`'s own check matched that same wrong value, so the two bugs canceled out by coincidence. Now both use the real named constant.

### Matchup-aware switch-in selection (highest-leverage fix)
`EnemySendOut`'s mon selection used to be pure "first unfainted mon in party order," for **every** trainer, for both deliberate switches and automatic fainted-mon replacement. New `AIChooseBestSwitchIn` scores every eligible candidate by (offensive potential against the player's current mon) minus (defensive risk from it), each via `GetTypeMatchupMultiplier`, biased `+400` so unsigned 16-bit subtraction never needs sign handling. Every intermediate value routes through new WRAM scratch bytes rather than juggling registers — this only runs on an actual switch decision (not once per frame), so the extra loads/stores cost nothing that matters. Ties break by earliest party order. The very first send-out of a fresh battle is unaffected (exactly one candidate exists regardless of scoring) — confirmed directly, not assumed.

### Two new move-choice modifications
- **Modification 4** (previously dead code): discourages re-using a stat-boosting move whose relevant stat is already maxed at +6 stages — direct complement to Modification 2, which encourages stat-boosts blind to whether the stat is capped. Wired into `SUPER_NERD`, `UNUSED_JUGGLER`, `POKEMANIAC`, `PSYCHIC_TR`, `CHIEF`, `SCIENTIST`, `GENTLEMAN`, `LORELEI`.
- **Modification 5** (new): kill-shot heuristic — if the player's mon is ≤1/4 HP and a strong/super-effective damaging move is available, heavily favor it. Wired into `BLACKBELT`, `GIOVANNI`, `COOLTRAINER_M`, `COOLTRAINER_F`, `BRUNO`, `BROCK`, `MISTY`, `LT_SURGE`, `ERIKA`, `KOGA`, `BLAINE`, `SABRINA`, `RIVAL2`, `RIVAL3`, `LORELEI`, `AGATHA`, `LANCE` — explicitly **not** `RIVAL1`.

### One-line bug fix
`CooltrainerFAI`'s intended 25%-chance gate was commented out (`; ret nc`), so her heal/switch logic ran unconditionally instead of 25% of the time. Uncommented.

## The one real bug this work introduced (and caught before shipping)
**Modification 5 called `GetTypeMatchupMultiplier` with a plain `call` across a bank boundary** — `GetTypeMatchupMultiplier` lives in `core.asm` (bank `0x0f`), `AIMoveChoiceModification5` lives in `trainer_ai.asm` (bank `0x0e`). RGBASM/RGBLINK don't track bank context per-instruction, so this assembled and linked cleanly, but would have silently executed whatever ROM data happened to be paged in at runtime — for every Modification-5 trainer, at exactly the tense low-HP moments this change was meant to sharpen.

The already-correct Modification 3 had the answer sitting right above it: it calls `AIGetTypeEffectiveness` (the *wrapper*, not `GetTypeMatchupMultiplier` directly) via `callfar`. **The distinction that matters:** `farcall`/`callfar`'s `Bankswitch` protocol clobbers `b` (destination bank) and `hl` (target address) — so it's only safe to `farcall`/`callfar` a function whose calling convention doesn't depend on live input registers surviving the jump. `AIGetTypeEffectiveness` reads/writes exclusively via WRAM — no register inputs to lose — so calling *that* across the boundary is safe; calling `GetTypeMatchupMultiplier` (whose calling convention is `b`/`c`/`d` register inputs) the same way is not.

This is the **third occurrence** of this exact bug class this project (see [[Cultist Dream Sequence]] for the first two) — see [[Lessons Learned - Bug Patterns]] for the general rule.

## How this was actually verified
A clean `make -Weverything` caught **none** of the above — not the cross-bank bug, not the type-effectiveness correctness, nothing behavioral. Verified instead via a PyBoy direct-function-call test harness (see [[PyBoy Testing Techniques]]) — every claimed fix (dual-type math including the mono-type non-double-counting case, switch-in's matchup pick + tie-break + fainted-mon skip, Modification 4's maxed/not-maxed threshold, Modification 5's HP-gate and effectiveness-gate) was confirmed with a specific expected value, not inferred from the code reading correctly.

Two "failures" hit along the way turned out to be **bugs in the test, not the game**:
1. Move ID constants are commented in hex without a `$` prefix — a test using a comment's number as decimal silently tests the wrong move.
2. Water is *not* super-effective against Grass (Grass resists Water) — a test assumption, not a game bug.

Both are folded into [[Lessons Learned - Bug Patterns]] as recurring traps.

## Related
- [[Permadeath Mode]] — the reason this work exists at all
- [[Hidden Tier System]] — a separate, independent system that also touches the same trainer battles (gym leader tier rolls)
- [[PyBoy Testing Techniques]] — the verification method, including the direct-function-call harness built specifically for this work
- [[Lessons Learned - Bug Patterns]] — the `farcall` register-clobber class (3rd occurrence) and the hex/decimal constant trap
