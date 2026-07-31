# Godot Port — Master Plan

**Goal:** a 1:1 playable port of Pokémon Purple in Godot 4.4 / GDScript.
**Project:** `C:\Users\jdsur\Documents\pokemonpurple`
**Source of truth:** the pokered disassembly. Data is *exported*, never retyped.

---

## The governing principle

> **Port the engines, convert the data. Never hand-build content.**

The ROM is already data-driven — maps, text, species, moves and trainers are all tables consumed by a handful of engines. The port mirrors that exactly:

| Layer | ROM | Godot |
|---|---|---|
| Data | `.blk`, `.asm` tables | exported JSON |
| Engines | assembly routines | GDScript autoloads/scenes |
| Content | — | *emerges from the two above* |

**Why this matters:** there are ~250 maps, 240 species, 170 moves and ~400 trainers. Hand-authoring any of that is how a port dies. The only things legitimately hand-written are **map scripts** (assembly state machines that can't be auto-translated) — and only ~50 maps have one.

**Corollary:** if a task feels like data entry, stop and write an exporter instead.

---

## Architecture

```
pokered repo                          Godot project
─────────────────────────────         ──────────────────────────────
tools/godot_export.py        ──────►  data/maps/*.json
                                      data/text/*.json
                                      data/species.json
                                      data/moves.json
                                      data/trainers.json
                                      data/type_chart.json
                                      assets/tilesets/*.png
                                      assets/sprites/**/*.png

                                      scripts/autoloads/
                                        GameState    event flags, party, save
                                        Dialogue     text macro engine
                                        GameData     species/moves/trainers
                                        SceneFlow    intro→title→menu→game
                                      scripts/overworld/   map loader, warps
                                      scripts/battle/      the battle engine
                                      scripts/scripts/     ported map scripts
```

### The two grids (never conflate)
- **tiles** 8×8 px — what the TileMapLayer draws
- **cells** 16×16 px — what actors move on (2×2 tiles)

One map block = 4×4 tiles = 2×2 cells. The exporter resolves this and ships `walkable` per-cell.

### Map scripts
ROM map scripts are state machines: `wCurMapScript` indexes a function table, each function advances the index. Ported as a `MapScript` base class with a `step(state)` method and the same index semantics — so a ported script reads recognisably like the original, which makes verification against the source possible.

---

## Phases

Each phase ends in something runnable. No phase depends on a later one.

### Phase 0 — Foundation ✅ DONE
Project scaffold, autoloads, map JSON exporter, tile/collision pipeline, grid movement, NPC interaction, two-line dialogue box. **Pallet Town is playable.**

### Phase 1 — Complete the data pipeline
Everything downstream is blocked without this, so it comes first.
- [ ] Export **all** maps (~250) + all tilesets + all map text
- [ ] Export **species** (240): stats, types, moves, evolutions, dex, sprites, cries
- [ ] Export **moves** (170): power, type, accuracy, PP, effect
- [ ] Export **type chart** (`data/types/type_matchups.asm`)
- [ ] Export **trainers**: classes, parties, AI flags
- [ ] Export **mon front/back pics** as PNGs
- [ ] Export **map scripts inventory** — which maps have scripts, so the hand-port list is explicit rather than discovered late

**Exit:** every map loads and is walkable; all game data queryable from `GameData`.

### Phase 2 — Core systems
- [ ] **Text engine**: full macro set, `<PLAYER>`/`<RIVAL>` tokens, per-character scroll, ▼ prompt, yes/no boxes
- [ ] **Script engine**: `MapScript` state machines + event flags + triggers (step-on, on-enter, on-interact)
- [ ] **Warps & connections**: door warps, map-edge connections, spawn facing
- [ ] **Party model**: species instance, HP/stats/moves/PP, **tier (1-10)**, **DEAD_BIT permadeath**
- [ ] **Save/load** (`user://`, JSON)
- [ ] **Menus**: Start menu, Pokémon list, status screen (with the **Roman-numeral tier badge**)

**Exit:** walk the whole overworld, talk to everyone, save and reload.

### Phase 3 — Startup sequence *(the requested slice, part 1)*
Replicating boot → Pallet Town, 1:1:
- [ ] **Gothic intro** — castle art, "PURPLE" letter-by-letter stamp, fade
- [ ] **Title screen** — logo, PURPLE VERSION, cycling mon, cry
- [ ] **Main menu** — New Game / Continue / Options
- [ ] **Oak's speech** — monologue, Oak + Nidorino pics, fade choreography
- [ ] **Naming screen** — player + rival, default-name list
- [ ] **Cultist dream** — the 3 branching questions → Fire/Water/Thunder stone
- [ ] Red's House 2F → 1F → Pallet Town

**Exit:** unbroken play from boot to standing in Pallet Town.

### Phase 4 — Battle engine
The largest phase. Data-driven from Phase 1.
- [ ] Battle scene: sprites, HP bars, text box, slide-in animation
- [ ] Menus: FIGHT/PKMN/ITEM/RUN, move select, PP
- [ ] **Gen 1 damage formula exactly** (incl. the crit and 1/256 quirks)
- [ ] Type chart incl. **dual-type stacking**
- [ ] Status conditions, stat stages, move effects
- [ ] **Tier modifier** (±5%/step on base stats)
- [ ] **Permadeath** — faint sets DEAD_BIT, never revivable
- [ ] Trainer AI incl. **Purple's smarter AI** (switch-in scoring, kill-shot heuristic)
- [ ] Faint / whiteout / **Game Over + credits**

**Exit:** a full trainer battle plays correctly.

### Phase 5 — The Gary fight *(the requested slice, part 2)*
Integration milestone tying Phases 3+4 together:
- [ ] `OaksLab` script: Oak's speech, ball choice → **Eevee**, rival takes his
- [ ] `PalletTown` script: Oak stops you at the grass, follow-to-lab
- [ ] `RIVAL1` battle with the lab-only Sand Attack strip
- [ ] Post-battle: Oak's replacement Eevee if yours died

**Exit: boot → Gary fight ends, uninterrupted.** ← *the current target*

### Phase 6 — The rest
Route-by-route: wild encounters, items, HMs, gyms, Elite Four. Content only — the engines are done.

---

## Verification strategy

Same discipline as the ROM work: **a clean run is not proof.**

| Check | How |
|---|---|
| Project loads | `godot --headless --import` (0 errors) |
| No runtime errors | `godot --headless --quit-after N` |
| Renders correctly | dev screenshot node → inspect the frame |
| Data matches ROM | exporter round-trip tests |
| Damage formula | unit-test against known Gen 1 values |

Screenshot verification already caught a spawn bug that a clean run did not.

---

## Rules for this port

1. **Never hand-type game data.** Write an exporter.
2. **One scene per *system*, not per *map*.** Pallet Town added zero scenes.
3. **Keep ROM names.** `wCurMapScript` → `cur_map_script`. Makes diffing against source possible.
4. **Port map scripts literally**, preserving state-machine indices, then refactor — never "improve" while porting.
5. **Purple's changes are not optional.** Permadeath, tiers, gothic text, Eevee starter, smarter AI are the point of the fork.

## Related
- [[Godot Port - Progress]] — running status
- [[Pokemon Data Map]] — where each piece of species data lives in the ROM
- [[Table Alignment - The Two Index Systems]] — the indexing trap the exporters must respect
