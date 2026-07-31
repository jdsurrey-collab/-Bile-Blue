	db DEX_MEGANIUM ; pokedex id

	db  80,  82, 100,  80,  91
	;   hp  atk  def  spd  spc

	db GRASS, GRASS ; type
	db 45 ; catch rate
	db 208 ; base exp

	INCBIN "gfx/pokemon/front/meganium.pic", 0, 1 ; sprite dimensions
	dw MeganiumPicFront, MeganiumPicBack

	db TACKLE, GROWL, RAZOR_LEAF, REFLECT ; level 1 learnset
	db GROWTH_MEDIUM_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, SOLARBEAM, MEGA_DRAIN, CUT, HYPER_BEAM, BODY_SLAM
	; end

	db 0 ; padding
