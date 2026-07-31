# Cultist Dream Sequence

**Status:** ✅ Done (and the single most heavily-debugged feature in the project so far — 4 separate freeze/bug rounds)

## Summary
Before the player takes a real step on day one, they dream of a cultist figure who asks 3 short branching questions. The answers determine which single evolution stone (Fire/Water/Thunder) they wake up having committed to — in effect, their Eevee's one possible evolution path for that save. This replaced an earlier, simpler version that just handed over all 3 stones for free with no choice involved. See [[Eevee-Only Starter]] for the starter context this replaces the free-stones part of.

## Key files
- `scripts/RedsHouse2F.asm` — trigger point (`RedsHouse2FDefaultScript`), the `text_asm` wrapper blocks for intro/3 questions/outro
- `text/RedsHouse2F.asm` — the actual dialogue content
- `engine/movie/cultist_dream.asm` — `PlayCultistDream`, `AskCultistQuestion`, `TallyCultistAnswer`, `DetermineCultistStone`
- `data/maps/objects/RedsHouse2F.asm` — `SPRITE_CHANNELER` object event (the cultist NPC)
- `data/maps/toggleable_objects.asm` / `constants/toggle_constants.asm` — `TOGGLE_REDSHOUSE2F_CULTIST` (hides/reveals the cultist sprite around the scene)
- `constants/event_constants.asm` — `EVENT_HAD_CULTIST_DREAM` (one-time gate flag)
- `constants/menu_constants.asm` — `CULTIST_Q1/Q2/Q3_MENU_TEMPLATE`
- `data/text_boxes.asm` — matching `text_box_text` rows
- `ram/wram.asm` — `wCultistVotes` (3-counter tally), `wCultistLastAnswer`, `wCultistAnswer`, `wTextBoxID`
- `data/items/marts.asm` — `CeladonMart4FClerkText`, had all 3 stones removed from its `script_mart` list

