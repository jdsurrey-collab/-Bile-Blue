	db DEX_DONPHAN ; pokedex id

	db  90, 120, 120,  50,  60
	;   hp  atk  def  spd  spc

	db GROUND, GROUND ; type
	db 60 ; catch rate
	db 189 ; base exp

	INCBIN "gfx/pokemon/front/donphan.pic", 0, 1 ; sprite dimensions
	dw DonphanPicFront, DonphanPicBack

	db HORN_ATTACK, GROWL, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, EARTHQUAKE, DIG, FISSURE, STRENGTH, HYPER_BEAM, BODY_SLAM
	; end

	db 0 ; padding
