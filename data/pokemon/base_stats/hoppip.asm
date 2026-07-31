	db DEX_HOPPIP ; pokedex id

	db  35,  35,  40,  50,  45
	;   hp  atk  def  spd  spc

	db GRASS, FLYING ; type
	db 255 ; catch rate
	db 74 ; base exp

	INCBIN "gfx/pokemon/front/hoppip.pic", 0, 1 ; sprite dimensions
	dw HoppipPicFront, HoppipPicBack

	db SPLASH, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE
	; end

	db 0 ; padding
