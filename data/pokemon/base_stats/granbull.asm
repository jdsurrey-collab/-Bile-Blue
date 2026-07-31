	db DEX_GRANBULL ; pokedex id

	db  90, 120,  75,  45,  60
	;   hp  atk  def  spd  spc

	db NORMAL, NORMAL ; type
	db 75 ; catch rate
	db 178 ; base exp

	INCBIN "gfx/pokemon/front/granbull.pic", 0, 1 ; sprite dimensions
	dw GranbullPicFront, GranbullPicBack

	db TACKLE, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, BODY_SLAM, TAKE_DOWN, DOUBLE_EDGE
	; end

	db 0 ; padding
