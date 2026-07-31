	db DEX_HERACROSS ; pokedex id

	db  80, 125,  75,  85,  67
	;   hp  atk  def  spd  spc

	db BUG, FIGHTING ; type
	db 45 ; catch rate
	db 200 ; base exp

	INCBIN "gfx/pokemon/front/heracross.pic", 0, 1 ; sprite dimensions
	dw HeracrossPicFront, HeracrossPicBack

	db TACKLE, LEER, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, MEGA_DRAIN, SWORDS_DANCE, CUT, SUBMISSION, SEISMIC_TOSS, COUNTER, MEGA_PUNCH, MEGA_KICK, STRENGTH
	; end

	db 0 ; padding
