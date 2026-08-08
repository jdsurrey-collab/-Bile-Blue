#!/usr/bin/env python3
"""
Export the pieces the Godot port's warp system and the cultist dream sequence
need, neither of which the earlier exporters cover:

  map_index.json     {MAP_CONST: exported-file-slug}, so a warp's target
                      (a constant like REDS_HOUSE_1F) can be resolved to the
                      actual map JSON to load.
  cultist_dream.json the dream sequence's dialogue AND the 3 answer choices
                      per question. The intro/questions/outro live in
                      text/RedsHouse2F.asm like normal map text (and are
                      already exported there), but the ANSWER CHOICES
                      (RAGE/CALM/FURY etc.) live in data/text_boxes.asm as a
                      menu template, which the per-map text exporter never
                      looks at -- so they need pulling separately.

    python tools/godot_export_extra.py
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GODOT = "/mnt/c/Users/jdsur/Documents/pokemonpurple" if os.name != "nt" \
    else r"C:\Users\jdsur\Documents\pokemonpurple"

sys.path.insert(0, os.path.join(ROOT, "tools"))
from godot_export_data import read


def export_map_index():
    out = {}
    for p in sorted(glob.glob(os.path.join(GODOT, "data", "maps", "*.json"))):
        with open(p, encoding="utf-8") as f:
            m = json.load(f)
        out[m["map_const"]] = os.path.basename(p)[:-5]
    return out


def export_cultist_dream():
    txt = read("text/RedsHouse2F.asm")

    def entries(label):
        m = re.search(rf"^_{label}::\n(.*?)(?=^_\w+::|\Z)", txt, re.S | re.M)
        if not m:
            return []
        out = []
        for k, s in re.findall(
                r'\b(text|line|cont|para|done|prompt|next)\b\s*"?([^"\n]*)"?',
                m.group(1)):
            if k in ("done", "prompt") or not s:
                continue
            out.append({"kind": k, "line": s})
        return out

    boxes = read("data/text_boxes.asm")

    def choices(label):
        m = re.search(rf"^{label}:\n(.*?)(?=^\w+:|\Z)", boxes, re.S | re.M)
        if not m:
            return []
        return [c.strip().rstrip("@")
                for c in re.findall(r'"([^"]*)"', m.group(1))]

    return {
        "intro": entries("RedsHouse2FCultistIntroText"),
        "questions": [
            {"prompt": entries("RedsHouse2FCultistQuestion1Text"),
             "choices": choices("CultistQ1Text")},
            {"prompt": entries("RedsHouse2FCultistQuestion2Text"),
             "choices": choices("CultistQ2Text")},
            {"prompt": entries("RedsHouse2FCultistQuestion3Text"),
             "choices": choices("CultistQ3Text")},
        ],
        "outro": entries("RedsHouse2FCultistOutroText"),
        "fallback": entries("RedsHouse2FCultistText"),
        # answer index 0/1/2 -> Fire/Water/Thunder, always, regardless of
        # each question's wording (CLAUDE.md item 8)
        "stones": ["FIRE_STONE", "WATER_STONE", "THUNDER_STONE"],
    }


def main():
    data_dir = os.path.join(GODOT, "data")
    os.makedirs(data_dir, exist_ok=True)

    idx = export_map_index()
    with open(os.path.join(data_dir, "map_index.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(idx, f, indent=1)
    print(f"map index: {len(idx)} maps")

    cd = export_cultist_dream()
    with open(os.path.join(data_dir, "cultist_dream.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(cd, f, indent=1)
    ok = all(len(q["choices"]) == 3 for q in cd["questions"]) and \
        len(cd["intro"]) > 0 and len(cd["outro"]) > 0
    print(f"cultist dream: intro={len(cd['intro'])} lines, "
          f"3 questions x 3 choices each={ok}, outro={len(cd['outro'])} lines")
    print("->", data_dir)


if __name__ == "__main__":
    main()
