#!/usr/bin/env python3
"""
Gen 2 species importer for Pokemon Purple.

Reads pokegold-reference/ and emits/patches everything Gen 1 needs for a new
species. Run with --manifest first to sanity-check the roster and index
assignment before any file is touched.

Two numbering systems matter here and must not be confused:
  * INTERNAL INDEX (1..255)  -> names, dex_order, cries, dex_entries,
                                evos_moves.  Asserts NUM_POKEMON_INDEXES.
  * DEX NUMBER    (1..N)     -> base_stats, palettes, menu_icons.
                                Asserts NUM_POKEMON (and NUM_POKEMON +/- 1).
"""
import os
import re
import sys
import glob
import argparse

# Derived from this file's location so the tools work from any checkout.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "pokegold-reference")

# Types Gen 1's engine simply does not have. Any species needing one is out of
# scope by explicit design decision (no new types this pass).
FORBIDDEN_TYPES = {"DARK", "STEEL"}

# Gen 1 dex is 1..151; new species are renumbered contiguously from here rather
# than keeping canonical Johto numbers, so the dex has no holes to render.
GEN1_LAST_DEX = 151

# Species excluded for reasons other than typing.
# UNOWN: 28 alphabet forms driven by a dedicated Gen 2 subsystem
# (unown_pic_pointers.asm) that Gen 1 has no equivalent for; it ships no
# front/back sprite in the normal per-species layout at all. Importing it as a
# single arbitrary form would be a poor fit, so it is out of scope.
EXCLUDED_SPECIES = {"UNOWN"}


def front_sprite_path(slug):
    """Gold/Silver-identical species ship one front.png instead of front_gold.png."""
    for name in ("front_gold.png", "front.png", "front_silver.png"):
        p = os.path.join(REF, f"gfx/pokemon/{slug}/{name}")
        if os.path.exists(p):
            return p
    return None


def back_sprite_path(slug):
    p = os.path.join(REF, f"gfx/pokemon/{slug}/back.png")
    return p if os.path.exists(p) else None


def parse_gen2_base_stats():
    """-> list of dicts, one per Gen 2 species, in canonical dex order."""
    out = []
    for path in sorted(glob.glob(os.path.join(REF, "data/pokemon/base_stats/*.asm"))):
        txt = open(path, encoding="utf-8").read()
        lines = txt.splitlines()

        m = re.search(r"db\s+([A-Z0-9_]+)\s*;\s*(\d+)", lines[0])
        if not m:
            continue
        const, dexnum = m.group(1), int(m.group(2))
        if dexnum <= GEN1_LAST_DEX:
            continue  # Gen 1 species already exist here

        stats = re.search(
            r"db\s+(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)", txt)
        hp, atk, dfn, spd, sat, sdf = (int(g) for g in stats.groups())

        types = re.search(r"db\s+([A-Z_]+),\s*([A-Z_]+)\s*;\s*type", txt)
        t1, t2 = types.group(1), types.group(2)

        catch = int(re.search(r"db\s+(\d+)\s*;\s*catch rate", txt).group(1))
        bexp = int(re.search(r"db\s+(\d+)\s*;\s*base exp", txt).group(1))
        growth = re.search(r"db\s+(GROWTH_[A-Z_]+)\s*;\s*growth rate", txt).group(1)

        out.append(dict(
            const=const, gen2_dex=dexnum, slug=os.path.basename(path)[:-4],
            hp=hp, atk=atk, dfn=dfn, spd=spd, sat=sat, sdf=sdf,
            type1=t1, type2=t2, catch=catch, base_exp=bexp, growth=growth,
        ))
    out.sort(key=lambda d: d["gen2_dex"])
    return out


def parse_gen2_dex_entry(slug):
    """-> (category, height_ft, height_in, weight_tenths_lb) or None."""
    path = os.path.join(REF, f"data/pokemon/dex_entries/gold/{slug}.asm")
    if not os.path.exists(path):
        return None
    txt = open(path, encoding="utf-8").read()
    cat = re.search(r'db\s+"([^"]*)@"', txt)
    hw = re.search(r"dw\s+(\d+),\s*(\d+)", txt)
    if not cat or not hw:
        return None
    # Gen 2 encodes height as feet*100 + inches, weight in tenths of a pound --
    # the same units Gen 1 wants, just packed differently.
    h = int(hw.group(1))
    return cat.group(1), h // 100, h % 100, int(hw.group(2))


# Map a species' primary type to the closest existing Gen 1 mon palette.
# Gen 1 has a fixed 10-palette vocabulary; there is no per-mon RGB here.
TYPE_TO_PAL = {
    "NORMAL": "PAL_BROWNMON", "FIGHTING": "PAL_BROWNMON", "FLYING": "PAL_CYANMON",
    "POISON": "PAL_PURPLEMON", "GROUND": "PAL_BROWNMON", "ROCK": "PAL_GRAYMON",
    "BUG": "PAL_GREENMON", "GHOST": "PAL_PURPLEMON", "FIRE": "PAL_REDMON",
    "WATER": "PAL_BLUEMON", "GRASS": "PAL_GREENMON", "ELECTRIC": "PAL_YELLOWMON",
    "PSYCHIC_TYPE": "PAL_PINKMON", "ICE": "PAL_CYANMON", "DRAGON": "PAL_BLUEMON",
}

