	db DEX_HOOTHOOT ; pokedex id

	db  60,  30,  30,  50,  46
	;   hp  atk  def  spd  spc

	db NORMAL, FLYING ; type
	db 255 ; catch rate
	db 58 ; base exp

	INCBIN "gfx/pokemon/front/hoothoot.pic", 0, 1 ; sprite dimensions
	dw HoothootPicFront, HoothootPicBack

	db TACKLE, GROWL, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, FLY, SKY_ATTACK, WHIRLWIND, RAZOR_WIND, BODY_SLAM, TAKE_DOWN, DOUBLE_EDGE
	; end

	db 0 ; padding
