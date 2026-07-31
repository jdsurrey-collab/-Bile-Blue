	db DEX_BAYLEEF ; pokedex id

	db  60,  62,  80,  60,  71
	;   hp  atk  def  spd  spc

	db GRASS, GRASS ; type
	db 45 ; catch rate
	db 141 ; base exp

	INCBIN "gfx/pokemon/front/bayleef.pic", 0, 1 ; sprite dimensions
	dw BayleefPicFront, BayleefPicBack

	db TACKLE, GROWL, RAZOR_LEAF, REFLECT ; level 1 learnset
	db GROWTH_MEDIUM_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, SOLARBEAM, MEGA_DRAIN, CUT
	; end

	db 0 ; padding
