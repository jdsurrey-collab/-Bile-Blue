# Build & Versioning

## Requirements
**rgbds 1.0.2** (`brew install rgbds` on macOS; see repo `INSTALL.md` for other platforms). This project builds under WSL2 Ubuntu in practice.

## Commands
```sh
make              # builds pokered.gbc — the only ROM this fork produces
make red          # same, explicit target name
make clean        # remove build artifacts (objects, compiled gfx, roms)
make RGBDS=path/to/rgbds/   # use a local rgbds install instead of the global one
```

There used to be a `pokeblue.gbc`/`pokeblue_debug.gbc` build path — removed from the Makefile entirely (see [[Single Merged ROM]]). `make blue`/`make blue_debug` no longer exist.

## What counts as "passing"
- `rgbasm`/`rgblink` run with `-Weverything -Wtruncation=1` — **build warnings are the lint step**, there's no separate linter.
- `make compare` (`sha1sum -c roms.sha1`) is the upstream project's only automated test, but it checks byte-perfect rebuilds against **upstream pokered/pokeblue checksums that no longer apply to this fork at all**. Don't rely on it here.
- The real correctness bar on this fork: a clean `make` under `-Weverything`, **plus** actually exercising new behavior via the [[PyBoy Testing Techniques]] harness. A clean build has already been proven insufficient multiple times this project (see [[Lessons Learned - Bug Patterns]]) — it catches zero behavioral bugs, only assembly errors.

## Versioned ROM snapshots
Recompiled ROMs worth keeping go in `Roms/vX.Y/` (e.g. `Roms/v0.1/pokered.gbc`). This folder is gitignored (`/Roms/` in `.gitignore`) — bump the version folder each time a build is worth snapshotting; don't commit the `.gbc` files themselves to git.

Current snapshots on disk: `v0.1` through `v0.22` (sequential, one per completed fix/feature round). See [[Version History]] for what each round actually shipped.

Older checkpoints (pre-Red/Blue-merge) may still contain a `pokeblue.gbc` alongside `pokered.gbc` — that's historical only; going forward there's ever only one ROM per checkpoint.

## Git remotes
- `origin` → the personal fork this project pushes to (GitHub: `jdsurrey-collab/-Bile-Blue`)
- `upstream` → the original `pret/pokered` repo, kept for pulling in upstream fixes

## Related
- [[Version History]]
- [[PyBoy Testing Techniques]]
- [[Architecture Map]]
