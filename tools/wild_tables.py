#!/usr/bin/env python3
"""
"Kanto Reborn" wild encounter tables for Pokemon Purple.

Rewrites data/wild/maps/*.asm so location actually matters and the 89 imported
Gen 2 species are catchable.

HOW RARITY WORKS HERE: each table has exactly NUM_WILDMONS (10) slots, and
data/wild/probabilities.asm gives each SLOT a fixed chance:

    slot 0  19.9% | slot 3  9.8% | slot 6  5.1% | slot 9  1.2%
    slot 1  19.9% | slot 4  9.8% | slot 7  5.1%
    slot 2  15.2% | slot 5  9.8% | slot 8  4.3%

So rarity is expressed purely by ORDER: earliest = commonest, last = the
"holy shit" slot. Tables below are written most-common-first, which is why the
marquee species always sits in slot 9.

Encounter rate (the def_grass_wildmons argument) is how often grass triggers a
battle at all, and is kept at each map's vanilla value.
"""
import os
import re

# Derived from this file's location so the tools work from any checkout.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS = os.path.join(ROOT, "data/wild/maps")

# map file -> [(level, species)] x10, ordered common -> rare.
T = {
"Route1": [(3,"PIDGEY"),(3,"RATTATA"),(4,"SENTRET"),(2,"RATTATA"),(4,"PIDGEY"),
           (3,"HOPPIP"),(5,"SPEAROW"),(4,"LEDYBA"),(5,"PICHU"),(5,"EEVEE")],
"Route2": [(4,"RATTATA"),(4,"PIDGEY"),(5,"CATERPIE"),(5,"WEEDLE"),(4,"SENTRET"),
           (5,"NIDORAN_F"),(5,"NIDORAN_M"),(6,"BELLSPROUT"),(6,"HOOTHOOT"),(6,"BULBASAUR")],
"ViridianForest": [(4,"CATERPIE"),(4,"WEEDLE"),(5,"METAPOD"),(5,"KAKUNA"),(5,"PIKACHU"),
                   (6,"ODDISH"),(6,"SPINARAK"),(6,"PARAS"),(7,"HERACROSS"),(7,"SCYTHER")],
"Route3": [(7,"SPEAROW"),(7,"NIDORAN_M"),(8,"NIDORAN_F"),(8,"JIGGLYPUFF"),(9,"MANKEY"),
           (8,"EKANS"),(9,"CLEFFA"),(9,"VULPIX"),(10,"CHARMANDER"),(10,"FARFETCHD")],
"MtMoon1F": [(8,"ZUBAT"),(8,"GEODUDE"),(9,"PARAS"),(9,"CLEFAIRY"),(10,"SANDSHREW"),
             (10,"RHYHORN"),(11,"MACHOP"),(11,"ONIX"),(12,"SLUGMA"),(12,"DRATINI")],
"MtMoonB1F": [(9,"ZUBAT"),(9,"GEODUDE"),(10,"PARAS"),(10,"CLEFAIRY"),(11,"SANDSHREW"),
              (11,"MAREEP"),(12,"MACHOP"),(12,"ONIX"),(13,"OMANYTE"),(13,"KABUTO")],
"MtMoonB2F": [(10,"ZUBAT"),(10,"GEODUDE"),(11,"PARAS"),(11,"CLEFAIRY"),(12,"RHYHORN"),
              (12,"SLUGMA"),(13,"MACHOP"),(13,"ONIX"),(14,"OMANYTE"),(14,"DRATINI")],
"Route4": [(10,"RATTATA"),(10,"SPEAROW"),(11,"EKANS"),(11,"SANDSHREW"),(12,"MANKEY"),
           (12,"MEOWTH"),(12,"SNUBBULL"),(13,"VULPIX"),(13,"PONYTA"),(13,"SQUIRTLE")],
"Route24": [(11,"BELLSPROUT"),(11,"ODDISH"),(12,"ABRA"),(12,"VENONAT"),(13,"CATERPIE"),
            (13,"HOPPIP"),(13,"PSYDUCK"),(14,"SLOWPOKE"),(14,"MAREEP"),(15,"DRATINI")],
"Route25": [(12,"BELLSPROUT"),(12,"ODDISH"),(13,"ABRA"),(13,"VENONAT"),(14,"WEEDLE"),
            (14,"SENTRET"),(14,"PSYDUCK"),(15,"SUNKERN"),(15,"AIPOM"),(16,"BULBASAUR")],
"Route5": [(13,"MEOWTH"),(13,"PIDGEY"),(14,"GROWLITHE"),(14,"VULPIX"),(15,"ODDISH"),
           (15,"BELLSPROUT"),(15,"SNUBBULL"),(16,"ABRA"),(16,"CUBONE"),(17,"EEVEE")],
"Route6": [(13,"MEOWTH"),(13,"PIDGEY"),(14,"GROWLITHE"),(14,"VULPIX"),(15,"PSYDUCK"),
           (15,"BELLSPROUT"),(15,"MARILL"),(16,"ABRA"),(16,"CUBONE"),(17,"GASTLY")],
"Route7": [(16,"GROWLITHE"),(16,"VULPIX"),(17,"MEOWTH"),(17,"PIDGEOTTO"),(18,"NATU"),
           (18,"GASTLY"),(18,"PONYTA"),(19,"DODUO"),(19,"MR_MIME"),(20,"KANGASKHAN")],
"Route8": [(16,"GROWLITHE"),(16,"VULPIX"),(17,"MEOWTH"),(17,"PIDGEOTTO"),(18,"ABRA"),
           (18,"GASTLY"),(18,"GIRAFARIG"),(19,"TANGELA"),(19,"DITTO"),(20,"CHANSEY")],
"Route9": [(15,"VOLTORB"),(15,"MAGNEMITE"),(16,"FEAROW"),(16,"RATICATE"),(17,"PIKACHU"),
           (17,"MAREEP"),(18,"ELEKID"),(18,"PONYTA"),(19,"GRAVELER"),(19,"TAUROS")],
"Route10": [(16,"VOLTORB"),(16,"MAGNEMITE"),(17,"FEAROW"),(17,"RATICATE"),(18,"PIKACHU"),
            (18,"CHINCHOU"),(19,"ELEKID"),(19,"FLAAFFY"),(20,"GRAVELER"),(20,"ELECTRODE")],
"RockTunnel1F": [(16,"ZUBAT"),(16,"GEODUDE"),(17,"MACHOP"),(17,"GRAVELER"),(18,"ONIX"),
                 (18,"RHYHORN"),(19,"CUBONE"),(19,"TEDDIURSA"),(20,"MAROWAK"),(20,"HITMONCHAN")],
"RockTunnelB1F": [(17,"ZUBAT"),(17,"GEODUDE"),(18,"MACHOP"),(18,"GRAVELER"),(19,"ONIX"),
                  (19,"PHANPY"),(20,"CUBONE"),(20,"SWINUB"),(21,"MAROWAK"),(21,"KANGASKHAN")],
"Route11": [(14,"DROWZEE"),(14,"EKANS"),(15,"SANDSHREW"),(15,"SPEAROW"),(16,"RATICATE"),
            (16,"NIDORINO"),(17,"NIDORINA"),(17,"DUNSPARCE"),(18,"HYPNO"),(18,"FARFETCHD")],
"DiglettsCave": [(18,"DIGLETT"),(18,"DIGLETT"),(19,"DUGTRIO"),(19,"GEODUDE"),(20,"PHANPY"),
                 (20,"RHYHORN"),(21,"SANDSLASH"),(21,"MAROWAK"),(22,"ONIX"),(22,"DONPHAN")],
"Route12": [(24,"VENONAT"),(24,"ODDISH"),(25,"PIDGEOTTO"),(25,"GLOOM"),(26,"HOPPIP"),
            (26,"YANMA"),(27,"TANGELA"),(27,"DODUO"),(28,"SCYTHER"),(28,"SNORLAX")],
"Route13": [(24,"VENONAT"),(24,"ODDISH"),(25,"PIDGEOTTO"),(25,"GLOOM"),(26,"SKIPLOOM"),
            (26,"YANMA"),(27,"TANGELA"),(27,"DODRIO"),(28,"PINSIR"),(28,"CHANSEY")],
"Route14": [(25,"VENOMOTH"),(25,"WEEPINBELL"),(26,"PIDGEOTTO"),(26,"GLOOM"),(27,"SKIPLOOM"),
            (27,"STANTLER"),(28,"TANGELA"),(28,"DODRIO"),(29,"SCYTHER"),(29,"DRATINI")],
"Route15": [(25,"VENOMOTH"),(25,"WEEPINBELL"),(26,"FEAROW"),(26,"GLOOM"),(27,"JUMPLUFF"),
            (27,"STANTLER"),(28,"TANGELA"),(28,"DODRIO"),(29,"PINSIR"),(29,"DRAGONAIR")],
"Route16": [(22,"RATTATA"),(22,"SPEAROW"),(23,"RATICATE"),(23,"FEAROW"),(24,"DODUO"),
            (24,"SNUBBULL"),(25,"GRIMER"),(25,"MURKROW_PLACEHOLDER"),(26,"GRANBULL"),(26,"SNORLAX")],
"Route17": [(24,"RATICATE"),(24,"FEAROW"),(25,"DODUO"),(25,"PONYTA"),(26,"DODRIO"),
            (26,"GRANBULL"),(27,"RAPIDASH"),(27,"MAGBY"),(28,"TAUROS"),(28,"MILTANK")],
"Route18": [(25,"RATICATE"),(25,"FEAROW"),(26,"DODUO"),(26,"PONYTA"),(27,"DODRIO"),
            (27,"GRANBULL"),(28,"RAPIDASH"),(28,"MAGBY"),(29,"TAUROS"),(29,"MILTANK")],
"Route21": [(26,"TENTACOOL"),(26,"PIDGEY"),(27,"RATTATA"),(27,"PIDGEOTTO"),(28,"TANGELA"),
            (28,"MARILL"),(29,"RATICATE"),(29,"QWILFISH"),(30,"CORSOLA"),(30,"MANTINE")],
"Route22": [(4,"RATTATA"),(4,"NIDORAN_M"),(5,"SPEAROW"),(5,"NIDORAN_F"),(6,"MANKEY"),
            (6,"SENTRET"),(6,"HOPPIP"),(7,"PICHU"),(7,"IGGLYBUFF"),(8,"TOGEPI")],
"Route23": [(34,"SPEAROW"),(34,"EKANS"),(35,"SANDSHREW"),(35,"FEAROW"),(36,"ARBOK"),
            (36,"SANDSLASH"),(37,"PRIMEAPE"),(37,"GRANBULL"),(38,"DITTO"),(38,"LARVITAR")],
"PokemonTower1F": [(20,"GASTLY"),(20,"GASTLY"),(21,"CUBONE"),(21,"HAUNTER"),(22,"ZUBAT"),
                   (22,"MISDREAVUS"),(23,"DROWZEE"),(23,"GOLBAT"),(24,"HYPNO"),(24,"MAROWAK")],
"PokemonTower2F": [(20,"GASTLY"),(20,"GASTLY"),(21,"CUBONE"),(21,"HAUNTER"),(22,"ZUBAT"),
                   (22,"MISDREAVUS"),(23,"DROWZEE"),(23,"GOLBAT"),(24,"HYPNO"),(24,"MAROWAK")],
"PokemonTower3F": [(21,"GASTLY"),(21,"GASTLY"),(22,"CUBONE"),(22,"HAUNTER"),(23,"ZUBAT"),
                   (23,"MISDREAVUS"),(24,"DROWZEE"),(24,"GOLBAT"),(25,"HYPNO"),(25,"GENGAR")],
"PokemonTower4F": [(21,"GASTLY"),(21,"GASTLY"),(22,"CUBONE"),(22,"HAUNTER"),(23,"ZUBAT"),
                   (23,"MISDREAVUS"),(24,"DROWZEE"),(24,"GOLBAT"),(25,"HYPNO"),(25,"GENGAR")],
"PokemonTower5F": [(22,"GASTLY"),(22,"GASTLY"),(23,"CUBONE"),(23,"HAUNTER"),(24,"ZUBAT"),
                   (24,"MISDREAVUS"),(25,"DROWZEE"),(25,"GOLBAT"),(26,"HYPNO"),(26,"GENGAR")],
"PokemonTower6F": [(23,"GASTLY"),(23,"GASTLY"),(24,"CUBONE"),(24,"HAUNTER"),(25,"ZUBAT"),
                   (25,"MISDREAVUS"),(26,"DROWZEE"),(26,"GOLBAT"),(27,"HYPNO"),(27,"GENGAR")],
"PokemonTower7F": [(24,"GASTLY"),(24,"HAUNTER"),(25,"CUBONE"),(25,"HAUNTER"),(26,"GOLBAT"),
                   (26,"MISDREAVUS"),(27,"HYPNO"),(27,"MAROWAK"),(28,"GENGAR"),(28,"WOBBUFFET")],
"SafariZoneCenter": [(22,"NIDORAN_F"),(22,"NIDORAN_M"),(23,"NIDORINA"),(23,"NIDORINO"),(24,"EXEGGCUTE"),
                     (24,"PARASECT"),(25,"VENOMOTH"),(25,"DODUO"),(26,"SCYTHER"),(26,"KANGASKHAN")],
"SafariZoneEast": [(23,"RHYHORN"),(23,"NIDORINA"),(24,"NIDORINO"),(24,"EXEGGCUTE"),(25,"PARASECT"),
                   (25,"PINECO"),(26,"DODUO"),(26,"DODRIO"),(27,"PINSIR"),(27,"CHANSEY")],
"SafariZoneNorth": [(24,"TAUROS"),(24,"RHYHORN"),(25,"EXEGGCUTE"),(25,"NIDORINO"),(26,"NIDORINA"),
                    (26,"DODUO"),(27,"DODRIO"),(27,"GLIGAR"),(28,"KANGASKHAN"),(28,"DRATINI")],
"SafariZoneWest": [(24,"TAUROS"),(24,"KANGASKHAN"),(25,"RHYHORN"),(25,"CHANSEY"),(26,"SCYTHER"),
                   (26,"PINSIR"),(27,"EXEGGCUTE"),(27,"SHUCKLE"),(28,"DRATINI"),(28,"DRAGONAIR")],
"SeafoamIslands1F": [(28,"ZUBAT"),(28,"GOLBAT"),(29,"SEEL"),(29,"SHELLDER"),(30,"SLOWPOKE"),
                     (30,"SWINUB"),(31,"PSYDUCK"),(31,"HORSEA"),(32,"DEWGONG"),(32,"SMOOCHUM")],
"SeafoamIslandsB1F": [(29,"ZUBAT"),(29,"GOLBAT"),(30,"SEEL"),(30,"SHELLDER"),(31,"SLOWPOKE"),
                      (31,"SWINUB"),(32,"DEWGONG"),(32,"HORSEA"),(33,"CLOYSTER"),(33,"JYNX")],
"SeafoamIslandsB2F": [(30,"ZUBAT"),(30,"GOLBAT"),(31,"SEEL"),(31,"SHELLDER"),(32,"SLOWBRO"),
                      (32,"PILOSWINE"),(33,"DEWGONG"),(33,"SEADRA"),(34,"CLOYSTER"),(34,"DELIBIRD")],
"SeafoamIslandsB3F": [(30,"ZUBAT"),(30,"GOLBAT"),(31,"SEEL"),(31,"SHELLDER"),(32,"SLOWBRO"),
                      (32,"PILOSWINE"),(33,"DEWGONG"),(33,"SEADRA"),(34,"CORSOLA"),(34,"LAPRAS")],
"SeafoamIslandsB4F": [(31,"GOLBAT"),(31,"SEEL"),(32,"SHELLDER"),(32,"SLOWBRO"),(33,"DEWGONG"),
                      (33,"PILOSWINE"),(34,"SEADRA"),(34,"CLOYSTER"),(35,"LAPRAS"),(36,"ARTICUNO")],
"PowerPlant": [(33,"MAGNEMITE"),(33,"VOLTORB"),(34,"MAGNETON"),(34,"ELECTRODE"),(35,"PIKACHU"),
               (35,"ELEKID"),(36,"RAICHU"),(36,"AMPHAROS"),(37,"PORYGON2"),(45,"ZAPDOS")],
"PokemonMansion1F": [(30,"RATTATA"),(30,"GRIMER"),(31,"RATICATE"),(31,"KOFFING"),(32,"MUK"),
                     (32,"SLUGMA"),(33,"WEEZING"),(33,"PONYTA"),(34,"DITTO"),(34,"MAGBY")],
"PokemonMansion2F": [(31,"RATTATA"),(31,"GRIMER"),(32,"RATICATE"),(32,"KOFFING"),(33,"MUK"),
                     (33,"SLUGMA"),(34,"WEEZING"),(34,"RAPIDASH"),(35,"DITTO"),(35,"MAGMAR")],
"PokemonMansion3F": [(32,"RATTATA"),(32,"GRIMER"),(33,"RATICATE"),(33,"KOFFING"),(34,"MUK"),
                     (34,"MAGCARGO"),(35,"WEEZING"),(35,"RAPIDASH"),(36,"DITTO"),(36,"MAGMAR")],
"PokemonMansionB1F": [(33,"GRIMER"),(33,"KOFFING"),(34,"RATICATE"),(34,"MUK"),(35,"WEEZING"),
                      (35,"MAGCARGO"),(36,"RAPIDASH"),(36,"MAGMAR"),(37,"DITTO"),(38,"ENTEI")],
"VictoryRoad1F": [(36,"MACHOKE"),(36,"GRAVELER"),(37,"GOLBAT"),(37,"ONIX"),(38,"RHYHORN"),
                  (38,"MAROWAK"),(39,"ARBOK"),(39,"SANDSLASH"),(40,"PRIMEAPE"),(40,"LARVITAR")],
"VictoryRoad2F": [(37,"MACHOKE"),(37,"GRAVELER"),(38,"GOLBAT"),(38,"ONIX"),(39,"RHYDON"),
                  (39,"MAROWAK"),(40,"PRIMEAPE"),(40,"PUPITAR"),(41,"DRAGONAIR"),(42,"MOLTRES")],
"VictoryRoad3F": [(38,"MACHOKE"),(38,"GRAVELER"),(39,"GOLBAT"),(39,"RHYDON"),(40,"MAROWAK"),
                  (40,"PRIMEAPE"),(41,"SANDSLASH"),(41,"PUPITAR"),(42,"DRAGONAIR"),(43,"AERODACTYL")],
"CeruleanCave1F": [(46,"GOLBAT"),(46,"KADABRA"),(47,"MAGNETON"),(47,"RHYDON"),(48,"DITTO"),
                   (48,"CHANSEY"),(49,"KANGASKHAN"),(49,"TAUROS"),(50,"DRAGONAIR"),(52,"RAIKOU")],
"CeruleanCave2F": [(48,"GOLBAT"),(48,"KADABRA"),(49,"MAGNETON"),(49,"RHYDON"),(50,"DITTO"),
                   (50,"CHANSEY"),(51,"ARBOK"),(51,"SNORLAX"),(52,"AERODACTYL"),(54,"SUICUNE")],
"CeruleanCaveB1F": [(50,"GOLBAT"),(50,"RHYDON"),(51,"DITTO"),(51,"CHANSEY"),(52,"SNORLAX"),
                    (52,"BLISSEY"),(53,"AERODACTYL"),(54,"DRAGONITE"),(60,"MEWTWO"),(60,"MEW")],
}

