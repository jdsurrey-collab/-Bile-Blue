	db DEX_IGGLYBUFF ; pokedex id

	db  90,  30,  15,  15,  30
	;   hp  atk  def  spd  spc

	db NORMAL, NORMAL ; type
	db 170 ; catch rate
	db 39 ; base exp

	INCBIN "gfx/pokemon/front/igglybuff.pic", 0, 1 ; sprite dimensions
	dw IgglybuffPicFront, IgglybuffPicBack

	db SING, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, BODY_SLAM, TAKE_DOWN, DOUBLE_EDGE
	; end

	db 0 ; padding
