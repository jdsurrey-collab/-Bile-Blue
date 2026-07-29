; A brief full-screen intro scene, shown once before the title screen: the
; gothic castle/graveyard silhouette fades in, then "PURPLE" stamps onto the
; screen one letter at a time (with a thud per letter), before fading back
; out into the normal DisplayTitleScreen sequence.
;
; Unlike the title screen itself, nothing else needs VRAM/wTileMap during
; this scene, so there's no risk of colliding with (for example) the front
; sprite graphics the title screen loads later - see CLAUDE.md for the VRAM
; conflict that bit the title-screen version of this idea.

DEF GOTHIC_STAMP_STARTCOL EQU 4
DEF GOTHIC_STAMP_STARTROW EQU 8
DEF GOTHIC_STAMP_TILE_BASE EQU 144 ; BG tile index of the stamp graphic's first tile (vChars1 tile 16)
DEF GOTHIC_STAMP_WIDTH EQU 11 ; tiles wide

PlayGothicIntro::
	xor a
	ldh [hAutoBGTransferEnabled], a
	call DisableLCD
	call ClearSprites
	xor a
	ldh [hSCX], a
	ldh [hSCY], a
	ld a, SCREEN_HEIGHT_PX ; keep the window off-screen; this scene doesn't use it
	ldh [hWY], a
	ldh [rWY], a

	ldpal a, SHADE_WHITE, SHADE_WHITE, SHADE_WHITE, SHADE_WHITE
	ldh [rBGP], a
	ldh [rOBP0], a
	ldh [rOBP1], a

; castle background tiles: first 128 into vChars2, the remaining 16 into
; the start of vChars1 (144 unique tiles total)
	ld hl, GothicIntroBgGraphics
	ld de, vChars2
	ld bc, 128 tiles
	ld a, BANK(GothicIntroBgGraphics)
	call FarCopyData2
	ld hl, GothicIntroBgGraphics tile 128
	ld de, vChars1
	ld bc, GothicIntroBgGraphicsEnd - GothicIntroBgGraphics - 128 tiles
	ld a, BANK(GothicIntroBgGraphics)
	call FarCopyData2

; "PURPLE" stamp tiles go right after the castle's vChars1 overflow.
; This graphic is 1bpp (black-on-white only), so it needs to be expanded
; to 2bpp on the way in, not straight-copied.
	ld hl, GothicIntroStampGraphics
	ld de, vChars1 tile 16
	ld bc, GothicIntroStampGraphicsEnd - GothicIntroStampGraphics
	ld a, BANK(GothicIntroStampGraphics)
	call FarCopyDataDouble

; stage the castle-only tilemap in WRAM, then expand it into vBGMap0 while
; the LCD is still off (safe to write VRAM directly here)
	ld hl, GothicIntroBgTilemap
	ld de, wTileMap
	ld bc, GothicIntroBgTilemapEnd - GothicIntroBgTilemap
	ld a, BANK(GothicIntroBgTilemap)
	call FarCopyData2
	call ExpandWTileMapToBGMap0

	xor a
	ldh [hAutoBGTransferDest], a
	ld a, HIGH(vBGMap0)
	ldh [hAutoBGTransferDest + 1], a

	call EnableLCD
	call GBFadeInFromWhite
	ld a, 1
	ldh [hAutoBGTransferEnabled], a

	ld c, 100
	call CheckForUserInterruption
	jr c, .skipStamp

	ld b, 0
	ld c, 2
	call StampGothicIntroLetterGroup ; P
	ld b, 2
	ld c, 2
	call StampGothicIntroLetterGroup ; U
	ld b, 4
	ld c, 2
	call StampGothicIntroLetterGroup ; R
	ld b, 6
	ld c, 2
	call StampGothicIntroLetterGroup ; P
	ld b, 8
	ld c, 1
	call StampGothicIntroLetterGroup ; L
	ld b, 9
	ld c, 2
	call StampGothicIntroLetterGroup ; E

	ld c, 100
	call CheckForUserInterruption
.skipStamp
	xor a
	ldh [hAutoBGTransferEnabled], a
	call GBFadeOutToWhite
	call ClearSprites
	xor a
	ldh [hSCX], a
	ret

; Fills the visible 20x18 area of vBGMap0 from wTileMap. Only used for the
; initial castle reveal, while the LCD is disabled - safe to hit VRAM
; directly. (Once the LCD is on, updates go through wTileMap + the
; auto BG transfer mechanism instead, via StampGothicIntroLetterGroup.)
ExpandWTileMapToBGMap0:
	ld hl, wTileMap
	ld de, vBGMap0
	ld b, SCREEN_HEIGHT
.rowLoop
	ld c, SCREEN_WIDTH
.colLoop
	ld a, [hli]
	ld [de], a
	inc de
	dec c
	jr nz, .colLoop
	ld a, e
	add TILEMAP_WIDTH - SCREEN_WIDTH
	ld e, a
	jr nc, .noCarry
	inc d
.noCarry
	dec b
	jr nz, .rowLoop
	ret

; Writes one letter's worth of tile-columns into wTileMap (all 3 stamp rows),
; waits for the auto BG transfer to carry it to VRAM, then thuds and pauses.
; b = starting column (0-10) within the stamp graphic/on screen group
; c = width in tile-columns of this letter (1 or 2)
StampGothicIntroLetterGroup:
	push bc
	hlcoord GOTHIC_STAMP_STARTCOL, GOTHIC_STAMP_STARTROW
	ld a, l
	add b
	ld l, a
	jr nc, .noCarry0
	inc h
.noCarry0
	ld a, GOTHIC_STAMP_TILE_BASE + 0 * GOTHIC_STAMP_WIDTH
	add b
	ld d, a
	ld e, c
.loop0
	ld a, d
	ld [hli], a
	inc d
	dec e
	jr nz, .loop0
	pop bc

	push bc
	hlcoord GOTHIC_STAMP_STARTCOL, GOTHIC_STAMP_STARTROW + 1
	ld a, l
	add b
	ld l, a
	jr nc, .noCarry1
	inc h
.noCarry1
	ld a, GOTHIC_STAMP_TILE_BASE + 1 * GOTHIC_STAMP_WIDTH
	add b
	ld d, a
	ld e, c
.loop1
	ld a, d
	ld [hli], a
	inc d
	dec e
	jr nz, .loop1
	pop bc

	push bc
	hlcoord GOTHIC_STAMP_STARTCOL, GOTHIC_STAMP_STARTROW + 2
	ld a, l
	add b
	ld l, a
	jr nc, .noCarry2
	inc h
.noCarry2
	ld a, GOTHIC_STAMP_TILE_BASE + 2 * GOTHIC_STAMP_WIDTH
	add b
	ld d, a
	ld e, c
.loop2
	ld a, d
	ld [hli], a
	inc d
	dec e
	jr nz, .loop2
	pop bc

	call Delay3
	ld a, SFX_INTRO_CRASH
	call PlaySound
	ld c, 20
	jp DelayFrames

GothicIntroBgGraphics: INCBIN "gfx/title/gothic_intro_bg.2bpp"
GothicIntroBgGraphicsEnd:

GothicIntroBgTilemap: INCBIN "gfx/title/gothic_intro_bg.tilemap"
GothicIntroBgTilemapEnd:

GothicIntroStampGraphics: INCBIN "gfx/title/gothic_intro_stamp.1bpp"
GothicIntroStampGraphicsEnd:
