# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, ItemClassification
from Options import OptionError

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

from .Stage_Shuffle import shuffle_stages_early, shuffle_stages, shuffle_bosses

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################


# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False


# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    if world.options.enable_kirby_fighters_locations.value < 2:
        raise OptionError("Outdated option name 'enable_kirby_fighters_locations'. Please use an updated YAML.")

    sectonia_boss_req = world.options.queen_sectonia_boss_requirement.value
    if sectonia_boss_req == -1:
        world.options.goal.value = sectonia_boss_req + 1
    else:
        world.options.goal.value = sectonia_boss_req

    if world.options.keychain_locations > 0 or world.options.goal_game_locations:
        pass
    else:
        location_total = 106
        item_total = 11
        if world.options.randomize_copy_abilities:
            item_total += 25
        #
        # These are never run due to them always exceeding the required number of locations.
        #
        # if world.options.keychain_locations == 1:
        #     location_total += 35
        # if world.options.keychain_locations == 2:
        #     location_total += 137
        # if world.options.goal_game_locations:
        #     location_total += 35
        #
        if world.options.kirby_fighters_locations:
            location_total += 10
        if world.options.ability_testing_room == 1:
            item_total += 1
        extra_locations = location_total - item_total
        # Ensuring that the number of Sun Stones added to the pool isn't higher than the number defined by the option.
        if extra_locations >= world.options.sun_stone_count.value:
            pass
        else:
            print("Not enough locations for all Sun Stones to be placed. Removing excess Sun Stones.")
            world.options.sun_stone_count.value = extra_locations

    sun_stones = world.options.sun_stone_count.value

    if world.options.level_1_boss_sun_stones > sun_stones:
        print("Not enough Sun Stones to match Level 1 Boss requirement. Lowering requirement to match number created.")
        world.options.level_1_boss_sun_stones.value = sun_stones

    if world.options.level_2_boss_sun_stones > sun_stones:
        print("Not enough Sun Stones to match Level 2 Boss requirement. Lowering requirement to match number created.")
        world.options.level_2_boss_sun_stones.value = sun_stones

    if world.options.level_3_boss_sun_stones > sun_stones:
        print("Not enough Sun Stones to match Level 3 Boss requirement. Lowering requirement to match number created.")
        world.options.level_3_boss_sun_stones.value = sun_stones

    if world.options.level_4_boss_sun_stones > sun_stones:
        print("Not enough Sun Stones to match Level 4 Boss requirement. Lowering requirement to match number created.")
        world.options.level_4_boss_sun_stones.value = sun_stones

    if world.options.level_5_boss_sun_stones > sun_stones:
        print("Not enough Sun Stones to match Level 5 Boss requirement. Lowering requirement to match number created.")
        world.options.level_5_boss_sun_stones.value = sun_stones

    if world.options.level_6_boss_sun_stones > sun_stones:
        print("Not enough Sun Stones to match Level 6 Boss requirement. Lowering requirement to match number created.")
        world.options.level_6_boss_sun_stones.value = sun_stones


# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    level_1_boss = world.options.level_1_boss_sun_stones.value
    if level_1_boss > 0: 
        remove_first_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 1 Boss" in loc.name
                             and f"- {level_1_boss} Sun Stone" not in loc.name]
    else:
        remove_first_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 1 Boss -" in loc.name]

    level_2_boss = world.options.level_2_boss_sun_stones.value
    if level_2_boss > 0: 
        remove_second_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 2 Boss" in loc.name
                              and f"- {level_2_boss} Sun Stone" not in loc.name]
    else:
        remove_second_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 2 Boss -" in loc.name]

    level_3_boss = world.options.level_3_boss_sun_stones.value
    if level_3_boss > 0: 
        remove_third_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 3 Boss" in loc.name
                             and f"- {level_3_boss} Sun Stone" not in loc.name]
    else:
        remove_third_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 3 Boss -" in loc.name]

    level_4_boss = world.options.level_4_boss_sun_stones.value
    if level_4_boss > 0: 
        remove_fourth_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 4 Boss" in loc.name
                              and f"- {level_4_boss} Sun Stone" not in loc.name]
    else:
        remove_fourth_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 4 Boss -" in loc.name]

    level_5_boss = world.options.level_5_boss_sun_stones.value
    if level_5_boss > 0: 
        remove_fifth_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 5 Boss" in loc.name
                             and f"- {level_5_boss} Sun Stone" not in loc.name]
    else:
        remove_fifth_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 5 Boss -" in loc.name]

    level_6_boss = world.options.level_6_boss_sun_stones.value
    if level_6_boss > 0: 
        remove_sixth_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 6 Boss" in loc.name
                             and f"- {level_6_boss} Sun Stone" not in loc.name]
    else:
        remove_sixth_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 6 Boss -" in loc.name]

    keychains = world.options.keychain_locations.value
    if keychains == 1:
        remove_keychains = [loc.name for loc in multiworld.get_locations(player) if "- Keychain" in loc.name
                            or "Left Keychain" in loc.name or "Right Keychain" in loc.name]
    elif keychains == 0:
        remove_keychains = [loc.name for loc in multiworld.get_locations(player) if "Keychain" in loc.name]
    else:
        remove_keychains = []

    stage_shuffle = world.options.stage_shuffle.value
    # Here we remove every 'Unlock Stage' location, since all stages are in their vanilla positions.
    if stage_shuffle == 0:
        remove_stages = [loc.name for loc in multiworld.get_locations(player)
                         if "Unlock 1st" in loc.name or "Unlock 2nd" in loc.name or "Unlock 3rd" in loc.name
                         or "Unlock 4th" in loc.name or "Unlock 5th" in loc.name or "Unlock EX" in loc.name]
    # In this case since only main stages are shuffled, we have to remove the unused 'Unlock EX Stage' locations.
    elif stage_shuffle == 1:
        remove_stages = [loc.name for loc in multiworld.get_locations(player)
                         if "Unlock EX" in loc.name or "Unlock 1st EX" in loc.name or "Unlock 2nd EX" in loc.name]
    # In this case only EX stages are shuffled, so we remove the 'Unlock Stage' locations for the vanilla main stages.
    elif stage_shuffle == 2:
        remove_stages = [loc.name for loc in multiworld.get_locations(player)
                         if "Unlock 1st Stage" in loc.name or "Unlock 2nd Stage" in loc.name
                         or "Unlock 3rd" in loc.name or "Unlock 4th" in loc.name or "Unlock 5th" in loc.name]
    # Finally, if all stages are shuffled, we don't have to remove their respective unlock locations.
    else:
        remove_stages = []

    if world.options.ability_testing_room.value == 0:
        remove_atr = []
    else:
        remove_atr = [loc.name for loc in multiworld.get_locations(player)
                      if loc.name == "Unlock Copy Ability Testing Room"]

    # Add your code here to calculate which locations to remove

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in remove_first_boss:
                    region.locations.remove(location)
                if location.name in remove_second_boss:
                    region.locations.remove(location)
                if location.name in remove_third_boss:
                    region.locations.remove(location)
                if location.name in remove_fourth_boss:
                    region.locations.remove(location)
                if location.name in remove_fifth_boss:
                    region.locations.remove(location)
                if location.name in remove_sixth_boss:
                    region.locations.remove(location)
                if location.name in remove_keychains:
                    region.locations.remove(location)
                if location.name in remove_stages:
                    region.locations.remove(location)
                if location.name in remove_atr:
                    region.locations.remove(location)

    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()


# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool


# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    # for itemName in itemNamesToRemove:
    #     item = next(i for i in item_pool if i.name == itemName)
    #     item_pool.remove(item)

    if world.options.ability_testing_room == 2:
        get_atr = [i.name for i in item_pool if i.name == "Copy Ability Testing Room"]
        for atr in get_atr:
            remove_atr = next(i for i in item_pool if i.name == atr)
            item_pool.remove(remove_atr)

    shuffle_stages_early(item_pool, world, multiworld, player)

    if world.options.sun_stone_count.value < 100:
        unneeded_sun_stones = 100 - world.options.sun_stone_count.value
        for _ in range(unneeded_sun_stones):
            remove_sun_stones = next(i for i in item_pool if i.name == "Sun Stone")
            item_pool.remove(remove_sun_stones)

    # If we want our excess Sun Stones to be progression items, we don't need to do anything here.
    if world.options.excess_sun_stones == 0:
        pass
    else:
        # Getting the number of Sun Stones that need to be progression items.
        prog_sun_stones = max(world.options.level_1_boss_sun_stones, world.options.level_2_boss_sun_stones,
                              world.options.level_3_boss_sun_stones, world.options.level_4_boss_sun_stones,
                              world.options.level_5_boss_sun_stones, world.options.level_6_boss_sun_stones)
        # Checking how many Sun Stones are in the pool.
        total_sun_stones = [i for i in item_pool if i.name == "Sun Stone"]
        # Calculating the number of unnecessary Sun Stones by subtracting the number in the pool by how many are needed.
        excess_sun_stones = len(total_sun_stones) - prog_sun_stones

        # Modifying the unneeded Sun Stones based on which option was chosen.
        if world.options.excess_sun_stones == 1:
            for _, item in zip(range(excess_sun_stones), total_sun_stones):
                item.classification = ItemClassification.useful
        elif world.options.excess_sun_stones == 2:
            for _, item in zip(range(excess_sun_stones), total_sun_stones):
                item.classification = ItemClassification.filler
        elif world.options.excess_sun_stones == 3:
            world.options.sun_stone_count.value = prog_sun_stones
            for _, item in zip(range(excess_sun_stones), total_sun_stones):
                sun_stones = next(i for i in item_pool if i.name == "Sun Stone")
                item_pool.remove(sun_stones)
        else:
            # All four valid options should have been accounted for, so we throw an error if it went wrong somewhere.
            raise OptionError("Invalid value for option 'Excess Sun Stones'. Please report this to the maintainer.")

    if world.options.keychain_locations == 0:
        rare_keychains = [i.name for i in item_pool if " Keychain" in i.name]
        for keychains_to_remove in rare_keychains:
            remove_keychains = next(i for i in item_pool if i.name == keychains_to_remove)
            item_pool.remove(remove_keychains)
    # Used to check if there's actually enough room in the pool for Rare Keychains.
    # We can skip this if we have Goal Game locations because they always provide just enough extra locations for Rares.
    elif world.options.keychain_locations == 1 and not world.options.goal_game_locations:
        # Higher location total here because we're including Rare Keychain locations.
        location_total = 141
        item_total = 11
        if world.options.randomize_copy_abilities:
            item_total += 25
        if world.options.kirby_fighters_locations:
            location_total += 10
        if world.options.ability_testing_room == 1:
            item_total += 1
        # The Sun Stone Count value should always match the number of Sun Stones in the item pool by this point.
        item_total += world.options.sun_stone_count.value
        open_locations = location_total - item_total
        if open_locations < 36:
            print("Not enough locations to place all Rare Keychains. Removing the excess.")
            # We remove the Queen Sectonia Keychain first because it doesn't have an equivalent location.
            sectonia_keychain = next(i for i in item_pool if i.name == "Queen Sectonia Keychain")
            item_pool.remove(sectonia_keychain)
            # If we still don't have enough room, we need to remove more Rare Keychains at random to make up for it.
            if open_locations < 35:
                rare_keychains = [i for i in item_pool if " Keychain" in i.name]
                taken_locations = 35 - open_locations
                for _ in range(taken_locations):
                    keychains_to_remove = world.random.choice(rare_keychains)
                    item_pool.remove(keychains_to_remove)
                    rare_keychains.remove(keychains_to_remove)
    else:
        pass

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)


# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool


# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location
    pass

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)


# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name


# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    # Grand Sun Stones are always the biggest major unlocks, so they should always be Progression + Useful.
    if item.name == "Grand Sun Stone":
        item.classification = ItemClassification.progression | ItemClassification.useful

    # Bomb has no specific use when story mode is set to easy logic, but is always needed for Kirby Fighters.
    # Though even when Kirby Fighters locations aren't enabled, Bomb is still nice to have.
    if item.name == "Bomb":
        if world.options.logic_difficulty == 0 and not world.options.kirby_fighters_locations:
            item.classification = ItemClassification.useful

    # Mike has an extra requirement added for easy logic, and all of its important requirements are considered 'hard'.
    # Neither of these apply to normal logic, so it's never required for anything but is still good to have.
    if item.name == "Mike":
        if world.options.logic_difficulty == 1:
            item.classification = ItemClassification.useful

    # Sleep is a purely detrimental ability, and (theoretically) it would only be disadvantageous to receive it.
    # We want it to be classified as a trap, but need to do it here so that it won't be duplicated by filler traps.
    if item.name == "Sleep":
        item.classification = ItemClassification.trap

    # Wing has no specific use when story mode is set to easy logic, but is still good to have.
    if item.name == "Wing":
        if world.options.logic_difficulty == 0:
            item.classification = ItemClassification.useful

    # Taking abilities from other areas is only needed in hard logic, and ability logic is only relevant if randomized.
    # It is however still convenient for if the player wants to go out of logic, or just use their favorite ability.
    if item.name == "Copy Ability Testing Room":
        if world.options.logic_difficulty < 2 or not world.options.randomize_copy_abilities:
            item.classification = ItemClassification.useful

    # If we don't need Sun Stones for any bosses, they don't have any use.
    required_sun_stones = max(world.options.level_1_boss_sun_stones, world.options.level_2_boss_sun_stones,
                              world.options.level_3_boss_sun_stones, world.options.level_4_boss_sun_stones,
                              world.options.level_5_boss_sun_stones, world.options.level_6_boss_sun_stones)
    if required_sun_stones == 0:
        if world.options.excess_sun_stones < 2:
            world.options.excess_sun_stones.value = 2
        if item.name == "Sun Stone":
            item.classification = ItemClassification.filler

    return item


# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    shuffle_bosses(world, multiworld, player)

    # We don't need to do anything if Stage Shuffle is disabled, so we quit out early.
    if world.options.stage_shuffle == 0:
        return []

    shuffle_stages(world, multiworld, player)


# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass


# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data


# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data


# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass


# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    
    ### Example way to use this hook: 
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string
    
    pass


