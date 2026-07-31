#!/usr/bin/env python3
"""
Generate the WordVault Pokedex reference: every species, everything it uses.

Reads the REAL data files (not the generators' inputs), so the notes cannot
drift from what is actually in the ROM. Regenerate after any species change.

Emits into Pokemon Vault/08 Pokedex/:
  Pokemon Data Map.md     -- where every piece of a species' data lives
  Master Index.md         -- all 240, one row each
  Dex 001-060.md .. 181-240.md -- full per-species detail
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Pokemon Vault", "08 Pokedex")

SLOT_PCT = [19.9, 19.9, 15.2, 9.8, 9.8, 9.8, 5.1, 5.1, 4.3, 1.2]


def read(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()


# ---------------------------------------------------------------- constants --
def species_index():
    out, val = {}, -1
    for line in read("constants/pokemon_constants.asm").splitlines():
        s = line.strip()
        if s.startswith("const_def"):
            m = re.match(r"const_def\s+(\d+)", s)
            val = (int(m.group(1)) - 1) if m else -1
            continue
        if s.startswith("const_next"):
            val = int(re.search(r"\$([0-9A-Fa-f]+)", s).group(1)) - 1
            continue
        if s.startswith("const_skip"):
            val += 1
            continue
        m = re.match(r"const\s+([A-Z_0-9]+)", s)
        if m:
            val += 1
            out[m.group(1)] = val
    return out


def dex_order_slugs():
    """dex number -> slug, from the INCLUDE order in base_stats.asm."""
    out, n = {}, 0
    for line in read("data/pokemon/base_stats.asm").splitlines():
        m = re.search(r'INCLUDE "data/pokemon/base_stats/([a-z0-9_]+)\.asm"', line)
        if m:
            n += 1
            out[n] = m.group(1)
    return out


# -------------------------------------------------------------- base stats --
def parse_base_stats(slug):
    txt = read(f"data/pokemon/base_stats/{slug}.asm")
    txt = re.sub(r"\\\s*\n\s*", " ", txt)  # join tmhm continuations
    d = {}
    m = re.search(r"db\s+(DEX_[A-Z_0-9]+)", txt)
    d["dexconst"] = m.group(1) if m else "?"
    m = re.search(r"db\s+(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\s*\n", txt)
    if m:
        d["stats"] = [int(g) for g in m.groups()]
    else:
        d["stats"] = [0] * 5
    m = re.search(r"db\s+([A-Z_]+),\s*([A-Z_]+)\s*;\s*type", txt)
    d["types"] = (m.group(1), m.group(2)) if m else ("?", "?")
    m = re.search(r"db\s+(\d+)\s*;\s*catch rate", txt)
    d["catch"] = int(m.group(1)) if m else 0
    m = re.search(r"db\s+(\d+)\s*;\s*base exp", txt)
    d["exp"] = int(m.group(1)) if m else 0
    m = re.search(r'INCBIN\s+"([^"]+)"', txt)
    d["picfile"] = m.group(1) if m else "?"
    m = re.search(r"dw\s+(\w+),\s*(\w+)", txt)
    d["pics"] = (m.group(1), m.group(2)) if m else ("?", "?")
    m = re.search(r"db\s+([A-Z_0-9, ]+?)\s*;\s*level 1 learnset", txt)
    d["lv1"] = [x.strip() for x in m.group(1).split(",")] if m else []
    m = re.search(r"db\s+(GROWTH_[A-Z_]+)", txt)
    d["growth"] = m.group(1) if m else "?"
    m = re.search(r"tmhm\s+([^\n;]+)", txt)
    d["tmhm"] = [x.strip() for x in m.group(1).split(",") if x.strip()] if m else []
    return d


# ------------------------------------------------------------ evos / moves --
def parse_evos_moves():
    txt = read("data/pokemon/evos_moves.asm")
    out = {}
    for m in re.finditer(r"^(\w+)EvosMoves:\n(.*?)(?=^\w+EvosMoves:|\Z)",
                         txt, re.S | re.M):
        label, body = m.group(1), m.group(2)
        evos, learn = [], []
        for e in re.finditer(r"db\s+EVOLVE_(\w+),\s*([^\n;]+)", body):
            evos.append((e.group(1), [a.strip() for a in e.group(2).split(",")]))
        for l in re.finditer(r"db\s+(\d+),\s*([A-Z_0-9]+)\s*$", body, re.M):
            learn.append((int(l.group(1)), l.group(2)))
        out[label] = (evos, learn)
    return out


# ------------------------------------------------------------- dex entries --
def parse_dex_entries():
    txt = read("data/pokemon/dex_entries.asm")
    out = {}
    for m in re.finditer(
            r"^(\w+)DexEntry:\n\s*db\s+\"([^\"]*)@\"\n\s*db\s+(\d+),(\d+)\n\s*dw\s+(\d+)",
            txt, re.M):
        out[m.group(1)] = (m.group(2), int(m.group(3)), int(m.group(4)),
                           int(m.group(5)))
    return out


def parse_dex_text():
    txt = read("data/pokemon/dex_text.asm")
    out = {}
    for m in re.finditer(r"^_(\w+)DexEntry::\n(.*?)\n\s*dex", txt, re.S | re.M):
        lines = re.findall(r'(?:text|next|page)\s+"([^"]*)"', m.group(2))
        out[m.group(1)] = lines
    return out


# ------------------------------------------------------------- misc tables --
def parse_simple(path, pat):
    return re.findall(pat, read(path))


def parse_wild():
    """slug-agnostic: SPECIES_CONST -> [(area, pct, lo, hi)]"""
    where = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "data/wild/maps/*.asm"))):
        name = os.path.basename(p)[:-4]
        if name == "nothing":
            continue
        txt = open(p, encoding="utf-8").read()
        m = re.search(r"def_grass_wildmons\s+(\d+)[^\n]*\n(.*?)\tend_grass_wildmons",
                      txt, re.S)
        if not m or int(m.group(1)) == 0:
            continue
        agg = {}
        for i, (lv, sp) in enumerate(re.findall(r"db\s+(\d+),\s*([A-Z_0-9]+)",
                                                m.group(2))):
            lv, pct = int(lv), (SLOT_PCT[i] if i < len(SLOT_PCT) else 0)
            if sp in agg:
                agg[sp][0] += pct
                agg[sp][1] = min(agg[sp][1], lv)
                agg[sp][2] = max(agg[sp][2], lv)
            else:
                agg[sp] = [pct, lv, lv]
        for sp, (pct, lo, hi) in agg.items():
            where.setdefault(sp, []).append((name, pct, lo, hi))
    return where


def pretty(c):
    s = c.replace("_", " ").title()
    return {"Nidoran M": "Nidoran♂", "Nidoran F": "Nidoran♀", "Ho Oh": "Ho-Oh",
            "Mr Mime": "Mr. Mime", "Farfetchd": "Farfetch'd"}.get(s, s)


def ptype(t):
    return t.replace("PSYCHIC_TYPE", "PSYCHIC").title()


def camel(slug):
    return "".join(p.capitalize() for p in re.split(r"[^a-z0-9]+", slug) if p)


# =============================================================== emit notes ==
def build():
    idx = species_index()
    slugs = dex_order_slugs()
    evos = parse_evos_moves()
    entries = parse_dex_entries()
    dtext = parse_dex_text()
    wild = parse_wild()

    pals = re.findall(r"db\s+(PAL_\w+)\s*;\s*(\S+)", read("data/pokemon/palettes.asm"))
    icons = re.findall(r"nybble\s+(ICON_\w+)\s*;\s*(\S+)", read("data/pokemon/menu_icons.asm"))
    cries = re.findall(r"mon_cry\s+(SFX_CRY_\d+),\s*(\$[0-9A-Fa-f]+),\s*(\$[0-9A-Fa-f]+)",
                       read("data/pokemon/cries.asm"))

    const_of_idx = {v: k for k, v in idx.items()}
    mons = []
    for dex in sorted(slugs):
        slug = slugs[dex]
        bs = parse_base_stats(slug)
        const = bs["dexconst"].replace("DEX_", "")
        i = idx.get(const)
        label = camel(slug)
        ev, learn = evos.get(label, ([], []))
        cat, ft, inch, wt = entries.get(label, ("?", 0, 0, 0))
        mons.append(dict(
            dex=dex, slug=slug, const=const, idx=i, label=label, bs=bs,
            evos=ev, learn=learn, cat=cat, ft=ft, inch=inch, wt=wt,
            text=dtext.get(label, []),
            pal=pals[dex][0] if dex < len(pals) else "?",
            icon=icons[dex - 1][0] if dex - 1 < len(icons) else "?",
            cry=cries[i - 1] if i and i - 1 < len(cries) else None,
            where=wild.get(const, []),
        ))
    return mons, const_of_idx


def emit_master(mons):
    L = ["# Master Index — All Pokémon", "",
         "*Auto-generated by `tools/pokedex_report.py`. Regenerate after any species change.*",
         "", f"**{len(mons)} species.** Detail pages: "
         + " · ".join(f"[[Dex {a:03d}-{b:03d}]]" for a, b in
                      [(1, 60), (61, 120), (121, 180), (181, 240)]),
         "", "| Dex | Idx | Name | Type | HP | Atk | Def | Spd | Spc | Palette | Icon |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for m in mons:
        t1, t2 = m["bs"]["types"]
        t = ptype(t1) if t1 == t2 else f"{ptype(t1)}/{ptype(t2)}"
        s = m["bs"]["stats"]
        L.append(f"| {m['dex']} | ${m['idx']:02X} | **{pretty(m['const'])}** | {t} | "
                 f"{s[0]} | {s[1]} | {s[2]} | {s[3]} | {s[4]} | "
                 f"{m['pal'].replace('PAL_','')} | {m['icon'].replace('ICON_','')} |")
    L += ["", "## Related", "- [[Pokemon Data Map]] — where each of these fields lives",
          "- [[Encounter Map - Locations & Rates]]", "- [[Where to Find Each Species]]", ""]
    open(os.path.join(OUT, "Master Index.md"), "w", encoding="utf-8",
         newline="\n").write("\n".join(L))


def emit_detail(mons, lo, hi):
    L = [f"# Dex {lo:03d}-{hi:03d}", "",
         "*Auto-generated by `tools/pokedex_report.py`.*",
         "*Every field a Pokémon uses, and the file it comes from — see [[Pokemon Data Map]].*",
         "", "[[Master Index]]", ""]
    for m in mons:
        if not lo <= m["dex"] <= hi:
            continue
        b = m["bs"]
        t1, t2 = b["types"]
        t = ptype(t1) if t1 == t2 else f"{ptype(t1)} / {ptype(t2)}"
        s = b["stats"]
        L += [f"## #{m['dex']:03d} {pretty(m['const'])}", "",
              f"*{m['cat'].title()} Pokémon* — {m['ft']}'{m['inch']:02d}\", "
              f"{m['wt']/10:.1f} lb", "",
              "| | |", "|---|---|",
              f"| **Type** | {t} |",
              f"| **Stats** | HP {s[0]} · Atk {s[1]} · Def {s[2]} · Spd {s[3]} · Spc {s[4]} |",
              f"| **Catch rate** | {b['catch']} |",
              f"| **Base exp** | {b['exp']} |",
              f"| **Growth** | {b['growth'].replace('GROWTH_','')} |",
              f"| **Palette** | `{m['pal']}` |",
              f"| **Menu icon** | `{m['icon']}` |"]
        if m["cry"]:
            L.append(f"| **Cry** | `{m['cry'][0]}` pitch {m['cry'][1]} length {m['cry'][2]} |")
        L += [f"| **Internal index** | `${m['idx']:02X}` ({m['idx']}) |",
              f"| **Sprites** | `gfx/pokemon/front/{m['slug']}.png` · "
              f"`gfx/pokemon/back/{m['slug']}b.png` |",
              f"| **Pic labels** | `{b['pics'][0]}` / `{b['pics'][1]}` |", ""]

        lv1 = [x for x in b["lv1"] if x != "NO_MOVE"]
        L.append("**Starting moves:** " + (", ".join(pretty(x) for x in lv1) or "—"))
        if m["learn"]:
            L.append("")
            L.append("**Learns by level:** " + ", ".join(
                f"{pretty(mv)} (L{lv})" for lv, mv in m["learn"]))
        if b["tmhm"]:
            L.append("")
            L.append("**TM/HM:** " + ", ".join(pretty(x) for x in b["tmhm"]))
        if m["evos"]:
            L.append("")
            for meth, args in m["evos"]:
                tgt = pretty(args[-1])
                if meth == "LEVEL":
                    L.append(f"**Evolves into:** {tgt} at level {args[0]}")
                elif meth == "ITEM":
                    L.append(f"**Evolves into:** {tgt} with {pretty(args[0])}")
                else:
                    L.append(f"**Evolves into:** {tgt} by {meth.title()}")
        if m["where"]:
            L += ["", "**Found in:**", "", "| Location | Chance | Level |", "|---|---|---|"]
            for area, pct, a, bb in sorted(m["where"], key=lambda x: -x[1]):
                lvl = f"{a}" if a == bb else f"{a}–{bb}"
                L.append(f"| {area} | {pct:.1f}% | {lvl} |")
        else:
            L += ["", "**Found in:** not in grass — obtain by evolution, gift, or event"]
        if m["text"]:
            L += ["", "> " + " ".join(m["text"])]
        L.append("")
    open(os.path.join(OUT, f"Dex {lo:03d}-{hi:03d}.md"), "w", encoding="utf-8",
         newline="\n").write("\n".join(L))


def main():
    os.makedirs(OUT, exist_ok=True)
    mons, _ = build()
    emit_master(mons)
    for lo, hi in [(1, 60), (61, 120), (121, 180), (181, 240)]:
        emit_detail(mons, lo, hi)
    print(f"wrote Master Index + 4 detail pages for {len(mons)} species")


if __name__ == "__main__":
    main()
