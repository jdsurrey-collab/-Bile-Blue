_NameRatersHouseNameRaterWantMeToRateText::
	text "Good day, good"
	line "day! I am the"
	cont "true NAME RATER!"

	para "Shall I judge the"
	line "nicknames of"
	cont "your #MON?"
	done

_NameRatersHouseNameRaterWhichPokemonText::
	text "Which #MON"
	line "shall I judge?"
	prompt

_NameRatersHouseNameRaterGiveItANiceNameText::
	text_ram wNameBuffer
	text ", is it?"
	line "That is a fair"
	cont "nickname enough!"

	para "But would you"
	line "have me grant"
	cont "it a finer name?"

	para "Well, then?"
	done

_NameRatersHouseNameRaterWhatShouldWeNameItText::
	text "So be it! What"
	line "shall we call it?"
	prompt

_NameRatersHouseNameRaterPokemonHasBeenRenamedText::
	text "Done! This #MON"
	line "has been renamed"
	cont "@"
	text_ram wBuffer
	text "!"

	para "Finer, by far,"
	line "than before!"
	done

_NameRatersHouseNameRaterComeAnyTimeYouLikeText::
	text "Very well! Come"
	line "again, any hour!"
	done

_NameRatersHouseNameRaterATrulyImpeccableNameText::
	text_ram wNameBuffer
	text ", is it?"
	line "That is a truly"
	cont "flawless name!"

	para "Guard it well,"
	line "@"
	text_ram wNameBuffer
	text "!"
	done
