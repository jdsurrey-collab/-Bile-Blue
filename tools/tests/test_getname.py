"""
Verify the GetName TM/HM-redirect fix in home/names2.asm.

The fix: the `cp HM01 / jp nc, GetMachineName` redirect at the top of GetName
used to fire for EVERY name list type. It is now skipped when
wNameListType == MONSTER_NAME, so species indexes can exceed HM01 ($C4).

This must be true WITHOUT regressing item names (which genuinely need the
redirect to render TMs/HMs in the bag), move names, or trainer names.
"""
import sys
from pyboy import PyBoy

import os
ROM = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pokered.gbc")

# from pokered.sym
GETNAME        = 0x378d   # bank 00 (home)
WNAMELISTINDEX = 0xd0b5
WNAMELISTTYPE  = 0xd0b6
WPREDEFBANK    = 0xd0b7
WNAMEBUFFER    = 0xcd6d
HLOADEDROMBANK = 0xffb8
TRAMPOLINE     = 0xdee2   # wCultistVotes, scratch

MONSTER_NAME, MOVE_NAME, ITEM_NAME, TRAINER_NAME = 1, 2, 4, 7
BANK_MONSTERNAMES, BANK_ITEMNAMES = 0x07, 0x01
BANK_MOVENAMES, BANK_TRAINERNAMES = 0x2c, 0x0e
HM01 = 0xC4

CHARMAP_BASE = {0x80: "A"}  # filled below


def decode(raw):
    """Decode pokered text encoding to ASCII (enough for names)."""
    out = []
    for b in raw:
        if b == 0x50:  # terminator '@'
            break
        if 0x80 <= b <= 0x99:
            out.append(chr(ord("A") + b - 0x80))
        elif 0xA0 <= b <= 0xB9:
            out.append(chr(ord("a") + b - 0xA0))
        elif 0xF6 <= b <= 0xFF:
            out.append(chr(ord("0") + b - 0xF6))
        elif b == 0x7F:
            out.append(" ")
        else:
            out.append(f"<{b:02x}>")
    return "".join(out)


def boot(pyboy, frames=600):
    # Do NOT poke 0xFF50 here. That poke is only correct when jumping straight
    # to a function without booting; doing it *while* booting unmaps the
    # Nintendo boot ROM mid-execution and crashes the CPU into cartridge ROM
    # (observed: PC stuck at $0038, SP wandering into SRAM). Booting normally
    # lets the boot ROM unmap itself, which leaves real cartridge code at
    # 0x0000-0x00FF anyway plus a sane stack and bank.
    for _ in range(frames):
        pyboy.tick()
    assert pyboy.register_file.SP > 0xC000, (
        f"stack not in WRAM after boot (SP=${pyboy.register_file.SP:04x}); "
        "game likely crashed before the test could run")


def call_getname(pyboy, list_type, index, predef_bank, timeout=200000):
    # trampoline: infinite `jr -2`
    pyboy.memory[TRAMPOLINE] = 0x18
    pyboy.memory[TRAMPOLINE + 1] = 0xFE

    pyboy.memory[WNAMELISTINDEX] = index
    pyboy.memory[WNAMELISTTYPE] = list_type
    pyboy.memory[WPREDEFBANK] = predef_bank
    # clear the output buffer so a stale read can't produce a false pass
    for i in range(16):
        pyboy.memory[WNAMEBUFFER + i] = 0x00

    sp = (pyboy.register_file.SP - 2) & 0xFFFF
    pyboy.memory[sp] = TRAMPOLINE & 0xFF
    pyboy.memory[sp + 1] = (TRAMPOLINE >> 8) & 0xFF
    pyboy.register_file.SP = sp
    pyboy.register_file.PC = GETNAME

    for _ in range(timeout):
        pyboy.tick()
        if pyboy.register_file.PC == TRAMPOLINE:
            raw = bytes(pyboy.memory[WNAMEBUFFER:WNAMEBUFFER + 16])
            return decode(raw)
    return None  # timed out


