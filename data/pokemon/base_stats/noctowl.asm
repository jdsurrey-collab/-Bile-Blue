	db DEX_NOCTOWL ; pokedex id

	db 100,  50,  50,  70,  86
	;   hp  atk  def  spd  spc

	db NORMAL, FLYING ; type
	db 90 ; catch rate
	db 162 ; base exp

	INCBIN "gfx/pokemon/front/noctowl.pic", 0, 1 ; sprite dimensions
	dw NoctowlPicFront, NoctowlPicBack

	db TACKLE, GROWL, PECK, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE
	; end

	db 0 ; padding
