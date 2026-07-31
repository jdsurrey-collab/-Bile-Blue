	db DEX_SKIPLOOM ; pokedex id

	db  55,  45,  50,  80,  55
	;   hp  atk  def  spd  spc

	db GRASS, FLYING ; type
	db 120 ; catch rate
	db 136 ; base exp

	INCBIN "gfx/pokemon/front/skiploom.pic", 0, 1 ; sprite dimensions
	dw SkiploomPicFront, SkiploomPicBack

	db SPLASH, TAIL_WHIP, TACKLE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE
	; end

	db 0 ; padding
