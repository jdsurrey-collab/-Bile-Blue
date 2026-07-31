#!/usr/bin/env python3
"""
Export the non-map game data (species, moves, types, trainers) for the Godot port.

Companion to godot_export.py, which handles maps/tilesets/text. Split because
this half is map-independent and only needs re-running when game data changes.

    python tools/godot_export_data.py

Everything is parsed from the .asm source rather than the built ROM, so the
export stays readable and diffable. The one thing it must respect is the two
index systems (see Pokemon Vault/05 Reference/Table Alignment): species are
emitted keyed by CONSTANT NAME, which is unambiguous, with both the internal
index and the dex number carried as fields.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GODOT = "/mnt/c/Users/jdsur/Documents/pokemonpurple" if os.name != "nt" \
    else r"C:\Users\jdsur\Documents\pokemonpurple"

sys.path.insert(0, os.path.join(ROOT, "tools"))
from pokedex_report import (species_index, dex_order_slugs, parse_base_stats,
                            parse_evos_moves, parse_dex_entries, parse_dex_text,
                            camel, read)


# --------------------------------------------------------------- constants --
def enum(path, pattern=r"const\s+([A-Z_0-9]+)", start=0):
    """Ordered constants -> {NAME: value}."""
    out, val = {}, start - 1
    for line in read(path).splitlines():
        s = line.strip()
        m = re.match(r"const_def\s+(\d+)", s)
        if m:
            val = int(m.group(1)) - 1
            continue
        if s.startswith("const_def"):
            val = start - 1
            continue
        m = re.match(r"const_next\s+\$([0-9A-Fa-f]+)", s)
        if m:
            val = int(m.group(1), 16) - 1
            continue
        m = re.match(pattern, s)
        if m:
            val += 1
            out[m.group(1)] = val
    return out


def export_types():
    """Type ids + the full effectiveness chart."""
    types = {}
    val = -1
    for line in read("constants/type_constants.asm").splitlines():
        s = line.strip()
        if s.startswith("const_def"):
            val = -1
            continue
        m = re.match(r"const_next\s+\$([0-9A-Fa-f]+)", s)
        if m:
            val = int(m.group(1), 16) - 1
            continue
        m = re.match(r"const\s+([A-Z_0-9]+)", s)
        if m:
            val += 1
            types[m.group(1)] = val

    # SUPER_EFFECTIVE=20, NOT_VERY_EFFECTIVE=05, NO_EFFECT=00 -> x2, x0.5, x0
    named = {"SUPER_EFFECTIVE": 20, "NOT_VERY_EFFECTIVE": 5, "NO_EFFECT": 0}
    chart = []
    for m in re.finditer(r"db\s+([A-Z_]+),\s*([A-Z_]+),\s*([A-Z_]+)",
                         read("data/types/type_matchups.asm")):
        atk, dfn, eff = m.groups()
        if atk not in types or dfn not in types or eff not in named:
            continue
        chart.append({"attacker": atk, "defender": dfn,
                      "multiplier": named[eff] / 10.0})
    return {"types": types, "chart": chart}


def export_moves():
    """Move table. Note effect/power/type/accuracy/pp order from the macro."""
    moves = {}
    order = []
    txt = read("data/moves/moves.asm")
    names = re.findall(r'li\s+"([^"]*)"', read("data/moves/names.asm"))
    idx = 0
    for m in re.finditer(
            r"move\s+([A-Z_0-9]+),\s*([A-Z_0-9]+),\s*(\d+),\s*([A-Z_0-9]+),"
            r"\s*(\d+),\s*(\d+)", txt):
        anim, effect, power, mtype, acc, pp = m.groups()
        name = names[idx] if idx < len(names) else anim
        idx += 1
        key = anim  # the animation field doubles as the move's own id
        moves[key] = dict(id=idx, name=name, effect=effect, power=int(power),
                          type=mtype, accuracy=int(acc), pp=int(pp))
        order.append(key)
    return {"moves": moves, "order": order}


def export_species():
    idx = species_index()
    slugs = dex_order_slugs()
    evos = parse_evos_moves()
    entries = parse_dex_entries()
    dtext = parse_dex_text()

    pals = re.findall(r"db\s+(PAL_\w+)", read("data/pokemon/palettes.asm"))
    icons = re.findall(r"nybble\s+(ICON_\w+)", read("data/pokemon/menu_icons.asm"))

    out = {}
    for dex in sorted(slugs):
        slug = slugs[dex]
        bs = parse_base_stats(slug)
        const = bs["dexconst"].replace("DEX_", "")
        label = camel(slug)
        ev, learn = evos.get(label, ([], []))
        cat, ft, inch, wt = entries.get(label, ("", 0, 0, 0))
        hp, atk, dfn, spd, spc = bs["stats"]

        evolutions = []
        for meth, args in ev:
            e = {"method": meth, "target": args[-1]}
            if meth == "LEVEL":
                e["level"] = int(args[0])
            elif meth == "ITEM":
                e["item"] = args[0]
            evolutions.append(e)

        out[const] = dict(
            dex=dex, index=idx.get(const, 0), slug=slug, label=label,
            name=const, category=cat,
            height_ft=ft, height_in=inch, weight_tenths_lb=wt,
            hp=hp, attack=atk, defense=dfn, speed=spd, special=spc,
            type1=bs["types"][0], type2=bs["types"][1],
            catch_rate=bs["catch"], base_exp=bs["exp"],
            growth_rate=bs["growth"],
            level1_moves=[m for m in bs["lv1"] if m != "NO_MOVE"],
            learnset=[{"level": lv, "move": mv} for lv, mv in learn],
            tmhm=bs["tmhm"],
            evolutions=evolutions,
            palette=pals[dex] if dex < len(pals) else "",
            menu_icon=icons[dex - 1] if dex - 1 < len(icons) else "",
            dex_text=dtext.get(label, []),
            front_sprite="res://assets/sprites/pokemon/front/%s.png" % slug,
            back_sprite="res://assets/sprites/pokemon/back/%s.png" % slug,
        )
    return out


def export_trainers():
    """Trainer classes and their parties.

    Party format is a run of `db level, SPECIES..., 0` groups, or a
    `db $FF, lvl, SPECIES, lvl, SPECIES, ..., 0` group when levels differ
    per mon. Each group is one numbered trainer of that class.
    """
    names = re.findall(r'li\s+"([^"]*)"', read("data/trainers/names.asm"))
    txt = read("data/trainers/parties.asm")
    out = {}
    for m in re.finditer(r"^(\w+)Data:\n(.*?)(?=^\w+Data:|\Z)", txt, re.S | re.M):
        cls, body = m.group(1), m.group(2)
        parties = []
        for line in body.splitlines():
            s = line.strip()
            if not s.startswith("db "):
                continue
            toks = [t.strip() for t in s[3:].split(",")]
            toks = [t for t in toks if t and not t.startswith(";")]
            if not toks:
                continue
            if toks[0] == "$FF":
                mons = []
                rest = toks[1:]
                for i in range(0, len(rest) - 1, 2):
                    if rest[i] == "0":
                        break
                    mons.append({"level": int(rest[i]), "species": rest[i + 1]})
                parties.append({"mixed_levels": True, "mons": mons})
            else:
                lvl = int(toks[0])
                mons = [{"level": lvl, "species": t}
                        for t in toks[1:] if t != "0"]
                parties.append({"mixed_levels": False, "mons": mons})
        if parties:
            out[cls] = {"parties": parties}
    return {"classes": out, "names": names}


def script_inventory():
    """Which maps have a real script -- the explicit hand-port list."""
    have = []
    for f in sorted(os.listdir(os.path.join(ROOT, "scripts"))):
        if not f.endswith(".asm"):
            continue
        name = f[:-4]
        body = read(f"scripts/{name}.asm")
        # A map with no logic is just a Default script that returns.
        n_scripts = len(re.findall(r"dw_const \w+Script,", body))
        if n_scripts > 1 or "CheckEvent" in body or "SetEvent" in body:
            have.append({"map": name, "states": n_scripts})
    return have


def main():
    out_dir = os.path.join(GODOT, "data")
    os.makedirs(out_dir, exist_ok=True)

    def dump(name, obj):
        p = os.path.join(out_dir, name)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(obj, f, indent=1)
        return p

    t = export_types()
    dump("type_chart.json", t)
    print(f"types      : {len(t['types'])} types, {len(t['chart'])} matchups")

    mv = export_moves()
    dump("moves.json", mv)
    print(f"moves      : {len(mv['moves'])}")

    sp = export_species()
    dump("species.json", sp)
    print(f"species    : {len(sp)}")

    tr = export_trainers()
    dump("trainers.json", tr)
    print(f"trainers   : {len(tr['classes'])} classes, {len(tr['names'])} names")

    inv = script_inventory()
    dump("script_inventory.json", inv)
    print(f"map scripts: {len(inv)} maps need a hand-ported script")

    print("->", out_dir)


if __name__ == "__main__":
    main()
