#!/usr/bin/env python3
"""Validates every exported map's connections against every other, so the
seamless-world stitching (Godot port, overworld_map.gd) is known to be sound
across all 221 maps instead of only the 2 borders manually walked in-engine.

Checks, per connection edge:
  - the target map file actually exists (map_index.json may point at a slug
    that was never exported, e.g. the 4 unused/duplicate maps skipped by
    godot_export.py)
  - the reverse connection exists on the target map, pointing back
  - the reverse offset is the exact negation (this is what a north/south or
    east/west pair must satisfy for _stitch()'s origin math to place both
    maps at mutually consistent world coordinates -- see the connection
    offset semantics documented in CLAUDE.md)
  - the two edges actually overlap in walkable cells once placed at their
    computed origins (a correct offset with zero real overlap would still
    "connect" numerically but be unwalkable in practice)

Run from the Godot project directory: py tools/verify_map_graph.py
(also copied to the pokered repo's tools/ since that's where the exporters
and their conventions live, even though it reads the Godot project's output)
"""
import json
import sys
from pathlib import Path

GODOT_ROOT = Path(r"C:\Users\jdsur\Documents\pokemonpurple")
MAPS_DIR = GODOT_ROOT / "data" / "maps"
BLOCK_CELLS = 2

OPPOSITE = {"north": "south", "south": "north", "west": "east", "east": "west"}


def load_all_maps():
    maps = {}
    for p in MAPS_DIR.glob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        maps[p.stem] = d
    return maps


def slug_for_map_const(map_index, map_const):
    return map_index.get(map_const)


def main():
    map_index = json.loads((GODOT_ROOT / "data" / "map_index.json").read_text(encoding="utf-8"))
    maps = load_all_maps()
    print(f"Loaded {len(maps)} maps, {len(map_index)} map_index entries")

    errors = []
    warnings = []

    for slug, d in maps.items():
        cw, ch = d["cells_w"], d["cells_h"]
        for conn in d.get("connections", []):
            direction = conn["dir"]
            target_const = conn["map"]
            offset = conn["offset_blocks"]
            target_slug = slug_for_map_const(map_index, target_const)

            if target_slug is None:
                warnings.append(f"{slug}: {direction}->{target_const} has no map_index entry (likely an unused/skipped map)")
                continue
            if target_slug not in maps:
                warnings.append(f"{slug}: {direction}->{target_const} (slug '{target_slug}') was never exported")
                continue

            target = maps[target_slug]
            tw, th = target["cells_w"], target["cells_h"]

            # Reverse-connection check.
            reverse = [c for c in target.get("connections", []) if c["map"] == d["map_const"]]
            if not reverse:
                errors.append(f"{slug} -> {target_slug} ({direction}): no reverse connection back from {target_slug}")
                continue
            rev = reverse[0]
            if rev["dir"] != OPPOSITE[direction]:
                errors.append(f"{slug} -> {target_slug}: reverse connection has dir '{rev['dir']}', expected '{OPPOSITE[direction]}'")
            if rev["offset_blocks"] != -offset:
                errors.append(f"{slug} -> {target_slug}: offset {offset} vs reverse {rev['offset_blocks']} (expected exact negation)")

            # Compute both maps' origins the same way overworld_map.gd's
            # _extend_neighbours() does, with `d` pinned at world (0,0), and
            # check the shared border actually has overlapping walkable cells.
            offset_cells = offset * BLOCK_CELLS
            origin = (0, 0)
            if direction == "north":
                t_origin = (origin[0] + offset_cells, origin[1] - th)
            elif direction == "south":
                t_origin = (origin[0] + offset_cells, origin[1] + ch)
            elif direction == "west":
                t_origin = (origin[0] - tw, origin[1] + offset_cells)
            else:  # east
                t_origin = (origin[0] + cw, origin[1] + offset_cells)

            # Border cells on each side, in world space.
            d_walk = d["walkable"]
            t_walk = target["walkable"]

            def d_cell(x, y):
                if x < 0 or y < 0 or x >= cw or y >= ch:
                    return False
                return bool(d_walk[y * cw + x])

            def t_cell(wx, wy):
                lx, ly = wx - t_origin[0], wy - t_origin[1]
                if lx < 0 or ly < 0 or lx >= tw or ly >= th:
                    return False
                return bool(t_walk[ly * tw + lx])

            overlap = 0
            if direction in ("north", "south"):
                y_d = 0 if direction == "north" else ch - 1
                for x in range(cw):
                    if not d_cell(x, y_d):
                        continue
                    wx, wy = x, (y_d - 1 if direction == "north" else y_d + 1)
                    if t_cell(wx, wy):
                        overlap += 1
            else:
                x_d = 0 if direction == "west" else cw - 1
                for y in range(ch):
                    if not d_cell(x_d, y):
                        continue
                    wx, wy = (x_d - 1 if direction == "west" else x_d + 1), y
                    if t_cell(wx, wy):
                        overlap += 1

            if overlap == 0:
                errors.append(f"{slug} -> {target_slug} ({direction}, offset {offset}): zero walkable overlap at the border")

    print(f"\n{len(errors)} errors, {len(warnings)} warnings\n")
    for w in warnings:
        print("WARN:", w)
    for e in errors:
        print("ERROR:", e)

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
