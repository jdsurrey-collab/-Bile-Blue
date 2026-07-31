# Test Suite

Eight suites in `tools/tests/`. Run them all:

```sh
for t in tools/tests/*.py; do echo "$t"; python "$t"; done
```

They need the PyBoy venv (`/root/pyboy-env/bin/python` in this WSL setup) and a current `pokered.gbc` + `pokered.sym`, so **build first**.

## What each one covers

| Test | Guards | Kind |
|---|---|---|
| `test_species_alignment.py` | All 243 species constants vs. the name-table bytes in the ROM | static |
| `test_base_stats_alignment.py` | `BaseStats` contiguous by **dex number** (the Mew hole) | static |
| `test_pic_banks.py` | All 239 pic banks vs. the **linker's own symbols** | static |
| `test_dex_line_budget.py` | All 89 gothic dex entries ≤18 chars/line + full coverage | static |
| `test_gen2_species.py` | Names + `IndexToPokedex` round-trip in the running ROM | emulated |
| `test_getname.py` | The `GetName` TM/HM-redirect fix, and that items/moves/trainers didn't regress | emulated |
| `test_permadeath.py` | `DEAD_BIT` is set on faint; `HealParty` refuses to revive the dead | emulated |
| `test_oakslab_replacement.py` | The wiped-party gate on Oak's replacement Eevee | emulated |

**Static** tests read the built ROM/symbols directly — fast, no emulator.
**Emulated** tests drive PyBoy with the direct-function-call harness ([[PyBoy Testing Techniques]]).

## Two rules these suites exist to enforce

**1. Resolve symbols and indexes at runtime — never hardcode.**
Tests read addresses from `pokered.sym` and species indexes from `constants/pokemon_constants.asm`. Fixing the off-by-one shifted every gap-filled index *and* moved the WRAM byte used as the PyBoy trampoline, which turned two suites red for reasons unrelated to the game. A stale trampoline fails as a **timeout**, which is indistinguishable from a genuinely broken function.

**2. Assert on memory, not on clean returns.**
`RemoveFaintedPlayerMon` runs faint animation code and `HealParty` is normally reached via `predef`; neither returns cleanly to a hand-pushed trampoline in a synthetic state. They "time out" even though the writes under test already happened. `test_permadeath.py` originally reported 2 false failures for exactly this reason — a permanently-red checked-in test is worse than none.

## What they do NOT cover
- Anything visual (sprite *quality*, SGB colour — PyBoy renders DMG grayscale only)
- Dex UI behaviour at 240 entries
- Save/load round-trip with the new layout
- Actual gameplay balance

Those still need a human on a real screen.

## Related
- [[Table Alignment - The Two Index Systems]]
- [[PyBoy Testing Techniques]]
- [[Lessons Learned - Bug Patterns]]
