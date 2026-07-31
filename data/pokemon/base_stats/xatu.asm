	db DEX_XATU ; pokedex id

	db  65,  75,  70,  95,  82
	;   hp  atk  def  spd  spc

	db PSYCHIC_TYPE, FLYING ; type
	db 75 ; catch rate
	db 171 ; base exp

	INCBIN "gfx/pokemon/front/xatu.pic", 0, 1 ; sprite dimensions
	dw XatuPicFront, XatuPicBack

	db PECK, LEER, NIGHT_SHADE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE
	; end

	db 0 ; padding
