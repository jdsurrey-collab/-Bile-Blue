# Kanto Reborn — Encounter Overhaul + Gen 2 Species Import

**Status:** 🔄 In progress — Phase 0 (species-index ceiling) ✅ done and verified

## Summary
Two combined efforts, being built together:
1. **Encounter overhaul** — rework every wild table so location actually matters (forests biologically diverse, caves strange, Power Plant dangerous, late-game areas producing genuinely absurd encounters), with rarity tiers and spawn-rate/catch-difficulty as *separate* axes.
2. **Gen 2 species import** — bring in all ~90 Gen 2 species that fit Gen 1's engine without new mechanics, sourced from the `pokegold-reference/` disassembly in the repo root.

Source design doc: `Pokemon Reborn` (repo root) — the encounter philosophy and per-route tables.

## Locked-in decisions

| Decision | Choice |
|---|---|
| Sequencing | Both together, not phased separately |
| Gen 2 scope | All ~90 species whose types already exist in Gen 1 (**no Dark/Steel**) |
| Excluded by type | Umbreon, Steelix, Scizor, Tyranitar, Sneasel, Houndour/Houndoom, Murkrow, Skarmory, Forretress, Magnemite/Magneton retyping |
| Route table size | Trim each to the existing 10-slot `NUM_WILDMONS` cap — no engine change |
| Legendaries | **Single-location** (scoped down from the doc's multi-location "home ranges") |
| Fishing | **Skipped** — Old/Good/Super Rod stay close to vanilla |
| Special stat | Gen 2's Sp.Atk/Sp.Def **averaged** into Gen 1's single Special |
| Sprites | Real Gen 2 art via pokered's own `tools/pkmncompress` pipeline |
| New moves | Small shortlist only (see below) |
| Trade evos (Politoed/Slowking/Kingdra) | Wild-catchable in **final form only**, no evolution chain built |
| Friendship evos (Pichu/Cleffa/Igglybuff/Crobat) | **Substituted level-up** thresholds |
| Pokédex | Full integration + Victorian-gothic flavor text for all new species |

## New moves shortlist (approved)
Each reuses an existing Gen 1 move-effect archetype — new numbers on proven logic, no new engine behavior:

| Move | Type | Reuses |
|---|---|---|
| Zap Cannon | Electric | Body Slam/Thunder's paralyze-on-hit, at 100% |
| Icy Wind | Ice | Bubblebeam (damage + stat-down) |
| Spark | Electric | Thundershock |
| Cotton Spore | Grass | String Shot, bigger drop |
| Sweet Scent | Normal | Sand Attack's accuracy-down, mirrored to evasion |

**Deliberately excluded:** Curse (branches completely differently for Ghost vs non-Ghost, changes 3 stats at once — no Gen 1 analogue), Rollout (needs a consecutive-*use* power accumulator; Rage's accumulator triggers on being *hit*, not on repeated use), Attract (needs per-individual gender, which Gen 1 does not track at all — only species-level gender *ratio* exists).

## Progress

| Phase | What | Status | Build |
|---|---|---|---|
| 0 | Species-index ceiling ([[Species Index Ceiling - GetName Fix]]) | ✅ 9/9 verified | v0.23 |
| 1 | WRAM budget + 89 species into all 8 tables | ✅ 12/12 verified | v0.24 |
| 2 | Base stats, sprites, palettes, icons, cries | ✅ | v0.24 |
| 3a | Real movesets + evolution chains | ✅ | v0.25 |
| 3b | 5 back-ported Gen 2 moves | ✅ 7/7 verified | v0.26 |
| 4 | Wild tables, 55 maps — **89/89 obtainable** | ✅ verified | v0.27 |
| 3c | Victorian-gothic dex entries | ⬜ not started | |
| 3d | Per-species TM/HM sets | ⬜ not started | |
| — | In-game playtest (dex UI, save/load) | ⬜ not started | |

**Final roster: 89** (100 Gen 2 − 10 Dark/Steel − Unown). Internal indexes to 243 (ceiling 255); dex renumbered contiguously 152–240.

## Encounter reference
- [[Encounter Map - Locations & Rates]] — every area, every species, real percentages and levels
- [[Where to Find Each Species]] — the reverse lookup, plus which species are evolve-only

Both are **auto-generated** from `data/wild/maps/*.asm` by `tools/wild_report.py`. Regenerate after any encounter change rather than editing by hand, so they can't drift from the ROM.

## Tooling (checked in)
- `tools/gen2_import.py` — roster + index assignment. `--manifest` inspects without writing.
- `tools/gen2_emit.py` — writes every table. Restores from `tools/gen2_pristine/` first (its edits aren't reversible in place).
- `tools/wild_tables.py` — encounter tables.
- `tools/tests/` — PyBoy regression tests.

## Two bugs that shipped in v0.27 (fixed in v0.29)

Both surfaced from play — "Wild MISSINGNO. appeared" and blurred sprites on the title screen.

### 1. Off-by-one in every index walker
`constants/pokemon_constants.asm` starts with a bare `const_def` then `const NO_MON ; $00` — the counter starts at **0** and `NO_MON` takes index `$00`. The tooling set its counter to `0` on `const_def` and incremented on the first `const`, making **every index +1 too high**.

Because both walkers shared the bug they agreed with each other, so the constants file got the *right lines* replaced and its generated `; $XX` comments looked self-consistent. But table patching writes by **position**, so all 36 gap-filled species had their name/dex-order/cry/dex-entry/evos pointer written one slot high — leaving their real slot reading `MISSINGNO` *and* clobbering the Gen 1 species one slot up (Bayleef's name landed on Growlithe).

The corrupted sprites came from the same shift hitting `PokedexOrder`: `IndexToPokedex` returned the wrong dex number → wrong `BaseStats` entry → wrong sprite pointer.

**Appended species (191+) were never affected** — only gap-filled ones — which is exactly why it presented as "*some* Pokémon are wrong".

Nothing caught it: the build was clean, `assert_table_length` only checks *lengths*, and the round-trip test happened to spot-check appended species plus two gap-filled ones whose neighbours were also gaps.

Now guarded by `test_species_alignment.py`, which cross-checks all 243 constants against the name-table bytes in the built ROM.

### 2. Sprite banks can't be derived from index ranges
`home/pics.asm` picked a mon's pic bank from hardcoded index thresholds. That only worked because vanilla's index order and pic-bank order grew in lockstep. Imported species break it both ways — scattered indexes, and sprites in six separate floating sections.

Replaced with an exact lookup table (`MonPicBanks`). Costs *fewer* Home-bank bytes than the range checks (~25 vs ~38) and can't silently desync. Verified by `test_pic_banks.py` against the **linker's own symbols**.

### Lesson
Tests now resolve symbols from `pokered.sym` and species indexes from the constants file at run time. Fixing the off-by-one shifted indexes *and* moved the WRAM trampoline byte, turning two suites red for reasons unrelated to the game — and a stale trampoline fails as a *timeout*, indistinguishable from a broken function.

## Key constraints discovered
- **WRAM, not `GetName`, was the real ceiling.** Dex flag arrays live in the *saved* region; only 10 free bytes existed and DMG WRAM isn't bankable. Solved with `MONS_PER_BOX` 20→19 (frees 56 bytes, costs 12 storage slots). 44 bytes still free.
- **Near vs far pointers govern what can float.** Dex prose can live in any bank (`text_far` is bank-aware), but `PokedexEntryPointers`/`EvosMovesPointerTable` use near `dw` pointers dereferenced in the current bank — their data must stay co-located.
- **Rarity is slot order.** `data/wild/probabilities.asm` fixes each slot's chance (slot 0 ≈19.9% → slot 9 ≈1.2%), so tables are written commonest-first.
- 19 empty ROM banks (45–63) remain for future growth.

## Known deviations from canon
- Zap Cannon paralyses at Gen 1's rate, not a guaranteed 100% (would need a new effect handler).
- Metronome can't roll the 5 new moves (vanilla's bound left byte-for-byte as shipped).
- Gen 2's split Sp.Atk/Sp.Def averaged into Gen 1's single Special.
- Politoed/Slowking/Kingdra have no evolution chain — wild-catchable in final form instead.
- Friendship/stat-based evolutions substituted with plain level thresholds.

## Related
- [[Species Index Ceiling - GetName Fix]] — Phase 0 detail
- [[Lessons Learned - Bug Patterns]] — the narrow-sibling rule this fix followed
- [[PyBoy Testing Techniques]] — including the boot-ROM correction this work surfaced
- [[Single Merged ROM]] — the existing 10-slot `NUM_WILDMONS` constraint
