_MrPsychicsHouseMrPsychicYouWantedThisText::
	text "...Wait! Speak"
	line "not a word!"

	para "You desired this!"
	prompt

_MrPsychicsHouseMrPsychicReceivedTM29Text::
	text "<PLAYER> received"
	line "@"
	text_ram wStringBuffer
	text "!@"
	text_end

_MrPsychicsHouseMrPsychicTM29ExplanationText::
	text "TM29 is PSYCHIC!"

	para "It may weaken"
	line "the foe's own"
	cont "SPECIAL powers."
	done

_MrPsychicsHouseMrPsychicTM29NoRoomText::
	text "Where do you mean"
	line "to place this?"
	done
