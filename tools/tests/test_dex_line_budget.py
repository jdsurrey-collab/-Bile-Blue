"""
Enforce the Pokedex/dialogue line budget on the gothic dex prose.

The text box is 20 tiles wide but the game does NOT reject overlong lines -- it
wraps mid-word and truncates the remainder, which is invisible until someone
screenshots it (exactly how the cultist dream's overflow was found). The
project-wide budget is ~18 visible characters, matching the longest lines in the
original shipped game.

Also checks coverage: every imported species must have an entry, and there must
be no entries for species that do not exist.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gen2_dex_text import DEX, MAX_LINE
from gen2_import import build_roster

results = []


def fail(msg):
    results.append(msg)


eligible, _, _ = build_roster()
slugs = {s["slug"] for s in eligible}

missing = sorted(slugs - set(DEX))
extra = sorted(set(DEX) - slugs)
for m in missing:
    fail(f"no dex prose for {m}")
for e in extra:
    fail(f"dex prose for unknown species {e}")

overlong = []
for slug, pages in DEX.items():
    if not 1 <= len(pages) <= 2:
        fail(f"{slug}: {len(pages)} pages, expected 1 or 2")
    for pi, page in enumerate(pages):
        if not 1 <= len(page) <= 3:
            fail(f"{slug} page {pi + 1}: {len(page)} lines, expected 1-3")
        for line in page:
            if len(line) > MAX_LINE:
                overlong.append((slug, len(line), line))

for slug, n, line in overlong:
    fail(f"{slug}: {n} chars (max {MAX_LINE}): {line!r}")

total_lines = sum(len(p) for pages in DEX.values() for p in pages)
longest = max((len(l) for pages in DEX.values() for p in pages for l in p),
              default=0)
print(f"species with prose : {len(DEX)}")
print(f"total lines        : {total_lines}")
print(f"longest line       : {longest} (budget {MAX_LINE})")
print(f"overlong lines     : {len(overlong)}")
print(f"missing / extra    : {len(missing)} / {len(extra)}")

if results:
    print()
    for r in results[:25]:
        print("  FAIL " + r)
    print(f"\nFAIL: {len(results)} problem(s)")
    sys.exit(1)
print("\nPASS: every species has prose and every line fits the budget")
