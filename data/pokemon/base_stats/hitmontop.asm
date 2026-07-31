	db DEX_HITMONTOP ; pokedex id

	db  50,  95,  95,  70,  72
	;   hp  atk  def  spd  spc

	db FIGHTING, FIGHTING ; type
	db 45 ; catch rate
	db 138 ; base exp

	INCBIN "gfx/pokemon/front/hitmontop.pic", 0, 1 ; sprite dimensions
	dw HitmontopPicFront, HitmontopPicBack

	db ROLLING_KICK, NO_MOVE, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, SUBMISSION, SEISMIC_TOSS, COUNTER, MEGA_PUNCH, MEGA_KICK, ROCK_SLIDE
	; end

	db 0 ; padding
