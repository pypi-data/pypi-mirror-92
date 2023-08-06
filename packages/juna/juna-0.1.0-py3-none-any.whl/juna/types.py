from enum import IntEnum, auto
from typing import List, Tuple
from pydantic.dataclasses import dataclass
from juna.utils import ExtendedEnum


class GameMode(ExtendedEnum):
    REGULAR = auto()
    IRONMAN = auto()
    HARDCORE_IRONMAN = auto()
    OLDSCHOOL_REGULAR = auto()
    OLDSCHOOL_IRONMAN = auto()
    OLDSCHOOL_HARDCORE_IRONMAN = auto()
    OLDSCHOOL_ULTIMATE_IRONMAN = auto()
    OLDSCHOOL_DEADMAN = auto()

    @classmethod
    def modern_modes(cls):
        return [
            cls.REGULAR,
            cls.IRONMAN,
            cls.HARDCORE_IRONMAN,
        ]

    @classmethod
    def oldschool_modes(cls):
        return [
            cls.OLDSCHOOL_REGULAR,
            cls.OLDSCHOOL_IRONMAN,
            cls.OLDSCHOOL_HARDCORE_IRONMAN,
            cls.OLDSCHOOL_ULTIMATE_IRONMAN,
            cls.OLDSCHOOL_DEADMAN,
        ]


class Skill(ExtendedEnum):
    OVERALL = auto()
    ATTACK = auto()
    DEFENCE = auto()
    STRENGTH = auto()
    CONSTITUTION = auto()
    RANGED = auto()
    PRAYER = auto()
    MAGIC = auto()
    COOKING = auto()
    WOODCUTTING = auto()
    FLETCHING = auto()
    FISHING = auto()
    FIREMAKING = auto()
    CRAFTING = auto()
    SMITHING = auto()
    MINING = auto()
    HERBLORE = auto()
    AGILITY = auto()
    THIEVING = auto()
    SLAYER = auto()
    FARMING = auto()
    RUNECRAFTING = auto()
    HUNTER = auto()
    CONSTRUCTION = auto()
    SUMMONING = auto()
    DUNGEONEERING = auto()
    DIVINATION = auto()
    INVENTION = auto()
    ARCHAEOLOGY = auto()

    @classmethod
    def modern_skills(cls) -> List[Tuple[any, str]]:
        return cls.list()

    @classmethod
    def oldschool_skills(cls) -> List[Tuple[any, str]]:
        return cls.list()[: Skill.SUMMONING.value]


