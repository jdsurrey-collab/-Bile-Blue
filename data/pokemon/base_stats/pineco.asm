	db DEX_PINECO ; pokedex id

	db  50,  65,  90,  15,  35
	;   hp  atk  def  spd  spc

	db BUG, BUG ; type
	db 190 ; catch rate
	db 60 ; base exp

	INCBIN "gfx/pokemon/front/pineco.pic", 0, 1 ; sprite dimensions
	dw PinecoPicFront, PinecoPicBack

	db TACKLE, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, MEGA_DRAIN, SWORDS_DANCE, CUT
	; end

	db 0 ; padding
