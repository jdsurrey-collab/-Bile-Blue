	db DEX_TYROGUE ; pokedex id

	db  35,  35,  35,  35,  35
	;   hp  atk  def  spd  spc

	db FIGHTING, FIGHTING ; type
	db 75 ; catch rate
	db 91 ; base exp

	INCBIN "gfx/pokemon/front/tyrogue.pic", 0, 1 ; sprite dimensions
	dw TyroguePicFront, TyroguePicBack

	db TACKLE, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, SUBMISSION, SEISMIC_TOSS, COUNTER, MEGA_PUNCH, MEGA_KICK
	; end

	db 0 ; padding
