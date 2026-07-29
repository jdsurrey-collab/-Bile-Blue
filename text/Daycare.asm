_DaycareGentlemanIntroText::
	text "I keep a DAYCARE."
	line "Shall I raise one"
	cont "of your #MON"
	cont "for you a while?"
	done

_DaycareGentlemanWhichMonText::
	text "Which #MON"
	line "shall I raise?"
	prompt

_DaycareGentlemanWillLookAfterMonText::
	text "Very well, I'll"
	line "look after @"
	text_ram wNameBuffer
	text_start
	cont "for a while."
	prompt

_DaycareGentlemanComeSeeMeInAWhileText::
	text "Return to me"
	line "in a while."
	done

_DaycareGentlemanMonHasGrownText::
	text "Your @"
	text_ram wNameBuffer
	text_start
	line "has grown a great"
	cont "deal!"

	para "By level, it has"
	line "grown by @"
	text_decimal wDayCareNumLevelsGrown, 1, 3
	text "!"

	para "Am I not skilled?"
	prompt

_DaycareGentlemanOweMoneyText::
	text "You owe me ¥@"
	text_bcd wDayCareTotalCost, 2 | LEADING_ZEROES | LEFT_ALIGN
	text_start
	line "for the return"
	cont "of this #MON."
	done

_DaycareGentlemanGotMonBackText::
	text "<PLAYER> got"
	line "@"
	text_ram wDayCareMonName
	text " back!"
	done

_DaycareGentlemanMonNeedsMoreTimeText::
	text "Back so soon?"
	line "Your @"
	text_ram wNameBuffer
	text_start
	cont "needs still more"
	cont "time with me."
	prompt
