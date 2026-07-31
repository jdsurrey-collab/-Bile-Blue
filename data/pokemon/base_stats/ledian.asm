	db DEX_LEDIAN ; pokedex id

	db  55,  35,  50,  85,  82
	;   hp  atk  def  spd  spc

	db BUG, FLYING ; type
	db 90 ; catch rate
	db 134 ; base exp

	INCBIN "gfx/pokemon/front/ledian.pic", 0, 1 ; sprite dimensions
	dw LedianPicFront, LedianPicBack

	db TACKLE, SUPERSONIC, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, MEGA_DRAIN, SWORDS_DANCE, CUT, FLY, SKY_ATTACK, WHIRLWIND, RAZOR_WIND
	; end

	db 0 ; padding
