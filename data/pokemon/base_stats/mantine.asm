	db DEX_MANTINE ; pokedex id

	db  65,  40,  70,  70, 110
	;   hp  atk  def  spd  spc

	db WATER, FLYING ; type
	db 25 ; catch rate
	db 168 ; base exp

	INCBIN "gfx/pokemon/front/mantine.pic", 0, 1 ; sprite dimensions
	dw MantinePicFront, MantinePicBack

	db TACKLE, BUBBLE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, SURF, WATER_GUN, BUBBLEBEAM, ICE_BEAM, BLIZZARD, FLY, SKY_ATTACK, WHIRLWIND, RAZOR_WIND
	; end

	db 0 ; padding
