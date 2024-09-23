# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, Visibility

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
    Prevent use of Kirby's Copy Abilities before obtaining them.
    """
    display_name = "Randomize Copy Abilities"

class RandomizeKeychains(Choice):
    """
    Add additional locations for the Keychains in Story Mode. Also adds the Rare Keychains to the pool as filler items.
    The Queen Sectonia Keychain obtained from collecting all Sun Stones is randomized, but has no equivalent location.
    """
    alias_false = 0
    option_no = 0
    option_only_rares = 1
    alias_true = 2
    option_yes = 2
    default = 1
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
    Add the ability to access the Copy Ability Testing Room to the item pool. If false, you're never logically considered to have access.
    """
    display_name = "Randomize Ability Testing Room"

class Level1BossRequirement(Range):
    """
    How many Sun Stones are required to battle the boss of Level 1.
    """
    display_name = "Sun Stones for Level 1 Boss"
    range_start = 0
    range_end = 100
    default = 5
    
class Level2BossRequirement(Range):
    """
    How many Sun Stones are required to battle the boss of Level 2.
    """
    display_name = "Sun Stones for Level 2 Boss"
    range_start = 0
    range_end = 100
    default = 11
    
class Level3BossRequirement(Range):
    """
    How many Sun Stones are required to battle the boss of Level 3.
    """
    display_name = "Sun Stones for Level 3 Boss"
    range_start = 0
    range_end = 100
    default = 18
    
class Level4BossRequirement(Range):
    """
    How many Sun Stones are required to battle the boss of Level 4.
    """
    display_name = "Sun Stones for Level 4 Boss"
    range_start = 0
    range_end = 100
    default = 26
    
class Level5BossRequirement(Range):
    """
    How many Sun Stones are required to battle the boss of Level 5.
    """
    display_name = "Sun Stones for Level 5 Boss"
    range_start = 0
    range_end = 100
    default = 36
    
class Level6BossRequirement(Range):
    """
    How many Sun Stones are required to battle the boss of Level 6.
    """
    display_name = "Sun Stones for Level 6 Boss"
    range_start = 0
    range_end = 100
    default = 43
    
class QueenSectoniaRequirement(Range):
    """
    How many bosses need to be fought before Queen Sectonia becomes available.
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