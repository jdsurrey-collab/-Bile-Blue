# Species Index Ceiling — the `GetName` Fix

**Status:** ✅ Done — shipped in `Roms/v0.23`, 9/9 PyBoy assertions passing
**Phase:** 0 of [[Kanto Reborn - Overview]]

## The problem
Gen 1 stores a Pokémon's species as a one-byte **internal index** (`constants/pokemon_constants.asm`) — distinct from its Pokédex number. That range runs 1–190 (`NUM_POKEMON_INDEXES`), with **36 unused gap values scattered inside it** (the vanilla MissingNo. slots — genuinely reclaimable; nothing reads them, the glitch is undefined-data behavior, not load-bearing code).

But a hard ceiling sat immediately above. `GetName` (`home/names2.asm`) opened with:

```asm
cp HM01
jp nc, GetMachineName
```

— unconditionally redirecting **any** name lookup at or above `HM01` (`$C4` = 196) into TM/HM name rendering, *regardless of which name list was being asked for*. Item IDs and species indexes share one numeric range here, and `GetName` couldn't tell them apart. pret already flagged it in-source:

> `; BUG: This applies to all names instead of just items.`

…backed by three `ASSERT`s pinning Pokémon/move/trainer counts below `HM01`. Any species at index ≥196 would have printed as "TM01" instead of its real name.

## The fix — deliberately narrower than the "correct" one
The strictly-correct fix is *"only redirect when `wNameListType == ITEM_NAME`."* That was **rejected**: it changes behavior for every list type at once, and the item list menu (`home/list_menu.asm`) genuinely depends on this redirect to render TMs/HMs in the bag — reaching it through a `wNameListType` set by whichever menu opened it, which is harder to fully enumerate than it looks.

Instead the redirect is **skipped only for `MONSTER_NAME`**:

```asm
ld a, [wNameListType]
cp MONSTER_NAME
jr z, .notMachineName
ld a, [wNameListIndex]
cp HM01
jp nc, GetMachineName
.notMachineName
```

Same unlock, but every other list type keeps the exact vanilla code path **byte for byte** — structurally incapable of regressing item/move/trainer/OT naming. This is a direct application of the [[Lessons Learned - Bug Patterns]] narrow-sibling rule (the `TitleClearScreen` lesson): prefer a change that *cannot* affect other callers over one that merely *shouldn't*.

The Pokémon `ASSERT` was dropped; the move and trainer ones stay, since neither has any reason to cross `HM01`.

### Register-ordering detail
The inserted `ld a, [wNameListType]` clobbers the index the following `cp HM01` needs, so `a` is reloaded from **`wNameListIndex`** (the function's documented input) before the compare. Reloading from `wNamedObjectIndex` would also work *at this exact point* but is the worse habit — that byte is unioned with `wTypeEffectiveness`/`wMoveType`/`wNumSetBits` in `ram/wram.asm` and is only incidentally valid here.

## Verification (9/9)
A clean `-Weverything` build proved nothing behavioral, as always on this project. Verified by direct-call assertions in PyBoy:

| Case | Result | Proves |
|---|---|---|
| `MONSTER_NAME @ $C4` | garbage bytes, **not** "TM01" | `GetMonName` path now taken — **the fix** |
| `MONSTER_NAME @ $F0` | garbage bytes, not TM/HM | holds well above the old ceiling |
| `MONSTER_NAME @ $99` | `BULBASAUR` | no regression below ceiling |
| `MONSTER_NAME @ $15` | `MEW` | no regression |
| `ITEM_NAME @ $C4` | `HM01` | **TM/HM redirect preserved for items** |
| `ITEM_NAME @ $C9` | `TM01` | same |
| `ITEM_NAME @ $04` | `POKé BALL` | normal item lookup intact |
| `MOVE_NAME @ $01` | `POUND` | move names intact |
| `TRAINER_NAME @ $01` | `YOUNGSTER` | trainer names intact |

Garbage at `$C4`/`$F0` is the **correct** result — there's no species there yet. What matters is that it's not a TM name.

## A harness bug found along the way
The first run reported 6 of 9 failing — all timeouts, all on the `GetMonName`/`GetMachineName` branches, *including a pure-vanilla case that couldn't possibly have been broken by the fix*. That pattern (a case with no plausible connection to the change also failing) is the tell for a harness problem.

Root cause: the harness poked `pyboy.memory[0xFF50] = 1` **and** booted the game. Those are contradictory — the poke unmaps the Nintendo boot ROM *while the CPU is still executing inside it*. Signature: `PC` parked at `$0038` (an `rst` vector — the classic "executing `$FF` filler" crash) and `SP` wandered into cart-RAM (`$a290`), **before** the forced `PC` jump ever happened.

Fix: **if you're booting the game at all, don't poke `0xFF50`** — the boot ROM unmaps itself on the way out, leaving real cartridge code at `0x0000-0x00FF` anyway, plus a sane stack (`SP=$dfe9`) and bank. Now recorded as a correction in [[PyBoy Testing Techniques]], with a cheap guard worth keeping: `assert SP > 0xC000` after boot, so a crashed boot fails loudly instead of masquerading as a failing function.

## Net effect
Species indexes are usable up to `$FF` → **~101 free slots** (36 reclaimed gaps + `$BF`–`$FF`) against **~90 needed**. The ceiling is no longer the binding constraint.

**Explicitly not yet done** (none covered by this phase, each needs its own verification): raising `NUM_POKEMON_INDEXES` itself, growing `MonsterNames`/`BaseStats`/`PokedexOrder`/`EvosMovesPointerTable`, and growing the Pokédex seen/owned bit arrays (`NUM_POKEMON`, currently 151).

## Related
- [[Kanto Reborn - Overview]] — the parent effort
- [[PyBoy Testing Techniques]] — the boot-ROM correction this surfaced
- [[Lessons Learned - Bug Patterns]] — the narrow-sibling rule applied here
