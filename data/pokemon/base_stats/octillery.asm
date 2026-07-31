	db DEX_OCTILLERY ; pokedex id

	db  75, 105,  75,  45,  90
	;   hp  atk  def  spd  spc

	db WATER, WATER ; type
	db 75 ; catch rate
	db 164 ; base exp

	INCBIN "gfx/pokemon/front/octillery.pic", 0, 1 ; sprite dimensions
	dw OctilleryPicFront, OctilleryPicBack

	db WATER_GUN, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, SURF, WATER_GUN, BUBBLEBEAM, ICE_BEAM, BLIZZARD, HYPER_BEAM, PSYCHIC_M
	; end

	db 0 ; padding
