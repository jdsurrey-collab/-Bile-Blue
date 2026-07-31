"""
END-TO-END: for every species, does the NAME the game prints match the SPRITE
it draws?

The earlier alignment tests each checked one link in isolation and all passed
while the game still showed wrong-name/wrong-sprite pairs, because the chain
crosses BOTH numbering systems and a mismatch between them is invisible to a
single-axis check:

    internal index  -> MonsterNames[i]              (name)
    internal index  -> PokedexOrder[i]              -> dex
    dex             -> BaseStats[dex-1]             -> pic POINTER
    internal index  -> MonPicBanks[i]               -> pic BANK
    (bank, pointer) -> must equal <Species>PicFront in the linker's symbols

Every one of those has to agree about which species it is talking about.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Offsets inside a base_stats entry (see data/pokemon/base_stats/*.asm):
#   0 dex id | 1-5 stats | 6-7 types | 8 catch | 9 exp | 10 sprite dims
#   11-12 dw PicFront | 13-14 dw PicBack | ...
OFF_DEXID = 0
OFF_PICFRONT = 11


def syms():
    out = {}
    for line in open(os.path.join(ROOT, "pokered.sym"), encoding="utf-8"):
        m = re.match(r"([0-9a-f]{2}):([0-9a-f]{4}) (\S+)", line.strip())
        if m:
            out[m.group(3)] = (int(m.group(1), 16), int(m.group(2), 16))
    return out


def species_constants():
    out, val = {}, -1
    for line in open(os.path.join(ROOT, "constants/pokemon_constants.asm"),
                     encoding="utf-8"):
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


def decode(b):
    o = []
    for c in b:
        if c == 0x50:
            break
        if 0x80 <= c <= 0x99:
            o.append(chr(65 + c - 0x80))
        elif 0xA0 <= c <= 0xB9:
            o.append(chr(97 + c - 0xA0))
        elif 0xF6 <= c <= 0xFF:
            o.append(chr(ord("0") + c - 0xF6))
        elif c in (0xE6, 0xF2):
            o.append(".")
        elif c == 0xE3:
            o.append("-")
        elif c == 0xEF:
            o.append("M")
        elif c == 0xF5:
            o.append("F")
        elif c == 0x7F:
            o.append(" ")
        else:
            o.append("?")
    return "".join(o).strip()


def norm(s):
    return re.sub(r"[^A-Z0-9]", "", s.upper())


def label_for(const):
    return "".join(p.capitalize() for p in const.split("_")) + "PicFront"


def flat(bank, addr):
    return bank * 0x4000 + (addr - 0x4000)


def main():
    S = syms()
    consts = species_constants()
    rom = open(os.path.join(ROOT, "pokered.gbc"), "rb").read()

    names_off = flat(*S["MonsterNames"])
    order_off = flat(*S["PokedexOrder"])
    stats_off = flat(*S["BaseStats"])
    banks_off = flat(*S["MonPicBanks"])

    # Derive entry stride from the ROM rather than duplicating the rsset math.
    stride = next((c for c in range(20, 64)
                   if all(rom[stats_off + i * c] == i + 1 for i in range(20))), None)
    if stride is None:
        print("FAIL: could not determine BASE_DATA_SIZE")
        sys.exit(1)

    # Not ordinary species: special-cased in home/pics.asm / GetMonHeader.
    EXEMPT = {"NO_MON", "MEW", "FOSSIL_KABUTOPS", "FOSSIL_AERODACTYL", "MON_GHOST"}

    checked = 0
    bad_name, bad_dex, bad_sprite = [], [], []

    for idx, const in sorted(consts.items()):
        if const in EXEMPT:
            continue
        lbl = label_for(const)
        if lbl not in S:
            continue
        checked += 1

        name = decode(rom[names_off + (idx - 1) * 10: names_off + (idx - 1) * 10 + 10])
        if norm(name) != norm(const):
            bad_name.append((idx, const, name))
            continue

        dex = rom[order_off + (idx - 1)]
        entry = stats_off + (dex - 1) * stride
        if rom[entry + OFF_DEXID] != dex:
            bad_dex.append((idx, const, dex, rom[entry + OFF_DEXID]))
            continue

        ptr = rom[entry + OFF_PICFRONT] | (rom[entry + OFF_PICFRONT + 1] << 8)
        bank = rom[banks_off + idx]
        want_bank, want_addr = S[lbl]
        if (bank, ptr) != (want_bank, want_addr):
            bad_sprite.append((idx, const, bank, ptr, want_bank, want_addr))

    print(f"species checked            : {checked}")
    print(f"name != constant          : {len(bad_name)}")
    print(f"dex id mismatch in stats   : {len(bad_dex)}")
    print(f"sprite points elsewhere    : {len(bad_sprite)}")

    for idx, const, name in bad_name[:8]:
        print(f"  NAME  ${idx:02X} {const}: table says {name!r}")
    for idx, const, dex, got in bad_dex[:8]:
        print(f"  DEX   ${idx:02X} {const}: order says dex {dex}, stats entry says {got}")
    for idx, const, b, p, wb, wp in bad_sprite[:12]:
        # Which species does it actually point at?
        who = next((k for k, v in S.items()
                    if v == (b, p) and k.endswith("PicFront")), "?")
        print(f"  SPRITE ${idx:02X} {const:<13} -> bank ${b:02X}:{p:04X} ({who}), "
              f"want ${wb:02X}:{wp:04X}")

    ok = not (bad_name or bad_dex or bad_sprite)
    print("\nPASS: every species' name and sprite refer to the same Pokemon"
          if ok else "\nFAIL: name/sprite mismatch")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
