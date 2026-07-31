	db DEX_REMORAID ; pokedex id

	db  35,  65,  35,  65,  50
	;   hp  atk  def  spd  spc

	db WATER, WATER ; type
	db 190 ; catch rate
	db 78 ; base exp

	INCBIN "gfx/pokemon/front/remoraid.pic", 0, 1 ; sprite dimensions
	dw RemoraidPicFront, RemoraidPicBack

	db WATER_GUN, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, SURF, WATER_GUN, BUBBLEBEAM, ICE_BEAM, BLIZZARD
	; end

	db 0 ; padding
