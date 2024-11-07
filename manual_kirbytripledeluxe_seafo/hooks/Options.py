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
    Regardless of the option chosen, Hypernova is never randomized.
    """
    display_name = "Randomize Copy Abilities"


class RandomizeKeychains(Choice):
    """
    Add additional locations for the Keychains in Story Mode. Also adds the Rare Keychains to the pool as filler items.
    The Queen Sectonia Keychain obtained from collecting all Sun Stones is randomized, but has no equivalent location.
    Only randomizing Rare Keychains adds 35 checks.
    Randomizing all Keychains adds an additional 102 checks, for a total of 137 added.
    """
    alias_false = 0
    option_no = 0
    alias_rare_keychains = 1
    alias_rares_only = 1
    option_only_rares = 1
    alias_true = 2
    option_yes = 2
    display_name = "Keychain Locations"


class GoalGames(DefaultOnToggle):
    """
    Add additional locations for doing each of the Goal Games across the stages.
    Technically, the location is based on the Keychain that is awarded for winning, but since it has no logical
    significance, you're free to decide whether it's for the Keychain or just doing the Goal Game by yourself.
    """
    display_name = "Goal Game Locations"


class KirbyFighters(Toggle):
    """
    Add additional locations for clearing Kirby Fighters with each of the available Copy Abilities.
    Recommended to only enable with Copy Abilities randomized, since otherwise they will all be available immediately.
    Adds 10 checks.
    """
    display_name = "Kirby Fighters Locations"


class ExtraStageKeys(DefaultOnToggle):
    """
    When enabled, the EX Stage Key items in the pool will become progressive.
    This means that Level 1's EX Stage will always be unlocked first, followed by Level 2's, and so on.
    """
    display_name = "Progressive EX Stage Keys"


class AbilityTestingRoom(Choice):
    """
    Determines how the Copy Ability Testing Room will be handled.
    'Postgame' means that it will be unlocked by defeating Queen Sectonia, as is the case normally.
    'Randomized' means that the ability to access it will become a shuffled item. An equivalent location is not created.
    'Disabled' means that the player will never be considered to have access to it at all.
    """
    alias_vanilla = 0
    option_postgame = 0
    option_randomized = 1
    alias_removed = 2
    option_disabled = 2
    display_name = "Ability Testing Room Access"


class StageRando(Choice):
    """
    Randomizes the positions of stages across the game.
    'Main Stages' means that only the stages that are normally needed to finish the game will be shuffled.
    'Extra Stages' means that the bonus stages unlocked by collecting all Sun Stones in a given level will be shuffled.
    'Split Pools' means that both types of stages will be shuffled, but only among themselves.
    'Fully Shuffled' means that any stage can appear in any other stage's position, regardless of the type.
    """
    alias_false = 0
    alias_no = 0
    alias_off = 0
    alias_vanilla = 0
    option_disabled = 0
    alias_main = 1
    option_main_stages = 1
    alias_ex = 2
    alias_ex_stages = 2
    alias_extra = 2
    option_extra_stages = 2
    alias_split = 3
    option_split_pools = 3
    alias_true = 4
    alias_yes = 4
    alias_on = 4
    alias_full = 4
    alias_shuffled = 4
    alias_enabled = 4
    option_fully_shuffled = 4
    display_name = "Stage Shuffle"


class BossRando(Choice):
    """
    If enabled, the level each boss is fought in will be randomized.
    So you could fight Flowery Woods in Endless Explosions, or Masked Dedede in Old Odyssey.
    Sun Stone requirements are determined based on levels, and will be the same regardless of which boss is there.
    Does not affect the boss refights in Royal Road.

    'Vanilla Dedede' forces the Masked Dedede fight to be placed at the end of Level 6, as is the case normally,
    allowing for vanilla-adjacent seeds that don't require fighting all bosses.

    'Early Dedede' forces the Masked Dedede fight to be placed in Level 1.
    This allows for the goal to be placed in a fixed position that doesn't require all Grand Sun Stones,
    permitting the goal requirement to purely be a set amount of Sun Stones without intruding on the other bosses.
    """
    alias_false = 0
    alias_no = 0
    alias_off = 0
    option_disabled = 0
    option_vanilla_dedede = 1
    option_early_dedede = 2
    alias_true = 3
    alias_yes = 3
    alias_on = 3
    alias_full = 3
    alias_shuffled = 3
    alias_enabled = 3
    option_fully_shuffled = 3
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

    Logic difficulty is only relevant when Copy Abilities are randomized.
    """
    option_easy = 0
    alias_medium = 1
    option_normal = 1
    option_hard = 2
    default = 1
    display_name = "Logic Difficulty"