# Route 16's slot 7 placeholder -> a real species (MURKROW is Dark, excluded).
T["Route16"][7] = (25, "FEAROW")

# --- coverage pass -----------------------------------------------------------
# The design doc's hard rule is "no Pokemon should be permanently missable". The
# first pass left 17 species with no route to obtaining them at all:
#   * POLITOED / SLOWKING / KINGDRA carry NO evolution chain by design decision
#     (their real method is held-item trade), so they MUST be wild-catchable.
#   * The Johto starters and several base forms were simply never placed, which
#     also strands everything downstream of them (CHIKORITA stranding BAYLEEF
#     and MEGANIUM, TYROGUE stranding HITMONTOP, WOOPER stranding QUAGSIRE...).
#   * LUGIA / HO_OH / CELEBI had no home.
# Each override displaces a slot whose occupant is confirmed available elsewhere,
# so nothing is traded away for these.
OVERRIDES = {
    ("Route24", 8): (14, "CHIKORITA"),      # was MAREEP (Route 9/10, Mt Moon B1F)
    ("Route3", 9): (10, "CYNDAQUIL"),       # was FARFETCHD (Route 11)
    ("Route25", 9): (16, "TOTODILE"),       # was BULBASAUR (Route 2)
    ("Route6", 6): (15, "WOOPER"),          # was MARILL (Route 21)
    ("Route21", 6): (29, "REMORAID"),       # was RATICATE (very widespread)
    ("RockTunnel1F", 8): (20, "SUDOWOODO"), # was MAROWAK (Tower, B1F, Diglett's)
    ("Route8", 8): (19, "SMEARGLE"),        # was DITTO (Route 23, Mansion, Cerulean)
    ("Route23", 7): (37, "TYROGUE"),        # was GRANBULL (Route 17/18)
    ("Route7", 5): (18, "ESPEON"),          # was GASTLY (Route 6/8, Tower)
    ("SafariZoneEast", 4): (25, "BELLOSSOM"),   # was PARASECT (Safari Center)
    ("PokemonTower7F", 4): (26, "CROBAT"),      # was GOLBAT (Seafoam, Victory, Cerulean)
    ("SafariZoneCenter", 8): (26, "POLITOED"),  # was SCYTHER (Viridian, Route 12/14)
    ("SeafoamIslandsB2F", 8): (34, "SLOWKING"), # was CLOYSTER (B1F, B4F)
    ("SeafoamIslandsB4F", 7): (34, "KINGDRA"),  # was CLOYSTER (B1F)
    ("SeafoamIslandsB3F", 9): (40, "LUGIA"),    # was LAPRAS (B4F)
    ("VictoryRoad3F", 9): (45, "HO_OH"),        # was AERODACTYL (Cerulean Cave 2F)
    ("CeruleanCave1F", 8): (50, "CELEBI"),      # was DRAGONAIR (Route 15, Safari W, Victory)
}
for (mp, slot), entry in OVERRIDES.items():
    T[mp][slot] = entry


