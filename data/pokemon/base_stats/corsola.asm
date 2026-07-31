	db DEX_CORSOLA ; pokedex id

	db  55,  55,  85,  35,  75
	;   hp  atk  def  spd  spc

	db WATER, ROCK ; type
	db 60 ; catch rate
	db 113 ; base exp

	INCBIN "gfx/pokemon/front/corsola.pic", 0, 1 ; sprite dimensions
	dw CorsolaPicFront, CorsolaPicBack

	db TACKLE, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, SURF, WATER_GUN, BUBBLEBEAM, ICE_BEAM, BLIZZARD, ROCK_SLIDE, EARTHQUAKE, DIG, STRENGTH, EXPLOSION
	; end

	db 0 ; padding
