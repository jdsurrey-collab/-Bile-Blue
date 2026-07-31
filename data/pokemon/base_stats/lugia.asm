	db DEX_LUGIA ; pokedex id

	db 106,  90, 130, 110, 122
	;   hp  atk  def  spd  spc

	db PSYCHIC_TYPE, FLYING ; type
	db 3 ; catch rate
	db 220 ; base exp

	INCBIN "gfx/pokemon/front/lugia.pic", 0, 1 ; sprite dimensions
	dw LugiaPicFront, LugiaPicBack

	db CONFUSION, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, FLY, SKY_ATTACK, WHIRLWIND, RAZOR_WIND, PSYCHIC_M, PSYWAVE, REFLECT, TELEPORT, DREAM_EATER, HYPER_BEAM, SURF, ICE_BEAM
	; end

	db 0 ; padding
