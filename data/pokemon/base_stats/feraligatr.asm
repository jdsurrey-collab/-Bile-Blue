	db DEX_FERALIGATR ; pokedex id

	db  85, 105, 100,  78,  81
	;   hp  atk  def  spd  spc

	db WATER, WATER ; type
	db 45 ; catch rate
	db 210 ; base exp

	INCBIN "gfx/pokemon/front/feraligatr.pic", 0, 1 ; sprite dimensions
	dw FeraligatrPicFront, FeraligatrPicBack

	db SCRATCH, LEER, RAGE, WATER_GUN ; level 1 learnset
	db GROWTH_MEDIUM_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE
	; end

	db 0 ; padding
