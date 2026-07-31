	db DEX_GIRAFARIG ; pokedex id

	db  70,  80,  65,  85,  77
	;   hp  atk  def  spd  spc

	db NORMAL, PSYCHIC_TYPE ; type
	db 60 ; catch rate
	db 149 ; base exp

	INCBIN "gfx/pokemon/front/girafarig.pic", 0, 1 ; sprite dimensions
	dw GirafarigPicFront, GirafarigPicBack

	db TACKLE, GROWL, CONFUSION, STOMP ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, PSYCHIC_M, PSYWAVE, REFLECT, TELEPORT, DREAM_EATER, BODY_SLAM, TAKE_DOWN, DOUBLE_EDGE
	; end

	db 0 ; padding
