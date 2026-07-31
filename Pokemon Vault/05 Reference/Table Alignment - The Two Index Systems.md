# Table Alignment — The Two Index Systems

**The single most dangerous class of bug in this project.** A misaligned species table is *never* a build error — `assert_table_length` only checks **lengths**, never contents. It ships silently and shows up in play as wrong names, wrong stats, or corrupted sprites.

Three separate alignment bugs shipped before this was properly understood. All three are now guarded by tests.

## The two systems

Gen 1 indexes species **two different ways**, and they are not interchangeable:

| Axis | Tables | Assert | Range |
|---|---|---|---|
| **Internal index** | `MonsterNames`, `PokedexOrder`, `CryData`, `PokedexEntryPointers`, `EvosMovesPointerTable`, `MonPicBanks` | `NUM_POKEMON_INDEXES` | 1–243 |
| **Dex number** | `BaseStats`, `MonsterPalettes`, `MonPartyData` | `NUM_POKEMON` (±1) | 1–240 |

`GetMonHeader` bridges them with `predef IndexToPokedex`.

**Rule:** before touching any species table, work out which axis it uses. Getting this wrong produces plausible-looking, completely wrong data.

## Bug 1 — the off-by-one (shipped in v0.27)

`constants/pokemon_constants.asm` opens with a bare `const_def` then `const NO_MON ; $00`. The counter starts at **0** and `NO_MON` legitimately consumes index `$00`.

The generators set their counter to `0` on `const_def` and incremented on the first `const` → **every index +1 too high**.

Because both walkers shared the bug they agreed with each other, so the *right lines* got replaced in the constants file and its generated `; $XX` comments looked self-consistent. But table patching writes by **position**, so all 36 gap-filled species had their name/dex-order/cry/dex-entry/evos pointer written one slot high — leaving their real slot reading `MISSINGNO` *and* clobbering the Gen 1 species one slot up.

Corrupted sprites came from the same shift hitting `PokedexOrder` → `IndexToPokedex` returned the wrong dex number → wrong `BaseStats` entry → wrong sprite pointer.

**Appended species (191+) were never affected**, which is why it presented as "*some* Pokémon are wrong."

→ Guarded by `test_species_alignment.py`

## Bug 2 — sprite banks from index ranges

`home/pics.asm` derived a mon's sprite ROM bank from hardcoded index thresholds. That only works because vanilla's index order and pic-bank order grew in lockstep. Imported species break it both ways: scattered indexes, and sprites in six separate floating sections.

Replaced with `MonPicBanks`, an exact per-species lookup. Costs *fewer* Home-bank bytes than the range checks (~25 vs ~38).

→ Guarded by `test_pic_banks.py` (checks against the **linker's own symbols**, not the generator's intent)

## Bug 3 — the Mew hole in BaseStats

`GetMonHeader` reads `BaseStats + (dex - 1) * BASE_DATA_SIZE`, so the table must be **contiguous by dex number**.

Vanilla ships only 150 entries: Mew (dex 151) is stored separately (a famous last-minute addition) and special-cased before the lookup. With nothing above dex 151, the hole was harmless.

It stopped being harmless the moment dex 152+ existed — **every imported species read the next species' entry**, and the last one read off the end of the table. Wrong base stats *and* a wrong sprite pointer, since `dw XPicFront, XPicBack` lives in that struct.

Fixed by filling the hole with Mew's own data (never read for Mew itself, which is still special-cased) and changing the assert from `NUM_POKEMON - 1` to `NUM_POKEMON`.

Found by a deliberate audit pass, **not** by any existing test — the internal-index tests all passed because this is the *other* axis.

→ Guarded by `test_base_stats_alignment.py`

## Why the build never catches these
- `assert_table_length` verifies **length only**
- A wrong species constant still assembles fine — it's a valid symbol
- Sprite/stat corruption is data, not code

**The only reliable check is comparing generated tables against the built ROM's actual bytes**, which is what the alignment tests do.

## Related
- [[Kanto Reborn - Overview]]
- [[Lessons Learned - Bug Patterns]]
- [[PyBoy Testing Techniques]]
