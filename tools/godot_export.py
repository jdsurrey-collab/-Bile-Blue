#!/usr/bin/env python3
"""
Export pokered/Pokemon Purple data into the Godot port.

Written generically so it scales to every map, not just the first one. Each map
becomes a single JSON with its tiles already expanded from blocks, so the Godot
side never needs to know about the blockset indirection.

    python tools/godot_export.py --map PalletTown
    python tools/godot_export.py --all

DATA MODEL (worth understanding before changing anything):

  tileset .png   16x6 = 96 tiles of 8x8 px, 4 DMG shades
  blockset .bst  128 blocks, each 16 bytes = a 4x4 arrangement of tile indices
  map .blk       width*height bytes of BLOCK indices
  collision      a list of TILE ids that are walkable (everything else is solid)

  So one map block = 4x4 tiles = 32x32 px, and the player moves on a 16x16 px
  grid -- i.e. each block is 2x2 player cells. That 16-vs-32 distinction is the
  single easiest thing to get wrong here.
"""
import argparse
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GODOT = r"C:\Users\jdsur\Documents\pokemonpurple"
if os.name != "nt":
    GODOT = "/mnt/c/Users/jdsur/Documents/pokemonpurple"

TILE_PX = 8
BLOCK_TILES = 4          # a block is 4x4 tiles
PLAYER_CELL_TILES = 2    # the player grid is 2x2 tiles (16x16 px)

# DMG palette. Source PNGs are 8-bit grayscale; index 0 is the lightest shade.
DMG = [(232, 232, 232), (160, 160, 160), (88, 88, 88), (24, 24, 24)]