class SunStoneCount(Range):
    """
    Determines the number of Sun Stones that will be added to the pool of randomized items.

    If there aren't enough locations for the number chosen, then Grand Sun Stones; EX Stage Keys; Copy Abilities;
    and the Copy Ability Testing Room will take priority over Sun Stones.

    The Sun Stone count also decides the upper limit for boss unlock conditions,
    and those requirements will be lowered to match this if necessary.

    The value of this option may be modified by other factors, such as a limited number of locations being added.
    The number in the spoiler log should always match the number of Sun Stones created after it was modified.

    Default value is 100.
    """
    range_start = 0
    range_end = 100
    default = 100
    display_name = "Number of Sun Stones"


class ExtraSunStones(Choice):
    """
    If some of the Sun Stones aren't needed for any given boss, this determines how the excess will be handled.

    'Progression' means that the excess can be placed on priority locations and won't be placed on excluded locations.
    This also determines that the excess are logically expected to be collected.

    'Useful' means that the excess won't be placed on either priority or excluded locations.
    They also won't be logically expected to be collected, making it likely that you'll gain access to bosses early.

    'Filler' means that the excess won't be placed on priority locations but can be placed on excluded locations.
    Just like with 'Useful', they also won't be logically expected to be collected.
    If no Sun Stones are required for any bosses, they will default to this.

    'Removed' means that the excess will be completely removed from the pool and replaced by Keychains.
    This is similar to 'Filler' but it removes the confusion as to how many Sun Stones you're expected to have.
    """
    alias_yes = 0
    alias_keep = 0
    alias_prog = 0
    option_progression = 0
    alias_never_exclude = 1
    option_useful = 1
    alias_normal = 2
    alias_trash = 2
    option_filler = 2
    alias_no = 3
    alias_remove = 3
    option_removed = 3
    display_name = "Excess Sun Stones"


class Level1BossRequirement(NamedRange):
    """
    How many Sun Stones are required to battle the boss of Level 1.
    Will be lowered to match the number of Sun Stones created if that number is lower than the requirement defined here.
    """
    display_name = "Sun Stones for Level 1 Boss"
    range_start = 0
    range_end = 100
    default = 5

    special_range_names = {
        "none": 0,
        "half": 3,
        "normal": 5,
        "extra": 8,
        "double": 10,
        "all": 100,
    }


class Level2BossRequirement(NamedRange):
    """
    How many Sun Stones are required to battle the boss of Level 2.
    Will be lowered to match the number of Sun Stones created if that number is lower than the requirement defined here.
    """
    display_name = "Sun Stones for Level 2 Boss"
    range_start = 0
    range_end = 100
    default = 11

    special_range_names = {
        "none": 0,
        "half": 6,
        "normal": 11,
        "extra": 17,
        "double": 22,
        "all": 100,
    }


class Level3BossRequirement(NamedRange):
    """
    How many Sun Stones are required to battle the boss of Level 3.
    Will be lowered to match the number of Sun Stones created if that number is lower than the requirement defined here.
    """
    display_name = "Sun Stones for Level 3 Boss"
    range_start = 0
    range_end = 100
    default = 18

    special_range_names = {
        "none": 0,
        "half": 9,
        "normal": 18,
        "extra": 27,
        "double": 36,
        "all": 100,
    }


