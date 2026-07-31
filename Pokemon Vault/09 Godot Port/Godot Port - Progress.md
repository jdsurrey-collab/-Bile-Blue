# Godot Port — Progress

*Running status. Plan lives in [[Port Plan]].*

## Phase 0 — Foundation ✅
Project scaffold, autoloads, grid movement, NPC interaction, dialogue box. **Pallet Town playable**, verified by screenshot.

## Phase 1 — Data pipeline 🔄 mostly done

| Export | Result |
|---|---|
| Maps | **221 / 225** |
| Tilesets | 19 (all) |
| Species | 240 |
| Moves | 170 (incl. the 5 back-ported) |
| Types | 16 types, 82 matchups |
| Trainers | 45 classes, 47 names |
| Map scripts needing hand-port | **100** (known list) |

**Skipped (4):** `UnusedDiglettsCaveCopy`, `UnusedEmptyMap`, `UnusedPokecenterCopy` (beta/unused, no header) and `UndergroundPathNorthSouth` (`.blk` size disagrees with its declared dimensions — worth a look, but one map).

**Still to do in Phase 1:** mon front/back pics as PNGs.

### The tileset-alias bug (worth remembering)
The first full export silently dropped **24 maps including Oak's Lab and both Red's House floors** — all with `FileNotFoundError`.

Cause: tileset names are spelled differently in two places, and several are pure **aliases** sharing another tileset's art:

| Map header says | `gfx/tilesets.asm` labels it | Real asset |
|---|---|---|
| `DOJO` | `Dojo_GFX` | `gym` |
| `MART` | `Mart_GFX` | `pokecenter` |
| `MUSEUM`, `FOREST_GATE` | `Museum_GFX`, `ForestGate_GFX` | `gate` |
| `REDS_HOUSE_1/2` | `RedsHouse1_GFX` | `reds_house` |

Deriving the filename from the tileset name *appears* to work because `"OVERWORLD".lower()` happens to be the real file — so Pallet Town passed and hid the problem. Fixed by parsing the stacked labels in `gfx/tilesets.asm` and matching on a normalised key (uppercase, underscores stripped).

**Lesson: a converter that works on the first sample proves nothing.** Run it across the whole corpus early — the failures are where the format's real complexity lives.

## Next
- [ ] Export mon front/back pics
- [ ] Phase 2: script engine, warps/connections, party model, save/load
- [ ] Phase 3: intro → title → menu → Oak speech → naming → cultist dream
- [ ] Phase 4: battle engine
- [ ] Phase 5: **boot → Gary fight ends** ← target

## Related
- [[Port Plan]] · [[Pokemon Data Map]] · [[Table Alignment - The Two Index Systems]]
