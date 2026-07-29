# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project scope

This is **Pokémon Purple**, a grimdark, gritty, Victorian-gothic reimagining of Pokémon Red/Blue, forked from the [pret/pokered](https://github.com/pret/pokered) disassembly. Four things distinguish it from vanilla pokered:

1. **Hardcore permadeath mode**: a Pokémon that faints in battle is permanently marked dead (bit 7 of `MON_STATUS`, unused by vanilla status ailments — see `constants/battle_constants.asm`'s `DEAD_BIT`). Dead Pokémon can never be revived (Pokémon Center, Revive, Max Revive all check the flag) and show `RIP` instead of `FNT` in the party screen (`home/pokemon.asm`). The player's own blackout behavior is untouched — whiting out still just returns you to the last Pokémon Center as in vanilla.
2. **Victorian-gothic story rewrite**: every NPC/sign/menu text in `text/*.asm` (plus the opening monologue in `data/text/text_2.asm`) has been rewritten in a darker, Victorian register (archaic diction, mourning/funeral imagery, class-conscious cruelty), each location given its own unique despair-flavored treatment while preserving the original substance. Each Gym Leader carries a distinct thematic flavor (Brock=stone/tomb, Misty=drowning, Surge=war veteran, Erika=beauty-and-rot, Koga=plague, Sabrina=madness, Blaine=ash/ruin, Giovanni=cold menace).
3. **Single merged ROM, no version exclusives**: this fork only builds one ROM (`pokered.gbc`; the `_BLUE` build path has been removed from the Makefile). All wild-encounter tables in `data/wild/maps/*.asm` that used to branch on `IF DEF(_RED)`/`IF DEF(_BLUE)` (Oddish/Bellsprout, Ekans/Sandshrew, Mankey/Meowth, Growlithe/Vulpix, Nidoran♂/♀, Scyther/Pinsir, etc.) have been flattened into a single unconditional list per map, so species from both original versions are catchable in this one ROM. Since each map's wild list is a fixed-size table (`NUM_WILDMONS = 10` slots, see `constants/pokemon_data_constants.asm`), duplicate filler slots were traded away rather than the table being lengthened — most exclusive species show up at reduced frequency compared to their native version, not 1:1 rate parity. The Game Corner prize lineup (`data/events/prizes.asm`, `prize_mon_levels.asm`) was intentionally left on its Red-version selection (Nidorina, Scyther/Dratini/Porygon) since the Blue-side equivalents (Nidorino, Pinsir) remain obtainable via wild-caught evolution/Safari Zone. Cosmetic-only `_RED`/`_BLUE` branches that don't gate catchable content (Game Corner slot-reel graphics, SGB border palette, the title-screen's randomly-chosen Pokémon list, default player/rival name suggestions) were left alone and simply resolve to their Red-flavored asset now that only `_RED` is ever defined.
4. **"Pokémon Purple" rebrand, with a gothic pre-title intro**: the cartridge still identifies as `POKEMON RED` at the hardware level (untouched — changing that has wider ripple effects than the branding warrants), but the presentation layer is re-themed throughout. `gfx/version.asm`'s `Version_GFX` points at `gfx/title/purple_version.png` (a small hand-generated "PURPLE VERSION" logo bitmap, 11 tiles wide, replacing the old `red_version.png`/`blue_version.png`), and `engine/movie/title.asm`'s `VersionOnTitleScreenText` is a single unconditional sequential tile-code run matching that width (the old code had a red/blue-specific quirk of skipping some tiles and splicing in the normal font's space glyph — not preserved, not needed now that there's only one version string). Before the title screen, `home/init.asm` now calls `farcall PlayGothicIntro` (`engine/movie/gothic_intro.asm`) instead of jumping straight there — this plays a brief full-screen scene: a Victorian-gothic castle/graveyard silhouette (`gfx/title/gothic_intro_bg.png`, converted to a 144-unique-tile, 4-shade DMG image via `rgbgfx -u -T`) fades in, "PURPLE" stamps across it letter-by-letter with a thud sound (`gfx/title/gothic_intro_stamp.png`, an Impact-font wordmark), then it all fades back out into the normal `DisplayTitleScreen` sequence. (`title.asm` itself no longer touches the castle art at all — an earlier attempt tried to show it as a title-screen backdrop peeking through the gaps around the logo/character, but that VRAM region turned out to double as where the cycling Pokémon's front sprite loads, corrupting both; a dedicated pre-title scene sidesteps the conflict entirely and shows far more of the image besides.)

   Several non-obvious pitfalls got hit building this, worth remembering for any future title/intro graphics work:
   - **Regenerate `-u`/`-T` graphics as a pair, and don't let them drift**: `rgbgfx -u -T` produces a deduplicated tile sheet *and* a tilemap whose indices only make sense together. The `.2bpp` is gitignored and rebuilt by `make` (`*.2bpp` in `.gitignore`), but the `.tilemap` is a checked-in source file `make clean` does *not* delete (matching this repo's existing convention for e.g. `gfx/sgb/red_border.tilemap`) — if you regenerate one without the other (or forget the `RGBGFXFLAGS += -u -T` Makefile line for a new image entirely, so the generic `%.2bpp: %.png` rule quietly rebuilds it *without* dedup), the tile sheet and tilemap silently stop matching and you get a corrupted-looking image with no build error. Always regenerate both from the same `rgbgfx` invocation and check they're both freshly written.
   - **1bpp vs 2bpp loading**: a graphic converted with `rgbgfx --depth 1` (used for simple black/white logos and text, e.g. the version-text and intro-stamp wordmarks) must be loaded with `FarCopyDataDouble` (which expands each 1bpp byte into a 2bpp pair), not `FarCopyData`/`FarCopyData2` (which do a straight byte copy and assume the source is already 2bpp). Using the wrong one compiles fine and produces visually scrambled tiles at runtime.
   - **hWY vs rWY**: `hWY` (HRAM) is a shadow copy that the VBlank handler (`home/vblank.asm`) copies into the real `rWY` register every frame (unless `wDisableVBlankWYUpdate` is set) — writing `rWY` directly without also updating `hWY` gets silently overwritten back on the next frame. If the window layer ends up covering the whole screen with a blank tile (this happened during `gothic_intro.asm` development — the entire scene looked pure white despite correct tile/tilemap data), check `hWY`/`rWY` before anything else.
   - **wTileMap vs VRAM**: the *title screen's own* tile placement (logo, mon, copyright) is written via `hlcoord`-style addressing into `wTileMap` (a WRAM staging buffer, `ram/wram.asm`), not directly into `vBGMap0`/`vBGMap1` — an automatic transfer/`TitleScreenCopyTileMapToVRAM` mechanism syncs it at specific points in the bounce/scroll choreography, and direct VRAM writes get silently clobbered on the next sync. (`gothic_intro.asm` avoids this entirely: it's a static scene with the LCD off during setup, so it writes `vBGMap0` directly for the initial reveal, and uses the auto BG transfer — `hAutoBGTransferEnabled`/`hAutoBGTransferDest` — only for the letter-by-letter stamp updates once the LCD is on.)
   - **ROMX bank switching for `FarCopyData`-family calls**: any data pulled in via `INCBIN` that doesn't live in the *same bank* as the code reading it must be copied with a bank-aware routine (`FarCopyData`/`FarCopyData2`/`FarCopyDataDouble`, which take the source bank in `a`) — a plain `CopyData` silently reads whatever bank happens to be paged in at the time, not the bank the label's `BANK()` value implies.
   - Also: this ROM's `layout.link` hand-assigns **every** section to a specific fixed bank with no slack; growing an existing section (even by a few bytes, e.g. widening the version-text graphic) can overflow a completely unrelated section sharing that bank. New/grown data is safest given its own floating `SECTION "...", ROMX` (no explicit bank) so the linker can bin-pack it anywhere with room, rather than bloating a section that's already tightly pinned — this is how `gothic_intro.asm` and the widened version-text graphic are both declared.

When touching dialogue in `text/*.asm`, keep to this Victorian-gothic despair tone, respect the ~18-visible-character-per-line budget for `text`/`line`/`cont`/`para` segments (the display box is 20 tiles wide; this matches the longest lines found in the original shipped/checksum-verified game), and preserve the existing macro skeleton (same count of `line`/`cont`/`para`/`done`/`prompt`) so box paging doesn't change.

When touching `data/wild/maps/*.asm`, remember there's no more `_RED`/`_BLUE` split to preserve — any new encounter added there just needs to keep the flat list at exactly `NUM_WILDMONS` (10) `db LEVEL, SPECIES` lines (`def_grass_wildmons`/`def_water_wildmons` assert this at build time).

## Git remotes

- `origin` → the personal fork this project pushes to (GitHub: `jdsurrey-collab/-Bile-Blue`)
- `upstream` → the original `pret/pokered` repo, kept for pulling in upstream fixes

## Build commands

Requires **rgbds 1.0.2** (`brew install rgbds` on macOS; see `INSTALL.md` for other platforms).

```sh
make              # builds pokered.gbc (the only ROM this fork produces)
make red          # same as above, explicit target name
make clean        # remove build artifacts (objects, compiled gfx, roms)
make RGBDS=path/to/rgbds/  # use a local rgbds install instead of the global one
```

There used to be a `pokeblue.gbc`/`pokeblue_debug.gbc` build path; it's been removed from the Makefile (see "Single merged ROM" above), so `make blue`/`make blue_debug` no longer exist.

`make compare` runs `sha1sum -c roms.sha1` to verify a byte-perfect rebuild — this is the project's only "test," and it references upstream pokered/pokeblue checksums that no longer apply here at all. **Don't rely on it on this fork.** A successful `make` (no assembler/linker errors under `-Weverything`) is the correctness bar for changes.

There's no separate lint step — `rgbasm`/`rgblink` are invoked with `-Weverything -Wtruncation=1`, so build warnings are the linting.

### Versioned ROM builds

Recompiled ROMs worth keeping go in `Roms/vX.Y/` (e.g. `Roms/v0.1/pokered.gbc`). This folder is gitignored (`/Roms/` in `.gitignore`) — bump the version folder each time you want to snapshot a build, don't commit the `.gbc` files themselves. (Older checkpoints in this folder from before the Red/Blue merge may still contain a `pokeblue.gbc` alongside `pokered.gbc` — that's just historical, going forward there's only ever one ROM per checkpoint.)

## Architecture

The disassembly mirrors the original ROM's bank layout; `main.asm` and `includes.asm` are the entry points that stitch everything together (`includes.asm` pulls in every file under `constants/` and `macros/` globally — they don't need per-file includes).

- **`constants/`** — global constant definitions (`rsreset`/`rsset` struct layouts, enums). `constants/pokemon_data_constants.asm` defines the party/box Pokémon struct (`MON_HP`, `MON_STATUS`, `PARTYMON_STRUCT_LENGTH`, etc.) referenced throughout `engine/` and `data/`.
- **`macros/`** — assembly macros, notably `macros/scripts/text.asm` (the `text`/`line`/`cont`/`para`/`done`/`prompt` text-printing DSL used by everything in `text/`).
- **`home/`** — "home bank" routines callable from anywhere via `rst`/`call` without a bank switch (party menu drawing, text printing, core utility functions).
- **`engine/`** — the actual game logic (battle engine in `engine/battle/`, menus in `engine/menus/`, overworld events in `engine/events/`, item effects in `engine/items/`), organized by subsystem.
- **`data/`** — static game data: trainer parties (`data/trainers/parties.asm`), Pokémon base stats, move data, etc.
- **`scripts/`** — one file per map, containing the event/warp/NPC-trigger logic for that location. Scripts reference dialogue via `text_far` pointers into `text/`.
- **`text/`** — one file per map (matching `scripts/`), containing the actual dialogue/sign/menu text for that location, using the macros from `macros/scripts/text.asm`.
- **`maps/`** — map blockset/tileset binary data and map header definitions (`maps.asm`).
- **`ram/`** — WRAM layout definitions (`ram/wram.asm`); this is where per-map state like `wPartyMon1HP` etc. lives.
- **`gfx/`, `audio/`** — graphics and music/sound source data.
- **`tools/`** — small C helper programs used by the build (graphics conversion, patch generation, include scanning) — see `tools/Makefile`.
- **`vc/`** — Virtual Console-specific constants/patches (the `red_vc` build target, not part of normal builds).

A useful mental model for dialogue work: `scripts/<Map>.asm` decides *when* text prints (`text_far _SomeLabelText`), and `text/<Map>.asm` defines *what* that label actually says. The label name is shared between the two, so grep for the label to jump between trigger logic and prose.
