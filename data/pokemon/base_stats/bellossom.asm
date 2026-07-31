	db DEX_BELLOSSOM ; pokedex id

	db  75,  80,  85,  50,  95
	;   hp  atk  def  spd  spc

	db GRASS, GRASS ; type
	db 45 ; catch rate
	db 184 ; base exp

	INCBIN "gfx/pokemon/front/bellossom.pic", 0, 1 ; sprite dimensions
	dw BellossomPicFront, BellossomPicBack

	db ABSORB, SWEET_SCENT, STUN_SPORE, PETAL_DANCE ; level 1 learnset
	db GROWTH_MEDIUM_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, SOLARBEAM, MEGA_DRAIN, CUT
	; end

	db 0 ; padding
