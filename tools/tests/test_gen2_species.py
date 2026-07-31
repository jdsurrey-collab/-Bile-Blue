"""Verify the Gen 2 species import round-trips in the real ROM.

A clean build only proves the tables are the right LENGTH. It cannot prove they
agree with each other -- a species landing at the wrong offset in one of the
five internal-index tables is a silent wrong-species bug, not a build error.
"""
import sys
from pyboy import PyBoy

import os
ROM = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pokered.gbc")
GETNAME, INDEXTOPOKEDEX_BANK, INDEXTOPOKEDEX = 0x378d, 0x10, 0x5660
WNAMELISTINDEX, WNAMELISTTYPE, WPREDEFBANK = 0xd0b5, 0xd0b6, 0xd0b7
WNAMEBUFFER, WPOKEDEXNUM, HLOADEDROMBANK = 0xcd6d, 0xd11e, 0xffb8
TRAMPOLINE = 0xdec0  # wCultistVotes
MONSTER_NAME, BANK_MONSTERNAMES = 1, 0x07


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
check("name @ $20 (gap-filled)", get_name(pyboy, 0x20), "CHIKORITA")
check("name @ $45 (gap-filled)", get_name(pyboy, 0x45), "SENTRET")
check("name @ $9D (gap-filled)", get_name(pyboy, 0x9D), "MAREEP")
check("name @ $EB (appended)", get_name(pyboy, 0xEB), "BLISSEY")
check("name @ $F3 (appended, max index)", get_name(pyboy, 0xF3), "CELEBI")

# --- names: existing species must be UNCHANGED (no table drift)
check("name @ $99 BULBASAUR unchanged", get_name(pyboy, 0x99), "BULBASAUR")
check("name @ $15 MEW unchanged", get_name(pyboy, 0x15), "MEW")

# --- index -> dex round-trip: proves names.asm and dex_order.asm agree
check("IndexToPokedex($20) CHIKORITA", index_to_dex(pyboy, 0x20), 152)
check("IndexToPokedex($45) SENTRET", index_to_dex(pyboy, 0x45), 161)
check("IndexToPokedex($F3) CELEBI", index_to_dex(pyboy, 0xF3), 240)
check("IndexToPokedex($99) BULBASAUR", index_to_dex(pyboy, 0x99), 1)
check("IndexToPokedex($15) MEW", index_to_dex(pyboy, 0x15), 151)

pyboy.stop(save=False)
print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
