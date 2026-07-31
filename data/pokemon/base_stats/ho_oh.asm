	db DEX_HO_OH ; pokedex id

	db 106, 130,  90,  90, 132
	;   hp  atk  def  spd  spc

	db FIRE, FLYING ; type
	db 3 ; catch rate
	db 220 ; base exp

	INCBIN "gfx/pokemon/front/ho_oh.pic", 0, 1 ; sprite dimensions
	dw HoOhPicFront, HoOhPicBack

	db SCRATCH, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, FLY, SKY_ATTACK, WHIRLWIND, RAZOR_WIND, FIRE_BLAST, BODY_SLAM, SKULL_BASH, HYPER_BEAM, REFLECT
	; end

	db 0 ; padding
