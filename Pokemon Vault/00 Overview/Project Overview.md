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
| 11 | Kanto Reborn — encounter overhaul + 89 Gen 2 species | 🔄 Feature-complete & verified; needs playtest | [[Kanto Reborn - Overview]] |

## The Godot port

A second, parallel project ports this ROM hack 1:1 to Godot 4.4/GDScript, at `C:\Users\jdsur\Documents\pokemonpurple` (not a git repo — this pokered repo is the source of truth, the Godot project is downstream of it). Governing principle: port the ENGINES, convert the DATA — never hand-build content. See **[[Port Plan]]** for the full plan and **[[Godot Port - Progress]]** for what's actually landed.

Status: Phases 0–4 done (data pipeline, seamless overworld/movement, party/save/menus, battle engine core). **Phase 5 ("boot → Gary fight ends") is done and verified end-to-end** — cultist dream, Pallet Town intercept, and Oak's Lab (starter choice + real rival battle + permadeath-aware post-battle heal/replacement) are all ported and confirmed with a from-cold-boot dev driver, zero shortcuts. Next up: Phase 6, Oak's Lab's post-battle content (parcel delivery, Pokédex gift, Route 22 rival rematch setup) — see [[Roadmap & Ideas]].

## The Pokédex reference

Every species, everything it uses, and where each piece lives:

- **[[Pokemon Data Map]]** — the map: ~14 files, two index systems, the sprite pipeline, who generates what
- **[[Master Index]]** — all 240 species, one row each
- **[[Dex 001-060]]** · **[[Dex 061-120]]** · **[[Dex 121-180]]** · **[[Dex 181-240]]** — full detail per species: stats, types, moves, TMs, evolution, sprite files, palette, icon, cry, internal index, encounter locations with rates, and dex prose

All auto-generated from the real data files by `tools/pokedex_report.py` — regenerate rather than hand-edit.

## Start here if you are picking this back up

- [[Known Gaps & Open Risks]] — what is verified, what is not, and what needs a human on a real screen
- [[Test Suite]] — eight regression suites; run them after any species-table change

## Cross-cutting reference

These aren't features — they're how the project actually gets built and debugged, and are worth knowing before touching anything:

- **[[Kanto Walkthrough - Base Game Route]]** — the vanilla game's full area-by-area route, transcribed from the Prima strategy guide, with Purple's own deviations called out up front; the master reference for planning any remaining content work
- [[Encounter Map - Locations & Rates]] — every area's wild species, real percentages and levels
- [[Where to Find Each Species]] — reverse lookup: pick a Pokémon, see everywhere it appears
- [[Architecture Map]] — what lives in `constants/`, `home/`, `engine/`, `data/`, `scripts/`, `text/`, `ram/`, `gfx/`, `audio/`
- [[PyBoy Testing Techniques]] — how this project actually verifies Z80 behavior with no interactive emulator available
- [[Table Alignment - The Two Index Systems]] — the most dangerous bug class here: misaligned species tables are never build errors
- [[Test Suite]] — the eight regression suites and what each one guards
- [[Lessons Learned - Bug Patterns]] — recurring bug classes hit more than once (register-clobbering `farcall`s, over-generalized "fix the shared function" mistakes, hex-vs-decimal constant comments)
- [[Build & Versioning]] — build commands, the `Roms/vX.Y` snapshot convention, why `make compare` doesn't apply here anymore

## What's next

See [[Roadmap & Ideas]] for open threads — right now that's mainly the rest of the soundtrack conversion, the remaining `ld a, ' '` blank-tile bug sites, and a discussed-but-not-started **memorial/graveyard system** for permadeath'd Pokémon.

## How to use this vault

- Every feature note follows the same shape: **Status**, **Summary**, **Key files**, **How it works**, **Bugs hit & fixes**, **Related**.
- Update the relevant note (and this table's status column) whenever a system changes — this vault is meant to track progress incrementally, not be a one-time snapshot.
- The repo's own root `CLAUDE.md` is the single source of truth for exact code-level detail; this vault restates it in a navigable, cross-linked form and is where day-to-day progress notes and the roadmap live instead.
