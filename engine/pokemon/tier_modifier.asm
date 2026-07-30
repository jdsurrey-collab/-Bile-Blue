; Pokémon Purple: modifies a base stat value by the current mon's tier.
; Called from CalcStat (home/move_mon.asm) via homecall, which clobbers a as
; part of its bank-switch dance, so input/output round-trip through
; hStatCalcBase instead of a register.
; INPUT: hStatCalcBase = base stat value (0-255), hStatCalcTier = tier (1-10)
; OUTPUT: hStatCalcBase = tier-modified base stat value, clamped to 0-255
; Doesn't derive the tier from hl/struct position because CalcStat's hl
; argument doesn't always point at a struct with a MON_TIER byte at a
; predictable offset (e.g. GetEnemyMonStat's scratch buffer, or
; LoadEnemyMonData's battle_struct-layout wEnemyMon) -- see the callers of
; CalcStat/CalcStats for how hStatCalcTier gets set instead.
ApplyTierModifier::
	push bc
	push de
	push hl
	ldh a, [hStatCalcBase]
	ld c, a ; c = base stat value
	ldh a, [hStatCalcTier]
	ld d, 0 ; d = 0: add the modifier, d = 1: subtract it
	cp BASE_TIER
	jr z, .noChange
	jr c, .belowBase
	sub BASE_TIER ; a = tier - BASE_TIER (positive step count)
	jr .haveSteps
.belowBase
	ld d, 1
	ld b, a
	ld a, BASE_TIER
	sub b         ; a = BASE_TIER - tier (positive step count)
.haveSteps
	; percent = steps * 5 (5% per tier step away from BASE_TIER)
	ld e, a
	sla a
	sla a
	add e
	ld b, a ; b = percent
	xor a
	ldh [hMultiplicand], a
	ldh [hMultiplicand + 1], a
	ld a, c
	ldh [hMultiplicand + 2], a
	ld a, b
	ldh [hMultiplier], a
	call Multiply ; hProduct = base * percent (fits in 16 bits)
	ld a, 100
	ldh [hDivisor], a
	ld b, 4
	call Divide   ; hQuotient = (base * percent) / 100
	ldh a, [hQuotient + 3]
	ld e, a ; e = delta
	ld a, d
	and a
	jr nz, .subtract
	ld a, c
	add e
	jr nc, .done
	ld a, 255 ; clamp
	jr .done
.subtract
	ld a, c
	sub e     ; delta is always < base here, so this can't borrow
	jr .done
.noChange
	ld a, c
.done
	ldh [hStatCalcBase], a
	pop hl
	pop de
	pop bc
	ret