class Activity(ExtendedEnum):
    ABYSSAL_SIRE = auto()
    AF15_COW_TIPPING = auto()
    AF15_RATS_KILLED = auto()
    ALCHEMICAL_HYDRA = auto()
    BA_ATTACKERS = auto()
    BA_COLLECTORS = auto()
    BA_DEFENDERS = auto()
    BA_HEALERS = auto()
    BARROWS_CHESTS = auto()
    BOUNTY_HUNTER = auto()
    BOUNTY_HUNTER_HUNTER = auto()
    BOUNTY_HUNTER_ROGUE = auto()
    BRYOPHYTA = auto()
    CALLISTO = auto()
    CASTLE_WARS_GAMES = auto()
    CERBERUS = auto()
    CFP_5_GAME_AVERAGE = auto()
    CHAMBERS_OF_XERIC = auto()
    CHAMBERS_OF_XERIC_CHALLENGE_MODE = auto()
    CHAOS_ELEMENTAL = auto()
    CHAOS_FANATIC = auto()
    CLUE_SCROLLS_ALL = auto()
    CLUE_SCROLLS_BEGINNER = auto()
    CLUE_SCROLLS_EASY = auto()
    CLUE_SCROLLS_ELITE = auto()
    CLUE_SCROLLS_HARD = auto()
    CLUE_SCROLLS_MASTER = auto()
    CLUE_SCROLLS_MEDIUM = auto()
    COMMANDER_ZILYANA = auto()
    CONQUEST = auto()
    CORPOREAL_BEAST = auto()
    CRAZY_ARCHAEOLOGIST = auto()
    DAGANNOTH_PRIME = auto()
    DAGANNOTH_REX = auto()
    DAGANNOTH_SUPREME = auto()
    DERANGED_ARCHAEOLOGIST = auto()
    DOMINION_TOWER = auto()
    DUEL_TOURNAMENT = auto()
    FIST_OF_GUTHIX = auto()
    GENERAL_GRAARDOR = auto()
    GG_ATHLETICS = auto()
    GG_RESOURCE_RACE = auto()
    GIANT_MOLE = auto()
    GROTESQUE_GUARDIANS = auto()
    HEIST_GUARD_LEVEL = auto()
    HEIST_ROBBER_LEVEL = auto()
    HESPORI = auto()
    KALPHITE_QUEEN = auto()
    KING_BLACK_DRAGON = auto()
    KRAKEN = auto()
    KREEARRA = auto()
    KRIL_TSUTSAROTH = auto()
    LEAGUE_POINTS = auto()
    LMS_RANK = auto()
    MIMIC = auto()
    MOBILISING_ARMIES = auto()
    NIGHTMARE = auto()
    OBOR = auto()
    RUNESCORE = auto()
    SARACHNIS = auto()
    SCORPIA = auto()
    SKOTIZO = auto()
    SOUL_WARS_ZEAL = auto()
    THE_CORRUPTED_GAUNTLET = auto()
    THE_CRUCIBLE = auto()
    THE_GAUNTLET = auto()
    THEATRE_OF_BLOOD = auto()
    THERMONUCLEAR_SMOKE_DEVIL = auto()
    TZKAL_ZUK = auto()
    TZTOK_JAD = auto()
    VENENATIS = auto()
    VETION = auto()
    VORKATH = auto()
    WE2_ARMADYL_LIFETIME_CONTRIBUTION = auto()
    WE2_ARMADYL_PVP_KILLS = auto()
    WE2_BANDOS_LIFETIME_CONTRIBUTION = auto()
    WE2_BANDOS_PVP_KILLS = auto()
    WINTERTODT = auto()
    ZALCANO = auto()
    ZULRAH = auto()

    @classmethod
    def modern_activities(cls):
        return [
            cls.BOUNTY_HUNTER,
            cls.BOUNTY_HUNTER_ROGUE,
            cls.DOMINION_TOWER,
            cls.THE_CRUCIBLE,
            cls.CASTLE_WARS_GAMES,
            cls.BA_ATTACKERS,
            cls.BA_DEFENDERS,
            cls.BA_COLLECTORS,
            cls.BA_HEALERS,
            cls.DUEL_TOURNAMENT,
            cls.MOBILISING_ARMIES,
            cls.CONQUEST,
            cls.FIST_OF_GUTHIX,
            cls.GG_ATHLETICS,
            cls.GG_RESOURCE_RACE,
            cls.WE2_ARMADYL_LIFETIME_CONTRIBUTION,
            cls.WE2_BANDOS_LIFETIME_CONTRIBUTION,
            cls.WE2_ARMADYL_PVP_KILLS,
            cls.WE2_BANDOS_PVP_KILLS,
            cls.HEIST_GUARD_LEVEL,
            cls.HEIST_ROBBER_LEVEL,
            cls.CFP_5_GAME_AVERAGE,
            cls.AF15_COW_TIPPING,
            cls.AF15_RATS_KILLED,
            cls.RUNESCORE,
            cls.CLUE_SCROLLS_EASY,
            cls.CLUE_SCROLLS_MEDIUM,
            cls.CLUE_SCROLLS_HARD,
            cls.CLUE_SCROLLS_ELITE,
            cls.CLUE_SCROLLS_MASTER,
        ]

    @classmethod
    def oldschool_activities(cls):
        return [
            cls.LEAGUE_POINTS,
            cls.BOUNTY_HUNTER_HUNTER,
            cls.BOUNTY_HUNTER_ROGUE,
            cls.CLUE_SCROLLS_ALL,
            cls.CLUE_SCROLLS_BEGINNER,
            cls.CLUE_SCROLLS_EASY,
            cls.CLUE_SCROLLS_MEDIUM,
            cls.CLUE_SCROLLS_HARD,
            cls.CLUE_SCROLLS_ELITE,
            cls.CLUE_SCROLLS_MASTER,
            cls.LMS_RANK,
            cls.SOUL_WARS_ZEAL,
            cls.ABYSSAL_SIRE,
            cls.ALCHEMICAL_HYDRA,
            cls.BARROWS_CHESTS,
            cls.BRYOPHYTA,
            cls.CALLISTO,
            cls.CERBERUS,
            cls.CHAMBERS_OF_XERIC,
            cls.CHAMBERS_OF_XERIC_CHALLENGE_MODE,
            cls.CHAOS_ELEMENTAL,
            cls.CHAOS_FANATIC,
            cls.COMMANDER_ZILYANA,
            cls.CORPOREAL_BEAST,
            cls.CRAZY_ARCHAEOLOGIST,
            cls.DAGANNOTH_PRIME,
            cls.DAGANNOTH_REX,
            cls.DAGANNOTH_SUPREME,
            cls.DERANGED_ARCHAEOLOGIST,
            cls.GENERAL_GRAARDOR,
            cls.GIANT_MOLE,
            cls.GROTESQUE_GUARDIANS,
            cls.HESPORI,
            cls.KALPHITE_QUEEN,
            cls.KING_BLACK_DRAGON,
            cls.KRAKEN,
            cls.KREEARRA,
            cls.KRIL_TSUTSAROTH,
            cls.MIMIC,
            cls.NIGHTMARE,
            cls.OBOR,
            cls.SARACHNIS,
            cls.SCORPIA,
            cls.SKOTIZO,
            cls.THE_GAUNTLET,
            cls.THE_CORRUPTED_GAUNTLET,
            cls.THEATRE_OF_BLOOD,
            cls.THERMONUCLEAR_SMOKE_DEVIL,
            cls.TZKAL_ZUK,
            cls.TZTOK_JAD,
            cls.VENENATIS,
            cls.VETION,
            cls.VORKATH,
            cls.WINTERTODT,
            cls.ZALCANO,
            cls.ZULRAH,
        ]


@dataclass
class SkillInfo:
    rank: int
    level: int
    experience: int


@dataclass
class ActivityInfo:
    rank: int
    score: int
