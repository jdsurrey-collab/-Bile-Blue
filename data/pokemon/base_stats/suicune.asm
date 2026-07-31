	db DEX_SUICUNE ; pokedex id

	db 100,  75, 115,  85, 102
	;   hp  atk  def  spd  spc

	db WATER, WATER ; type
	db 3 ; catch rate
	db 215 ; base exp

	INCBIN "gfx/pokemon/front/suicune.pic", 0, 1 ; sprite dimensions
	dw SuicunePicFront, SuicunePicBack

	db BITE, LEER, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, SURF, WATER_GUN, BUBBLEBEAM, ICE_BEAM, BLIZZARD, HYPER_BEAM, REFLECT
	; end

	db 0 ; padding
