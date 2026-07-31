# Permadeath Mode

**Status:** ✅ Done

## Summary
A Pokémon that faints in battle is **permanently marked dead**, not just "fainted." Dead Pokémon can never be revived by any normal means, and the party screen shows `RIP` instead of `FNT` for them. This is the mechanical backbone the rest of the project's stakes-raising features (hidden tiers, smarter AI) lean on — without real permanent loss, neither of those would matter as much.

## Key files
- `constants/battle_constants.asm` — `DEAD_BIT` (bit 7 of `MON_STATUS`, a bit vanilla status ailments never use)
- `home/pokemon.asm` — party screen display logic (`RIP` vs `FNT`)
- Pokémon Center / Revive / Max Revive item-use code — all check the flag before allowing any heal-from-faint action

## How it works
- `MON_STATUS`'s bit 7 is otherwise unused by vanilla Gen 1 (real status ailments — poison, burn, paralysis, etc. — only ever use the lower bits). Repurposing it as `DEAD_BIT` costs nothing structurally.
- When a Pokémon faints in battle, that bit gets set permanently on its struct.
- Every revival path (Pokémon Center heal-all, the `Revive`/`Max Revive` items) checks the bit first and refuses to act on a dead Pokémon.
- The party screen (`home/pokemon.asm`) prints `RIP` instead of `FNT` for any Pokémon with the bit set, so death reads as permanent at a glance, not just "currently fainted."

## The one escape hatch: Oak's Lab

**Status:** ✅ Fixed in `Roms/v0.28`

The rival battle in Oak's Lab is the **only** fight you can lose without blacking out — `HandlePlayerBlackOut` carries a vanilla special case:

```asm
ld a, [wCurMap]
cp OAKS_LAB
ret z   ; starter battle in oak's lab: don't black out
```

Vanilla gets away with this because it just heals your 0-HP starter afterward. Permadeath breaks the assumption: the starter is *dead*, `HealParty` correctly refuses to revive it, the battle doesn't black you out — and then the game blacks out the moment you take a step, forever, with no living Pokémon to recover with.

Reported from play as *"if our Eevee dies it respawns"*; the real behaviour was the blackout loop. (Static analysis had predicted exactly this, and the player's repro — *"it made me black out as soon as I took a step"* — confirmed it.)

**Fix:** Oak hands over the last ball on the table. `OaksLabGiveReplacementIfWiped` (`scripts/OaksLab.asm`), called from `OaksLabRivalEndBattleScript` right after its existing `predef HealParty`.

Three things about it are deliberate:
- **The ordering is load-bearing.** `HealParty` runs *first*, so a merely fainted mon is already back up and does **not** trigger the gift — only a genuinely dead one still reads as wiped.
- **The dead Eevee stays in the party.** Permadeath means you carry your dead; the replacement is a second Pokémon, not a resurrection. This also prevents the gate re-firing, since the party then holds a living mon.
- **Uses `DisplayTextID`, not `PrintText`** — it's a plain script function, the same rule that caused the [[Cultist Dream Sequence]] freeze.

Verified by `tools/tests/test_oakslab_replacement.py` (5/5) and `test_permadeath.py` (4/4).

### Follow-up bug: the text had no box

Reported from play — Oak's line appeared as bare text on the map, with input feeling unresponsive.

`OaksLab_Script` sets `BIT_NO_AUTO_TEXT_BOX` in `wAutoTextBoxDrawingControl` on **every** dispatch, and `DisplayTextIDInit` skips `TextBoxBorder` entirely when that bit is set. A plain `text_far` therefore renders with no bubble. The unresponsiveness followed from that: `DisplayTextID` still waits for A (plus a vanilla 30-frame joypad poll timer), but with no box and no prompt arrow there was nothing telling you to press it.

This map has **two** working patterns, and the new text used neither:

| Pattern | Used by | How the box appears |
|---|---|---|
| `text_asm` + `PrintText` | 18 texts | `PrintText` draws its own `MESSAGE_BOX` |
| Script calls `EnableAutoTextBoxDrawing` first | 8 texts | Restores the auto-drawn border |

Fixed by converting to `text_asm` + `PrintText` (pattern 1) — self-contained, so it doesn't depend on the script's flag state. Verified structurally: the entry now compiles to first-byte `$08` (`TX_ASM`), matching the working boxed texts.

**Note this is the mirror image of the [[Cultist Dream Sequence]] rule, not a contradiction.** `PrintText` is wrong from a *plain script function* (it skips `DisplayTextID`'s init/close); it is correct *inside a `text_asm` block* that `DisplayTextID` has already dispatched into. Which one applies depends entirely on where you are in the call chain.

## Deliberately unchanged
- **The player's own blackout/whiteout behavior is untouched.** Whiting out (all Pokémon fainted) still just returns the player to the last-visited Pokémon Center exactly like vanilla Red/Blue — there's no separate "game over" state layered on top. Permadeath is per-Pokémon, not a run-ending condition.

## Related
- [[Hidden Tier System]] — the other stakes-raising system; tiers make individual Pokémon feel less interchangeable, which matters more once death is permanent
- [[Smarter Trainer AI]] — built explicitly *because* permadeath raises the real cost of every trainer battle, and vanilla AI barely reacted to the battle state at all
- [[Roadmap & Ideas]] — the discussed-but-unbuilt graveyard/memorial system at the Pokémon Center would be the natural next extension of this system
