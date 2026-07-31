# SGB Screen-Colorization Cleanup

**Status:** 🔄 Mostly done — title screen fully fixed without regression; one latent bug class confirmed present in ~30 other files, not yet touched

## Summary
This game's presentation is meant to read as clean black/white/gray on real hardware and Super Game Boy alike, never tinted. Several stray SGB palette definitions were flattened to plain white, and — after multiple rounds of "still dotted" reports — two independent real bugs were found and fixed: a border-palette dither issue, and a title-screen-specific blank-tile bug that took real digging (and one regression) to fully resolve.

## Key files
- `data/sgb/sgb_border.asm` — `PAL_SGB1`/`PAL_SGB2`/`PAL_SGB3` (border decoration palettes)
- `data/sgb/sgb_palettes.asm` — `PAL_LOGO1`/`PAL_LOGO2`/`PAL_MEWMON`/`PAL_TITLEMON` (new)
- `data/sgb/sgb_packets.asm` — `BlkPacket_Titlescreen`, `PalPacket_Titlescreen`, `PalPacket_PartyMenu`, `PalPacket_TrainerCard`, `PalPacket_Generic`
- `constants/palette_constants.asm` — `PAL_TITLEMON` constant
- `engine/movie/title.asm` — `ClearBothBGMaps`, 3 call sites now using `TitleClearScreen`
- `engine/movie/intro.asm` — 1 call site now using `TitleClearScreen`
- `home/copy2.asm` — `ClearScreen` (reverted to vanilla), new sibling `TitleClearScreen`
- `constants/charmap.asm` — the charmap mapping at the root of the whole bug class (`' '` → tile `$7F`, not blank)

## The border fix (round 1 — real, but incomplete)
`PAL_SGB1`/`PAL_SGB2`/`PAL_SGB3` (under `IF DEF(_RED)`) each colorized a different region of the SGB *border* graphic — originally a pink/salmon, green, and blue-purple dotted pattern respectively. The border art uses a checkerboard dither of 2 DMG shades to fake a mid-tone gray on real hardware; SGB-colorizing those two dither shades as genuinely different hues turns the smooth gray into visible two-color dots.
**Fix:** flattened all three to plain white (`RGB 31,31,31` ×4).
**This did not fully resolve the user's report** — a second, unrelated dot pattern lived inside the game screen itself, not the border.

## The title-screen background dot pattern (rounds 2–5 — the real hunt)

### Round 2: `ClearBothBGMaps` — right bug class, wrong buffer (partially)
`title.asm`'s `ClearBothBGMaps` filled the whole background with char literal `' '`, which `constants/charmap.asm` resolves to tile `$7F` — not blank in `gfx/font/font.png`, but the small raised "." glyph used as a date separator in the copyright string. Invisible on plain DMG grayscale; visible as a tiled dot pattern once SGB colorization made shade 0 and shade 3 genuinely different hues.
**Fix:** filled with `$40` instead — a raw numeric tile index (bypasses the charmap), confirmed genuinely all-zero.
**Not the whole story:** this function clears VRAM directly, but the title screen's *own* tile placement (logo, mon-cycling, copyright) is written into `wTileMap` (WRAM), synced to VRAM later by an automatic transfer. The user re-reported "still purple and green with dots" on the same rebuilt ROM — confirmed via "which ROM are you on" / "19" that this wasn't a stale-build misunderstanding.

### Round 3: `ClearScreen` — the actual culprit for the visible backdrop
`home/copy2.asm`'s `ClearScreen` — what actually clears `wTileMap` — had the **exact same bug**, completely independently: `ld a, ' '` → tile `$7F`. Caught by loading the built ROM into PyBoy and reading `wTileMap`'s WRAM bytes directly — every "blank" cell in the mon-cycling area really did hold `$7F`. With `LCDC` bit 4 clear (confirmed live, not assumed — the "$8800 signed" addressing mode), tile `$7F` resolves to VRAM address `$9000 + $7F*16 = $97F0`, landing inside the title screen's own loaded logo/copyright graphics — a real, non-blank alternating-row pattern.
**Fix (first attempt):** changed `ClearScreen` itself to fill with `$40`.
**Lesson:** two visually similar "dotted background" reports in the same session had two unrelated root causes (border palette vs. this charmap/tile-index mismatch) — always re-derive from raw tile bytes rather than assuming a second report means the first fix was incomplete.

