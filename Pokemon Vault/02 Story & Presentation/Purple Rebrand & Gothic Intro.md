# "Pokémon Purple" Rebrand & Gothic Pre-Title Intro

**Status:** ✅ Done

## Summary
The cartridge still identifies as `POKEMON RED` at the hardware level (deliberately untouched — wider ripple effects than the branding warrants), but the entire presentation layer is re-themed: a new "PURPLE VERSION" logo, and a brief gothic pre-title scene (castle/graveyard silhouette fading in, "PURPLE" stamping across it letter-by-letter) that plays before the normal title screen sequence.

## Key files
- `gfx/version.asm` — `Version_GFX`, points at `gfx/title/purple_version.png` (11 tiles wide, replacing `red_version.png`/`blue_version.png`)
- `engine/movie/title.asm` — `VersionOnTitleScreenText` (now a single unconditional sequential tile-code run)
- `home/init.asm` — now calls `farcall PlayGothicIntro` before jumping to the title screen
- `engine/movie/gothic_intro.asm` — the intro scene itself
- `gfx/title/gothic_intro_bg.png` — castle/graveyard silhouette (144-unique-tile, 4-shade DMG image, converted via `rgbgfx -u -T`)
- `gfx/title/gothic_intro_stamp.png` — "PURPLE" Impact-font wordmark stamp graphic

## How it works
- `Version_GFX` swaps in the new hand-generated logo bitmap; `VersionOnTitleScreenText` was simplified to one unconditional run matching its width (the old code had a red/blue-specific quirk splicing in the font's space glyph — not needed now that there's only one version string).
- Before the title screen, `home/init.asm` calls `farcall PlayGothicIntro`: the castle/graveyard silhouette fades in, "PURPLE" stamps across it letter-by-letter with a thud sound, then it all fades back out into the normal `DisplayTitleScreen` sequence.
- `title.asm` itself no longer touches the castle art at all. An earlier attempt tried showing it as a title-screen backdrop peeking through gaps around the logo/character — but that VRAM region turned out to double as where the cycling Pokémon's front sprite loads, corrupting both. A dedicated pre-title scene sidesteps the conflict and shows far more of the image besides.

## Non-obvious pitfalls (worth remembering for any future title/intro graphics work)

- **Regenerate `-u`/`-T` graphics as a pair, never separately.** `rgbgfx -u -T` produces a deduplicated tile sheet *and* a tilemap whose indices only make sense together. The `.2bpp` is gitignored/rebuilt by `make`, but the `.tilemap` is a checked-in source file `make clean` does *not* delete. Regenerating one without the other (or forgetting the `RGBGFXFLAGS += -u -T` Makefile line for a brand-new image) silently desyncs them — corrupted-looking image, **no build error**.
- **1bpp vs 2bpp loading matters.** A `rgbgfx --depth 1` graphic (simple B/W logos/text) must be loaded with `FarCopyDataDouble` (expands each 1bpp byte into a 2bpp pair) — not `FarCopyData`/`FarCopyData2` (straight byte copy, assumes source is already 2bpp). Wrong one compiles fine, scrambles tiles at runtime.
- **`hWY` vs `rWY`.** `hWY` (HRAM) is a shadow the VBlank handler copies into the real `rWY` register every frame — writing `rWY` directly without updating `hWY` gets silently overwritten next frame. Caused an entire scene to render pure white during development; check `hWY`/`rWY` first if a window-layer scene looks blank.
- **`wTileMap` vs VRAM.** The title screen's own tile placement (logo, mon, copyright) is written into `wTileMap` (WRAM staging buffer), not directly into `vBGMap0`/`vBGMap1` — an automatic transfer mechanism syncs it at specific choreography points; direct VRAM writes get silently clobbered on the next sync. (`gothic_intro.asm` avoids this by being a static LCD-off scene that writes `vBGMap0` directly for its initial reveal.) **This exact distinction is also the root of the [[SGB Colorization Cleanup]] dot-pattern bugs** — see that note.
- **ROMX bank switching for `FarCopyData`-family calls.** Any `INCBIN`'d data not living in the same bank as the code reading it needs a bank-aware copy routine (`FarCopyData`/`FarCopyData2`/`FarCopyDataDouble`, source bank in `a`) — a plain `CopyData` silently reads whatever bank happens to be paged in, not the bank the label's `BANK()` implies.
- **`layout.link` has zero slack per bank.** Growing an existing section even slightly can overflow a completely unrelated section sharing that bank. New/grown data is safest in its own floating `SECTION "...", ROMX` (no explicit bank) so the linker can bin-pack it — this is how `gothic_intro.asm` and the widened version-text graphic are both declared.

## Related
- [[SGB Colorization Cleanup]] — the `wTileMap`-vs-VRAM distinction from this feature is the direct root cause of that bug hunt
- [[Lessons Learned - Bug Patterns]] — general bank-switching and register-clobber lessons that recur across this project
