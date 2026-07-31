# CLAUDE.md

## Project Overview
**Pokémon Purple** is a grimdark, Victorian-gothic reimagining of Pokémon Red/Blue, forked from the [pret/pokered](https://github.com/pret/pokered) Game Boy disassembly. It merges Red and Blue into one ROM, replaces the starter trio with an Eevee-only choice tied to a branching dream sequence, adds permadeath, a hidden per-Pokémon power tier, a from-scratch industrial-goth soundtrack, and a smarter trainer battle AI — all while staying within pure Gen 1 hardware/mechanics.

This vault is the project's navigation and progress-tracking layer. See [Project Overview](00%20Overview/Project%20Overview.md) for the full breakdown, or jump straight into a system folder below.

## Tech Stack
- **RGBDS** (assembler/linker/rgbfix/rgbgfx toolchain for Game Boy), version 1.0.2
- Z80 assembly (`.asm`), built via `make` — see [Build & Versioning](00%20Overview/Build%20&%20Versioning.md)
- Verification via a headless **PyBoy** (Python Game Boy emulator) test harness — see [PyBoy Testing Techniques](05%20Reference/PyBoy%20Testing%20Techniques.md)
- No JS/npm anywhere in this repo — this is a bare-metal ROM hack, not a web project

## Architecture
See [Architecture Map](05%20Reference/Architecture%20Map.md) for the full folder-by-folder breakdown (`constants/`, `home/`, `engine/`, `data/`, `scripts/`, `text/`, `ram/`, `gfx/`, `audio/`).

## Commands
```sh
make              # builds pokered.gbc (the only ROM this fork produces)
make clean        # remove build artifacts
make RGBDS=path/to/rgbds/   # use a local rgbds install
```
No `npm`/JS commands apply to this project — ignore the generic template defaults.

## Code Style
- Dialogue in `text/*.asm` must hold to Victorian-gothic tone and the ~18-visible-character-per-line box budget (see [Victorian-Gothic Rewrite](02%20Story%20&%20Presentation/Victorian-Gothic%20Rewrite.md))
- Any new `data/wild/maps/*.asm` entries must keep the flat 10-slot `NUM_WILDMONS` table (see [Single Merged ROM](02%20Story%20&%20Presentation/Single%20Merged%20ROM.md))
- Never pass/return a value through register `a`/`b`/`hl` across a `farcall`/`callfar` — always WRAM/HRAM (see [Lessons Learned](05%20Reference/Lessons%20Learned%20-%20Bug%20Patterns.md))

## Important Notes
- A fix verified correct in one screen/context does **not** transfer to every caller of a shared function — give it a narrowly-scoped sibling instead of generalizing (the `ClearScreen`/`TitleClearScreen` regression — see [Lessons Learned](05%20Reference/Lessons%20Learned%20-%20Bug%20Patterns.md)).
- `make compare` no longer applies to this fork (checksums are upstream pokered/pokeblue's) — a clean `make -Weverything` plus PyBoy behavioral verification is the real bar.
- Full authoritative detail always lives in the repo's own root `CLAUDE.md` — this vault is a navigable companion to it, not a replacement.

## Out of Scope
- No Gen 2+ mechanics (held items, breeding, new stats/types) — the AI and battle-system work stays pure Gen 1, by explicit design intent.
- The cartridge header still identifies as `POKEMON RED` at the hardware level — intentionally untouched.
- The player's own blackout/whiteout behavior is vanilla — only fainted-Pokémon permadeath was added.
