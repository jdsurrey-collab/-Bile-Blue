	db DEX_CLEFFA ; pokedex id

	db  50,  25,  28,  15,  50
	;   hp  atk  def  spd  spc

	db NORMAL, NORMAL ; type
	db 150 ; catch rate
	db 37 ; base exp

	INCBIN "gfx/pokemon/front/cleffa.pic", 0, 1 ; sprite dimensions
	dw CleffaPicFront, CleffaPicBack

	db POUND, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, BODY_SLAM, TAKE_DOWN, DOUBLE_EDGE
	; end

	db 0 ; padding
