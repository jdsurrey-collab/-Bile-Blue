	db DEX_LEDYBA ; pokedex id

	db  40,  20,  30,  55,  60
	;   hp  atk  def  spd  spc

	db BUG, FLYING ; type
	db 255 ; catch rate
	db 54 ; base exp

	INCBIN "gfx/pokemon/front/ledyba.pic", 0, 1 ; sprite dimensions
	dw LedybaPicFront, LedybaPicBack

	db TACKLE, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, MEGA_DRAIN, SWORDS_DANCE, CUT, FLY, SKY_ATTACK, WHIRLWIND, RAZOR_WIND
	; end

	db 0 ; padding
