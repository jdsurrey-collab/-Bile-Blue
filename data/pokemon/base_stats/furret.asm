	db DEX_FURRET ; pokedex id

	db  85,  76,  64,  90,  50
	;   hp  atk  def  spd  spc

	db NORMAL, NORMAL ; type
	db 90 ; catch rate
	db 116 ; base exp

	INCBIN "gfx/pokemon/front/furret.pic", 0, 1 ; sprite dimensions
	dw FurretPicFront, FurretPicBack

	db SCRATCH, DEFENSE_CURL, QUICK_ATTACK, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC, RAGE, MIMIC, DOUBLE_TEAM, REST, SUBSTITUTE, BIDE, SWIFT, BODY_SLAM, TAKE_DOWN, DOUBLE_EDGE
	; end

	db 0 ; padding
