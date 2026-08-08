# Kanto Walkthrough — Base Game Route

*Transcribed from `PrimaPokemon Guide.pdf` (Prima's Official Strategy Guide, Red/Blue, 1998) — its "A Walk Through the World of Pokémon" section, pages 7–60 of the book (PDF pages 9–62). This is the master reference for **what the vanilla game actually contains, area by area, in play order** — use it to plan any remaining content work, in either this ROM hack or [[Godot Port - Progress|the Godot port]], without having to re-derive the base game's structure from memory or from the ROM disassembly directly.*

*Vanilla facts only below unless a line is explicitly marked **Purple:** — this fork changes several of the systems the guide assumes. See "How Purple diverges" up front before using this as a checklist for either project.*

## How Purple diverges from this walkthrough

Read this before treating any line below as "what to build/verify":

- **No 3-way starter choice** (item 6). Every ball in Oak's Lab gives **EEVEE**. The guide's "choose Bulbasaur/Charmander/Squirtle" step, and every downstream "which starter did you pick" branch (the Rival's team, TM/HM order convenience, type-matchup advice), doesn't apply — Purple's Rival always starts with Eevee too, evolving into Jolteon/Flareon/Vaporeon (or staying Eevee) from his 2nd battle onward, rolled once per save.
- **No free starting stones** — replaced by the **cultist dream** (item 8): a Red's House 2F sequence, before the player's first real step, that commits them to Fire/Water/Thunder Stone based on 3 branching answers. The guide's own Celadon Dept. Store 4F stone purchases are also removed (CLAUDE.md item 8's "closing the loophole") — stones are Eevee-only and permanent via the dream alone.
- **Permadeath** (item 1): a fainted Pokémon is gone for good (`RIP`, not `FNT`). This changes the *feel* of every trainer/wild fight below, though not the underlying map/event structure — the guide's "don't worry, you can always heal at a Pokémon Center" framing needs a mental asterisk throughout.
- **Hidden power tiers** (item 5): gym leaders roll tier 6–8 live; regular trainers/wild Pokémon roll their own tier (wild weighted low); every gift/starter/fossil/trade Pokémon stays neutral (tier 5). The exact levels below are still correct — tiers modify stats, not levels.
- **Flattened wild tables, single ROM** (item 3): the guide's separate Red/Blue "Any Pokémon?" columns are moot here — Purple only builds one ROM with both versions' species available (at reduced rate) in the same wild list. Don't treat the Red-only/Blue-only species split below as still meaningful for *this* fork; it's meaningful only as a record of what vanilla had to work with.
- **Smarter trainer AI** (item 10) sharpens move choice and switch-in logic for exactly the roster this walkthrough calls out as "Gym Leader" / "Elite Four" / rival's 2nd-3rd battles — the trainer data (species/levels) below is unchanged, only how they play it.
- **Kanto Reborn** (item 12, in progress): 89 Gen 2 species have been imported into the wild tables and are catchable alongside the roster below, at reduced frequency — the guide's "Any Pokémon?" lists per area are the Gen-1-only baseline this was layered on top of, not the current in-game encounter table (see [[Encounter Map - Locations & Rates]] for what's actually live now).
- **Gothic text rewrite** (item 2): every NPC line the guide paraphrases has been rewritten in Victorian-gothic register in this fork. The guide's dialogue summaries below are for *event structure* (who says what happens, in what order), not actual in-game text — see `text/<Map>.asm` for what's really shown.
- **Godot port status**: as of this note, only Pallet Town, Red's House 1F/2F, and Oak's Lab are ported and script-wired (verified end-to-end, see [[Godot Port - Progress]]). Every other area below — Route 1 (partially, as far as the stitched overworld already renders it) onward — has, at most, its map/tile data exported and nothing else; none of its NPCs, items, trainers, or story beats have a MapScript yet.

## Quick-reference: gym leaders & Elite Four (species/levels, vanilla)