class Level4BossRequirement(NamedRange):
    """
    How many Sun Stones are required to battle the boss of Level 4.
    Will be lowered to match the number of Sun Stones created if that number is lower than the requirement defined here.
    """
    display_name = "Sun Stones for Level 4 Boss"
    range_start = 0
    range_end = 100
    default = 26

    special_range_names = {
        "none": 0,
        "half": 13,
        "normal": 26,
        "extra": 39,
        "double": 52,
        "all": 100,
    }


class Level5BossRequirement(NamedRange):
    """
    How many Sun Stones are required to battle the boss of Level 5.
    Will be lowered to match the number of Sun Stones created if that number is lower than the requirement defined here.
    """
    display_name = "Sun Stones for Level 5 Boss"
    range_start = 0
    range_end = 100
    default = 36

    special_range_names = {
        "none": 0,
        "half": 18,
        "normal": 36,
        "extra": 54,
        "double": 72,
        "all": 100,
    }


class Level6BossRequirement(NamedRange):
    """
    How many Sun Stones are required to battle the boss of Level 6.
    Will be lowered to match the number of Sun Stones created if that number is lower than the requirement defined here.
    """
    display_name = "Sun Stones for Level 6 Boss"
    range_start = 0
    range_end = 100
    default = 43

    special_range_names = {
        "none": 0,
        "half": 22,
        "normal": 43,
        "extra": 65,
        "double": 86,
        "all": 100,
    }


class QueenSectoniaRequirement(NamedRange):
    """
    How many bosses need to be fought before Queen Sectonia becomes available.
    The fight is always considered to be accessible immediately after defeating the prerequisite number of bosses,
    and the positions of the bosses has no impact on this.
    If set to vanilla, she's always fought directly after defeating Masked Dedede's Revenge, as is the case normally.
    """
    display_name = "Bosses Before Queen Sectonia"
    range_start = 1
    range_end = 6
    default = -1

    special_range_names = {
        "vanilla": -1,
        "minimum": 1,
        "maximum": 6,
    }


class FillerTrapPercent(NamedRange):
    """
    How many random Keychains will be replaced by Lose Ability Traps.
    Lose Ability Traps make Kirby eject whatever ability he had. They do nothing if he didn't have one.
    
    0 means no traps are added, 100 means all random Keychains will be replaced by traps.
    """
    display_name = "Filler Trap Percentage"
    range_start = 0
    range_end = 100

    special_range_names = {
        "none": 0,
        "some": 25,
        "half": 50,
        "most": 75,
        "all": 100,
    }


class Goal(Range):
    range_start = 0
    range_end = 6
    visibility = Visibility.none


class DeprecatedFightersName(Choice):
    option_false = 0
    option_true = 1
    option_disabled = 2
    default = 2
    visibility = Visibility.none


# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["randomize_copy_abilities"] = RandomizeAbilities
    options["keychain_locations"] = RandomizeKeychains
    options["goal_game_locations"] = GoalGames
    options["kirby_fighters_locations"] = KirbyFighters
    options["progressive_ex_stage_keys"] = ExtraStageKeys
    options["ability_testing_room"] = AbilityTestingRoom
    options["stage_shuffle"] = StageRando
    options["boss_shuffle"] = BossRando
    options["logic_difficulty"] = LogicDifficulty
    options["sun_stone_count"] = SunStoneCount
    options["excess_sun_stones"] = ExtraSunStones
    options["level_1_boss_sun_stones"] = Level1BossRequirement
    options["level_2_boss_sun_stones"] = Level2BossRequirement
    options["level_3_boss_sun_stones"] = Level3BossRequirement
    options["level_4_boss_sun_stones"] = Level4BossRequirement
    options["level_5_boss_sun_stones"] = Level5BossRequirement
    options["level_6_boss_sun_stones"] = Level6BossRequirement
    options["queen_sectonia_boss_requirement"] = QueenSectoniaRequirement
    options["enable_kirby_fighters_locations"] = DeprecatedFightersName
    return options


# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    options["filler_traps"] = FillerTrapPercent
    options["goal"] = Goal
    return options
