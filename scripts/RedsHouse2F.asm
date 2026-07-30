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

	text_end ; unused
