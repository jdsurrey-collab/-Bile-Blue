; Pokémon Purple: the player dreams of a cultist before ever waking up on
; day one. Their answers to 3 questions determine which single evolution
; stone they receive -- a real, permanent commitment for the save (the
; other two are no longer purchasable, see Celadon Mart 4F). Called once
; from RedsHouse2FDefaultScript (scripts/RedsHouse2F.asm), gated on
; EVENT_HAD_CULTIST_DREAM so it never replays on later visits.
;
; Built from only the most battle-tested primitives in this engine
; (ShowObject/HideObject, DisplayTextID) rather than either of two patterns
; that turned out not to work from a normal map script:
;   - the OakSpeech-style full-screen-portrait cutscene the first version of
;     this used (GBFadeOutToBlack/ClearScreen/predef DisplayPicCenteredOr
;     UpperRight) -- no precedent anywhere in this codebase for being invoked
;     outside special pre-title/intro contexts, and it froze with a
;     corrupted screen.
;   - calling PrintText directly from PlayCultistDream itself -- PrintText
;     skips DisplayTextIDInit's setup (only DisplayTextID performs it), so it
;     silently hung with nothing ever drawn to screen and input locked up.
; Every other auto-triggered narration sequence in this disassembly (e.g.
; OaksLab.asm's OaksLabOakChooseMonSpeechScript) drives text via
; ldh [hTextID]/call DisplayTextID; PrintText is only ever called from
; *within* a text_asm block that DisplayTextID has already dispatched into
; (see the RedsHouse2FCultist*Text wrappers in scripts/RedsHouse2F.asm).
; This file now just orchestrates those DisplayTextID calls plus the
; NPC reveal, matching BillsHouse.asm's own NPC-walks-in-and-talks model for
; the reveal itself.
PlayCultistDream::
	ld a, TOGGLE_REDSHOUSE2F_CULTIST
	ld [wToggleableObjectIndex], a
	predef ShowObject
	call UpdateSprites

	xor a
	ld [wCultistVotes], a
	ld [wCultistVotes + 1], a
	ld [wCultistVotes + 2], a

	ld a, TEXT_REDSHOUSE2F_CULTIST_INTRO
	ldh [hTextID], a
	call DisplayTextID

	ld a, TEXT_REDSHOUSE2F_CULTIST_Q1
	ldh [hTextID], a
	call DisplayTextID

	ld a, TEXT_REDSHOUSE2F_CULTIST_Q2
	ldh [hTextID], a
	call DisplayTextID

	ld a, TEXT_REDSHOUSE2F_CULTIST_Q3
	ldh [hTextID], a
	call DisplayTextID

	call DetermineCultistStone ; OUTPUT: a = item id
	ld [wCurItem], a
	ld a, 1
	ld [wItemQuantity], a
	ld hl, wNumBagItems
	call AddItemToInventory

	ld a, TEXT_REDSHOUSE2F_CULTIST_OUTRO
	ldh [hTextID], a
	call DisplayTextID

	ld a, TOGGLE_REDSHOUSE2F_CULTIST
	ld [wToggleableObjectIndex], a
	predef HideObject
	call UpdateSprites

	SetEvent EVENT_HAD_CULTIST_DREAM
	ret

; INPUT: [wTextBoxID] already set by the caller (CULTIST_Q1/Q2/Q3_MENU_
;        TEMPLATE) -- NOT passed through `a`, see note below
; OUTPUT: [wCultistAnswer] = chosen answer index -- always 0 = Fire,
;         1 = Water, 2 = Thunder, regardless of each question's wording --
;         NOT returned through `a`, see note below
; Called via farcall from the RedsHouse2FCultist*Question*Text text_asm
; blocks (scripts/RedsHouse2F.asm), themselves dispatched by DisplayTextID --
; NOT called directly from PlayCultistDream, since the question prompt text
; and this menu both need to run from within an active text-script context.
; No B-button cancel (only PAD_A is watched): the dream doesn't let you walk
; away without answering.
;
; farcall's Bankswitch (home/bankswitch.asm) clobbers `a` on BOTH sides of
; the call -- it loads the destination bank into `a` right before jumping
; in, and reloads the source bank into `a` right after the callee returns --
; so a value handed to this function via `a` (the menu template ID) never
; actually survived to see its first instruction, and a value returned via
; `a` (the chosen answer) never survived the trip back to the caller either.
; This shipped once as `ld a, CULTIST_Q1_MENU_TEMPLATE` / `farcall
; AskCultistQuestion` and was confirmed, by hooking the ROM and reading
; registers directly, to actually enter this function with a = the callee's
; bank number (1) -- not 22 -- which is why DisplayTextBoxID drew a blank
; MESSAGE_BOX instead of the intended menu (it matched wTextBoxID's stale
; leftover value of 1 in TextBoxCoordTable instead). wTextBoxID/wCultistAnswer
; now carry the value both ways instead, sidestepping the farcall boundary
; entirely. (Earlier notes elsewhere in this project only flagged homecall's
; return-side `pop af` as clobbering `a` -- plain farcall turns out to do it
; on both the call *and* return side, which is easy to miss since Bankswitch
; still looks "self-contained" at a glance.)
;
; Saves/restores the screen around the popup (matching YesNoChoice, the
; proven pattern for a menu that pops up over an already-drawn dialogue box
; mid-scene) rather than DoBuySellQuitMenu's bare draw-and-leave-it, which is
; only ever reached via a full mart-screen redraw afterward and was never
; actually a safe precedent for 3 popups drawn back-to-back over a single
; unchanging room scene -- without this, each question's box tiles were never
; erased before the next question's prompt printed elsewhere on screen.
AskCultistQuestion::
	call SaveScreenTilesToBuffer1
	call DisplayTextBoxID
	ld a, PAD_A
	ld [wMenuWatchedKeys], a
	ld a, 2
	ld [wMaxMenuItem], a
	ld a, 1
	ld [wTopMenuItemY], a
	ld a, 1
	ld [wTopMenuItemX], a
	xor a
	ld [wCurrentMenuItem], a
	ld [wLastMenuItem], a
	ld [wMenuWatchMovingOutOfBounds], a
	call HandleMenuInput
	call PlaceUnfilledArrowMenuCursor
	call LoadScreenTilesFromBuffer1
	ld a, [wCurrentMenuItem]
	ld [wCultistAnswer], a
	ret

; INPUT: [wCultistAnswer] = answer index (0-2) -- see the farcall note above
; for why this isn't just taken as an `a` argument
TallyCultistAnswer::
	push hl
	push bc
	ld a, [wCultistAnswer]
	ld hl, wCultistVotes
	ld c, a
	ld b, 0
	add hl, bc
	inc [hl]
	pop bc
	pop hl
	ret

; OUTPUT: a = item id of the winning stone
; With exactly 3 votes cast total, either one answer has a majority (2 or
; 3 votes -- the other two can't also reach 2), or it's a 3-way 1-1-1 split,
; in which case wCultistAnswer (the 3rd question's own answer) decides.
DetermineCultistStone::
	ld hl, wCultistVotes
	ld a, [hli]
	cp 2
	jr nc, .fire
	ld a, [hli]
	cp 2
	jr nc, .water
	ld a, [hl]
	cp 2
	jr nc, .thunder
	ld a, [wCultistAnswer] ; 1-1-1 split: the final answer seals it
	jr .gotIndex
.fire
	xor a
	jr .gotIndex
.water
	ld a, 1
	jr .gotIndex
.thunder
	ld a, 2
.gotIndex
	ld hl, CultistStoneItems
	ld c, a
	ld b, 0
	add hl, bc
	ld a, [hl]
	ret

CultistStoneItems:
	db FIRE_STONE, WATER_STONE, THUNDER_STONE
