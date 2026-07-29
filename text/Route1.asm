_Route1Youngster1MartSampleText::
	text "I clerk at the"
	line "#MON MART."

	para "A convenient"
	line "shop, if you"
	cont "can call it that,"
	cont "in VIRIDIAN CITY."

	para "Go on, then-"
	line "take a sample."
	cont "It won't save you."
	prompt

_Route1Youngster1GotPotionText::
	text "<PLAYER> got"
	line "@"
	text_ram wStringBuffer
	text "!@"
	text_end

_Route1Youngster1AlsoGotPokeballsText::
	text "We also stock #"
	line "BALLs, for those"
	cont "who still hunt."
	done

_Route1Youngster1NoRoomText::
	text "You're already"
	line "burdened enough."
	done

_Route1Youngster2Text::
	text "See those ledges"
	line "along the road?"

	para "Leap if you dare-"
	line "the fall won't"
	cont "kill you. Probably."

	para "Quicker back to"
	line "PALLET TOWN,"
	cont "that way."
	done

_Route1SignText::
	text "ROUTE 1"
	line "PALLET TOWN -"
	cont "VIRIDIAN CITY"
	done
