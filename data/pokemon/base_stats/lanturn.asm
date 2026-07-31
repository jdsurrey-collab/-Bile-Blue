	db DEX_LANTURN ; pokedex id

	db 125,  58,  58,  67,  76
	;   hp  atk  def  spd  spc

	db WATER, ELECTRIC ; type
	db 75 ; catch rate
	db 156 ; base exp

	INCBIN "gfx/pokemon/front/lanturn.pic", 0, 1 ; sprite dimensions
	dw LanturnPicFront, LanturnPicBack

	db BUBBLE, THUNDER_WAVE, SUPERSONIC, NO_MOVE ; level 1 learnset
	db GROWTH_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, SURF, WATER_GUN, BUBBLEBEAM, ICE_BEAM, BLIZZARD, THUNDERBOLT, THUNDER, THUNDER_WAVE, FLASH
	; end

	db 0 ; padding
