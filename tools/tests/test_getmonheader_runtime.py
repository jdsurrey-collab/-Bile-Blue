"""
RUNTIME check of the name/sprite chain: actually call GetMonHeader in the
emulator and confirm the sprite pointer it loads belongs to the species whose
name the game would print.

The static test (test_name_sprite_match.py) proves the TABLES agree. This proves
the CODE that walks them agrees too -- IndexToPokedex, the BaseStats indexing in
GetMonHeader, and the special cases it applies before the table lookup. A bug in
any of those produces exactly the reported symptom (right name, wrong avatar)
while every table is individually perfect.
"""
import os
import re
import sys
from pyboy import PyBoy

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROM = os.path.join(ROOT, "pokered.gbc")

OFF_PICFRONT = 11  # within wMonHeader / a base_stats entry


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
            out[m.group(1)] = val
    return out


def label_for(const):
    return "".join(p.capitalize() for p in const.split("_")) + "PicFront"


S = syms()
IDX = species_constants()
GETMONHEADER = S["GetMonHeader"][1]
wCurSpecies = S["wCurSpecies"][1]
wMonHeader = S["wMonHeader"][1]
hLoadedROMBank = S["hLoadedROMBank"][1]
TRAMPOLINE = S["wCultistVotes"][1]

pyboy = PyBoy(ROM, window="null")
for _ in range(600):
    pyboy.tick()
assert pyboy.register_file.SP > 0xC000, "boot crashed"


def call(addr, timeout=300000):
    pyboy.memory[TRAMPOLINE] = 0x18
    pyboy.memory[TRAMPOLINE + 1] = 0xFE
    sp = (pyboy.register_file.SP - 2) & 0xFFFF
    pyboy.memory[sp] = TRAMPOLINE & 0xFF
    pyboy.memory[sp + 1] = (TRAMPOLINE >> 8) & 0xFF
    pyboy.register_file.SP = sp
    pyboy.register_file.PC = addr
    for _ in range(timeout):
        pyboy.tick()
        if pyboy.register_file.PC == TRAMPOLINE:
            return True
    return False


def header_picfront(index):
    pyboy.memory[wCurSpecies] = index
    if not call(GETMONHEADER):
        return None
    lo = pyboy.memory[wMonHeader + OFF_PICFRONT]
    hi = pyboy.memory[wMonHeader + OFF_PICFRONT + 1]
    return lo | (hi << 8)


# A spread across every risky region: gap-filled, appended, boundaries, and
# vanilla species on both sides of the old Mew hole (dex 151).
TARGETS = ["CHIKORITA", "BAYLEEF", "CYNDAQUIL", "TOTODILE", "SENTRET", "MAREEP",
           "MISDREAVUS", "HERACROSS", "BLISSEY", "RAIKOU", "LUGIA", "CELEBI",
           "BULBASAUR", "CHARMANDER", "MEWTWO", "DRAGONITE", "PIKACHU", "EEVEE",
           "SNORLAX", "ARTICUNO"]

results = []
for const in TARGETS:
    if const not in IDX:
        continue
    lbl = label_for(const)
    if lbl not in S:
        continue
    want = S[lbl][1]
    got = header_picfront(IDX[const])
    ok = got == want
    results.append(ok)
    if not ok:
        who = next((k[:-8] for k, v in S.items()
                    if k.endswith("PicFront") and v[1] == got), "?")
        print(f"FAIL {const:<12} idx ${IDX[const]:02X}: header points at "
              f"${got:04X} ({who}), want ${want:04X}")
    else:
        print(f"PASS {const:<12} idx ${IDX[const]:02X} -> ${got:04X}")

pyboy.stop(save=False)
print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
