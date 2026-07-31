	db DEX_DUNSPARCE ; pokedex id

	db 100,  70,  70,  45,  65
	;   hp  atk  def  spd  spc

	db NORMAL, NORMAL ; type
	db 190 ; catch rate
	db 75 ; base exp

	INCBIN "gfx/pokemon/front/dunsparce.pic", 0, 1 ; sprite dimensions
	dw DunsparcePicFront, DunsparcePicBack

	db RAGE, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE
	; end

	db 0 ; padding
