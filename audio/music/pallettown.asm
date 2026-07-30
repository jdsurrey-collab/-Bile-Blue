Music_PalletTown_Ch1::
; Pokémon Purple: much slower, lower, and more sustained than the bright
; bouncy original -- parallel (G) minor, dropped an octave, heavy tempo cut,
; and the busiest arpeggio run near the end thinned out (adjacent short
; notes merged into fewer, longer ones) to kill the skipping/bumping feel.
	tempo 230
	volume 7, 7
	duty_cycle 2
	note_type 12, 13, 1
.mainloop:
	octave 2
	note A#, 4
	octave 3
	note C_, 2
	note D_, 4
	note G_, 2
	note D_, 2
	note C_, 2
	octave 2
	note A#, 4
	note G_, 2
	octave 3
	note D_, 4
	note D_, 2
	note C_, 2
	octave 2
	note A#, 2
	rest 2
	note A#, 2
	octave 3
	note C_, 2
	octave 2
	note A#, 2
	octave 3
	note C_, 8
	rest 2
	octave 2
	note A#, 2
	octave 3
	note C_, 2
	octave 2
	note A_, 2
	note A#, 2
	note G_, 2
	note A_, 2
	note F_, 2
	note A#, 4
	octave 3
	note C_, 2
	note D_, 4
	note G_, 2
	note D_, 2
	note C_, 2
	octave 2
	note A#, 4
	note G_, 2
	octave 3
	note D_, 4
	note D_, 2
	note G_, 2
	note F_, 2
	note D#, 4
	note D_, 2
	note C_, 4
	octave 2
	note A_, 2
	note A#, 2
	octave 3
	note C_, 2
	note D_, 2
	note C_, 2
	octave 2
	note A#, 2
	note A_, 2
	note G_, 4
	note F_, 4
	octave 3
	note C_, 2
	octave 2
	note G_, 2
	note D#, 2
	note G_, 2
	octave 3
	note D_, 2
	octave 2
	note A_, 2
	note F_, 2
	note A_, 2
	note_type 12, 12, 2
	note A#, 4
	note D_, 4
	note A#, 4
	note D_, 4
	octave 3
	note C_, 2
	octave 2
	note G_, 4
	octave 3
	note D_, 2
	octave 2
	note A_, 2
	note F_, 2
	note A_, 2
	note A#, 4
	note D_, 4
	note A#, 4
	note D_, 4
	note A_, 4
	note C_, 4
	note A_, 4
	note C_, 4
	note F_, 4
	note D_, 4
	note G_, 4
	note D_, 4
	sound_loop 0, .mainloop

	sound_ret ; unused

Music_PalletTown_Ch2::
	duty_cycle 2
.mainloop:
	note_type 12, 14, 1
	octave 4
	note D_, 2
	note_type 12, 11, 1
	note C_, 2
	note_type 12, 14, 1
	octave 3
	note A#, 2
	note_type 12, 12, 1
	note A_, 2
	note_type 12, 14, 1
	octave 4
	note G_, 2
	note_type 12, 12, 1
	note D#, 2
	note_type 12, 14, 1
	note F_, 2
	note D#, 2
	note D_, 6
	octave 3
	note A#, 2
	note G_, 2
	note G_, 2
	note A_, 2
	note A#, 2
	octave 4
	note C_, 10
	octave 3
	note F_, 2
	note G_, 2
	note A_, 2
	note A#, 6
	octave 4
	note C_, 1
	octave 3
	note A#, 1
	note A_, 8
	octave 4
	note D_, 2
	note_type 12, 11, 1
	note C_, 2
	note_type 12, 14, 1
	octave 3
	note A#, 2
	note_type 12, 12, 1
	octave 4
	note D_, 2
	note_type 12, 14, 1
	note G_, 2
	note_type 12, 11, 1
	note F_, 2
	note_type 12, 12, 1
	note F_, 2
	note_type 12, 14, 1
	note G_, 2
	note D#, 6
	note D_, 2
	note D_, 8
	note C_, 2
	octave 3
	note A#, 2
	note A_, 2
	note G_, 2
	octave 4
	note D_, 2
	note C_, 2
	octave 3
	note A#, 2
	note A_, 2
	note G_, 10
	note G_, 2
	note A_, 2
	note A#, 2
	octave 4
	note C_, 8
	note D_, 6
	note C_, 2
	octave 3
	note A#, 8
	rest 2
	note G_, 2
	note A_, 2
	note A#, 2
	octave 4
	note C_, 4
	note C_, 4
	note D_, 6
	note C_, 1
	note D_, 1
	octave 3
	note A#, 8
	rest 2
	note A#, 2
	note A_, 2
	note G_, 2
	note A_, 8
	note D#, 4
	note A#, 4
	note A_, 8
	note G_, 4
	note D#, 4
	note F_, 8
	note G_, 4
	note A#, 4
	note A#, 8
	note A_, 8
	sound_loop 0, .mainloop

	sound_ret ; unused

Music_PalletTown_Ch3::
; Pokémon Purple: was the busiest arpeggiated line in the piece (the main
; source of the original's "skipping/bumping" feel) -- thinned to roughly
; half as many attacks, each held twice as long.
	vibrato 20, 5, 5
	note_type 12, 3, 1
.mainloop:
	octave 3
	note G_, 12
	note F_, 4
	note G_, 12
	note A_, 4
	note D#, 12
	note F_, 4
	note G_, 12
	note D#, 4
	note G_, 12
	note F_, 4
	note G_, 12
	note A_, 4
	note D#, 12
	note A_, 4
	note G_, 12
	note D#, 4
	note C_, 8
	note D_, 8
	note G_, 8
	note D#, 4
	note D_, 4
	note C_, 8
	note D_, 8
	note G_, 8
	note A_, 4
	note G_, 4
	note D#, 8
	note A_, 8
	note D#, 8
	note G_, 8
	note F_, 8
	note D#, 8
	note D#, 8
	note F_, 8
	sound_loop 0, .mainloop

	sound_ret ; unused
