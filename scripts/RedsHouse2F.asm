RedsHouse2F_Script:
	call EnableAutoTextBoxDrawing
	ld hl, RedsHouse2F_ScriptPointers
	ld a, [wRedsHouse2FCurScript]
	jp CallFunctionInTable

RedsHouse2F_ScriptPointers:
	def_script_pointers
	dw_const RedsHouse2FDefaultScript, SCRIPT_REDSHOUSE2F_DEFAULT
	dw_const RedsHouse2FNoopScript,    SCRIPT_REDSHOUSE2F_NOOP

RedsHouse2FDefaultScript:
; Pokémon Purple: before the player ever takes a real step, they dream of
; the cultist who decides their Eevee's fate. wRedsHouse2FCurScript resets
; every time this map is re-entered, so this needs a real persistent event
; flag rather than relying on the script-state flip below to keep it from
; replaying on later visits.
	CheckEvent EVENT_HAD_CULTIST_DREAM
	jr nz, .alreadyDreamed
	farcall PlayCultistDream
.alreadyDreamed
	xor a
	ldh [hJoyHeld], a
	ld a, PLAYER_DIR_UP
	ld [wPlayerMovingDirection], a
	ld a, SCRIPT_REDSHOUSE2F_NOOP
	ld [wRedsHouse2FCurScript], a
	ret

RedsHouse2FNoopScript:
	ret

RedsHouse2F_TextPointers:
	def_text_pointers
	dw_const RedsHouse2FCultistText,          TEXT_REDSHOUSE2F_CULTIST
	dw_const RedsHouse2FCultistIntroText,     TEXT_REDSHOUSE2F_CULTIST_INTRO
	dw_const RedsHouse2FCultistQuestion1Text, TEXT_REDSHOUSE2F_CULTIST_Q1
	dw_const RedsHouse2FCultistQuestion2Text, TEXT_REDSHOUSE2F_CULTIST_Q2
	dw_const RedsHouse2FCultistQuestion3Text, TEXT_REDSHOUSE2F_CULTIST_Q3
	dw_const RedsHouse2FCultistOutroText,     TEXT_REDSHOUSE2F_CULTIST_OUTRO

; Pokémon Purple: PlayCultistDream (engine/movie/cultist_dream.asm) sets
; hTextID to these directly from a different bank/object file, so unlike a
; normal map's TEXT_ constants (only ever used from within their own
; scripts/<Map>.asm) these need to be real linker-visible symbols.
EXPORT TEXT_REDSHOUSE2F_CULTIST_INTRO
EXPORT TEXT_REDSHOUSE2F_CULTIST_Q1
EXPORT TEXT_REDSHOUSE2F_CULTIST_Q2
EXPORT TEXT_REDSHOUSE2F_CULTIST_Q3
EXPORT TEXT_REDSHOUSE2F_CULTIST_OUTRO

; Pokémon Purple: the cultist is only ever on-screen during the scripted
; dream sequence (engine/movie/cultist_dream.asm), which has full control
; the whole time, so this normal walk-up-and-press-A text is unreachable in
; practice -- it exists so the object_event has a valid text pointer.
RedsHouse2FCultistText:
	text_far _RedsHouse2FCultistText
	text_end

; Pokémon Purple: PlayCultistDream drives the dream through DisplayTextID
; (ldh [hTextID]/call DisplayTextID) rather than calling PrintText directly --
; PrintText alone skips DisplayTextIDInit's setup and hangs with nothing drawn
; when called from a plain default-script context (confirmed by every other
; auto-triggered narration sequence in this disassembly, e.g. OaksLab.asm's
; OaksLabOakChooseMonSpeechScript, using DisplayTextID exclusively; PrintText
; is only ever called from *within* a text_asm block that DisplayTextID has
; already dispatched into). These text_asm wrappers are that entry point.
RedsHouse2FCultistIntroText:
	text_asm
	ld hl, .Text
	call PrintText
	jp TextScriptEnd
.Text:
	text_far _RedsHouse2FCultistIntroText
	text_end

RedsHouse2FCultistQuestion1Text:
	text_asm
	ld hl, .Text
	call PrintText
	ld a, CULTIST_Q1_MENU_TEMPLATE
	farcall AskCultistQuestion
	ld [wCultistLastAnswer], a
	farcall TallyCultistAnswer
	jp TextScriptEnd
.Text:
	text_far _RedsHouse2FCultistQuestion1Text
	text_end

RedsHouse2FCultistQuestion2Text:
	text_asm
	ld hl, .Text
	call PrintText
	ld a, CULTIST_Q2_MENU_TEMPLATE
	farcall AskCultistQuestion
	ld [wCultistLastAnswer], a
	farcall TallyCultistAnswer
	jp TextScriptEnd
.Text:
	text_far _RedsHouse2FCultistQuestion2Text
	text_end

RedsHouse2FCultistQuestion3Text:
	text_asm
	ld hl, .Text
	call PrintText
	ld a, CULTIST_Q3_MENU_TEMPLATE
	farcall AskCultistQuestion
	ld [wCultistLastAnswer], a
	farcall TallyCultistAnswer
	jp TextScriptEnd
.Text:
	text_far _RedsHouse2FCultistQuestion3Text
	text_end

RedsHouse2FCultistOutroText:
	text_asm
	ld hl, .Text
	call PrintText
	jp TextScriptEnd
.Text:
	text_far _RedsHouse2FCultistOutroText
	text_end
