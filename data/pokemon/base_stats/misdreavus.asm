	db DEX_MISDREAVUS ; pokedex id

	db  60,  60,  60,  85,  85
	;   hp  atk  def  spd  spc

	db GHOST, GHOST ; type
	db 45 ; catch rate
	db 147 ; base exp

	INCBIN "gfx/pokemon/front/misdreavus.pic", 0, 1 ; sprite dimensions
	dw MisdreavusPicFront, MisdreavusPicBack

	db GROWL, PSYWAVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, PSYCHIC_M, DREAM_EATER, PSYWAVE, EXPLOSION
	; end

	db 0 ; padding
