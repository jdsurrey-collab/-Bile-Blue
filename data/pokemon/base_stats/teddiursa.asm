	db DEX_TEDDIURSA ; pokedex id

	db  60,  80,  50,  40,  50
	;   hp  atk  def  spd  spc

	db NORMAL, NORMAL ; type
	db 120 ; catch rate
	db 124 ; base exp

	INCBIN "gfx/pokemon/front/teddiursa.pic", 0, 1 ; sprite dimensions
	dw TeddiursaPicFront, TeddiursaPicBack

	db SCRATCH, LEER, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, BODY_SLAM, TAKE_DOWN, DOUBLE_EDGE
	; end

	db 0 ; padding
