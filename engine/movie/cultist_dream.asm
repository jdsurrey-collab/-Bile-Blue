; Pokémon Purple: the player dreams of a cultist before ever waking up on
; day one. Their answers to 3 questions determine which single evolution
; stone they receive -- a real, permanent commitment for the save (the
; other two are no longer purchasable, see Celadon Mart 4F). Called once
; from RedsHouse2FDefaultScript (scripts/RedsHouse2F.asm), gated on
; EVENT_HAD_CULTIST_DREAM so it never replays on later visits.
PlayCultistDream::
	call GBFadeOutToBlack
	call ClearScreen
	ld de, ChannelerPic
	lb bc, BANK(ChannelerPic), 0
	predef DisplayPicCenteredOrUpperRight
	call GBFadeInFromBlack
	ld hl, CultistIntroText
	call PrintText

; Pokémon Purple: clear the portrait away before the Q&A -- the answer-menu
; box (top-left, same coords DoBuySellQuitMenu uses) would otherwise overlap
; a centered portrait, since that only ever shares the screen with plain
; dialogue (which stays confined to the bottom message box).
	call GBFadeOutToBlack
	call ClearScreen
	call GBFadeInFromBlack

	xor a
	ld [wCultistVotes], a
	ld [wCultistVotes + 1], a
	ld [wCultistVotes + 2], a

	ld hl, CultistQuestion1Text
	call PrintText
	ld a, CULTIST_Q1_MENU_TEMPLATE
	call AskCultistQuestion
	call TallyCultistAnswer

	ld hl, CultistQuestion2Text
	call PrintText
	ld a, CULTIST_Q2_MENU_TEMPLATE
	call AskCultistQuestion
	call TallyCultistAnswer

	ld hl, CultistQuestion3Text
	call PrintText
	ld a, CULTIST_Q3_MENU_TEMPLATE
	call AskCultistQuestion
	ld b, a ; the final answer, kept as the tie-break vote
	call TallyCultistAnswer

	call DetermineCultistStone ; INPUT: b; OUTPUT: a = item id
	ld [wCurItem], a
	ld a, 1
	ld [wItemQuantity], a
	ld hl, wNumBagItems
	call AddItemToInventory

	ld hl, CultistOutroText
	call PrintText

	SetEvent EVENT_HAD_CULTIST_DREAM

	call GBFadeOutToWhite
	call ClearScreen
	call GBFadeInFromWhite
	ret

; INPUT: a = menu template ID (CULTIST_Q1/Q2/Q3_MENU_TEMPLATE)
; OUTPUT: a = chosen answer index -- always 0 = Fire, 1 = Water, 2 = Thunder,
;             regardless of each question's actual wording
; No B-button cancel (only PAD_A is watched): the dream doesn't let you walk
; away without answering.
AskCultistQuestion:
	ld [wTextBoxID], a
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
	ld a, [wCurrentMenuItem]
	ret

; INPUT: a = answer index (0-2)
TallyCultistAnswer:
	push hl
	push bc
	ld hl, wCultistVotes
	ld c, a
	ld b, 0
	add hl, bc
	inc [hl]
	pop bc
	pop hl
	ret

; INPUT: b = the 3rd question's own answer index (tie-break)
; OUTPUT: a = item id of the winning stone
; With exactly 3 votes cast total, either one answer has a majority (2 or
; 3 votes -- the other two can't also reach 2), or it's a 3-way 1-1-1 split,
; in which case the final question's own answer decides.
DetermineCultistStone:
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
	ld a, b ; 1-1-1 split: the final answer seals it
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

CultistIntroText:
	text "???: Hush, <PLAYER>."
	line "Thou dost not wake."

	para "The Order has kept"
	line "watch o'er thy sleep."

	para "Speak truly now, and"
	line "thy nature shall be"
	cont "sealed this night."
	done

CultistQuestion1Text:
	text "When the world"
	line "wrongs you, what"
	cont "stirs in your breast?"
	done

CultistQuestion2Text:
	text "When hope is lost,"
	line "what carries you"
	cont "onward still?"
	done

CultistQuestion3Text:
	text "Last: what shall"
	line "your familiar"
	cont "become, in the end?"
	done

CultistOutroText:
	text "???: It is done."
	line "Thy path is set,"
	cont "though thou dost not"
	cont "yet recall it."

	para "Wake, <PLAYER>."
	done
