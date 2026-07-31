	db DEX_CROBAT ; pokedex id

	db  85,  90,  80, 130,  75
	;   hp  atk  def  spd  spc

	db POISON, FLYING ; type
	db 90 ; catch rate
	db 204 ; base exp

	INCBIN "gfx/pokemon/front/crobat.pic", 0, 1 ; sprite dimensions
	dw CrobatPicFront, CrobatPicBack

	db SCREECH, LEECH_LIFE, SUPERSONIC, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, FLY, SKY_ATTACK, WHIRLWIND, RAZOR_WIND, MEGA_DRAIN, EXPLOSION, SELFDESTRUCT, DOUBLE_EDGE
	; end

	db 0 ; padding
