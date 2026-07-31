	db DEX_CROCONAW ; pokedex id

	db  65,  80,  80,  58,  61
	;   hp  atk  def  spd  spc

	db WATER, WATER ; type
	db 45 ; catch rate
	db 143 ; base exp

	INCBIN "gfx/pokemon/front/croconaw.pic", 0, 1 ; sprite dimensions
	dw CroconawPicFront, CroconawPicBack

	db SCRATCH, LEER, RAGE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE
	; end

	db 0 ; padding