def main():
    results = []

    def check(desc, got, predicate, expectation):
        ok = predicate(got)
        results.append((ok, desc, got, expectation))
        print(f"{'PASS' if ok else 'FAIL'}  {desc}\n"
              f"      got={got!r}  expected: {expectation}")

    pyboy = PyBoy(ROM, window="null")
    boot(pyboy)

    # --- 1. THE FIX: a species index at/above HM01 must NOT become a TM name.
    # There is no real species at 0xC4 yet, so the name read is past the end of
    # MonsterNames -- that's fine. What matters is that it went down the
    # GetMonName path, not GetMachineName (which would yield "TM.."/"HM..").
    got = call_getname(pyboy, MONSTER_NAME, HM01, BANK_MONSTERNAMES)
    check(f"MONSTER_NAME @ ${HM01:02X} (>= HM01) does not return a TM/HM name",
          got,
          lambda g: g is not None and not g.startswith(("TM", "HM")),
          "any non-TM/HM string (proves GetMonName path taken)")

    got = call_getname(pyboy, MONSTER_NAME, 0xF0, BANK_MONSTERNAMES)
    check("MONSTER_NAME @ $F0 (well above HM01) does not return a TM/HM name",
          got,
          lambda g: g is not None and not g.startswith(("TM", "HM")),
          "any non-TM/HM string")

    # --- 2. NO REGRESSION: species below HM01 still resolve correctly.
    # Internal index $99 == BULBASAUR in Gen 1's index order.
    got = call_getname(pyboy, MONSTER_NAME, 0x99, BANK_MONSTERNAMES)
    check("MONSTER_NAME @ $99 still resolves to BULBASAUR",
          got, lambda g: g == "BULBASAUR", "BULBASAUR")

    got = call_getname(pyboy, MONSTER_NAME, 0x15, BANK_MONSTERNAMES)
    check("MONSTER_NAME @ $15 still resolves to MEW",
          got, lambda g: g == "MEW", "MEW")

    # --- 3. NO REGRESSION: item IDs at/above HM01 must STILL become TM/HM names.
    # This is the path home/list_menu.asm depends on to show TMs in the bag.
    got = call_getname(pyboy, ITEM_NAME, HM01, BANK_ITEMNAMES)
    check(f"ITEM_NAME @ ${HM01:02X} (HM01) still returns an HM name",
          got, lambda g: g is not None and g.startswith("HM"), "HM01")

    got = call_getname(pyboy, ITEM_NAME, 0xC9, BANK_ITEMNAMES)
    check("ITEM_NAME @ $C9 (TM01) still returns a TM name",
          got, lambda g: g is not None and g.startswith("TM"), "TM01")

    # --- 4. NO REGRESSION: normal item below HM01 still resolves by name list.
    got = call_getname(pyboy, ITEM_NAME, 0x04, BANK_ITEMNAMES)
    check("ITEM_NAME @ $04 still resolves to POKe BALL",
          got, lambda g: g is not None and "BALL" in g, "a POKE BALL-ish name")

    # --- 5. NO REGRESSION: move names and trainer names unaffected.
    got = call_getname(pyboy, MOVE_NAME, 0x01, BANK_MOVENAMES)
    check("MOVE_NAME @ $01 still resolves to POUND",
          got, lambda g: g == "POUND", "POUND")

    got = call_getname(pyboy, TRAINER_NAME, 0x01, BANK_TRAINERNAMES)
    check("TRAINER_NAME @ $01 still resolves to a real trainer class name",
          got, lambda g: g is not None and len(g) > 2
          and not g.startswith(("TM", "HM")), "a real trainer name")

    pyboy.stop(save=False)

    print("\n" + "=" * 60)
    failed = [r for r in results if not r[0]]
    print(f"{len(results) - len(failed)}/{len(results)} passed")
    if failed:
        for _, desc, got, exp in failed:
            print(f"  FAILED: {desc} (got {got!r}, expected {exp})")
        sys.exit(1)
    print("All GetName checks passed.")


if __name__ == "__main__":
    main()
