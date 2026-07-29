_BluesHouseDaisyRivalAtLabText::
	text "Oh, <PLAYER>."
	line "<RIVAL>'s gone to"
	cont "Grandfather's lab."
	done

_BluesHouseDaisyOfferMapText::
	text "Grandfather sends"
	line "you on an errand?"
	cont "Take this, then-"
	cont "it may help."
	prompt

_GotMapText::
	text "<PLAYER> got a"
	line "@"
	text_ram wStringBuffer
	text "!@"
	text_end

_BluesHouseDaisyBagFullText::
	text "You carry too much"
	line "already, I think."
	done

_BluesHouseDaisyUseMapText::
	text "The TOWN MAP shows"
	line "where you have"
	cont "wandered to."
	done

_BluesHouseDaisyWalkingText::
	text "#MON are living"
	line "things, not tools."
	cont "Let them rest,"
	cont "or lose them."
	done

_BluesHouseTownMapText::
	text "A fine map. It"
	line "may save your life."
	done
