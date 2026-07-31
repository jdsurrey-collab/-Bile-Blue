"""
Isolate the reported Oak's Lab bug: a dead Eevee coming back after the first
rival battle.

Two independent halves, tested separately so the failure is unambiguous:
  A. Does RemoveFaintedPlayerMon actually write DEAD_BIT into the PARTY struct?
  B. Does HealParty correctly refuse to revive a mon that has DEAD_BIT set?

OaksLabRivalEndBattleScript calls `predef HealParty` unconditionally after that
battle (vanilla behaviour -- you cannot black out in the lab, see the
`cp OAKS_LAB / ret z` special case in HandlePlayerBlackOut), so if either half
is broken the starter comes back to life there and only there.
"""
import os
import sys
from pyboy import PyBoy

ROM = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "pokered.gbc")

REMOVE_FAINTED = (0x0f, 0x4741)
HEAL_PARTY = (0x03, 0x76de)

wPlayerMonNumber = 0xcc2f
wBattleMonHP = 0xd015
wBattleMonStatus = 0xd018
wPartyCount = 0xd163
wPartySpecies = 0xd164
wPartyMon1Species = 0xd16b
wPartyMon1HP = 0xd16c
wPartyMon1Status = 0xd16f
wPartyMon1MaxHP = 0xd18d
hLoadedROMBank = 0xffb8
TRAMPOLINE = 0xdec0

DEAD_BIT = 7
EEVEE = 0x66  # internal index; exact value irrelevant to the test


def call(pyboy, bank, addr, timeout=400000):
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
            return True
    return False


def setup_party(pyboy, status=0, hp=0):
    """One-mon party, mon 0, at `hp` HP with `status`."""
    pyboy.memory[wPartyCount] = 1
    pyboy.memory[wPartySpecies] = EEVEE
    pyboy.memory[wPartySpecies + 1] = 0xFF  # list terminator
    pyboy.memory[wPartyMon1Species] = EEVEE
    pyboy.memory[wPartyMon1HP] = hp >> 8
    pyboy.memory[wPartyMon1HP + 1] = hp & 0xFF
    pyboy.memory[wPartyMon1Status] = status
    pyboy.memory[wPartyMon1MaxHP] = 0
    pyboy.memory[wPartyMon1MaxHP + 1] = 20
    pyboy.memory[wPlayerMonNumber] = 0


results = []


def check(desc, got, want):
    ok = got == want
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {desc}\n      got {got}, want {want}")


pyboy = PyBoy(ROM, window="null")
for _ in range(600):
    pyboy.tick()
assert pyboy.register_file.SP > 0xC000, "boot crashed"

# --- A. does fainting actually mark the PARTY mon dead? ---------------------
setup_party(pyboy, status=0, hp=0)
pyboy.memory[wBattleMonHP] = 0
pyboy.memory[wBattleMonHP + 1] = 0
pyboy.memory[wBattleMonStatus] = 0
# NOTE: the return value of call() is intentionally ignored for these two.
# RemoveFaintedPlayerMon runs faint animation/sound code and HealParty is
# normally reached via predef; neither returns cleanly to a hand-pushed
# trampoline in a synthetic (non-battle) state, so they "time out" even though
# the memory writes under test have already happened. Assert on the memory,
# which is the actual contract, not on the return.
call(pyboy, *REMOVE_FAINTED)
party_status = pyboy.memory[wPartyMon1Status]
check("party mon 0 has DEAD_BIT set after fainting",
      bool(party_status & (1 << DEAD_BIT)), True)

# --- B. does HealParty refuse to revive a dead mon? ------------------------
setup_party(pyboy, status=1 << DEAD_BIT, hp=0)
call(pyboy, *HEAL_PARTY)
hp = (pyboy.memory[wPartyMon1HP] << 8) | pyboy.memory[wPartyMon1HP + 1]
status = pyboy.memory[wPartyMon1Status]
check("dead mon still has 0 HP after HealParty", hp, 0)
check("dead mon still has DEAD_BIT after HealParty",
      bool(status & (1 << DEAD_BIT)), True)

# --- C. control: a merely-fainted (not dead) mon SHOULD be healed -----------
setup_party(pyboy, status=0, hp=0)
call(pyboy, *HEAL_PARTY)
hp = (pyboy.memory[wPartyMon1HP] << 8) | pyboy.memory[wPartyMon1HP + 1]
check("control: non-dead 0-HP mon IS restored to max HP", hp, 20)

pyboy.stop(save=False)
print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
