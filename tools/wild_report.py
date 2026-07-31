#!/usr/bin/env python3
"""
Generate the WordVault encounter-map note from the REAL wild tables.

Reads data/wild/maps/*.asm (the built source of truth, not the designer's
input data) so the note can never drift from what is actually in the ROM.
Slot chances come from data/wild/probabilities.asm.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS = os.path.join(ROOT, "data/wild/maps")
OUT = os.path.join(ROOT, "Pokemon Vault/07 Kanto Reborn/Encounter Map - Locations & Rates.md")

# Progression order, with display names. Anything not listed is appended after.
ORDER = [
    ("Route1", "Route 1"), ("Route2", "Route 2"), ("ViridianForest", "Viridian Forest"),
    ("Route22", "Route 22"), ("Route3", "Route 3"),
    ("MtMoon1F", "Mt. Moon 1F"), ("MtMoonB1F", "Mt. Moon B1F"), ("MtMoonB2F", "Mt. Moon B2F"),
    ("Route4", "Route 4"), ("Route24", "Route 24"), ("Route25", "Route 25"),
    ("Route5", "Route 5"), ("Route6", "Route 6"),
    ("Route11", "Route 11"), ("DiglettsCave", "Diglett's Cave"),
    ("Route9", "Route 9"), ("Route10", "Route 10"),
    ("RockTunnel1F", "Rock Tunnel 1F"), ("RockTunnelB1F", "Rock Tunnel B1F"),
    ("Route7", "Route 7"), ("Route8", "Route 8"),
    ("PokemonTower3F", "Pokémon Tower 3F"), ("PokemonTower4F", "Pokémon Tower 4F"),
    ("PokemonTower5F", "Pokémon Tower 5F"), ("PokemonTower6F", "Pokémon Tower 6F"),
    ("PokemonTower7F", "Pokémon Tower 7F"),
    ("Route12", "Route 12"), ("Route13", "Route 13"), ("Route14", "Route 14"),
    ("Route15", "Route 15"), ("Route16", "Route 16"), ("Route17", "Route 17"),
    ("Route18", "Route 18"),
    ("SafariZoneCenter", "Safari Zone — Center"), ("SafariZoneEast", "Safari Zone — East"),
    ("SafariZoneNorth", "Safari Zone — North"), ("SafariZoneWest", "Safari Zone — West"),
    ("Route21", "Route 21"),
    ("SeafoamIslands1F", "Seafoam Islands 1F"), ("SeafoamIslandsB1F", "Seafoam Islands B1F"),
    ("SeafoamIslandsB2F", "Seafoam Islands B2F"), ("SeafoamIslandsB3F", "Seafoam Islands B3F"),
    ("SeafoamIslandsB4F", "Seafoam Islands B4F"),
    ("PowerPlant", "Power Plant"),
    ("PokemonMansion1F", "Pokémon Mansion 1F"), ("PokemonMansion2F", "Pokémon Mansion 2F"),
    ("PokemonMansion3F", "Pokémon Mansion 3F"), ("PokemonMansionB1F", "Pokémon Mansion B1F"),
    ("Route23", "Route 23"),
    ("VictoryRoad1F", "Victory Road 1F"), ("VictoryRoad2F", "Victory Road 2F"),
    ("VictoryRoad3F", "Victory Road 3F"),
    ("CeruleanCave1F", "Cerulean Cave 1F"), ("CeruleanCave2F", "Cerulean Cave 2F"),
    ("CeruleanCaveB1F", "Cerulean Cave B1F"),
]


def slot_chances():
    txt = open(os.path.join(ROOT, "data/wild/probabilities.asm"), encoding="utf-8").read()
    raw = [int(m.group(1)) for m in re.finditer(r"wild_chance\s+(\d+)", txt)]
    # Table lists cumulative-style per-slot weights; last slot is the remainder.
    if sum(raw) < 256:
        raw = raw + [256 - sum(raw)]
    return [r / 256 * 100 for r in raw]


def pretty(species):
    s = species.replace("_", " ").title()
    return {"Nidoran M": "Nidoran♂", "Nidoran F": "Nidoran♀",
            "Ho Oh": "Ho-Oh", "Mr Mime": "Mr. Mime",
            "Farfetchd": "Farfetch'd"}.get(s, s)


def parse(name):
    p = os.path.join(MAPS, name + ".asm")
    txt = open(p, encoding="utf-8").read()
    m = re.search(r"def_grass_wildmons\s+(\d+)[^\n]*\n(.*?)\tend_grass_wildmons", txt, re.S)
    if not m:
        return None, []
    rate = int(m.group(1))
    entries = [(int(a), b) for a, b in
               re.findall(r"db\s+(\d+),\s*([A-Z_0-9]+)", m.group(2))]
    return rate, entries


def main():
    ch = slot_chances()
    seen = set()
    ordered = list(ORDER)
    for f in sorted(os.listdir(MAPS)):
        n = f[:-4]
        if n not in dict(ORDER) and n != "nothing":
            ordered.append((n, n))

    lines = [
        "# Encounter Map — Locations & Rates",
        "",
        "*Auto-generated from `data/wild/maps/*.asm` by `tools/wild_report.py`.*",
        "*Regenerate after any encounter change rather than editing by hand.*",
        "",
        "## How the percentages work",
        "",
        "Each map has exactly **10 slots**, and `data/wild/probabilities.asm` gives every",
        "*slot* a fixed chance — rarity is expressed purely by **position in the list**:",
        "",
        "| Slot | Chance |", "|---|---|",
    ]
    for i, c in enumerate(ch):
        lines.append(f"| {i} | {c:.1f}% |")
    lines += [
        "",
        "So tables are written commonest-first, and the marquee species always sits in",
        "slot 9 (~1.2%) — the \"holy shit\" slot.",
        "",
        "**Encounter rate** (shown per area) is a separate number: how often walking in",
        "grass triggers *any* battle. Higher = more frequent encounters.",
        "",
        "Species new to this ROM (Gen 2 import) are shown in **bold**.",
        "",
        "---",
        "",
    ]

    import sys
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    try:
        from gen2_import import build_roster
        new = {s["const"] for s in build_roster()[0]}
    except Exception:
        new = set()

    for key, label in ordered:
        if key in seen or not os.path.exists(os.path.join(MAPS, key + ".asm")):
            continue
        seen.add(key)
        rate, entries = parse(key)
        if not entries:
            continue
        agg = {}
        for i, (lvl, sp) in enumerate(entries):
            pct = ch[i] if i < len(ch) else 0
            if sp in agg:
                agg[sp][0] += pct
                agg[sp][1] = min(agg[sp][1], lvl)
                agg[sp][2] = max(agg[sp][2], lvl)
            else:
                agg[sp] = [pct, lvl, lvl]
        lines.append(f"## {label}")
        lines.append("")
        lines.append(f"*Encounter rate: {rate}*")
        lines.append("")
        lines.append("| Pokémon | Chance | Level |")
        lines.append("|---|---|---|")
        for sp, (pct, lo, hi) in sorted(agg.items(), key=lambda kv: -kv[1][0]):
            nm = pretty(sp)
            if sp in new:
                nm = f"**{nm}**"
            lvl = f"{lo}" if lo == hi else f"{lo}–{hi}"
            lines.append(f"| {nm} | {pct:.1f}% | {lvl} |")
        lines.append("")

    lines += [
        "---",
        "",
        "## Related",
        "- [[Kanto Reborn - Overview]] — the design decisions behind these tables",
        "- [[Single Merged ROM]] — the 10-slot `NUM_WILDMONS` constraint",
        "",
    ]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(f"wrote {OUT} ({len(seen)} areas)")
    write_species_index(ch, new)


def write_species_index(ch, new):
    """Reverse lookup: species -> every place it can be found, best odds first."""
    out = os.path.join(ROOT, "Pokemon Vault/07 Kanto Reborn/Where to Find Each Species.md")
    label_of = dict(ORDER)
    where = {}
    for f in sorted(os.listdir(MAPS)):
        if not f.endswith(".asm") or f == "nothing.asm":
            continue
        key = f[:-4]
        _, entries = parse(key)
        agg = {}
        for i, (lvl, sp) in enumerate(entries):
            pct = ch[i] if i < len(ch) else 0
            if sp in agg:
                agg[sp][0] += pct
                agg[sp][1] = min(agg[sp][1], lvl)
                agg[sp][2] = max(agg[sp][2], lvl)
            else:
                agg[sp] = [pct, lvl, lvl]
        for sp, (pct, lo, hi) in agg.items():
            where.setdefault(sp, []).append((pct, label_of.get(key, key), lo, hi))

    # Evolution-only species: reachable but never found in grass.
    evo_parent = {}
    txt = open(os.path.join(ROOT, "data/pokemon/evos_moves.asm"), encoding="utf-8").read()
    for blk in re.finditer(r"^(\w+)EvosMoves:\n(.*?)(?=^\w+EvosMoves:|\Z)", txt, re.S | re.M):
        for e in re.finditer(r"db\s+EVOLVE_(\w+),(?:[^,\n]+,)*\s*([A-Z_0-9]+)", blk.group(2)):
            evo_parent.setdefault(e.group(2), []).append(blk.group(1))

    lines = [
        "# Where to Find Each Species",
        "",
        "*Auto-generated from `data/wild/maps/*.asm` by `tools/wild_report.py`.*",
        "*The reverse of [[Encounter Map - Locations & Rates]] — look up a Pokémon,*",
        "*get every place it appears, best odds first.*",
        "",
        "Species new to this ROM (Gen 2 import) are in **bold**. Anything marked",
        "*evolve only* never appears in grass and must be evolved into.",
        "",
        "| Pokémon | Where | Chance | Level |",
        "|---|---|---|---|",
    ]
    for sp in sorted(where, key=pretty):
        nm = pretty(sp)
        if sp in new:
            nm = f"**{nm}**"
        for j, (pct, loc, lo, hi) in enumerate(sorted(where[sp], key=lambda t: -t[0])):
            lvl = f"{lo}" if lo == hi else f"{lo}–{hi}"
            lines.append(f"| {nm if j == 0 else ''} | {loc} | {pct:.1f}% | {lvl} |")

    evo_only = sorted(set(evo_parent) - set(where), key=pretty)
    if evo_only:
        lines += ["", "## Evolve-only (never in grass)", "",
                  "| Pokémon | Evolve from |", "|---|---|"]
        for sp in evo_only:
            nm = pretty(sp)
            if sp in new:
                nm = f"**{nm}**"
            parents = ", ".join(pretty(p) for p in sorted(set(evo_parent[sp])))
            lines.append(f"| {nm} | {parents} |")

    lines += ["", "## Related", "- [[Encounter Map - Locations & Rates]]",
              "- [[Kanto Reborn - Overview]]", ""]
    open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(f"wrote {out} ({len(where)} species in grass, {len(evo_only)} evolve-only)")


if __name__ == "__main__":
    main()