### Round 4: `PAL_MEWMON` overcorrection (a parallel, unrelated regression caught mid-hunt)
A separate pass also flattened `PAL_MEWMON`'s background color directly, reasoning it's the palette the title screen's Pokémon-cycling backdrop uses. True — but `PAL_MEWMON` is *also* shared by the party menu, trainer card, and naming screen's `PalPacket_Generic`. That one change silently re-tinted all of those too, surfaced by the user via an unrelated-looking "why is the naming screen whiter now" screenshot.
**Fix:** reverted `PAL_MEWMON`, added a dedicated `PAL_TITLEMON` (`constants/palette_constants.asm`, appended after `PAL_GAMEFREAK` so no other index shifts) with the same foreground colors but a pure-white background, and pointed `PalPacket_Titlescreen`'s 3rd `PAL_SET` argument at it instead.
**Lesson:** before whitening any named palette in `sgb_palettes.asm`, grep `sgb_packets.asm` for every `PAL_SET`/`ATTR_BLK` referencing it — a palette shared across unrelated screens needs its own dedicated copy for a screen-specific tweak.

### Round 5: the `ClearScreen` regression (a second, real user-reported bug from the round-3 fix)
Round 3's fix generalized a title-screen-only-verified change to a function used by **~25 other files** (`engine/battle/core.asm`, `engine/battle/animations.asm`, `engine/battle/end_of_battle.asm`, `engine/menus/party_menu.asm`, `engine/pokemon/evos_moves.asm`, and more). `$40` was only ever confirmed blank in the *title screen's specific VRAM state* — during battle or the party menu, completely different graphics occupy that address, so the "blank" fill instead showed wrong graphic data. Reported directly by the user: *"weird grays during battle... the pokemon screen that popped up was full of blurry artifacts"* (right after collecting Eevee from Oak).
**Fix:** reverted `ClearScreen` back to vanilla (`ld a, ' '`, i.e. tile `$7F` — a latent, not-currently-known-to-be-visibly-wrong artifact everywhere else it's used). Added a **new, narrowly-scoped sibling function**, `TitleClearScreen` (same Home bank, callable via plain `call` from anywhere), identical except it fills with `$40`. Only the 4 actual title/intro call sites were repointed at it (3 in `title.asm`, 1 in `intro.asm`). Confirmed via PyBoy: `ClearScreen` fills with `0x7f`, `TitleClearScreen` fills with `0x40`, checked in separate fresh PyBoy instances to avoid stale-state false positives.
**Standing lesson (see [[Lessons Learned - Bug Patterns]]):** a fix verified correct in one specific screen/context does not transfer to every caller of a shared, low-level utility function — give it its own narrowly-scoped sibling instead of generalizing, unless independently verified safe for literally every caller.

## Known open issue — not yet acted on
The same `ld a, ' '` bug (→ tile `$7F`, invisible on DMG, SGB-dependent visibility) exists in **roughly 30 more places**: `home/window.asm`, `home/vcopy.asm`, `home/text.asm`, `engine/battle/core.asm`, `engine/battle/animations.asm`, `engine/gfx/hp_bar.asm`, `engine/battle/print_type.asm`, `engine/pokemon/status_screen.asm`, `engine/link/cable_club.asm`, `engine/items/town_map.asm`, `engine/menus/pokedex.asm`, `engine/menus/start_sub_menus.asm`, `engine/overworld/player_state.asm`, `engine/movie/hall_of_fame.asm`, `engine/movie/credits.asm`, `engine/movie/trade.asm`. **Only the two feeding the title screen have been fixed.** This is a documented latent-bug class, not confirmed to visibly affect gameplay anywhere else yet — don't fix speculatively; wait for an actual reported artifact on one of these screens, then fix that one call site narrowly. Tracked in [[Roadmap & Ideas]].

## Verification constraint
PyBoy renders in plain DMG grayscale — **no SGB colorization support at all**. A screenshot from it never shows whether a palette edit did what was intended, only whether the ROM still boots/runs. `assert_table_length NUM_SGB_PALS` passing at build time is the correctness check available for palette-table changes. Tile-*content* bugs (is this tile actually blank?), on the other hand, **are** directly verifiable via PyBoy by reading raw VRAM/WRAM bytes — see [[PyBoy Testing Techniques]].

## Related
- [[Purple Rebrand & Gothic Intro]] — the `wTileMap`-vs-VRAM distinction this whole bug class hinges on
- [[PyBoy Testing Techniques]] — the direct-VRAM-read technique that actually cracked rounds 2–3 and 5
- [[Lessons Learned - Bug Patterns]] — the "don't generalize a narrowly-verified fix" lesson, restated in full
