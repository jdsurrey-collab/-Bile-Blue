	db DEX_DELIBIRD ; pokedex id

	db  45,  55,  45,  75,  55
	;   hp  atk  def  spd  spc

	db ICE, FLYING ; type
	db 45 ; catch rate
	db 183 ; base exp

	INCBIN "gfx/pokemon/front/delibird.pic", 0, 1 ; sprite dimensions
	dw DelibirdPicFront, DelibirdPicBack

	db TACKLE, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, ICE_BEAM, BLIZZARD, BODY_SLAM, FLY, SKY_ATTACK, WHIRLWIND, RAZOR_WIND
	; end

	db 0 ; padding