TYPE_TO_ICON = {
    "NORMAL": "ICON_QUADRUPED", "FIGHTING": "ICON_MON", "FLYING": "ICON_BIRD",
    "POISON": "ICON_MON", "GROUND": "ICON_QUADRUPED", "ROCK": "ICON_MON",
    "BUG": "ICON_BUG", "GHOST": "ICON_MON", "FIRE": "ICON_QUADRUPED",
    "WATER": "ICON_WATER", "GRASS": "ICON_GRASS", "ELECTRIC": "ICON_QUADRUPED",
    "PSYCHIC_TYPE": "ICON_MON", "ICE": "ICON_MON", "DRAGON": "ICON_SNAKE",
}


def camel(slug):
    """porygon2 -> Porygon2 ; mr__mime -> MrMime (label-safe)."""
    parts = [p for p in re.split(r"[^a-z0-9]+", slug) if p]
    return "".join(p.capitalize() for p in parts)


def fold_special(sat, sdf):
    """Gen 1 has ONE Special stat. Average the Gen 2 split, per design decision."""
    return (sat + sdf) // 2


def find_gap_indices(constants_path):
    """Reclaimable internal-index slots (vanilla MissingNo. holes)."""
    gaps = []
    val = -1
    for line in open(constants_path, encoding="utf-8"):
        s = line.strip()
        if s.startswith("const_def"):
            val = 0
            continue
        if s.startswith("const_next"):
            m = re.search(r"const_next\s+\$([0-9A-Fa-f]+)", s)
            val = int(m.group(1), 16) - 1
            continue
        if s.startswith("const_skip"):
            val += 1
            gaps.append(val)
        elif s.startswith("const ") or s.startswith("const\t"):
            val += 1
    return gaps


def build_roster():
    species = parse_gen2_base_stats()
    eligible, excluded = [], []
    for s in species:
        if (s["type1"] in FORBIDDEN_TYPES or s["type2"] in FORBIDDEN_TYPES
                or s["const"] in EXCLUDED_SPECIES):
            excluded.append(s)
        else:
            eligible.append(s)

    # Read gaps from the PRISTINE copy, never the live tree. Once gen2_emit.py
    # has run, the live file has every `const_skip` replaced by a real species,
    # so scanning it finds zero gaps, pushes everything into the appended range
    # and silently reports a wrong (inflated) NUM_POKEMON_INDEXES.
    pristine = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "gen2_pristine/constants/pokemon_constants.asm")
    src = pristine if os.path.exists(pristine) else os.path.join(
        ROOT, "constants/pokemon_constants.asm")
    gaps = find_gap_indices(src)
    next_free = 191  # first index past vanilla's NUM_POKEMON_INDEXES (190)

    for i, s in enumerate(eligible):
        s["dex"] = GEN1_LAST_DEX + 1 + i
        if i < len(gaps):
            s["index"] = gaps[i]
            s["slot"] = "gap"
        else:
            s["index"] = next_free + (i - len(gaps))
            s["slot"] = "appended"
        s["special"] = fold_special(s["sat"], s["sdf"])
        s["label"] = camel(s["slug"])
        s["pal"] = TYPE_TO_PAL.get(s["type1"], "PAL_MEWMON")
        s["icon"] = TYPE_TO_ICON.get(s["type1"], "ICON_MON")
        s["dexinfo"] = parse_gen2_dex_entry(s["slug"])
    return eligible, excluded, gaps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    eligible, excluded, gaps = build_roster()
    if args.limit:
        eligible = eligible[:args.limit]

    if args.manifest:
        print(f"Gen 2 species found       : {len(eligible) + len(excluded)}")
        print(f"Excluded (Dark/Steel)     : {len(excluded)}")
        print("  " + ", ".join(s["const"] for s in excluded))
        print(f"Eligible for import       : {len(eligible)}")
        print(f"Reclaimable index gaps    : {len(gaps)}")
        maxidx = max(s["index"] for s in eligible)
        print(f"Max internal index        : {maxidx} (ceiling 255)")
        print(f"New NUM_POKEMON_INDEXES   : {maxidx}")
        print(f"New NUM_POKEMON           : {eligible[-1]['dex']}")
        missing = [s["slug"] for s in eligible if not s["dexinfo"]]
        print(f"Missing dex entry data    : {len(missing)} {missing[:5]}")
        nofront = [s["slug"] for s in eligible if not front_sprite_path(s["slug"])]
        noback = [s["slug"] for s in eligible if not back_sprite_path(s["slug"])]
        print(f"Missing front sprite      : {len(nofront)} {nofront[:5]}")
        print(f"Missing back sprite       : {len(noback)} {noback[:5]}")
        print()
        print(f"{'idx':>4} {'dex':>4} {'slot':<9} {'name':<12} "
              f"{'types':<22} {'HP/At/Df/Sp/Spc':<18} {'pal':<13} icon")
        for s in eligible:
            t = s["type1"] if s["type1"] == s["type2"] else f"{s['type1']}/{s['type2']}"
            statline = f"{s['hp']}/{s['atk']}/{s['dfn']}/{s['spd']}/{s['special']}"
            print(f"{s['index']:>4} {s['dex']:>4} {s['slot']:<9} {s['const']:<12} "
                  f"{t:<22} {statline:<18} {s['pal']:<13} {s['icon']}")
        return

    print("no action selected; use --manifest", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
