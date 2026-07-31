# Lessons Learned — Recurring Bug Patterns

*Bug classes that have hit more than once across this project. Worth checking against before writing new bank-crossing or shared-utility code, regardless of which feature you're touching.*

## 1. `farcall`/`callfar` clobbers registers on BOTH sides of the call — never pass/return values through them
`Bankswitch` (`home/bankswitch.asm`) loads `a`/`b` with the destination bank right before jumping into the callee, and reloads them with the source bank right after the callee's `ret` — a value placed in `a`, `b`, or `hl` on either side of a `farcall`/`callfar` is gone by the time it matters.

**Occurred 3 times this project:**
1. [[Hidden Tier System]] — `ApplyTierModifier`'s return value in `a` was lost to `homecall`'s bank-restore `pop af`. Fixed with `hStatCalcTier`/`hStatCalcBase` HRAM bytes.
2. [[Cultist Dream Sequence]] — `AskCultistQuestion` took its menu-template argument and returned its answer both through `a` across a `farcall`, both directions silently broken. Fixed by routing both ways through WRAM (`wTextBoxID` in, `wCultistAnswer` out).
3. [[Smarter Trainer AI]] — `AIMoveChoiceModification5` called `GetTypeMatchupMultiplier` (a `b`/`c`/`d`-register-input function) via a plain cross-bank `call` that assembled fine but would execute garbage at runtime; the *safe* fix was calling the WRAM-only `AIGetTypeEffectiveness` wrapper via `callfar` instead.

**Standing rule:** before adding a `farcall`/`callfar` to any function, check what that function's calling convention actually is. If it takes register inputs or returns a register output, `farcall` is unsafe for it — always use a WRAM/HRAM byte instead, checked in both directions. If it reads/writes exclusively via WRAM/HRAM, it's safe to `farcall`.

## 2. A fix verified correct in one context does not transfer to every caller of a shared function
[[SGB Colorization Cleanup]]'s `ClearScreen` regression: a title-screen-specific "$40 is blank here" fix was generalized to a function used by ~25 unrelated files (battle core, party menu, evolution screens). `$40` was only ever proven blank in the *title screen's* specific VRAM state — during battle/party-menu, different graphics occupy that address, so the "blank" fill showed wrong data instead ("weird grays," "blurry artifacts" — reported directly by the user).

**Standing rule:** when a fix to a widely-shared, low-level utility function is only verified correct in the one specific screen/context that prompted it, that verification does not transfer to every other caller. Give the fix its own narrowly-scoped sibling function (see `TitleClearScreen` next to `ClearScreen` in `home/copy2.asm`) instead of generalizing the shared one — unless independently verified safe for literally every caller.

## 3. A clean build proves nothing behavioral
Confirmed across every feature this project: `-Weverything` catches assembly errors, never logic bugs. The only way any of the real bugs documented in [[Cultist Dream Sequence]], [[SGB Colorization Cleanup]], or [[Smarter Trainer AI]] were actually found was by running the built ROM in PyBoy and reading live registers/WRAM — see [[PyBoy Testing Techniques]].

**Standing rule:** treat "it built with no warnings" as necessary, never sufficient. Any change with real runtime behavior needs to be exercised, not just compiled.

## 4. Generated data can be self-consistently wrong
Three separate species-table misalignments shipped (see [[Table Alignment - The Two Index Systems]]). The common thread: **the generator and its own output agreed with each other**, so everything looked right.

The index off-by-one is the sharpest example — the same broken walker produced both the index assignment *and* the `; $XX` comments documenting it, so the constants file was internally consistent and completely wrong. `assert_table_length` passed because lengths were correct; only *contents* were shifted.

**Standing rule:** never validate generated data against the generator's own model of it. Validate against something independent — the built ROM's bytes, or the linker's symbol table. Every alignment test in this project does exactly that, which is why they catch what the build cannot.

## 5. Fixing an index bug invalidates every test that hardcodes one
Correcting the off-by-one shifted 36 species' indexes *and* moved the WRAM byte being used as the PyBoy trampoline. Two green suites went red for reasons that had nothing to do with the game.

Worse, a stale trampoline fails as a **timeout** — indistinguishable from a genuinely broken function, and the exact symptom that sent an earlier investigation down the wrong path entirely.

**Standing rule:** tests resolve addresses from `pokered.sym` and species indexes from `constants/pokemon_constants.asm` at runtime. Hardcode nothing that the build can move.

## 6. Move/effect ID constant comments are hex, without a `$` prefix
`constants/move_constants.asm`/`constants/move_effect_constants.asm` write e.g. `const MEDITATE ; 60` meaning **hex** `$60` = decimal 96 — not decimal 60 (which is actually `PSYBEAM`). Misreading this as decimal silently builds a test (or any other code) around the wrong move entirely.

**Verify by counting positional index directly, independent of the comment:**
```sh
grep -n "const [A-Z]" file.asm | awk -F: '{print NR-1, $0}'
```
Or cross-check the move's actual compiled bytes in `data/moves/moves.asm` against the ROM file at the right offset. Hit while testing [[Smarter Trainer AI]]'s Modification 5.

## 7. Don't trust a remembered type-chart/game-fact assumption — check `data/types/type_matchups.asm`
A test for [[Smarter Trainer AI]] asserted "Water Gun should be encouraged against a Grass-type target" — wrong: Grass resists Water in every generation, so this was never going to be super-effective. The assumption, not the code, was the bug.

**Standing rule:** cross-check any specific game-mechanics fact against the actual data table before writing a test or fix around it — don't trust a remembered assumption, even a seemingly obvious one.

## 8. A "second report of the same symptom" doesn't mean the first fix was incomplete — it might be a second, unrelated bug
Two visually similar "dotted background" reports in the same session ([[SGB Colorization Cleanup]]) had two completely unrelated root causes: a border-palette dither issue, and a title-screen charmap/tile-index mismatch. Assuming the second report meant the first fix "didn't fully work" would have wasted time re-checking already-correct code.

**Standing rule:** re-derive from raw data (tile bytes, palette tables, register state) each time, rather than assuming a repeated-looking symptom shares its predecessor's root cause.

## Related
- [[PyBoy Testing Techniques]] — the tool that actually surfaces these bugs
- [[Cultist Dream Sequence]], [[Hidden Tier System]], [[SGB Colorization Cleanup]], [[Smarter Trainer AI]] — full incident writeups each pattern is drawn from
