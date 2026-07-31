# Pokémon Purple — Project Overview

*Start here. This is the vault's homepage — everything else hangs off this note.*

## What this is

A grimdark, gritty, **Victorian-gothic reimagining of Pokémon Red/Blue**, forked from the [pret/pokered](https://github.com/pret/pokered) disassembly. Same Gen 1 hardware, same core battle math — the changes are systemic (permadeath, hidden power tiers, smarter AI) and presentational (gothic rewrite, rebrand, original soundtrack), never a Gen 2+ mechanics import.

Repo root: `c:\Users\jdsur\Desktop\PokemonPurple`
GitHub fork: `jdsurrey-collab/-Bile-Blue` (remote `origin`); `upstream` still points at `pret/pokered` for pulling fixes.

## The ten pillars

Each of these is a full system, documented in its own note. This list mirrors the root `CLAUDE.md`'s own numbered breakdown, in the same order.

| # | System | Status | Note |
|---|---|---|---|
| 1 | Hardcore permadeath | ✅ Done | [[Permadeath Mode]] |
| 2 | Victorian-gothic story rewrite | ✅ Done | [[Victorian-Gothic Rewrite]] |
| 3 | Single merged ROM (no version exclusives) | ✅ Done | [[Single Merged ROM]] |
| 4 | "Purple" rebrand + gothic pre-title intro | ✅ Done | [[Purple Rebrand & Gothic Intro]] |
| 5 | Hidden per-Pokémon power tier | ✅ Done | [[Hidden Tier System]] |
| 6 | Eevee-only starter | ✅ Done | [[Eevee-Only Starter]] |
| 7 | Industrial-goth score | 🔄 In progress — 5 tracks done, most of the OST still vanilla | [[Industrial-Goth Score]] |
| 8 | Cultist dream sequence (replaces free starting stones) | ✅ Done | [[Cultist Dream Sequence]] |
| 9 | SGB screen-colorization cleanup | 🔄 Mostly done — one latent bug class (~30 sites) still open | [[SGB Colorization Cleanup]] |
| 10 | Smarter trainer battle AI | ✅ Done | [[Smarter Trainer AI]] |
| 11 | Kanto Reborn — encounter overhaul + 89 Gen 2 species | 🔄 Data complete & verified; prose/TM polish open | [[Kanto Reborn - Overview]] |

## Cross-cutting reference

These aren't features — they're how the project actually gets built and debugged, and are worth knowing before touching anything:

- [[Architecture Map]] — what lives in `constants/`, `home/`, `engine/`, `data/`, `scripts/`, `text/`, `ram/`, `gfx/`, `audio/`
- [[PyBoy Testing Techniques]] — how this project actually verifies Z80 behavior with no interactive emulator available
- [[Lessons Learned - Bug Patterns]] — recurring bug classes hit more than once (register-clobbering `farcall`s, over-generalized "fix the shared function" mistakes, hex-vs-decimal constant comments)
- [[Build & Versioning]] — build commands, the `Roms/vX.Y` snapshot convention, why `make compare` doesn't apply here anymore

## What's next

See [[Roadmap & Ideas]] for open threads — right now that's mainly the rest of the soundtrack conversion, the remaining `ld a, ' '` blank-tile bug sites, and a discussed-but-not-started **memorial/graveyard system** for permadeath'd Pokémon.

## How to use this vault

- Every feature note follows the same shape: **Status**, **Summary**, **Key files**, **How it works**, **Bugs hit & fixes**, **Related**.
- Update the relevant note (and this table's status column) whenever a system changes — this vault is meant to track progress incrementally, not be a one-time snapshot.
- The repo's own root `CLAUDE.md` is the single source of truth for exact code-level detail; this vault restates it in a navigable, cross-linked form and is where day-to-day progress notes and the roadmap live instead.
