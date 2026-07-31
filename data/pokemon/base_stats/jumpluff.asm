	db DEX_JUMPLUFF ; pokedex id

	db  75,  55,  70, 110,  70
	;   hp  atk  def  spd  spc

	db GRASS, FLYING ; type
	db 45 ; catch rate
	db 176 ; base exp

	INCBIN "gfx/pokemon/front/jumpluff.pic", 0, 1 ; sprite dimensions
	dw JumpluffPicFront, JumpluffPicBack

	db SPLASH, TAIL_WHIP, TACKLE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE
	; end

	db 0 ; padding
