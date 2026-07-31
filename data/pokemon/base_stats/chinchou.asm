	db DEX_CHINCHOU ; pokedex id

	db  75,  38,  38,  67,  56
	;   hp  atk  def  spd  spc

	db WATER, ELECTRIC ; type
	db 190 ; catch rate
	db 90 ; base exp

	INCBIN "gfx/pokemon/front/chinchou.pic", 0, 1 ; sprite dimensions
	dw ChinchouPicFront, ChinchouPicBack

	db BUBBLE, THUNDER_WAVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, SURF, WATER_GUN, BUBBLEBEAM, ICE_BEAM, BLIZZARD, THUNDERBOLT, THUNDER, THUNDER_WAVE, FLASH
	; end

	db 0 ; padding
