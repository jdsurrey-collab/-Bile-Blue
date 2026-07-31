	db DEX_BLISSEY ; pokedex id

	db 255,  10,  10,  55, 105
	;   hp  atk  def  spd  spc

	db NORMAL, NORMAL ; type
	db 30 ; catch rate
	db 255 ; base exp

	INCBIN "gfx/pokemon/front/blissey.pic", 0, 1 ; sprite dimensions
	dw BlisseyPicFront, BlisseyPicBack

	db POUND, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, BODY_SLAM, TAKE_DOWN, DOUBLE_EDGE, SOFTBOILED, PSYCHIC_M, REFLECT, EGG_BOMB
	; end

	db 0 ; padding
