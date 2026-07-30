; Pokémon Purple: the cultist from the dream sequence (engine/movie/cultist_dream.asm)
	object_const_def
	const_export REDSHOUSE2F_CULTIST

RedsHouse2F_Object:
	db $a ; border block

	def_warp_events
	warp_event  7,  1, REDS_HOUSE_1F, 3

	def_bg_events

	def_object_events
	object_event  2,  6, SPRITE_CHANNELER, STAY, NONE, TEXT_REDSHOUSE2F_CULTIST

	def_warps_to REDS_HOUSE_2F
