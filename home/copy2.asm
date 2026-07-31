FarCopyData2::
; Identical to FarCopyData, but uses hROMBankTemp
; as temp space instead of wBuffer.
	ldh [hROMBankTemp], a
	ldh a, [hLoadedROMBank]
	push af
	ldh a, [hROMBankTemp]
	ldh [hLoadedROMBank], a
	ld [rROMB], a
	call CopyData
	pop af
	ldh [hLoadedROMBank], a
	ld [rROMB], a
	ret

FarCopyData3::
; Copy bc bytes from a:de to hl.
	ldh [hROMBankTemp], a
	ldh a, [hLoadedROMBank]
	push af
	ldh a, [hROMBankTemp]
	ldh [hLoadedROMBank], a
	ld [rROMB], a
	push hl
	push de
	push de
	ld d, h
	ld e, l
	pop hl
	call CopyData
	pop de
	pop hl
	pop af
	ldh [hLoadedROMBank], a
	ld [rROMB], a
	ret

FarCopyDataDouble::
; Expand bc bytes of 1bpp image data
; from a:hl to 2bpp data at de.
	ldh [hROMBankTemp], a
	ldh a, [hLoadedROMBank]
	push af
	ldh a, [hROMBankTemp]
	ldh [hLoadedROMBank], a
	ld [rROMB], a
.loop
	ld a, [hli]
	ld [de], a
	inc de
	ld [de], a
	inc de
	dec bc
	ld a, c
	or b
	jr nz, .loop
	pop af
	ldh [hLoadedROMBank], a
	ld [rROMB], a
	ret

CopyVideoData::
; Wait for the next VBlank, then copy c 2bpp
; tiles from b:de to hl, 8 tiles at a time.
; This takes c/8 frames.

	ldh a, [hAutoBGTransferEnabled]
	push af
	xor a ; disable auto-transfer while copying
	ldh [hAutoBGTransferEnabled], a

	ldh a, [hLoadedROMBank]
	ldh [hROMBankTemp], a

	ld a, b
	ldh [hLoadedROMBank], a
	ld [rROMB], a

	ld a, e
	ldh [hVBlankCopySource], a
	ld a, d
	ldh [hVBlankCopySource + 1], a

	ld a, l
	ldh [hVBlankCopyDest], a
	ld a, h
	ldh [hVBlankCopyDest + 1], a

.loop
	ld a, c
	cp 8
	jr nc, .keepgoing

.done
	ldh [hVBlankCopySize], a
	call DelayFrame
	ldh a, [hROMBankTemp]
	ldh [hLoadedROMBank], a
	ld [rROMB], a
	pop af
	ldh [hAutoBGTransferEnabled], a
	ret

.keepgoing
	ld a, 8
	ldh [hVBlankCopySize], a
	call DelayFrame
	ld a, c
	sub 8
	ld c, a
	jr .loop

CopyVideoDataDouble::
; Wait for the next VBlank, then copy c 1bpp
; tiles from b:de to hl, 8 tiles at a time.
; This takes c/8 frames.
	ldh a, [hAutoBGTransferEnabled]
	push af
	xor a ; disable auto-transfer while copying
	ldh [hAutoBGTransferEnabled], a
	ldh a, [hLoadedROMBank]
	ldh [hROMBankTemp], a

	ld a, b
	ldh [hLoadedROMBank], a
	ld [rROMB], a

	ld a, e
	ldh [hVBlankCopyDoubleSource], a
	ld a, d
	ldh [hVBlankCopyDoubleSource + 1], a

	ld a, l
	ldh [hVBlankCopyDoubleDest], a
	ld a, h
	ldh [hVBlankCopyDoubleDest + 1], a

.loop
	ld a, c
	cp 8
	jr nc, .keepgoing

.done
	ldh [hVBlankCopyDoubleSize], a
	call DelayFrame
	ldh a, [hROMBankTemp]
	ldh [hLoadedROMBank], a
	ld [rROMB], a
	pop af
	ldh [hAutoBGTransferEnabled], a
	ret

.keepgoing
	ld a, 8
	ldh [hVBlankCopyDoubleSize], a
	call DelayFrame
	ld a, c
	sub 8
	ld c, a
	jr .loop

ClearScreenArea::
; Clear tilemap area cxb at hl.
	ld a, ' '
	ld de, SCREEN_WIDTH
.loopRows
	push hl
	push bc
.loopTiles
	ld [hli], a
	dec c
	jr nz, .loopTiles
	pop bc
	pop hl
	add hl, de
	dec b
	jr nz, .loopRows
	ret

CopyScreenTileBufferToVRAM::
; Copy wTileMap to the BG Map starting at b * $100.
; This is done in thirds of 6 rows, so it takes 3 frames.

	ld c, SCREEN_HEIGHT / 3

	lb hl, 0, 0
	decoord 0, 6 * 0
	call .setup
	call DelayFrame

	lb hl, SCREEN_HEIGHT / 3, 0
	decoord 0, 6 * 1
	call .setup
	call DelayFrame

	lb hl, 2 * SCREEN_HEIGHT / 3, 0
	decoord 0, 6 * 2
	call .setup
	jp DelayFrame

.setup
	ld a, d
	ldh [hVBlankCopyBGSource+1], a
	call GetRowColAddressBgMap
	ld a, l
	ldh [hVBlankCopyBGDest], a
	ld a, h
	ldh [hVBlankCopyBGDest+1], a
	ld a, c
	ldh [hVBlankCopyBGNumRows], a
	ld a, e
	ldh [hVBlankCopyBGSource], a
	ret

ClearScreen::
; Clear wTileMap, then wait
; for the bg map to update.
	ld bc, SCREEN_AREA
	inc b
	hlcoord 0, 0
	ld a, ' '
.loop
	ld [hli], a
	dec c
	jr nz, .loop
	dec b
	jr nz, .loop
	jp Delay3

; Pokémon Purple: identical to ClearScreen above, except it fills with the
; raw tile index $40 instead of the char literal ' ' (which the project-wide
; charmap, constants/charmap.asm, resolves to tile $7F -- not actually blank
; in gfx/font/font.png, see CLAUDE.md item 9). ClearScreen itself is used
; far too broadly (battle core/animations, party menu, evolution, and
; roughly twenty other unrelated screens) to safely change what it fills
; with globally -- $40 was only ever confirmed blank in the specific VRAM
; state the title/pre-title intro sequence loads (a first attempt that
; changed ClearScreen itself caused "blurry artifacts"/wrong tiles showing
; up in battle and the receive-a-Pokémon screen instead, since $40 resolves
; to whatever graphic those OTHER screens happen to have loaded at that
; address, not blank). Only ever call this from engine/movie/title.asm or
; engine/movie/intro.asm (the only two contexts $40 has actually been
; confirmed blank in) -- like ClearScreen, this function itself lives in the
; Home bank, so a plain `call` to it is safe from any other bank regardless.
TitleClearScreen::
	ld bc, SCREEN_AREA
	inc b
	hlcoord 0, 0
	ld a, $40
.loop
	ld [hli], a
	dec c
	jr nz, .loop
	dec b
	jr nz, .loop
	jp Delay3
