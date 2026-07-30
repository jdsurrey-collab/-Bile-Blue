Music_MeetProfOak_Ch1::
; Pokémon Purple: this was a bright, declarative "Oak stops you!" fanfare --
; rewritten from scratch as something genuinely unsettling instead of just
; darkened. Sparse, low, dissonant (B against an F natural -- a tritone,
; the classic "wrong" interval), heavily toned down in volume, mostly
; silence. Deliberately NOT kept in lockstep with Ch2/Ch3 below -- letting
; the three drift in and out of phase against each other is what makes it
; feel unpredictable rather than just slow.
	tempo 240
	volume 6, 6
	duty_cycle 0
	note_type 12, 7, 2
	octave 2
	note B_, 8
	rest 12
	note F_, 6
	rest 14
.mainloop:
	note C_, 4
	rest 16
	note B_, 10
	rest 10
	note F_, 6
	rest 16
	note B_, 4
	rest 20
	sound_loop 0, .mainloop

Music_MeetProfOak_Ch2::
; low sustained drone, occasionally clashing against Ch1
	vibrato 20, 5, 3
	duty_cycle 1
	note_type 12, 5, 1
	octave 2
	note F_, 16
	rest 16
.mainloop:
	note F_, 24
	rest 8
	note C_, 16
	rest 16
	octave 1
	note B_, 20
	rest 12
	octave 2
	note F_, 16
	rest 24
	sound_loop 0, .mainloop

Music_MeetProfOak_Ch3::
; distant, irregular heartbeat -- two low thuds, then a long uneasy silence
	note_type 12, 3, 0
	octave 2
	rest 16
.mainloop:
	note B_, 2
	rest 6
	note B_, 2
	rest 20
	note F_, 2
	rest 6
	note F_, 2
	rest 24
	sound_loop 0, .mainloop
