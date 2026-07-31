	db DEX_YANMA ; pokedex id

	db  65,  65,  45,  95,  60
	;   hp  atk  def  spd  spc

	db BUG, FLYING ; type
	db 75 ; catch rate
	db 147 ; base exp

	INCBIN "gfx/pokemon/front/yanma.pic", 0, 1 ; sprite dimensions
	dw YanmaPicFront, YanmaPicBack

	db TACKLE, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE
	; end

	db 0 ; padding
