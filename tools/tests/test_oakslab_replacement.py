"""
Verify OaksLabAnyMonAlive, the gate on Oak's replacement-Eevee gift.

Context: the Oak's Lab rival battle is the ONLY fight in the game you can lose
without blacking out (HandlePlayerBlackOut has a vanilla `cp OAKS_LAB / ret z`).
With permadeath that produced a hard softlock -- the dead starter is not revived
by HealParty, the player never blacks out of the battle, and then blacks out the
instant they take a step, forever. OaksLabGiveReplacementIfWiped hands over the
last ball on the table instead, gated on this check.

Ordering that matters: `predef HealParty` runs BEFORE this gate, so a merely
fainted mon is already back on its feet and correctly does NOT trigger the gift;
only a genuinely dead one still reads as wiped.
"""
import os
import sys
from pyboy import PyBoy

ROM = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "pokered.gbc")

ALIVE = (0x07, 0x500a)  # OaksLabAnyMonAlive
wPartyCount = 0xd163
wPartySpecies = 0xd164
wPartyMon1HP = 0xd16c
wPartyMon1Status = 0xd16f
PARTYMON_STRUCT_LENGTH = 44
TRAMPOLINE = 0xdec0
hLoadedROMBank = 0xffb8
ZF = 0x80
DEAD = 0x80

pyboy = PyBoy(ROM, window="null")
for _ in range(600):
    pyboy.tick()
assert pyboy.register_file.SP > 0xC000, "boot crashed"


def call(bank, addr, timeout=200000):
    pyboy.memory[TRAMPOLINE] = 0x18
    pyboy.memory[TRAMPOLINE + 1] = 0xFE
    pyboy.memory[0x2000] = bank
    pyboy.memory[hLoadedROMBank] = bank
    sp = (pyboy.register_file.SP - 2) & 0xFFFF
    pyboy.memory[sp] = TRAMPOLINE & 0xFF
    pyboy.memory[sp + 1] = (TRAMPOLINE >> 8) & 0xFF
    pyboy.register_file.SP = sp
    pyboy.register_file.PC = addr
    for _ in range(timeout):
        pyboy.tick()
        if pyboy.register_file.PC == TRAMPOLINE:
            return pyboy.register_file.F
    return None


def party(mons):
    pyboy.memory[wPartyCount] = len(mons)
    for i, (hp, st) in enumerate(mons):
        pyboy.memory[wPartySpecies + i] = 0x66
        base = wPartyMon1HP + i * PARTYMON_STRUCT_LENGTH
        pyboy.memory[base] = hp >> 8
        pyboy.memory[base + 1] = hp & 0xFF
        pyboy.memory[wPartyMon1Status + i * PARTYMON_STRUCT_LENGTH] = st
    pyboy.memory[wPartySpecies + len(mons)] = 0xFF


results = []


def check(desc, got, want):
    ok = got == want
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'} {desc}: got {got}, want {want}")


def wiped():
    return bool(call(*ALIVE) & ZF)


party([(0, DEAD)])
check("lone DEAD mon -> reports wiped (gift fires)", wiped(), True)

party([(20, 0)])
check("lone healthy mon -> not wiped (no gift)", wiped(), False)

# Guards against the gift re-firing once the player already has a replacement.
party([(0, DEAD), (18, 0)])
check("dead + healthy -> not wiped", wiped(), False)

party([(0, DEAD), (0, DEAD)])
check("all dead -> reports wiped", wiped(), True)

# Cannot occur in practice (HealParty revives this case first), but the
# behaviour is safe either way.
party([(0, 0)])
check("fainted-but-not-dead -> wiped", wiped(), True)

pyboy.stop(save=False)
print(f"{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
