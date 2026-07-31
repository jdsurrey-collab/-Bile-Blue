"""Verify the Gen 2 species import round-trips in the real ROM.

A clean build only proves the tables are the right LENGTH. It cannot prove they
agree with each other -- a species landing at the wrong offset in one of the
five internal-index tables is a silent wrong-species bug, not a build error.
"""
import sys
from pyboy import PyBoy

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROM = os.path.join(ROOT, "pokered.gbc")


def _syms():
    out = {}
    for line in open(os.path.join(ROOT, "pokered.sym"), encoding="utf-8"):
        m = re.match(r"([0-9a-f]{2}):([0-9a-f]{4}) (\S+)", line.strip())
        if m:
            out[m.group(3)] = (int(m.group(1), 16), int(m.group(2), 16))
    return out


def _species_index():
    """{CONST: internal index}, walked exactly as rgbasm does.

    Note the -1 default: `const_def` with no argument starts at 0 and NO_MON
    takes index $00. Getting this wrong by one is precisely the bug this suite
    exists to catch -- see tools/tests/test_species_alignment.py.
    """
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


_S = _syms()
IDX = _species_index()
GETNAME = _S["GetName"][1]
INDEXTOPOKEDEX_BANK, INDEXTOPOKEDEX = _S["IndexToPokedex"]
WNAMELISTINDEX = _S["wNameListIndex"][1]
WNAMELISTTYPE = _S["wNameListType"][1]
WPREDEFBANK = _S["wPredefBank"][1]
WNAMEBUFFER = _S["wNameBuffer"][1]
WPOKEDEXNUM = _S["wPokedexNum"][1]
HLOADEDROMBANK = _S["hLoadedROMBank"][1]
TRAMPOLINE = _S["wCultistVotes"][1]
MONSTER_NAME = 1
BANK_MONSTERNAMES = _S["MonsterNames"][0]


def decode(raw):
    out = []
    for b in raw:
        if b == 0x50:
            break
        if 0x80 <= b <= 0x99:
            out.append(chr(ord("A") + b - 0x80))
        elif 0xA0 <= b <= 0xB9:
            out.append(chr(ord("a") + b - 0xA0))
        elif 0xF6 <= b <= 0xFF:
            out.append(chr(ord("0") + b - 0xF6))
        elif b == 0x7F:
            out.append(" ")
        elif b == 0xE3:
            out.append("-")
        else:
            out.append(f"<{b:02x}>")
    return "".join(out)


def call(pyboy, addr, bank=None, timeout=300000):
    pyboy.memory[TRAMPOLINE] = 0x18
    pyboy.memory[TRAMPOLINE + 1] = 0xFE
    if bank is not None:
        pyboy.memory[0x2000] = bank
        pyboy.memory[HLOADEDROMBANK] = bank
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


def get_name(pyboy, index):
    pyboy.memory[WNAMELISTINDEX] = index
    pyboy.memory[WNAMELISTTYPE] = MONSTER_NAME
    pyboy.memory[WPREDEFBANK] = BANK_MONSTERNAMES
    for i in range(16):
        pyboy.memory[WNAMEBUFFER + i] = 0
    if not call(pyboy, GETNAME):
        return None
    return decode(bytes(pyboy.memory[WNAMEBUFFER:WNAMEBUFFER + 16]))


def index_to_dex(pyboy, index):
    pyboy.memory[WPOKEDEXNUM] = index
    if not call(pyboy, INDEXTOPOKEDEX, bank=INDEXTOPOKEDEX_BANK):
        return None
    return pyboy.memory[WPOKEDEXNUM]


results = []


def check(desc, got, want):
    ok = got == want
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {desc}: got {got!r}, want {want!r}")


pyboy = PyBoy(ROM, window="null")
for _ in range(600):
    pyboy.tick()
assert pyboy.register_file.SP > 0xC000, "boot crashed"

# --- names: new species must resolve, at gap-filled AND appended slots
check("name @ $20 (gap-filled)", get_name(pyboy, IDX["CHIKORITA"]), "CHIKORITA")
check("name @ $45 (gap-filled)", get_name(pyboy, IDX["SENTRET"]), "SENTRET")
check("name @ $9D (gap-filled)", get_name(pyboy, IDX["MAREEP"]), "MAREEP")
check("name @ $EB (appended)", get_name(pyboy, IDX["BLISSEY"]), "BLISSEY")
check("name @ $F3 (appended, max index)", get_name(pyboy, IDX["CELEBI"]), "CELEBI")

# --- names: existing species must be UNCHANGED (no table drift)
check("name @ $99 BULBASAUR unchanged", get_name(pyboy, IDX["BULBASAUR"]), "BULBASAUR")
check("name @ $15 MEW unchanged", get_name(pyboy, IDX["MEW"]), "MEW")

# --- index -> dex round-trip: proves names.asm and dex_order.asm agree
check("IndexToPokedex($20) CHIKORITA", index_to_dex(pyboy, IDX["CHIKORITA"]), 152)
check("IndexToPokedex($45) SENTRET", index_to_dex(pyboy, IDX["SENTRET"]), 161)
check("IndexToPokedex($F3) CELEBI", index_to_dex(pyboy, IDX["CELEBI"]), 240)
check("IndexToPokedex($99) BULBASAUR", index_to_dex(pyboy, IDX["BULBASAUR"]), 1)
check("IndexToPokedex($15) MEW", index_to_dex(pyboy, IDX["MEW"]), 151)

pyboy.stop(save=False)
print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
