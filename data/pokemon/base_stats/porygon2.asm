	db DEX_PORYGON2 ; pokedex id

	db  85,  80,  90,  60, 100
	;   hp  atk  def  spd  spc

	db NORMAL, NORMAL ; type
	db 45 ; catch rate
	db 180 ; base exp

	INCBIN "gfx/pokemon/front/porygon2.pic", 0, 1 ; sprite dimensions
	dw Porygon2PicFront, Porygon2PicBack

	db TACKLE, CONVERSION, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, BODY_SLAM, TAKE_DOWN, DOUBLE_EDGE, TRI_ATTACK, PSYCHIC_M, THUNDERBOLT, ICE_BEAM, HYPER_BEAM
	; end

	db 0 ; padding
