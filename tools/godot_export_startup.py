#!/usr/bin/env python3
"""
Export the startup-sequence assets and text: gothic intro, title screen,
main menu, Oak's speech, naming screen.

Companion to godot_export.py (maps) and godot_export_data.py (species/moves).
Everything here is either a static image (recoloured to DMG the same way the
other exporters do) or dialogue text (parsed the same way map text is).

    python tools/godot_export_startup.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GODOT = "/mnt/c/Users/jdsur/Documents/pokemonpurple" if os.name != "nt" \
    else r"C:\Users\jdsur\Documents\pokemonpurple"

sys.path.insert(0, os.path.join(ROOT, "tools"))
from godot_export import export_sprite, DMG  # reuse the DMG recolour logic
from godot_export_data import read


def export_image(src_rel, dest_dir, dest_name, keep_alpha=False):
    """Like export_sprite, but for arbitrary images (not just gfx/sprites/*)."""
    from PIL import Image
    src = os.path.join(ROOT, src_rel)
    if not os.path.exists(src):
        print(f"  MISSING: {src_rel}")
        return False
    im = Image.open(src).convert("L")
    shades = sorted(set(im.getdata()), reverse=True)
    lut = {v: DMG[min(i, 3)] for i, v in enumerate(shades)}
    out = Image.new("RGBA" if keep_alpha else "RGB", im.size)
    px = []
    for p in im.getdata():
        r, g, b = lut[p]
        if keep_alpha:
            px.append((r, g, b, 0) if p == shades[0] else (r, g, b, 255))
        else:
            px.append((r, g, b))
    out.putdata(px)
    os.makedirs(dest_dir, exist_ok=True)
    out.save(os.path.join(dest_dir, dest_name))
    return True


def export_1bpp_image(src_rel, dest_dir, dest_name):
    """1bpp source images (mode '1') are pure black/white -- no shade ranking
    needed, just map True/False straight to the DMG extremes and key white as
    transparent (these are wordmark overlays, meant to sit on a background)."""
    from PIL import Image
    src = os.path.join(ROOT, src_rel)
    im = Image.open(src).convert("1")
    out = Image.new("RGBA", im.size)
    px = []
    for p in im.getdata():
        px.append((24, 24, 24, 255) if p == 0 else (0, 0, 0, 0))
    out.putdata(px)
    os.makedirs(dest_dir, exist_ok=True)
    out.save(os.path.join(dest_dir, dest_name))


def parse_named_text(path, labels):
    """Pull specific _Label:: entries out of a text/*.asm-style file, in the
    same {kind, line} shape the map exporter uses, so Dialogue.build_pages()
    works unchanged on startup text too."""
    txt = read(path)
    out = {}
    for label in labels:
        m = re.search(rf"^_{label}::\n(.*?)(?=^_\w+::|\Z)", txt, re.S | re.M)
        if not m:
            continue
        parts = []
        for k, s in re.findall(
                r'\b(text|line|cont|para|done|prompt|next)\b\s*"?([^"\n]*)"?',
                m.group(1)):
            if k in ("done", "prompt") or not s:
                continue
            parts.append({"kind": k, "line": s})
        out[label] = parts
    return out


def main():
    assets = os.path.join(GODOT, "assets", "startup")
    data_dir = os.path.join(GODOT, "data")
    os.makedirs(assets, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    # --- images --------------------------------------------------------
    export_image("gfx/title/pokemon_logo.png", assets, "pokemon_logo.png")
    export_1bpp_image("gfx/title/purple_version.png", assets, "purple_version.png")
    export_image("gfx/title/gothic_intro_bg.png", assets, "gothic_intro_bg.png")
    export_1bpp_image("gfx/title/gothic_intro_stamp.png", assets, "gothic_intro_stamp.png")
    export_image("gfx/trainers/prof.oak.png", assets, "prof_oak.png")
    export_image("gfx/trainers/rival1.png", assets, "rival1.png")
    export_sprite("red", assets)
    export_sprite("oak", assets)
    export_sprite("blue", assets)
    print("startup images exported")

    # --- Oak's speech / naming text, from data/text/text_2.asm ---------
    labels = [
        "OakSpeechText1", "OakSpeechText2A", "OakSpeechText2B",
        "IntroducePlayerText", "IntroduceRivalText", "OakSpeechText3",
        "YourNameIsText", "HisNameIsText",
    ]
    text = parse_named_text("data/text/text_2.asm", labels)
    with open(os.path.join(data_dir, "startup_text.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(text, f, indent=1)
    print(f"startup text: {len(text)}/{len(labels)} labels found")

    # --- misc startup constants -----------------------------------------
    misc = {
        "player_names": ["RED", "ASH", "JACK"],
        "rival_names": ["BLUE", "GARY", "JOHN"],
        "title_mons": ["BULBASAUR", "CHARMANDER", "SQUIRTLE"],  # cosmetic cycle
        "copyright": "©'95.'96.'98 GAME FREAK inc.",
    }
    with open(os.path.join(data_dir, "startup_misc.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(misc, f, indent=1)
    print("startup misc constants exported")
    print("->", assets)


if __name__ == "__main__":
    main()