def read(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()


# ------------------------------------------------------------------ parsing --
def map_dimensions():
    """{MAP_CONST: (width, height)} in BLOCKS, from constants/map_constants.asm."""
    out = {}
    for m in re.finditer(r"map_const\s+([A-Z_0-9]+),\s*(\d+),\s*(\d+)",
                         read("constants/map_constants.asm")):
        out[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return out


def map_header(name):
    """-> (MAP_CONST, TILESET_NAME, [(dir, target_const, offset_blocks), ...])

    The offset is the block-space alignment of the target map relative to this
    one -- an X offset for north/south connections (the target's left edge vs.
    this map's left edge), a Y offset for east/west (target's top edge vs. this
    map's top edge). Needed to stitch maps of different widths/heights into one
    continuous seamless world; getting the axis wrong silently misaligns every
    connection between two differently-sized maps (anything narrower/wider than
    its neighbour, e.g. Route 1 (10 blocks wide) under Viridian City (20)).
    """
    txt = read(f"data/maps/headers/{name}.asm")
    m = re.search(r"map_header\s+\w+,\s*([A-Z_0-9]+),\s*(\w+)", txt)
    conns = [(c.group(1), c.group(3), int(c.group(4)))
             for c in re.finditer(
                 r"connection\s+(\w+),\s*(\w+),\s*([A-Z_0-9]+),\s*(-?\d+)", txt)]
    return m.group(1), m.group(2), conns


def tileset_assets():
    """{TILESET_NAME: (gfx_basename, blockset_basename)}.

    Several tilesets are pure ALIASES that share another's graphics -- Dojo uses
    gym, Mart uses pokecenter, Museum and ForestGate use gate, RedsHouse1/2 use
    reds_house. gfx/tilesets.asm expresses that by stacking labels above a single
    INCBIN, so collect the labels that pile up before each one. Deriving the
    filename from the tileset name instead silently loses those maps -- which is
    exactly what happened first time round, and it took out Oak's Lab.
    """
    txt = read("gfx/tilesets.asm")
    gfx, blk = {}, {}
    pend_g, pend_b = [], []
    for line in txt.splitlines():
        s = line.strip()
        m = re.match(r"(\w+)_GFX::", s)
        if m:
            pend_g.append(m.group(1))
        m = re.match(r"(\w+)_Block::", s)
        if m:
            pend_b.append(m.group(1))
        m = re.search(r'INCBIN\s+"gfx/tilesets/([a-z0-9_]+)\.2bpp"', s)
        if m:
            for t in pend_g:
                gfx[t] = m.group(1)
            pend_g = []
        m = re.search(r'INCBIN\s+"gfx/blocksets/([a-z0-9_]+)\.bst"', s)
        if m:
            for t in pend_b:
                blk[t] = m.group(1)
            pend_b = []
    # Keyed on a NORMALISED name (uppercase, underscores stripped), because the
    # two sources spell tilesets differently: map headers write DOJO,
    # REDS_HOUSE_1, FOREST_GATE while gfx/tilesets.asm labels them Dojo_GFX,
    # RedsHouse1_GFX, ForestGate_GFX. Matching literally misses every alias and
    # falls back to a derived filename -- which only *looks* fine for Overworld,
    # since "OVERWORLD".lower() happens to be the real file. That silently
    # dropped Oak's Lab, both Red's House floors and 20-odd other maps.
    return {_norm_tileset(t): (gfx.get(t, t.lower()), blk.get(t, t.lower()))
            for t in set(gfx) | set(blk)}


def _norm_tileset(name):
    return re.sub(r"[^A-Z0-9]", "", name.upper())


def collision_tiles(tileset):
    """Walkable TILE ids for a tileset, from collision_tile_ids.asm.

    Labels are shared (RedsHouse1_Coll:: and RedsHouse2_Coll:: sit on the same
    coll_tiles line), so collect every label that stacks above a given line.
    """
    txt = read("data/tilesets/collision_tile_ids.asm")
    pending, table = [], {}
    for line in txt.splitlines():
        s = line.strip()
        m = re.match(r"(\w+)_Coll::", s)
        if m:
            pending.append(_norm_tileset(m.group(1)))
            continue
        if s.startswith("coll_tiles"):
            ids = [int(x, 16) for x in re.findall(r"\$([0-9a-fA-F]+)", s)]
            for lbl in pending:
                table[lbl] = ids
            pending = []
    return set(table.get(_norm_tileset(tileset), []))


def warp_tiles(tileset):
    txt = read("data/tilesets/warp_tile_ids.asm")
    m = re.search(rf"\.{tileset}WarpTileIDs:\n\s*warp_tiles ([^\n]+)", txt)
    return set(int(x, 16) for x in re.findall(r"\$([0-9a-fA-F]+)", m.group(1))) if m else set()


_DIRECTIONS = {"DOWN": "down", "UP": "up", "LEFT": "left", "RIGHT": "right"}


_CLASS_KEY_OVERRIDES = {
    # constants/trainer_constants.asm's PSYCHIC_TR is disambiguated from the
    # Pokemon type constant PSYCHIC (trainer_const values and move/type
    # constants share one C-style namespace) -- naively transformed this
    # would be "PsychicTr", but the real party-data label in
    # data/trainers/parties.asm is just "PsychicData" (no "Tr" suffix, no
    # collision to avoid there). Confirmed by cross-checking every
    # trainer_const entry's naive transform against every *Data: label in
    # parties.asm -- this is the only real mismatch found.
    "PsychicTr": "Psychic",
}


def _class_key(opp_snake_case):
    """"BUG_CATCHER" -> "BugCatcher" -- matches data/trainers/parties.asm's own
    label convention (and therefore tools/godot_export_data.py's trainers.json
    class keys) exactly, since trainer_const's OPP_<NAME> and *Data: labels are
    generated from the same underlying enum order (constants/trainer_constants.asm).
    A small number of trainer_const names deliberately diverge from their
    party-data label to avoid colliding with an unrelated constant (see
    _CLASS_KEY_OVERRIDES) -- those are corrected here rather than in every
    caller."""
    key = "".join(w.capitalize() for w in opp_snake_case.split("_"))
    return _CLASS_KEY_OVERRIDES.get(key, key)


_trainer_parties_cache = None


def trainer_parties():
    """{ClassKey: [[{"species","level"}, ...], ...]} -- one list per numbered
    trainer (wTrainerNo, 1-based) of that class, straight from
    data/trainers/parties.asm. Self-contained rather than importing
    godot_export_data.py -- each tool in this project is a standalone script,
    not a shared library, and this parse is ~15 lines."""
    global _trainer_parties_cache
    if _trainer_parties_cache is not None:
        return _trainer_parties_cache
    txt = read("data/trainers/parties.asm")
    out = {}
    for m in re.finditer(r"^(\w+)Data:\n(.*?)(?=^\w+Data:|\Z)", txt, re.S | re.M):
        cls, body = m.group(1), m.group(2)
        parties = []
        for line in body.splitlines():
            s = line.strip()
            if not s.startswith("db "):
                continue
            toks = [t.strip() for t in s[3:].split(",") if t.strip() and not t.strip().startswith(";")]
            if not toks:
                continue
            if toks[0] == "$FF":
                mons, rest = [], toks[1:]
                for i in range(0, len(rest) - 1, 2):
                    if rest[i] == "0":
                        break
                    mons.append({"species": rest[i + 1], "level": int(rest[i])})
            else:
                lvl = int(toks[0])
                mons = [{"species": t, "level": lvl} for t in toks[1:] if t != "0"]
            if mons:
                parties.append(mons)
        if parties:
            out[cls] = parties
    _trainer_parties_cache = out
    return out


_trainer_base_money_cache = None


def trainer_base_money():
    """{ClassKey: base_money} from data/trainers/pic_pointers_money.asm --
    real money reward per level is base_money * enemy's level
    (engine/battle/read_trainer_party.asm's wAmountMoneyWon loop, confirmed
    by reading that code directly rather than assumed)."""
    global _trainer_base_money_cache
    if _trainer_base_money_cache is not None:
        return _trainer_base_money_cache
    txt = read("data/trainers/pic_pointers_money.asm")
    out = {}
    for m in re.finditer(r"pic_money\s+(\w+)Pic,\s*(\d+)", txt):
        out[m.group(1)] = int(m.group(2))
    _trainer_base_money_cache = out
    return out


def parse_trainer_headers(name):
    """{TEXT_CONST: {"event_flag", "sight_range", "challenge_lines_label",
    "defeat_lines_label"}} for every trainer NPC on this map -- sight range,
    the "already defeated" event flag, and the pre/post-battle text are NOT
    in the object_event data at all (see parse_objects' own trainer-flag
    handling); they live in a separate per-map trainer-header table in
    scripts/<Map>.asm, correlated to a specific object_event only through
    that trainer's own text-stub function explicitly naming its header
    (`ld hl, <Map>TrainerHeaderN`) -- there is no positional/ordinal
    shortcut reliable enough to skip this cross-reference (a map's very
    first object can be a non-trainer sign, offsetting every ordinal by one,
    exactly why real map scripts use `def_trainers N` to begin with).

    The `trainer` macro's own args are (event_flag, view_range,
    TextBeforeBattle, TextEndBattle, TextAfterBattle) -- TextBeforeBattle is
    the real pre-fight challenge line (-> NPCBattleData.challenge_lines);
    TextEndBattle/TextAfterBattle are both only ever shown together right
    after a WIN (a player loss blacks out unconditionally with no
    trainer-specific text at all, confirmed in home/trainers.asm --
    EndTrainerBattle short-circuits reward/text/flag handling entirely on
    the blackout sentinel), so both are folded into one
    NPCBattleData.defeat_lines sequence here rather than inventing an
    unreachable "talk to an already-defeated trainer" repeat-text feature
    for content that would never actually be shown (the ROM permanently
    hides a defeated trainer's sprite, see home/trainers.asm's
    EndTrainerBattle -> HideObject call).
    """
    try:
        txt = read(f"scripts/{name}.asm")
    except FileNotFoundError:
        return {}

    text_label_for_const = dict(
        (const, label) for label, const in
        re.findall(r"dw_const\s+(\w+),\s*(TEXT_\w+)", txt))

    headers = {}
    for m in re.finditer(
            r"(\w*TrainerHeader\w*):\n\s*trainer\s+(\w+),\s*(\d+),\s*(\w+),\s*(\w+),\s*(\w+)", txt):
        headers[m.group(1)] = dict(
            event_flag=m.group(2), sight_range=int(m.group(3)),
            challenge_label=m.group(4), end_label=m.group(5), after_label=m.group(6))

    label_blocks = dict(re.findall(r"^(\w+):\n(.*?)(?=^\w+:\n|\Z)", txt, re.S | re.M))

    out = {}
    for text_const, label in text_label_for_const.items():
        block = label_blocks.get(label, "")
        hm = re.search(r"ld hl,\s*(\w*TrainerHeader\w*)", block)
        if not hm or hm.group(1) not in headers:
            continue
        h = headers[hm.group(1)]
        out[text_const] = dict(
            event_flag=h["event_flag"], sight_range=h["sight_range"],
            challenge_lines_label=_resolve_text_label(label_blocks, h["challenge_label"]),
            defeat_lines_labels=[_resolve_text_label(label_blocks, h["end_label"]),
                                  _resolve_text_label(label_blocks, h["after_label"])],
        )
    return out


def _resolve_text_label(label_blocks, script_label):
    """<Map>.asm's own text-stub label (e.g. Route3Youngster1BattleText) just
    wraps a `text_far _RealLabel` pointing into text/<Map>.asm -- resolve to
    that real label (without the leading underscore) so it matches
    parse_text()'s own keys directly, no further lookup needed. Bounded to
    this one label's own already-extracted block (not a fresh whole-file
    regex) so a stub with no text_far at all can't accidentally bleed a
    non-greedy match into some unrelated later label."""
    block = label_blocks.get(script_label, "")
    m = re.search(r"text_far\s+_(\w+)", block)
    return m.group(1) if m else None


def parse_objects(name):
    """warps / signs / npcs, in PLAYER-CELL coordinates (already 16x16 grid).

    Every NPC's real facing direction (DOWN/UP/LEFT/RIGHT) is exported now,
    not just trainers' -- it was silently dropped entirely before (every
    generated NPC defaulted to "down"). Trainer NPCs are the 8-comma-arg
    form of object_event (TRAINER bit implied by argument count in the real
    macro, not a visible token in source -- confirmed by reading the actual
    ROM source lines directly, not the macro's own internals) and get their
    party/sight-range/reward/flag/text resolved here so nothing downstream
    (tools/generate_npc_zones.py) needs its own ROM-parsing logic at all.
    """
    txt = read(f"data/maps/objects/{name}.asm")
    warps = [dict(x=int(a), y=int(b), target=c, target_warp=int(d))
             for a, b, c, d in
             re.findall(r"warp_event\s+(\d+),\s*(\d+),\s*(\w+),\s*(\d+)", txt)]
    signs = [dict(x=int(a), y=int(b), text=c)
             for a, b, c in
             re.findall(r"bg_event\s+(\d+),\s*(\d+),\s*(\w+)", txt)]

    trainer_headers = parse_trainer_headers(name)
    texts = parse_text(name)
    parties = trainer_parties()
    base_money = trainer_base_money()

    npcs = []
    for a, b, spr, mv, rng, tid, opp, set_no in re.findall(
            r"object_event\s+(\d+),\s*(\d+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)"
            r"(?:,\s*(OPP_\w+),\s*(\d+))?", txt):
        n = dict(x=int(a), y=int(b), sprite=spr, movement=mv, range=rng, text=tid)
        if rng in _DIRECTIONS:
            n["facing"] = _DIRECTIONS[rng]
        if opp:
            cls = _class_key(opp[len("OPP_"):])
            party = parties.get(cls, [])
            set_i = int(set_no)
            mons = party[set_i - 1] if 1 <= set_i <= len(party) else []
            n["is_trainer"] = True
            n["trainer_class"] = cls
            n["trainer_set"] = set_i
            n["party"] = mons
            if mons:
                n["reward_money"] = base_money.get(cls, 0) * mons[-1]["level"]
            hdr = trainer_headers.get(tid)
            if hdr:
                n["sight_range"] = hdr["sight_range"]
                n["defeated_flag"] = hdr["event_flag"]
                n["challenge_lines"] = texts.get(hdr["challenge_lines_label"], [])
                defeat_lines = []
                for lbl in hdr["defeat_lines_labels"]:
                    defeat_lines.extend(texts.get(lbl, []))
                n["defeat_lines"] = defeat_lines
        npcs.append(n)
    return warps, signs, npcs


def parse_text(name):
    """-> {LABEL: [ {kind, line}, ... ]} from text/<Map>.asm"""
    try:
        txt = read(f"text/{name}.asm")
    except FileNotFoundError:
        return {}
    out = {}
    for m in re.finditer(r"^_(\w+)::\n(.*?)(?=^_\w+::|\Z)", txt, re.S | re.M):
        parts = []
        for k, s in re.findall(r'\b(text|line|cont|para|done|prompt|next)\b\s*"?([^"\n]*)"?',
                               m.group(2)):
            if k in ("done", "prompt"):
                continue
            if s:
                parts.append({"kind": k, "line": s})
        if parts:
            out[m.group(1)] = parts
    return out


# ------------------------------------------------------------------- images --
def export_tileset(tileset, dest_dir):
    from PIL import Image
    src = os.path.join(ROOT, f"gfx/tilesets/{tileset.lower()}.png")
    im = Image.open(src).convert("L")
    shades = sorted(set(im.getdata()), reverse=True)  # lightest first
    lut = {v: DMG[min(i, 3)] for i, v in enumerate(shades)}
    out = Image.new("RGB", im.size)
    out.putdata([lut[p] for p in im.getdata()])
    os.makedirs(dest_dir, exist_ok=True)
    out.save(os.path.join(dest_dir, f"{tileset.lower()}.png"))
    return im.size[0] // TILE_PX, im.size[1] // TILE_PX


def export_sprite(sprite_file, dest_dir):
    from PIL import Image
    src = os.path.join(ROOT, f"gfx/sprites/{sprite_file}.png")
    if not os.path.exists(src):
        return False
    im = Image.open(src).convert("L")
    shades = sorted(set(im.getdata()), reverse=True)
    lut = {v: DMG[min(i, 3)] for i, v in enumerate(shades)}
    out = Image.new("RGBA", im.size)
    px = []
    for p in im.getdata():
        r, g, b = lut[p]
        # Lightest shade is the transparent key in overworld sprite sheets.
        px.append((r, g, b, 0) if p == shades[0] else (r, g, b, 255))
    out.putdata(px)
    os.makedirs(dest_dir, exist_ok=True)
    out.save(os.path.join(dest_dir, f"{sprite_file}.png"))
    return True


# -------------------------------------------------------------------- build --
def build_map(name, dims):
    const, tileset, conns = map_header(name)
    wb, hb = dims[const]
    blocks = open(os.path.join(ROOT, f"maps/{name}.blk"), "rb").read()
    if len(blocks) != wb * hb:
        raise SystemExit(f"{name}: .blk is {len(blocks)} bytes, expected {wb*hb}")

    assets = tileset_assets()
    gfx_name, blk_name = assets.get(_norm_tileset(tileset), (tileset.lower(), tileset.lower()))
    bst = open(os.path.join(ROOT, f"gfx/blocksets/{blk_name}.bst"), "rb").read()

    # Expand blocks -> a flat grid of 8x8 tile indices.
    tw, th = wb * BLOCK_TILES, hb * BLOCK_TILES
    tiles = [0] * (tw * th)
    for by in range(hb):
        for bx in range(wb):
            blk = blocks[by * wb + bx]
            base = blk * BLOCK_TILES * BLOCK_TILES
            for ty in range(BLOCK_TILES):
                for tx in range(BLOCK_TILES):
                    tiles[(by * BLOCK_TILES + ty) * tw + bx * BLOCK_TILES + tx] = \
                        bst[base + ty * BLOCK_TILES + tx]

    # Walkability on the PLAYER grid (16x16 px = 2x2 tiles). Gen 1 tests the
    # tile the player is standing on, which is the lower-left tile of the pair.
    walk_ids = collision_tiles(tileset)
    warp_ids = warp_tiles(tileset)
    pw, ph = tw // PLAYER_CELL_TILES, th // PLAYER_CELL_TILES
    walk, warpable = [], []
    for py in range(ph):
        for px_ in range(pw):
            t = tiles[(py * PLAYER_CELL_TILES + 1) * tw + px_ * PLAYER_CELL_TILES]
            walk.append(t in walk_ids)
            warpable.append(t in warp_ids)

    warps, signs, npcs = parse_objects(name)
    return dict(
        name=name, map_const=const, tileset=gfx_name,
        blocks_w=wb, blocks_h=hb,
        tiles_w=tw, tiles_h=th, tiles=tiles,
        cells_w=pw, cells_h=ph, walkable=walk, warp_tile=warpable,
        connections=[{"dir": d, "map": m, "offset_blocks": o} for d, m, o in conns],
        warps=warps, signs=signs, npcs=npcs,
    )


SPRITE_FILE = {
    "SPRITE_OAK": "oak", "SPRITE_GIRL": "girl", "SPRITE_FISHER": "fisher",
    "SPRITE_RED": "red", "SPRITE_BLUE": "blue", "SPRITE_MOM": "mom",
    "SPRITE_YOUNGSTER": "youngster", "SPRITE_CHANNELER": "channeler",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", action="append", default=[])
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    dims = map_dimensions()
    names = args.map or ["PalletTown"]
    if args.all:
        names = [os.path.basename(p)[:-4]
                 for p in sorted(glob_blk())]

    data_dir = os.path.join(GODOT, "data", "maps")
    text_dir = os.path.join(GODOT, "data", "text")
    ts_dir = os.path.join(GODOT, "assets", "tilesets")
    sp_dir = os.path.join(GODOT, "assets", "sprites", "characters")
    for d in (data_dir, text_dir, ts_dir, sp_dir):
        os.makedirs(d, exist_ok=True)

    done_ts = set()
    skipped = []
    for name in names:
        # Some .blk files have no header (unused/beta maps), and a few tilesets
        # have no collision entry. Skip those rather than aborting the batch --
        # the summary at the end reports exactly what was left out.
        try:
            m = build_map(name, dims)
        except (FileNotFoundError, KeyError, AttributeError, SystemExit) as e:
            skipped.append((name, type(e).__name__))
            continue
        slug = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
        with open(os.path.join(data_dir, f"{slug}.json"), "w",
                  encoding="utf-8", newline="\n") as f:
            json.dump(m, f, indent=1)
        if m["tileset"] not in done_ts:
            wt, ht = export_tileset(m["tileset"], ts_dir)
            done_ts.add(m["tileset"])
            print(f"  tileset {m['tileset']}: {wt}x{ht} tiles")
        with open(os.path.join(text_dir, f"{slug}.json"), "w",
                  encoding="utf-8", newline="\n") as f:
            json.dump(parse_text(name), f, indent=1)
        for n in m["npcs"]:
            f = SPRITE_FILE.get(n["sprite"], n["sprite"].replace("SPRITE_", "").lower())
            if export_sprite(f, sp_dir):
                n["sprite_file"] = f
        # rewrite with sprite_file resolved
        with open(os.path.join(data_dir, f"{slug}.json"), "w",
                  encoding="utf-8", newline="\n") as f:
            json.dump(m, f, indent=1)
        print(f"{name}: {m['cells_w']}x{m['cells_h']} cells, "
              f"{len(m['warps'])} warps, {len(m['signs'])} signs, "
              f"{len(m['npcs'])} npcs")

    export_sprite("red", sp_dir)
    if skipped:
        print(f"\nskipped {len(skipped)} maps (no header / no collision data):")
        for n, why in skipped[:12]:
            print(f"  {n} ({why})")
        if len(skipped) > 12:
            print(f"  ... and {len(skipped) - 12} more")
    print("done ->", GODOT)


def glob_blk():
    import glob as g
    return g.glob(os.path.join(ROOT, "maps", "*.blk"))


if __name__ == "__main__":
    main()
