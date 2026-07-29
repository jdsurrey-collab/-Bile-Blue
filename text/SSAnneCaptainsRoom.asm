_SSAnneCaptainsRoomRubCaptainsBackText::
	text "CAPTAIN: Ooargh..."
	line "I feel wretched..."
	cont "Urrp! So ill..."

	para "<PLAYER> rubbed"
	line "the CAPTAIN's"
	cont "back."

	para "Rub-rub..."
	line "Rub-rub...@"
	text_end

_SSAnneCaptainsRoomCaptainIFeelMuchBetterText::
	text "CAPTAIN: Whew."
	line "My thanks. I"
	cont "feel restored."

	para "Care to see my"
	line "CUT technique?"

	para "I'd show you,"
	line "if not for this"
	cont "illness..."

	para "Here, then. Take"
	line "this instead."

	para "Teach it to your"
	line "#MON, and CUT"
	cont "whenever you"
	cont "please."
	prompt

_SSAnneCaptainsRoomCaptainReceivedHM01Text::
	text "<PLAYER> got"
	line "@"
	text_ram wStringBuffer
	text "!@"
	text_end

_SSAnneCaptainsRoomCaptainNotSickAnymoreText::
	text "CAPTAIN: Whew!"

	para "Now that I'm"
	line "well, I suppose"
	cont "it's time."
	done

_SSAnneCaptainsRoomCaptainHM01NoRoomText::
	text "Oh no. No room"
	line "left for this!"
	done

_SSAnneCaptainsRoomTrashText::
	text "Yuck. I shouldn't"
	line "have looked."
	done

_SSAnneCaptainsRoomSeasickBookText::
	text "How to Conquer"
	line "Seasickness..."
	cont "The CAPTAIN reads"
	cont "this, endlessly."
	done
