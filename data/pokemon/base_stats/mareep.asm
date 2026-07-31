	db DEX_MAREEP ; pokedex id

	db  55,  40,  40,  35,  55
	;   hp  atk  def  spd  spc

	db ELECTRIC, ELECTRIC ; type
	db 235 ; catch rate
	db 59 ; base exp

	INCBIN "gfx/pokemon/front/mareep.pic", 0, 1 ; sprite dimensions
	dw MareepPicFront, MareepPicBack

	db TACKLE, GROWL, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, THUNDERBOLT, THUNDER, THUNDER_WAVE, FLASH
	; end

	db 0 ; padding
