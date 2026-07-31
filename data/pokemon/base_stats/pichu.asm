	db DEX_PICHU ; pokedex id

	db  20,  40,  15,  60,  35
	;   hp  atk  def  spd  spc

	db ELECTRIC, ELECTRIC ; type
	db 190 ; catch rate
	db 42 ; base exp

	INCBIN "gfx/pokemon/front/pichu.pic", 0, 1 ; sprite dimensions
	dw PichuPicFront, PichuPicBack

	db THUNDERSHOCK, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, THUNDERBOLT, THUNDER, THUNDER_WAVE, FLASH
	; end

	db 0 ; padding
