	db DEX_SUNFLORA ; pokedex id

	db  75,  75,  55,  30,  95
	;   hp  atk  def  spd  spc

	db GRASS, GRASS ; type
	db 120 ; catch rate
	db 146 ; base exp

	INCBIN "gfx/pokemon/front/sunflora.pic", 0, 1 ; sprite dimensions
	dw SunfloraPicFront, SunfloraPicBack

	db ABSORB, POUND, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, SOLARBEAM, MEGA_DRAIN, CUT
	; end

	db 0 ; padding
