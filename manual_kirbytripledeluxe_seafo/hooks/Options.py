# Object classes from AP that represent different types of options that you can create
from Options import (FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange,
                     OptionGroup, Visibility)

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value


####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#


class RandomizeAbilities(DefaultOnToggle):
    """
    Prevent the use of Kirby's Copy Abilities before obtaining them.
    """
    display_name = "Randomize Copy Abilities"


class RandomizeKeychains(Choice):
    """
    Add additional locations for the Keychains in Story Mode. Also adds the Rare Keychains to the pool as filler items.
    The Queen Sectonia Keychain obtained from collecting all Sun Stones is randomized, but has no equivalent location.
    """
    alias_false = 0
    option_no = 0
    alias_rares_only = 1
    option_only_rares = 1
    alias_true = 2
    option_yes = 2
    default = 0
    display_name = "Randomize Keychains"


class ExtraStageKeys(DefaultOnToggle):
    """
    When enabled, the EX Stage Key items in the pool will become progressive.
    This means that Level 1's EX Stage will always be unlocked first, followed by Level 2's, and so on.
    """
    display_name = "Progressive EX Stage Keys"


class KirbyFighters(Toggle):
    """
    Add additional locations for clearing Kirby Fighters with each of the available Copy Abilities.
    """
    display_name = "Add Kirby Fighters Locations"


class AbilityTestingRoom(Toggle):
    """
    Add the ability to access the Copy Ability Testing Room to the item pool.
    If false, you're never logically considered to have access.
    """
    display_name = "Randomize Ability Testing Room"


class StageRando(Toggle):
    """
    Randomizes the position of stages across the game.
    All non-boss stages, including EX stages, are in the pool.
    So your first stage in Fine Fields could be a Wild World stage, and the EX stage
    could be a normal stage from Royal Road.
    """
    display_name = "Stage Shuffle"


class BossRando(Toggle):
    """
    Randomizes the level each boss is fought in.
    So you could fight Flowery Woods in Endless Explosions, or Masked Dedede in Old Odyssey.
    Sun Stone requirements are determined based on levels, and will be the same regardless of which boss is there.
    Does not affect the boss refights in Royal Road.
    """
    display_name = "Boss Shuffle"


class LogicDifficulty(Choice):
    """
    Adjusts the expectations for the player's use of abilities.

    Easy only expects the player to use immediately accessible abilities, or if none are available,
    abilities that were presented to the player shortly before. It has a focus on using the 'intended' methods.
    Note that even on easy logic, the player is expected to beat all stages and bosses without needing an ability.

    Normal expects the player to use almost any valid ability that can be found in the stage.
    It also expects the use of some basic tricks that can be done without an ability.
    Some difficult tricks are still left out of logic.

    Hard expects the player to use almost everything at their disposal.
    Once the player gains access to an ability through any stage, boss, or the Copy Ability Testing Room,
    they can be expected to bring that ability to anywhere that it can be used.
    Damage boosting and using ability stars as projectiles can be also expected.
    Note that the player is not expected to bring Crash and Mike through mid-boss fights.

    Logic difficulty is only relevant when copy abilities are randomized.
    """
    option_easy = 0
    alias_medium = 1
    option_normal = 1
    option_hard = 2
    default = 1
    display_name = "Logic Difficulty"


class Level1BossRequirement(NamedRange):
    """
    How many Sun Stones are required to battle the boss of Level 1.
    """
    display_name = "Sun Stones for Level 1 Boss"
    range_start = 0
    range_end = 100
    default = 5

    special_range_names = {
        "vanilla": 5,
    }


class Level2BossRequirement(NamedRange):
    """
    How many Sun Stones are required to battle the boss of Level 2.
    """
    display_name = "Sun Stones for Level 2 Boss"
    range_start = 0
    range_end = 100
    default = 11

    special_range_names = {
        "vanilla": 11,
    }


class Level3BossRequirement(NamedRange):
    """
    How many Sun Stones are required to battle the boss of Level 3.
    """
    display_name = "Sun Stones for Level 3 Boss"
    range_start = 0
    range_end = 100
    default = 18

    special_range_names = {
        "vanilla": 18,
    }


class Level4BossRequirement(NamedRange):
    """
    How many Sun Stones are required to battle the boss of Level 4.
    """
    display_name = "Sun Stones for Level 4 Boss"
    range_start = 0
    range_end = 100
    default = 26

    special_range_names = {
        "vanilla": 26,
    }


class Level5BossRequirement(NamedRange):
    """
    How many Sun Stones are required to battle the boss of Level 5.
    """
    display_name = "Sun Stones for Level 5 Boss"
    range_start = 0
    range_end = 100
    default = 36

    special_range_names = {
        "vanilla": 36,
    }


class Level6BossRequirement(NamedRange):
    """
    How many Sun Stones are required to battle the boss of Level 6.
    """
    display_name = "Sun Stones for Level 6 Boss"
    range_start = 0
    range_end = 100
    default = 43

    special_range_names = {
        "vanilla": 43,
    }


class QueenSectoniaRequirement(Range):
    """
    How many bosses need to be fought before Queen Sectonia becomes available.
    Default value is 6.
    """
    display_name = "Bosses Before Queen Sectonia"
    range_start = 1
    range_end = 6
    default = 6


class FillerTrapPercent(Range):
    """
    How many random Keychains will be replaced by Lose Ability Traps.
    Lose Ability Traps make Kirby eject whatever ability he had. They do nothing if he didn't have one.
    
    0 means no traps are added, 100 means all random Keychains will be replaced by traps.
    """
    display_name = "Filler Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0


class Goal(Range):
    range_start = 0
    range_end = 5
    visibility = Visibility.none


# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["randomize_copy_abilities"] = RandomizeAbilities
    options["keychain_locations"] = RandomizeKeychains
    options["progressive_ex_stage_keys"] = ExtraStageKeys
    options["enable_kirby_fighters_locations"] = KirbyFighters
    options["randomize_ability_testing_room"] = AbilityTestingRoom
    options["stage_shuffle"] = StageRando
    options["boss_shuffle"] = BossRando
    options["logic_difficulty"] = LogicDifficulty
    options["level_1_boss_sun_stones"] = Level1BossRequirement
    options["level_2_boss_sun_stones"] = Level2BossRequirement
    options["level_3_boss_sun_stones"] = Level3BossRequirement
    options["level_4_boss_sun_stones"] = Level4BossRequirement
    options["level_5_boss_sun_stones"] = Level5BossRequirement
    options["level_6_boss_sun_stones"] = Level6BossRequirement
    options["queen_sectonia_boss_requirement"] = QueenSectoniaRequirement
    return options


# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    options["filler_traps"] = FillerTrapPercent
    options["goal"] = Goal
    return options
