	db DEX_TYPHLOSION ; pokedex id

	db  78,  84,  78, 100,  97
	;   hp  atk  def  spd  spc

	db FIRE, FIRE ; type
	db 45 ; catch rate
	db 209 ; base exp

	INCBIN "gfx/pokemon/front/typhlosion.pic", 0, 1 ; sprite dimensions
	dw TyphlosionPicFront, TyphlosionPicBack

	db TACKLE, LEER, SMOKESCREEN, EMBER ; level 1 learnset
	db GROWTH_MEDIUM_SLOW ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, FIRE_BLAST, BODY_SLAM, SKULL_BASH, HYPER_BEAM, EARTHQUAKE
	; end

	db 0 ; padding