Tiers/AI differ in Purple; species and levels below are what the ROM actually ships (confirmed against `data/trainers/parties.asm` if you need to cross-check — the guide and the ROM should agree since Purple didn't touch base trainer rosters).

| Trainer | Team | Reward |
|---|---|---|
| Brock (Pewter) | Geodude 12, Onix 14 | Boulder Badge, TM34 Bide |
| Misty (Cerulean) | Staryu 18, Starmie 21 | Cascade Badge, TM11 Bubble Beam |
| Lt. Surge (Vermilion) | Voltorb 21, Pikachu 18, Raichu 24 | Thunder Badge, TM24 Thunderbolt |
| Erika (Celadon) | Victreebel 29, Tangela 24, Vileplume 29 | Rainbow Badge, TM21 Mega Drain |
| Koga (Fuchsia) | Koffing 37, Muk 39, Koffing 37, Weezing 43 | Soul Badge, TM06 Toxic |
| Sabrina (Saffron) | Kadabra 38, Mr. Mime 37, Venomoth 38, Alakazam 43 | Marsh Badge, TM46 Psywave |
| Blaine (Cinnabar) | Growlithe 42, Ponyta 40, Rapidash 42, Arcanine 47 | Volcano Badge, TM38 Fire Blast |
| Giovanni (Viridian, 8th/last) | Rhyhorn 45, Dugtrio 42, Nidoqueen 44, Nidoking 45, Rhydon 50 | Earth Badge, TM27 Fissure |
| Lorelei (E4 #1) | Dewgong 54, Cloyster 53, Slowbro 54, Jynx 56, Lapras 56 | — |
| Bruno (E4 #2) | Onix 53, Hitmonchan 55, Hitmonlee 55, Onix 56, Machamp 58 | — |
| Agatha (E4 #3) | Gengar 56, Golbat 56, Haunter 55, Arbok 58, Gengar 60 | — |
| Lance (E4 #4) | Gyarados 58, Dragonair 56, Dragonair 56, Aerodactyl 60, Dragonite 62 | — |
| Rival (final, Champion) | Pidgeot 61 + a starter-themed trio (his evolved starter, Exeggutor, Gyarados/Arcanine) around LV61-65 | — |

Note Viridian's gym is the **8th and last** badge, not the 2nd — it's locked until you've beaten the other seven, and Giovanni doubles as the Team Rocket boss you meet earlier in Mt. Moon/Rocket Hideout/Silph Co.

## The route, area by area, in play order

Each entry: **Things To Do** (story beats/events), **Get** (key items — TMs/HMs/badges/plot items; ordinary wild-catch/shop items omitted), **Leads to**.

### Pallet Town (start)
- Do: choose a Pokémon at Oak's Lab **(Purple: always Eevee, all 3 balls)**; later, deliver Oak's Parcel to Oak for a Pokédex; get a Town Map from the Rival's sister.
- Get: Potion (home), Town Map, Pokédex.
- Leads to: Route 1 → Viridian City.

### Route 1
- Get: Potion.

### Viridian City (1st visit)
- Do: pick up Oak's Parcel at the Poké Mart. Gym is closed (it's the 8th badge, see above).
- Get: Oak's Parcel.
- Leads to: back to Pallet Town to deliver the parcel, then out again via Route 1 → Route 2 → Viridian Forest → Pewter City.

### Route 2 / Viridian Forest
- Do: 3 bug trainers in the forest (Weedle/Caterpie/Kakuna, LV6-9).
- Get: Poké Ball, Antidote, Potion (forest); HM05 Flash + HP Up + Moon Stone are gated behind Route 2's *other* side, reached later via Diglett's Cave from the Vermilion side (Cut needed either way).
- Leads to: Pewter City.

### Pewter City
- Do: defeat **Brock** (Boulder Badge, TM34); visit the Pewter Museum of Science; get the Old Amber there.
- Get: Boulder Badge, TM34 Bide, Old Amber (Aerodactyl fossil).
- Leads to: Route 3 → Mt. Moon.

### Route 3 → Mt. Moon → Route 4
- Do: Mt. Moon has Team Rocket digging for fossils on B2; a Super Nerd guards the Dome/Helix Fossil choice on B2.
- Get (Mt. Moon): Potion x2, TM12 Water Gun, Rare Candy, Escape Rope, Moon Stone, HP Up, TM01 Mega Punch, **Dome Fossil or Helix Fossil (pick one)**.
- Get (Route 4): TM04 Whirlwind.
- Leads to: Cerulean City.

### Cerulean City
- Do: defeat **Misty** (Cascade Badge, TM11); Nugget Bridge (5 Rocket trainers) and the "Practice Area" (Hikers) on Routes 24/25 to reach Bill's House; help **Bill** at his house for the S.S. Ticket; trade a Poliwhirl for a Jynx; buy the Bicycle with the Bike Voucher (received later, from Vermilion's Fan Club).
- Get: Cascade Badge, TM11 Bubble Beam, TM28 Dig (from a Rocket behind a burgled house), Nugget, TM45 Thunder Wave, TM19 Seismic Toss, S.S. Ticket, Bicycle.
- Leads to: Routes 24/25 (Bill's House, dead end) → back through Cerulean → Route 5/Underground Path/Route 6 → Vermilion City; **or** later, Route 4 → Rock Tunnel → Lavender Town.

### Route 5 / Route 6 / Underground Path (Cerulean↔Vermilion)
- Get: nothing notable (Daycare Center is on the field between the two roads).
- Leads to: Vermilion City.

### Vermilion City
- Do: get **HM01 Cut** from the S.S. Anne's Captain (after helping him with seasickness aboard); defeat **Lt. Surge** (Thunder Badge, TM24) — his gym is electrically locked, needs 2 switches found via trainer battles; talk to the Pokémon Fan Club president for the Bike Voucher; trade a Spearow for a Farfetch'd; get the Old Rod from the Fishing Guru.
- Get: Bike Voucher, Old Rod, Thunder Badge, TM24 Thunderbolt, HM01 Cut (via S.S. Anne).
- S.S. Anne (docked at Vermilion): ~17 trainers LV17-23; the Captain's own battle gates HM01.
- Leads to: Route 11 → Diglett's Cave (needs Snorlax on Route 12 out of the way first, or go around) → back to Route 2's other side, **or** Route 6 → Cerulean → Route 9/Rock Tunnel → Lavender.

### Route 11 / Diglett's Cave
- Get (Route 11): TM08 Body Slam, Great Ball, Max Ether, Rare Candy, HM01 (redundant pickup point per guide layout), TM44 Rest, Ether, Max Potion, Itemfinder (from Oak's Aide after catching 30 species).
- Diglett's Cave: shortcut between Vermilion and Route 2's west side (near Pewter/Viridian Forest); needs Cut in from one side.

### Route 9 → Rock Tunnel → Route 10
- Get (Route 9): TM30 Teleport.
- Rock Tunnel: needs HM05 Flash (or fight blind). No key items on 1F/B1.
- Leads to: Lavender Town.

### Lavender Town
- Do: use the **Silph Scope** (from Celadon's Rocket Hideout — this is out of order per the "quick path," Lavender is often revisited after Celadon) to see through Pokémon Tower's ghosts; rescue **Mr. Fuji**, get the Poké Flute; visit the Name Rater if you need to fix a nicknamed evolution.
- Get: Poké Flute. Pokémon Tower items: Escape Rope, HP Up, Awakening, Elixir, Nugget, X Accuracy, Rare Candy. A wild Cubone/mother Marowak ghost fight on 7F.
- Leads to: Route 8 (underground path to Saffron) or Route 7 (from Celadon side).

### Route 7 / Route 8 (Lavender↔Saffron↔Celadon)
- Get: nothing notable — a guarded roadblock on Route 8 needs a Soda Pop to pass (bought from Celadon Dept. Store vending machines, **Purple: still present, unrelated to the removed stone purchases**).

### Celadon City
- Do: defeat **Erika** (Rainbow Badge, TM21); get a rare Eevee from Celadon Mansion's secret room; get a Coin Purse from the Bar; visit the Game Corner and the Rocket Hideout beneath it for the **Silph Scope** and Giovanni's boss fight (Team Rocket leader, 1st encounter — LV24-29 Ground/Rock team); shop the big Department Store (stones sold on 4F in vanilla — **Purple: removed**, see above).
- Get: Rainbow Badge, TM21 Mega Drain, Silph Scope, Coin Purse, TM13 Ice Beam, TM18 Counter, TM41 Softboiled, TM48 Rock Slide, TM49 Tri Attack. Rocket Hideout: Escape Rope, Hyper Potion, Nugget, TM07 Horn Drill, Moon Stone, Super Potion, Rare Candy, TM10 Double-Edge, Lift Key, TM02 Razor Wind, HP Up.
- Leads to: back to Lavender (Poké Tower) with the Silph Scope, then onward to Saffron.

### Route 16 / 17 / 18 (Cycling Road)
- Do: wake the Snorlax blocking the road (needs Poké Flute); get **HM02 Fly** from a house past it.
- Get: HM02 Fly.
- Leads to: Fuchsia City (south end of Cycling Road).

### Saffron City
- Do: defeat the head of the **Fighting Dojo** (choice of a Hitmonlee or Hitmonchan as reward, instead of a badge); rescue Silph Co.'s President from Team Rocket (2nd Giovanni fight, tougher, LV~35-41) and receive the **Master Ball**; defeat **Sabrina** (Marsh Badge, TM46) — her gym is teleport-pad-based.
- Get: Marsh Badge, TM46 Psywave, TM29 Psychic, TM31 Mimic (from a girl if you trade her a Poké Doll from Celadon), Master Ball. Silph Co. (11 floors, ~30 trainers LV25+): TM36 Self-Destruct, Hyper Potion, Escape Rope, Max Revive, Full Heal, Key Card, Protein, TM09 Take Down, HP Up, X Accuracy, TM03 Swords Dance, Calcium, Carbos, Rare Candy, TM26 Earthquake, Master Ball.
- Leads to: Route 5 (underground to Cerulean, already used) or Route 7 → Celadon; via Route 8 back to Lavender.

### Route 12 / 13 / 14 / 15
- Do: another sleeping Snorlax on Route 12 (Poké Flute again).
- Get: TM16 (per guide listing — verify against `data/moves/tm_prices.asm`/`data/pokemon/tmhm.asm` before relying on this one, guide OCR was ambiguous here), Super Rod (Route 12, from a Fishing Guru's brother), Iron, TM20 + Exp. All (Routes 14/15, after collecting 50 species).
- Leads to: Fuchsia City.

### Fuchsia City
- Do: defeat **Koga** (Soul Badge, TM06); get the Good Rod; get **HM04 Strength** from the Safari Zone's Game Warden (trade Gold Teeth for it); visit the **Safari Zone**.
- Get: Soul Badge, TM06 Toxic, Good Rod, HM04 Strength. Safari Zone: Nugget, Carbos, TM37 Egg Bomb, Max Potion, Full Restore, TM40 Skull Bash, Protein, Gold Teeth, Max Revive, TM32 Double Team, **HM03 Surf** (from the Area 3 contest house, within the time limit).
- Leads to: Route 19/20 → Seafoam Islands → Cinnabar Island.

### Route 19 / 20 / Seafoam Islands
- Do: legendary **Articuno** at the bottom of Seafoam Islands (needs Surf to reach, and to solve a boulder/current puzzle on the last 2 floors).
- Get: nothing notable besides Articuno itself.
- Leads to: Cinnabar Island.

### Cinnabar Island
- Do: resurrect your fossil at the **Pokémon Lab**; find the **Secret Key** in the (Burglar-infested) Pokémon House to unlock the Gym; defeat **Blaine** (Volcano Badge, TM38).
- Get: Secret Key, Volcano Badge, TM38 Fire Blast, TM35 Metronome. Pokémon House: Escape Rope, Carbos, Calcium, Max Potion, Iron, Rare Candy, TM22 Solarbeam, Full Restore, TM14 Blizzard.
- Leads to: Route 21 (Surf) → Pallet Town.

### Route 21 → Pallet Town → Route 1 → Viridian City
- Get: nothing further notable on Route 21 itself (a duplicate-looking item list in the guide's own layout appears to be a Pokémon House carryover, not a genuine second cache — don't double-count it).

### Viridian City (final visit)
- Do: defeat **Giovanni** at the Viridian Gym — his true 3rd and final appearance, now revealed as Gym Leader (Earth Badge, TM27 Fissure). This is the **8th and last badge**.
- Get: Earth Badge, TM27 Fissure.
- Leads to: Route 22 → Route 23 → Victory Road (all 8 badges required past Route 23's guard checkpoint).

### Route 22 / Route 23
- Do: **Rival battle** on Route 22 (already fought the Elite Four once in his own playthrough, per guide flavor text — a warm-up/skill-check fight before the player's own run at them). **Purple: this is the "2nd wave" Rival encounter, item 6 — his Eevee has evolved by now** per the rolled `wRivalStarter`.
- Get: nothing notable.
- Leads to: Victory Road → Indigo Plateau.

### Victory Road
- Do: puzzle dungeon (boulders on pressure plates hold doors open — 2 routes through, both reach the far end); legendary **Moltres** at the end.
- Get: Rare Candy, TM43 Sky Attack, TM05 Mega Kick, Full Heal, TM17 Submission, Guard Spec, Max Revive, Full Restore.
- Leads to: Indigo Plateau.

### Indigo Plateau — the Elite Four + Champion
- Do: **Lorelei → Bruno → Agatha → Lance**, back-to-back with no way to leave and restock mid-run (Pokémon Center access before entering); then the **final Rival battle** (Champion). Winning ends the game, roll credits, and unlocks Hall of Fame.
- Get: nothing new — merchandise here is just the usual mart goods at Cerulean-tier prices.
- Aftermath: game doesn't truly end — save restarts at Pallet Town's Pokémon Center, free to keep exploring/catching, replay the Elite Four endlessly, etc.

### Post-game / bonus (not part of the critical path)
- **Power Plant** (via Surf from Route 10's area, near Cerulean): legendary **Zapdos**, plus dense Electric-type wilds.
- Not transcribed in detail here (guide's own walkthrough section ends at the Elite Four, page 60/PDF 62) — see the guide's per-Pokémon movelist/Pokédex sections (PDF pages 64+) if deeper reference is ever needed.

## What this unlocks for planning

- **Godot port Phase 6+ map order**, if following the natural play sequence: Route 1 (stitching already exists) → Viridian City → Route 2/Viridian Forest → Pewter City → ... — i.e. this table doubles as the map-script build queue, in the order a real player would actually reach them, so each new area is reachable/testable the moment it's built rather than needing later areas stubbed in first.
- **Which of Purple's changes need a script-level decision per area**, not just data: Oak's Parcel/Pokédex (Viridian↔Pallet loop) is the very next thing after Phase 5's "Gary fight ends," and per CLAUDE.md's own item 12 roadmap note, that's exactly the deferred Phase 6 content.
- **A sanity check for existing ROM-hack trainer/item work** — cross-reference any future gym/Elite Four rebalancing discussion against the vanilla baseline table above rather than reconstructing it from `data/trainers/parties.asm` each time.

## Related
- [[Godot Port - Progress]] · [[Port Plan]] · [[Roadmap & Ideas]]
- [[Encounter Map - Locations & Rates]] — the *current*, Purple-and-Kanto-Reborn-accurate wild encounter data (this note's "Any Pokémon?" lists are the vanilla baseline only)
- [[Architecture Map]] — where `scripts/<Map>.asm` / `text/<Map>.asm` actually live for each area named above
