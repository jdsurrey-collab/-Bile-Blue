# Industrial-Goth Score

**Status:** 🔄 In progress — 5 tracks converted, rest of the OST still vanilla

## Summary
The soundtrack is being redone track by track into original, dark, minor-key compositions with a driving industrial pulse — mood-inspired (brief: "something like Marilyn Manson's *Sweet Dreams (Are Made of This)* cover"), **never a transcription of any real copyrighted song**. Only mood/genre hallmarks get borrowed (relentless minor-key ostinato bass, sparse haunting lead, heavier duty-cycle tone), not actual melodies.

## Tracks converted so far

| Track | File | Treatment |
|---|---|---|
| `Music_TitleScreen` | `audio/music/titlescreen.asm` | First one done — established the technique. First pass just recolored the melody into minor and read as "the original, but lower"; the version that stuck was a full from-scratch recompose keeping only the note-length/rest skeleton for cross-channel sync. |
| `Music_Routes2` | `audio/music/routes2.asm` (plays during Oak's intro/naming) | Parallel-minor conversion of the existing melody — the lighter-touch version of the technique, no full recompose needed. |
| `Music_WildBattle` / `Music_TrainerBattle` | `audio/music/wildbattle.asm`, `trainerbattle.asm` | **Exception to the key-conversion approach** — already tense/chromatic in the original (Gen 1 battle themes lean dissonant by design), so nothing to flatten. Only tempo/duty-cycle/vibrato touched; pitch untouched (`Music_TrainerBattle` alone is ~1850 lines — not a safe hand-edit target with no audio preview regardless). |
| `Music_PalletTown` | `audio/music/pallettown.asm` | Most aggressive rework: parallel-minor + a full octave dropped + drastic tempo cut + rhythm thinning (adjacent short repeated notes pairwise-merged, exactly halving attack rate on the busiest channel while preserving total duration). Brief was specifically "much much slower... less skipping and bumping" — tempo/register/key alone reads as "slower," not "less bouncy"; the rhythm itself had to change too. |
| `Music_OaksLab` | `audio/music/oakslab.asm` (Oak's "choose your Pokémon" speech) | Same sustained-brooding treatment as Pallet Town (parallel minor + octave drop + tempo cut), **not** the horror treatment — has to carry a long dialogue scene, that much silence would feel like the music cut out. |

Also converted (horror stinger, distinct from the above list's melodic tracks):

| Track | File | Treatment |
|---|---|---|
| `Music_MeetProfOak` | `audio/music/meetprofoak.asm` (Oak stops you from walking into the grass) | Full from-scratch rewrite for genuine horror: gutted to isolated low notes separated by long silence, built around a deliberate tritone (B against F natural), volume pulled down throughout. The 3 channels are **deliberately not length-matched** here — letting them drift out of phase reads as unpredictable/wrong, which suits a horror stinger (would sound broken on a driving battle theme). |

**Everything else in the OST is still the bright vanilla original.** See [[Roadmap & Ideas]] for candidate next tracks.

## The reusable technique

- **Key**: parallel-minor conversion is the default move — flatten the major 3rd/6th/7th relative to the original's major key (e.g. G major→G minor is B→A#, E→D#, F#→F) and leave the rest. Preserves contour/rhythm while genuinely darkening color. A chromatic secondary-dominant leading tone is usually still valid tension in the parallel minor and worth keeping. **Skip this step** if the source is already tense/chromatic (see battle themes above).
- **Octave-shifting via find-replace is order-dependent and will silently corrupt notes** if done carelessly — naively replacing `octave 4`→`octave 3` then `octave 3`→`octave 2` in two passes re-shifts the first pass's own output. Use a placeholder string per source octave first, or rewrite from an already-read copy in one pass. Bit `Music_OaksLab` mid-edit once; caught only because the build was checked afterward, not because anything would flag it automatically — a wrong octave compiles fine.
- **Channel roles for a fresh recompose**: channel 3 (wave) = driving root-fifth ostinato pulse, the single biggest lever for "industrial" feel; channel 1 (pulse, `duty_cycle 1`) = sparser haunting lead; channel 2 (pulse, `duty_cycle 2`) = harmony fill, favoring safe tonic/dominant/minor-3rd tones so it stays consonant without individual verification against channel 1; channel 4 (noise/drums) usually doesn't need to change.
- **Timbre**: slower tempo (larger `tempo` value), deeper `vibrato`, `note_type` envelopes tuned for sustained/droning character. For genuine horror rather than "sad," also pull master `volume` and per-note envelope volumes down, lean on rests/silence.
- **"Less skipping/bumping" needs rhythm change, not just tempo.** Slowing a busy, evenly-subdivided rhythm down doesn't remove its bounciness — pairwise-merge adjacent short notes into fewer longer ones (merging two notes of length N into one of length 2N preserves total duration exactly, so sync is untouched, while genuinely halving attack rate).
- **When adapting an existing track**, keep every channel's exact note-length/rest/`sound_call`/`sound_loop` skeleton identical to the source, only change pitch/duty/envelope/tempo — guarantees the 4 channels stay in sync without needing to verify by ear. When composing fresh, keep each channel's own note-length arithmetic internally consistent — except when the goal is deliberately unsettling (see `Music_MeetProfOak`), where letting channels drift is a feature.
- **No audio playback in this working environment** — every change is composed blind, never verified by ear before being handed off. Treat first attempts as a draft; expect an iteration round based on what it actually sounds like once played.

## Related
- [[Roadmap & Ideas]] — candidate next tracks to convert
- [[Build & Versioning]] — how to get a build to actually listen to a track
