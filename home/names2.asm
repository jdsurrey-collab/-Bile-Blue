NamePointers::
; entries correspond to *_NAME constants
	dw MonsterNames
	dw MoveNames
	dw UnusedBadgeNames
	dw ItemNames
	dw wPartyMonOT ; player's OT names list
	dw wEnemyMonOT ; enemy's OT names list
	dw TrainerNames

GetName::
; arguments:
; [wNameListIndex] = which name
; [wNameListType] = which list
; [wPredefBank] = bank of list
;
; returns pointer to name in de
	ld a, [wNameListIndex]
	ld [wNamedObjectIndex], a

	; TM/HM names are stored separately from item names, so an item ID at or
	; above HM01 has to be rendered as "TM##"/"HM##" rather than looked up in
	; a name list. Vanilla applied that redirect to EVERY name list instead of
	; just items (pret flags this as a bug) -- which effectively capped
	; Pokémon/move/trainer IDs at HM01 ($C4), since any ID at or above it
	; printed a TM/HM name instead of its real one.
	;
	; Pokémon Purple needs species indexes above that ceiling (the Gen 2
	; species import; see CLAUDE.md), so the redirect is now skipped for
	; MONSTER_NAME. Deliberately scoped to skipping MONSTER_NAME rather than
	; the arguably "more correct" restriction to ITEM_NAME only: every other
	; list type then keeps the exact vanilla code path byte for byte, so this
	; cannot regress item/move/trainer/OT naming anywhere -- including the
	; item list menu (home/list_menu.asm), which relies on this redirect to
	; show TMs/HMs in the bag. Moves and trainers still assert below, since
	; neither has any reason to cross HM01.
	ASSERT NUM_ATTACKS < HM01, \
		"A bug in GetName will get TM/HM names for moves above ${x:HM01}."
	ASSERT NUM_TRAINERS < HM01, \
		"A bug in GetName will get TM/HM names for trainers above ${x:HM01}."
	ld a, [wNameListType]
	cp MONSTER_NAME
	jr z, .notMachineName
	ld a, [wNameListIndex]
	cp HM01
	jp nc, GetMachineName
.notMachineName

	ldh a, [hLoadedROMBank]
	push af
	push hl
	push bc
	push de
	ld a, [wNameListType]
	dec a
	jr nz, .otherEntries
	; 1 = MONSTER_NAME
	call GetMonName
	ld hl, NAME_LENGTH
	add hl, de
	ld e, l
	ld d, h
	jr .gotPtr
.otherEntries
	; 2-7 = other names
	ld a, [wPredefBank]
	ldh [hLoadedROMBank], a
	ld [rROMB], a
	ld a, [wNameListType]
	dec a
	add a
	ld d, 0
	ld e, a
	jr nc, .skip
	inc d
.skip
	ld hl, NamePointers
	add hl, de
	ld a, [hli]
	ldh [hSwapTemp + 1], a
	ld a, [hl]
	ldh [hSwapTemp], a
	ldh a, [hSwapTemp]
	ld h, a
	ldh a, [hSwapTemp + 1]
	ld l, a
	ld a, [wNameListIndex]
	ld b, a ; wanted entry
	ld c, 0 ; entry counter
.nextName
	ld d, h
	ld e, l
.nextChar
	ld a, [hli]
	cp '@'
	jr nz, .nextChar
	inc c
	ld a, b
	cp c
	jr nz, .nextName
	ld h, d
	ld l, e
	ld de, wNameBuffer
	ld bc, NAME_BUFFER_LENGTH
	call CopyData
.gotPtr
	ld a, e
	ld [wUnusedNamePointer], a
	ld a, d
	ld [wUnusedNamePointer + 1], a
	pop de
	pop bc
	pop hl
	pop af
	ldh [hLoadedROMBank], a
	ld [rROMB], a
	ret