def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    stage_shuffle = world.options.stage_shuffle
    boss_shuffle = world.options.boss_shuffle
    # We first check if both options have been disabled, and quit out if they have been.
    if stage_shuffle == 0 and boss_shuffle == 0:
        return
    # If either option has been enabled in any fashion, we can continue.
    if stage_shuffle > 0 or boss_shuffle > 0:
        hint_data.update({player: {}})
    # Stage Shuffle first checks for if it has been enabled.
    if stage_shuffle > 0:
        # Next, it needs to check for the specific value.
        # 1 and 3 both shuffle main stages among themselves.
        if stage_shuffle == 1 or stage_shuffle == 3:
            # First, we need to create a list of all the locations that stages can be placed on.
            # TODO: Maybe rewrite this to fetch the location names instead?
            main_stage_locs = ["Level 1 - 1st Stage", "Level 1 - 2nd Stage",
                               "Level 1 - 3rd Stage", "Level 1 - 4th Stage",
                               "Level 2 - 1st Stage", "Level 2 - 2nd Stage",
                               "Level 2 - 3rd Stage", "Level 2 - 4th Stage",
                               "Level 3 - 1st Stage", "Level 3 - 2nd Stage",
                               "Level 3 - 3rd Stage", "Level 3 - 4th Stage",
                               "Level 3 - 5th Stage",
                               "Level 4 - 1st Stage", "Level 4 - 2nd Stage",
                               "Level 4 - 3rd Stage", "Level 4 - 4th Stage",
                               "Level 4 - 5th Stage",
                               "Level 5 - 1st Stage", "Level 5 - 2nd Stage",
                               "Level 5 - 3rd Stage", "Level 5 - 4th Stage",
                               "Level 5 - 5th Stage",
                               "Level 6 - 1st Stage", "Level 6 - 2nd Stage",
                               "Level 6 - 3rd Stage", "Level 6 - 4th Stage",
                               "Level 6 - 5th Stage"]
            # Then we get the shuffled order of stages.
            main_stage_items = world.main_stage_order[player]
            # This next function only needs to be run as many times as
            # there are locations for main stages to be placed on.
            # In this case, whether it's items or locations doesn't matter, since both always have the same count.
            for _ in range(len(main_stage_locs)):
                # Next, we iterate through the relevant locations and get their names,
                # along with the name of their corresponding stage item.
                main_stage_loc = main_stage_locs.pop(0)
                main_stage_item = main_stage_items.pop(0)
                # Here, we get locations in the multiworld that share their
                # region's name with the name of the stage item we're looking at.
                # These conveniently always line up, so we can just check for it directly.
                for main_loc in multiworld.get_locations(player):
                    if main_stage_item in main_loc.parent_region.name:
                        # Finally, we assign an entrance hint based on where the corresponding stage item is located.
                        hint_data[player][main_loc.address] = main_stage_loc
                        # The rest of the Stage Shuffle functions work almost identically to this one.

        # 2 and 3 both shuffle EX stages among themselves.
        if stage_shuffle == 2 or stage_shuffle == 3:
            ex_stage_locs = ["Level 1 - EX Stage", "Level 2 - EX Stage", "Level 3 - EX Stage",
                             "Level 4 - EX Stage", "Level 5 - EX Stage",
                             "Level 6 - 1st EX Stage", "Level 6 - 2nd EX Stage"]
            ex_stage_items = world.ex_stage_order[player]
            for _ in range(len(ex_stage_locs)):
                ex_stage_loc = ex_stage_locs.pop(0)
                ex_stage_item = ex_stage_items.pop(0)
                for ex_loc in multiworld.get_locations(player):
                    if ex_stage_item in ex_loc.parent_region.name:
                        hint_data[player][ex_loc.address] = ex_stage_loc

        # 4 shuffles all stages among themselves, such that they can take the place of any other stage in the game.
        if stage_shuffle == 4:
            stage_locs = ["Level 1 - 1st Stage", "Level 1 - 2nd Stage",
                          "Level 1 - 3rd Stage", "Level 1 - 4th Stage", "Level 1 - EX Stage",
                          "Level 2 - 1st Stage", "Level 2 - 2nd Stage",
                          "Level 2 - 3rd Stage", "Level 2 - 4th Stage", "Level 2 - EX Stage",
                          "Level 3 - 1st Stage", "Level 3 - 2nd Stage", "Level 3 - 3rd Stage",
                          "Level 3 - 4th Stage", "Level 3 - 5th Stage", "Level 3 - EX Stage",
                          "Level 4 - 1st Stage", "Level 4 - 2nd Stage", "Level 4 - 3rd Stage",
                          "Level 4 - 4th Stage", "Level 4 - 5th Stage", "Level 4 - EX Stage",
                          "Level 5 - 1st Stage", "Level 5 - 2nd Stage", "Level 5 - 3rd Stage",
                          "Level 5 - 4th Stage", "Level 5 - 5th Stage", "Level 5 - EX Stage",
                          "Level 6 - 1st Stage", "Level 6 - 2nd Stage",
                          "Level 6 - 3rd Stage", "Level 6 - 4th Stage",
                          "Level 6 - 5th Stage", "Level 6 - 1st EX Stage", "Level 6 - 2nd EX Stage"]
            stage_items = world.stage_order[player]
            for _ in range(len(stage_locs)):
                stage_loc = stage_locs.pop(0)
                stage_item = stage_items.pop(0)
                for loc in multiworld.get_locations(player):
                    if stage_item in loc.parent_region.name:
                        hint_data[player][loc.address] = stage_loc

    # Boss Shuffle works a little differently when compared to Stage Shuffle, but for the most part it's the same.
    # This code is designed to work for all versions of Boss Shuffle, so we can just check if it's enabled.
    if boss_shuffle > 0:
        boss_locs = ["Level 1 Boss", "Level 2 Boss", "Level 3 Boss", "Level 4 Boss", "Level 5 Boss", "Level 6 Boss"]
        boss_items = world.boss_order[player]
        # We go by the item count instead of the location count because there
        # can be fewer items than locations listed if Masked Dedede isn't shuffled.
        # This way, since the names and order are always the same, we can handle it all within a single check.
        for _ in range(len(boss_items)):
            boss_loc = boss_locs.pop(0)
            boss_item = boss_items.pop(0)
            # Since the item names don't match the region names in this case,
            # we check for which item we're looking at and get its equivalent region name.
            # There's probably a more efficient way of doing this, but I couldn't figure it out.
            if boss_item == "VS Flowery Woods":
                boss_item = "Fine Fields Boss"
            if boss_item == "VS Paintra":
                boss_item = "Lollipop Land Boss"
            if boss_item == "VS Kracko":
                boss_item = "Old Odyssey Boss"
            if boss_item == "VS Coily Rattler":
                boss_item = "Wild World Boss"
            if boss_item == "VS Pyribbit":
                boss_item = "Endless Explosions Boss"
            if boss_item == "VS Masked Dedede":
                boss_item = "Royal Road Boss"
            for boss in multiworld.get_locations(player):
                if boss_item in boss.parent_region.name:
                    hint_data[player][boss.address] = boss_loc