## How it works
- **Trigger**: `RedsHouse2FDefaultScript` — the very first script that runs the first time the player has a real overworld position on a fresh save (`MainMenu → StartNewGame → OakSpeech → naming → PrepareForSpecialWarp(REDS_HOUSE_2F) → EnterMap → OverworldLoop`). Gated by the `EVENT_HAD_CULTIST_DREAM` event flag (not the script's own scratch state, which resets every map re-entry).
- **The cultist** is a normal, tiny overworld sprite (`SPRITE_CHANNELER`) standing in the room, hidden by default and revealed/hidden with `predef ShowObject`/`HideObject` around the scene — not a full-screen portrait cutscene.
- **The 3 questions** each pop an answer-select menu (`AskCultistQuestion`, a hand-rolled variant of `DoBuySellQuitMenu`'s pattern). Only `PAD_A` is watched — no B-button cancel; the dream doesn't let you walk away without answering.
- **Scoring**: answer index 0/1/2 always means Fire/Water/Thunder regardless of each question's wording, tallied into `wCultistVotes`. With exactly 3 votes cast, either one answer has an outright majority (2 or 3), or it's a 1-1-1 three-way split — in which case the 3rd question's own answer is the tie-break ("your final answer seals it").
- **Closing the loophole**: this is meant to be a real permanent commitment, not flavor. `CeladonMart4FClerkText` (Celadon Dept. Store 4F) was the *only* other legitimate source of any of the 3 stones anywhere in the ROM — all 3 were removed from its item list (Leaf Stone/Poké Doll untouched, since Leaf Stone is unrelated to Eevee).

## Bugs hit & fixes (in order — this is the project's richest bug-pattern case study)

### 1. Full-screen portrait cutscene froze with a corrupted screen
First attempt reused `OakSpeech`'s cutscene toolkit (`GBFadeOutToBlack`/`ClearScreen`/`predef DisplayPicCenteredOrUpperRight`) to show a full-screen `ChannelerPic`. Built and ran, but froze immediately — that whole pattern has **no precedent for being invoked from a normal map script**; it's exclusive to special pre-title/intro contexts outside the standard per-frame overworld script dispatch.
**Fix:** switched to the NPC-sprite-in-room model (matching `BillsHouse.asm`'s NPC-walks-in-and-talks pattern) — the map stays on screen the whole time, sprites/dialogue overlay on top.
**Lesson:** a clean build is not evidence a cutscene-style scene will actually run correctly from a normal script context.

### 2. Scene still hung with the NPC-sprite model
The sprite appeared, but no textbox/input — `PlayCultistDream` was calling `PrintText` directly (a plain default-script function via `farcall`) instead of `DisplayTextID`. `PrintText` only draws a box and hands off to `TextCommandProcessor`; `DisplayTextID` additionally runs `farcall DisplayTextIDInit` first and proper wait/close steps after. Every other auto-triggered narration script in the codebase calls `DisplayTextID` for exactly this reason.
**Fix:** gave the cultist's intro/3 questions/outro their own `TEXT_REDSHOUSE2F_CULTIST_*` IDs and `text_asm` wrapper blocks; `PlayCultistDream` now just sequences `ldh [hTextID], a` / `call DisplayTextID`.
**Lesson:** matching one proven precedent isn't enough if a *different* piece of the same scene still deviates from what every other working example does.

### 3. Menu freeze — register clobber in `AskCultistQuestion` itself
`AskCultistQuestion`'s first draft called `SaveScreenTilesToBuffer1` *before* `ld [wTextBoxID], a` — but `SaveScreenTilesToBuffer1` clobbers `a` internally, so the menu-template-ID argument was gone by the time it was supposed to be stored, and `DisplayTextBoxID` landed almost anywhere depending on the garbage left behind (manifested inconsistently — garbled-but-selectable one run, hard freeze the next).
**Fix:** store `a` into `wTextBoxID` *first*, then call `SaveScreenTilesToBuffer1`.
**Lesson:** any time a fix introduces a new call before an existing `ld [wSomething], a`, check whether that new call clobbers `a` first.

### 4. The real bug behind "menu at top-left, no text, then freeze" — `farcall` clobbers `a` on *both* sides
Diagnosed by emulating the built ROM in PyBoy (see [[PyBoy Testing Techniques]]) and reading registers live at a hook on `AskCultistQuestion`'s entry: `a` held `$01` (the callee's own bank number) instead of the intended menu template ID `$16`. `Bankswitch` reloads `a` with the destination bank right before jumping in, *and* reloads it with the source bank right after the callee's `ret` — a value placed in `a` on either side of a `farcall` is gone by the time it matters.
**Fix:** routed both directions through WRAM instead of registers — the caller sets `wTextBoxID` itself before the `farcall`; `AskCultistQuestion` writes its answer to a new `wCultistAnswer` byte as its last action instead of returning it in `a`.
**Standing lesson (see [[Lessons Learned - Bug Patterns]]):** never pass or return a value through `a` across *any* `farcall` — always WRAM/HRAM, checked in both directions. This bug class recurred a third time later in [[Smarter Trainer AI]].

## Other notable details
- **Dialogue length budget was missed on the first pass** — several lines exceeded the ~18-char/line box budget (e.g. "and I shall whisper" at 20 chars) and wrapped mid-word, caught from a screenshot showing "whisp"/"r" split. All dialogue was rewritten and re-counted line-by-line, including the `<PLAYER>` token's worst-case ~7-char width.
- Move/effect ID constant comments are hex-without-`$`-prefix — irrelevant to this feature's gameplay logic, but relevant if writing tests against it (see [[Lessons Learned - Bug Patterns]]).

## Related
- [[Eevee-Only Starter]] — the feature this scene's stone-choice replaces the "free stones" part of
- [[PyBoy Testing Techniques]] — how bug #4 was actually root-caused (couldn't have been found by reading source alone)
- [[Lessons Learned - Bug Patterns]] — the `farcall` register-clobber class, in full, across all 3 of its occurrences
