_CopycatsHouse2FCopycatDoYouLikePokemonText::
	text "<PLAYER>: Hi! Do"
	line "you like #MON?"

	para "<PLAYER>: Uh no, I"
	line "just asked you."

	para "<PLAYER>: Huh?"
	line "You're odd!"

	para "COPYCAT: Hmm?"
	line "Quit mimicking?"

	para "But that's my"
	line "one true hobby!"
	prompt

_CopycatsHouse2FCopycatTM31PreReceiveText::
	text "Oh my!"
	line "A # DOLL!"

	para "For me?"
	line "My thanks!"

	para "Then take this"
	line "in kind!"
	prompt

_CopycatsHouse2FCopycatReceivedTM31Text::
	text "<PLAYER> received"
	line "@"
	text_ram wStringBuffer
	text "!@"
	text_end

_CopycatsHouse2FCopycatTM31Explanation1Text::
	text_start

	para "TM31 holds my"
	line "favorite, MIMIC!"

	para "Use it on a fine"
	line "#MON!@"
	text_end

_CopycatsHouse2FCopycatTM31Explanation2Text::
	text "<PLAYER>: Hi!"
	line "Thanks for TM31!"

	para "<PLAYER>: Pardon?"

	para "<PLAYER>: Is it"
	line "such fun, mimick-"
	cont "ing my every"
	cont "move?"

	para "COPYCAT: You bet!"
	line "It's a scream!"
	done

_CopycatsHouse2FCopycatTM31NoRoomText::
	text "Don't you want"
	line "this?@"
	text_end

_CopycatsHouse2FDoduoText::
	text "DODUO: Giiih!"

	para "MIRROR MIRROR ON"
	line "THE WALL, WHO IS"
	cont "THE FAIREST ONE"
	cont "OF ALL?"
	done

_CopycatsHouse2FRareDollText::
	text "A rare #MON,"
	line "surely! Huh?"
	cont "Just a doll!"
	done

_CopycatsHouse2FSNESText::
	text "A game with MARIO"
	line "wearing a bucket"
	cont "on his head!"
	done

_CopycatsHouse2FPCMySecretsText::
	text "..."

	para "My Secrets!"

	para "Skill: Mimicry!"
	line "Hobby: Collecting"
	cont "dolls!"
	cont "Favorite #MON:"
	cont "CLEFAIRY!"
	done

_CopycatsHouse2FPCCantSeeText::
	text "Huh? Can't see!"
	done
