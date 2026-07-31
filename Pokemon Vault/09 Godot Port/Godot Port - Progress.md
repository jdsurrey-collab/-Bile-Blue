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

## Phase 3 — Startup sequence 🔄 in progress, core flow working end-to-end

Built and **verified by screenshot at every stage** (a clean run is not proof — see [[Test Suite]]'s equivalent rule on the ROM side):

| Stage | Status |
|---|---|
| Gothic intro (castle silhouette, PURPLE stamp, skippable) | ✅ |
| Title screen (logo, PURPLE VERSION, cycling starter, copyright) | ✅ |
| Main menu (NEW GAME/CONTINUE/OPTION) | ✅ |
| Oak's speech (real portrait, full gothic monologue, rival portrait swap) | ✅ |
| Naming screen (RED/ASH/JACK + BLUE/GARY/JOHN suggestions, letter grid) | ✅ |
| Lands in Red's House 2F | ✅ |

**New:** `tools/godot_export_startup.py` — exports the gothic intro art, title/logo/version graphics, Oak/rival portraits, and Oak's monologue text (`OakSpeechText1/2A/2B`, naming lines) straight from `data/text/text_2.asm`. `SceneFlow` autoload sequences the chain; `NamingScreen` is a reusable overlay component (matching how the ROM reaches naming via a mid-script `predef` call, not a scene swap).

### A real bug this caught: dialogue advancement was scene-bound
`Dialogue.advance()` was only ever wired up in `player.gd`'s `_process` — which only exists in the **overworld** scene. Oak's Speech has no player node, so its dialogue showed page one and then **never advanced again**. The verification driver's final state (`player=RED rival=BLUE`) looked like a pass at first glance, but that was `GameState`'s untouched *initial* defaults, not evidence naming had run — a fake-pass that only screenshot inspection caught.

Fixed by moving "interact advances the box" into the `Dialogue` autoload itself, since it's the one thing present in every scene. Removed the now-duplicate handling from `player.gd` (leaving both would double-advance, skipping a page per press).

### The verification-driver rabbit hole (worth remembering)
Building a synthetic-input test harness surfaced the same "testing each link isn't testing the chain" lesson as the ROM side, in a new shape:

1. **First attempt** toggled press/release on a fixed real-time schedule — raced with scene transitions still inside an unrelated `await` (a fade tween), so a press could fire and release *before* the target scene was even listening.
2. **Second attempt** held the button continuously until an observable check passed — but the game's own scripts correctly use `is_action_just_pressed` (a real button press is a discrete edge, not a held state), which only fires **once**, at the start of a hold. If that single frame doesn't line up with the target's `_process()` (an ordering quirk between an autoload and whatever scene is current), a multi-second continuous hold produces zero further chances.
3. **Fix**: pulse the input in short press/release cycles instead of one continuous hold — each cycle is a fresh edge, giving many independent chances rather than betting everything on one frame.

None of this is a defect in the shipped input code, which is standard, correct practice for real human input. It only matters for *driving* the game programmatically.

## Next
- [ ] Export mon front/back pics
- [ ] Phase 2: script engine, warps/connections, party model, save/load
- [ ] Phase 3 remainder: cultist dream sequence, Red's House 1F, warp into Pallet Town
- [ ] Phase 4: battle engine
- [ ] Phase 5: **boot → Gary fight ends** ← target

## Related
- [[Port Plan]] · [[Pokemon Data Map]] · [[Table Alignment - The Two Index Systems]]