def main():
    changed = 0
    for name, entries in T.items():
        path = os.path.join(MAPS, name + ".asm")
        if not os.path.exists(path):
            raise SystemExit(f"no such map file: {path}")
        if len(entries) != 10:
            raise SystemExit(f"{name}: {len(entries)} slots, need exactly 10")
        txt = open(path, encoding="utf-8").read()
        m = re.search(r"def_grass_wildmons\s+(\d+)[^\n]*\n(.*?)(\tend_grass_wildmons)",
                      txt, re.S)
        if not m:
            raise SystemExit(f"{name}: no grass block found")
        # A grass rate of 0 means the map has no grass encounters at all, and the
        # macro asserts the slot list is EMPTY in that case (Pokemon Tower 1F/2F
        # are the entrance and rival-battle floors; SeaRoutes is water-only).
        # Filling those in is a build error, not a silent one -- but skip them
        # explicitly rather than relying on that.
        if int(m.group(1)) == 0:
            print(f"  skip {name}: grass encounter rate is 0")
            continue
        body = "".join(f"\tdb {lv:2d}, {sp}\n" for lv, sp in entries)
        txt = txt[:m.start(2)] + body + txt[m.end(2):]
        open(path, "w", encoding="utf-8", newline="\n").write(txt)
        changed += 1
    print(f"rewrote grass tables for {changed} maps")


if __name__ == "__main__":
    main()
