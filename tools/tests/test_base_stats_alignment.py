"""
Verify BaseStats is contiguous BY DEX NUMBER.

GetMonHeader reads `BaseStats + (dex - 1) * BASE_DATA_SIZE`, so any hole in the
table shifts every entry above it. Vanilla had exactly such a hole: Mew (dex
151) is stored separately and special-cased before the lookup, which was
harmless only because nothing existed above dex 151. Adding dex 152+ made every
imported species read the NEXT species' entry -- wrong stats and, because
`dw XPicFront, XPicBack` lives in this struct, a wrong sprite pointer too.

This checks the dex axis. test_species_alignment.py checks the internal-index
axis; the two numbering systems fail independently, so both are needed.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def syms():
    out = {}
    for line in open(os.path.join(ROOT, "pokered.sym"), encoding="utf-8"):
        m = re.match(r"([0-9a-f]{2}):([0-9a-f]{4}) (\S+)", line.strip())
        if m:
            out[m.group(3)] = (int(m.group(1), 16), int(m.group(2), 16))
    return out


def dex_constants():
    """{DEX_NAME: dex number} from constants/pokedex_constants.asm."""
    out, val = {}, 0
    for line in open(os.path.join(ROOT, "constants/pokedex_constants.asm"),
                     encoding="utf-8"):
        s = line.strip()
        if s.startswith("const_def"):
            m = re.match(r"const_def\s+(\d+)", s)
            val = (int(m.group(1)) - 1) if m else 0
            continue
        m = re.match(r"const\s+(DEX_[A-Z_0-9]+)", s)
        if m:
            val += 1
            out[m.group(1)] = val
    return out


def main():
    S = syms()
    rom = open(os.path.join(ROOT, "pokered.gbc"), "rb").read()
    bank, addr = S["BaseStats"]
    base = bank * 0x4000 + (addr - 0x4000)

    # BASE_DATA_SIZE, read from the struct definition rather than hardcoded.
    src = open(os.path.join(ROOT, "constants/pokemon_data_constants.asm"),
               encoding="utf-8").read()
    # The first byte of each entry is the dex id, which is what we verify.
    dexc = dex_constants()
    n = max(dexc.values())

    # Derive entry size by finding the stride that makes byte 0 of each entry
    # equal its own dex number for the first 20 species. This avoids duplicating
    # the rsset arithmetic and fails loudly if the struct ever changes size.
    stride = None
    for cand in range(20, 64):
        if all(rom[base + i * cand] == i + 1 for i in range(20)):
            stride = cand
            break
    if stride is None:
        print("FAIL: could not determine BASE_DATA_SIZE from the ROM")
        sys.exit(1)

    bad = []
    for dex in range(1, n + 1):
        got = rom[base + (dex - 1) * stride]
        if got != dex:
            bad.append((dex, got))

    print(f"BASE_DATA_SIZE (derived): {stride}")
    print(f"dex entries checked     : {n}")
    print(f"misaligned entries      : {len(bad)}")
    for dex, got in bad[:12]:
        print(f"  dex {dex}: entry says dex id {got}")

    ok = not bad
    print("\nPASS: BaseStats is contiguous by dex number"
          if ok else "\nFAIL: BaseStats is misaligned by dex number")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
