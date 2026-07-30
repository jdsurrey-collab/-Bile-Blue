DEF tier_chance_num = MIN_TIER
DEF tier_chance_total = 0

MACRO tier_chance
	DEF tier_chance_total += \1
	db tier_chance_total - 1
	db tier_chance_num
	DEF tier_chance_num += 1
ENDM

WildTierChances:
; Pokémon Purple: rarity table for a wild-caught mon's hidden power tier.
; Walked the same way as WildMonEncounterSlotChances (engine/battle/wild_encounters.asm):
; roll a random byte, find the first entry whose cumulative threshold is >= it.
	table_width 2
	tier_chance 90 ; 90/256 = 35.2% chance of tier 1
	tier_chance 51 ; 51/256 = 19.9% chance of tier 2
	tier_chance 36 ; 36/256 = 14.1% chance of tier 3
	tier_chance 26 ; 26/256 = 10.2% chance of tier 4
	tier_chance 18 ; 18/256 =  7.0% chance of tier 5 (base)
	tier_chance 13 ; 13/256 =  5.1% chance of tier 6
	tier_chance  9 ;  9/256 =  3.5% chance of tier 7
	tier_chance  6 ;  6/256 =  2.3% chance of tier 8
	tier_chance  4 ;  4/256 =  1.6% chance of tier 9
	tier_chance  3 ;  3/256 =  1.2% chance of tier 10
	assert_table_length MAX_TIER
	ASSERT tier_chance_total == 256, "WildTierChances sum to {d:tier_chance_total}, not 256!"
