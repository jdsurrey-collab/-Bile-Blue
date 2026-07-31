	db DEX_WOBBUFFET ; pokedex id

	db 190,  33,  58,  33,  45
	;   hp  atk  def  spd  spc

	db PSYCHIC_TYPE, PSYCHIC_TYPE ; type
	db 45 ; catch rate
	db 177 ; base exp

	INCBIN "gfx/pokemon/front/wobbuffet.pic", 0, 1 ; sprite dimensions
	dw WobbuffetPicFront, WobbuffetPicBack

	db COUNTER, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE
	; end

	db 0 ; padding
