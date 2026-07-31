	db DEX_ARIADOS ; pokedex id

	db  70,  90,  70,  40,  60
	;   hp  atk  def  spd  spc

	db BUG, POISON ; type
	db 90 ; catch rate
	db 134 ; base exp

	INCBIN "gfx/pokemon/front/ariados.pic", 0, 1 ; sprite dimensions
	dw AriadosPicFront, AriadosPicBack

	db POISON_STING, STRING_SHOT, CONSTRICT, NO_MOVE ; level 1 learnset
	db GROWTH_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, MEGA_DRAIN, SWORDS_DANCE, CUT, EXPLOSION, SELFDESTRUCT
	; end

	db 0 ; padding
