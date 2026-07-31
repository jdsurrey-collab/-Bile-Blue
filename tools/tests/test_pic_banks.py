"""
Verify MonPicBanks gives the REAL bank of every species' front sprite.

home/pics.asm used to derive this from hardcoded index ranges, which silently
broke for all 89 imported Gen 2 species (their indexes are scattered through the
reclaimed gaps while their sprites live in separate "Pics Gen2 N" sections), so
each rendered as a corrupted block. This checks the generated table against the
linker's own symbol table -- the ground truth for where each pic actually is.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_syms():
    syms = {}
    for line in open(os.path.join(ROOT, "pokered.sym"), encoding="utf-8"):
        m = re.match(r"([0-9a-f]{2}):([0-9a-f]{4}) (\S+)", line.strip())
        if m:
            syms[m.group(3)] = (int(m.group(1), 16), int(m.group(2), 16))
    return syms


def species_constants():
    path = os.path.join(ROOT, "constants/pokemon_constants.asm")
    out, val = {}, -1
    for line in open(path, encoding="utf-8"):
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
            out[val] = m.group(1)
    return out


def label_for(const):
    """RHYDON -> RhydonPicFront, NIDORAN_M -> NidoranMPicFront."""
    return "".join(p.capitalize() for p in const.split("_")) + "PicFront"


def main():
    syms = load_syms()
    consts = species_constants()
    rom = open(os.path.join(ROOT, "pokered.gbc"), "rb").read()

    bank, addr = syms["MonPicBanks"]
    off = bank * 0x4000 + (addr - 0x4000)

    # Not ordinary species entries; special-cased in home/pics.asm before the table.
    EXEMPT = {"MEW", "FOSSIL_KABUTOPS", "FOSSIL_AERODACTYL", "MON_GHOST", "NO_MON"}

    checked = mismatch = missing = 0
    problems = []
    for idx, const in sorted(consts.items()):
        if const in EXEMPT:
            continue
        lbl = label_for(const)
        if lbl not in syms:
            missing += 1
            problems.append(f"  ${idx:02X} {const}: no symbol {lbl}")
            continue
        real_bank = syms[lbl][0]
        table_bank = rom[off + idx]
        checked += 1
        if real_bank != table_bank:
            mismatch += 1
            if len(problems) < 15:
                problems.append(
                    f"  ${idx:02X} {const:<14} table says bank ${table_bank:02X}, "
                    f"sprite is really in bank ${real_bank:02X}")

    print(f"species checked      : {checked}")
    print(f"missing pic symbols  : {missing}")
    print(f"bank mismatches      : {mismatch}")
    for p in problems:
        print(p)

    ok = mismatch == 0 and missing == 0
    print("\nPASS: every species' pic bank matches the linker"
          if ok else "\nFAIL: pic bank table is wrong")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
