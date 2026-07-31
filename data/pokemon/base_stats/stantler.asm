	db DEX_STANTLER ; pokedex id

	db  73,  95,  62,  85,  75
	;   hp  atk  def  spd  spc

	db NORMAL, NORMAL ; type
	db 45 ; catch rate
	db 165 ; base exp

	INCBIN "gfx/pokemon/front/stantler.pic", 0, 1 ; sprite dimensions
	dw StantlerPicFront, StantlerPicBack

	db TACKLE, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, BODY_SLAM, TAKE_DOWN, DOUBLE_EDGE
	; end

	db 0 ; padding
