# Architecture Map

The disassembly mirrors the original ROM's bank layout. `main.asm` and `includes.asm` are the entry points that stitch everything together (`includes.asm` pulls in every file under `constants/` and `macros/` globally — they don't need per-file includes).

| Folder | What lives there |
|---|---|
| `constants/` | Global constant definitions (`rsreset`/`rsset` struct layouts, enums). `constants/pokemon_data_constants.asm` defines the party/box Pokémon struct (`MON_HP`, `MON_STATUS`, `PARTYMON_STRUCT_LENGTH`, etc.) referenced throughout `engine/` and `data/`. |
| `macros/` | Assembly macros — notably `macros/scripts/text.asm` (the `text`/`line`/`cont`/`para`/`done`/`prompt` DSL used by everything in `text/`). |
| `home/` | "Home bank" routines callable from anywhere via `rst`/`call` without a bank switch — party menu drawing, text printing, core utility functions. |
| `engine/` | The actual game logic: battle engine (`engine/battle/`), menus (`engine/menus/`), overworld events (`engine/events/`), item effects (`engine/items/`), organized by subsystem. |
| `data/` | Static game data — trainer parties (`data/trainers/parties.asm`), Pokémon base stats, move data, etc. |
| `scripts/` | One file per map — event/warp/NPC-trigger logic for that location. References dialogue via `text_far` pointers into `text/`. |
| `text/` | One file per map (matching `scripts/`) — actual dialogue/sign/menu text, using the macros from `macros/scripts/text.asm`. |
| `maps/` | Map blockset/tileset binary data and map header definitions (`maps.asm`). |
| `ram/` | WRAM layout definitions (`ram/wram.asm`) — where per-map state like `wPartyMon1HP` lives. |
| `gfx/`, `audio/` | Graphics and music/sound source data. |
| `tools/` | Small C helper programs used by the build (graphics conversion, patch generation, include scanning) — see `tools/Makefile`. |
| `vc/` | Virtual Console-specific constants/patches (the `red_vc` build target, not part of normal builds). |

## Mental model for dialogue work
`scripts/<Map>.asm` decides **when** text prints (`text_far _SomeLabelText`); `text/<Map>.asm` defines **what** that label actually says. The label name is shared between the two — grep for it to jump between trigger logic and prose.

## Related
- [[Victorian-Gothic Rewrite]] — the biggest consumer of the `scripts/`/`text/` split
- [[Build & Versioning]]
