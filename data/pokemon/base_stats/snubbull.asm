	db DEX_SNUBBULL ; pokedex id

	db  60,  80,  50,  30,  40
	;   hp  atk  def  spd  spc

	db NORMAL, NORMAL ; type
	db 190 ; catch rate
	db 63 ; base exp

	INCBIN "gfx/pokemon/front/snubbull.pic", 0, 1 ; sprite dimensions
	dw SnubbullPicFront, SnubbullPicBack

	db TACKLE, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, BODY_SLAM, TAKE_DOWN, DOUBLE_EDGE
	; end

	db 0 ; padding
