# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, ItemClassification

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

import re


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
    if world.options.enable_kirby_fighters_locations:
        raise Exception("Outdated option name 'enable_kirby_fighters_locations' detected. Please use an updated YAML.")
    sectonia_boss_req = get_option_value(multiworld, player, "queen_sectonia_boss_requirement")
    if sectonia_boss_req == -1:
        world.options.goal.value = sectonia_boss_req + 1
    else:
        world.options.goal.value = sectonia_boss_req


# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    level_1_boss = get_option_value(multiworld, player, "level_1_boss_sun_stones")
    if level_1_boss > 0: 
        remove_first_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 1 Boss" in loc.name
                             and f"- {level_1_boss} Sun Stone" not in loc.name]
    else:
        remove_first_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 1 Boss -" in loc.name]

    level_2_boss = get_option_value(multiworld, player, "level_2_boss_sun_stones")
    if level_2_boss > 0: 
        remove_second_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 2 Boss" in loc.name
                              and f"- {level_2_boss} Sun Stone" not in loc.name]
    else:
        remove_second_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 2 Boss -" in loc.name]

    level_3_boss = get_option_value(multiworld, player, "level_3_boss_sun_stones")
    if level_3_boss > 0: 
        remove_third_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 3 Boss" in loc.name
                             and f"- {level_3_boss} Sun Stone" not in loc.name]
    else:
        remove_third_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 3 Boss -" in loc.name]

    level_4_boss = get_option_value(multiworld, player, "level_4_boss_sun_stones")
    if level_4_boss > 0: 
        remove_fourth_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 4 Boss" in loc.name
                              and f"- {level_4_boss} Sun Stone" not in loc.name]
    else:
        remove_fourth_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 4 Boss -" in loc.name]

    level_5_boss = get_option_value(multiworld, player, "level_5_boss_sun_stones")
    if level_5_boss > 0: 
        remove_fifth_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 5 Boss" in loc.name
                             and f"- {level_5_boss} Sun Stone" not in loc.name]
    else:
        remove_fifth_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 5 Boss -" in loc.name]

    level_6_boss = get_option_value(multiworld, player, "level_6_boss_sun_stones")
    if level_6_boss > 0: 
        remove_sixth_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 6 Boss" in loc.name
                             and f"- {level_6_boss} Sun Stone" not in loc.name]
    else:
        remove_sixth_boss = [loc.name for loc in multiworld.get_locations(player) if "Level 6 Boss -" in loc.name]

    keychains = get_option_value(multiworld, player, "keychain_locations")
    if keychains == 1:
        remove_keychains = [loc.name for loc in multiworld.get_locations(player) if "- Keychain" in loc.name
                            or "Left Keychain" in loc.name or "Right Keychain" in loc.name]
    elif keychains == 0:
        remove_keychains = [loc.name for loc in multiworld.get_locations(player) if "Keychain" in loc.name]
    else:
        remove_keychains = []

    stage_shuffle = get_option_value(multiworld, player, "stage_shuffle")
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

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)

    keychains = get_option_value(multiworld, player, "keychain_locations")
    if keychains == 0:
        rare_keychains = [i.name for i in item_pool if " Keychain" in i.name]
        for keychains_to_remove in rare_keychains:
            remove_keychains = next(i for i in item_pool if i.name == keychains_to_remove)
            item_pool.remove(remove_keychains)

    stage_shuffle = get_option_value(multiworld, player, "stage_shuffle")
    if stage_shuffle == 0:
        # No stages are shuffled here, so we don't need any stage items.
        stages = [i.name for i in item_pool
                  if "Stage 1" in i.name or "Stage 2" in i.name or "Stage 3" in i.name
                  or "Stage 4" in i.name or "Stage 5" in i.name or "Stage EX" in i.name]
        for stages_to_remove in stages:
            remove_stages = next(i for i in item_pool if i.name == stages_to_remove)
            item_pool.remove(remove_stages)
    elif stage_shuffle == 1:
        # EX stages aren't shuffled here, so we don't need their items.
        ex_stages = [i.name for i in item_pool if "Stage EX" in i.name]
        for ex_stages_to_remove in ex_stages:
            remove_ex_stages = next(i for i in item_pool if i.name == ex_stages_to_remove)
            item_pool.remove(remove_ex_stages)

        # Since only main stages are shuffled, we need to get one for the player to start with.
        main_stages = [i for i in item_pool
                       if "Stage 1" in i.name or "Stage 2" in i.name or "Stage 3" in i.name
                       or "Stage 4" in i.name or "Stage 5" in i.name]
        first_stage = world.random.choice(main_stages)
        multiworld.push_precollected(first_stage)
        item_pool.remove(first_stage)
    elif stage_shuffle == 2:
        # Main stages aren't shuffled here, so we don't need their items.
        main_stages = [i.name for i in item_pool
                       if "Stage 1" in i.name or "Stage 2" in i.name or "Stage 3" in i.name
                       or "Stage 4" in i.name or "Stage 5" in i.name]
        for main_stages_to_remove in main_stages:
            remove_main_stages = next(i for i in item_pool if i.name == main_stages_to_remove)
            item_pool.remove(remove_main_stages)
    elif stage_shuffle == 3:
        # Since stages are shuffled, we need to get one for the player to start with.
        # We're only checking for main stages here because EX stages should always be shuffled between themselves.
        main_stages = [i for i in item_pool
                       if "Stage 1" in i.name or "Stage 2" in i.name or "Stage 3" in i.name
                       or "Stage 4" in i.name or "Stage 5" in i.name]
        first_stage = world.random.choice(main_stages)
        multiworld.push_precollected(first_stage)
        item_pool.remove(first_stage)
    elif stage_shuffle == 4:
        # Since stages are shuffled, we need to get one for the player to start with.
        # In this case, we can start with any stage since they can each be in any position.
        stages = [i for i in item_pool
                  if "Stage 1" in i.name or "Stage 2" in i.name or "Stage 3" in i.name
                  or "Stage 4" in i.name or "Stage 5" in i.name or "Stage EX" in i.name]
        first_stage = world.random.choice(stages)
        multiworld.push_precollected(first_stage)
        item_pool.remove(first_stage)
    else:
        raise Exception("Invalid value for option 'Stage Shuffle'. Please report this to the maintainer.")

    # If we want our excess Sun Stones to be progression items, we don't need to do anything here.
    if world.options.excess_sun_stones == 0:
        return item_pool

    # Getting the number of how many Sun Stones need to be progression items.
    prog_sun_stones = max(world.options.level_1_boss_sun_stones, world.options.level_2_boss_sun_stones,
                          world.options.level_3_boss_sun_stones, world.options.level_4_boss_sun_stones,
                          world.options.level_5_boss_sun_stones, world.options.level_6_boss_sun_stones)
    # Checking how many Sun Stones are in the pool.
    total_sun_stones = [i for i in item_pool if i.name == "Sun Stone"]
    # Calculating the number of unnecessary Sun Stones by subtracting the number in the pool by how many are needed.
    excess_sun_stones = len(total_sun_stones) - prog_sun_stones

    # If we know that our excess Sun Stones are being removed, it doesn't matter how many are needed.
    # So we do this step before checking if we should end.
    if world.options.excess_sun_stones == 3:
        for _, item in zip(range(excess_sun_stones), total_sun_stones):
            sun_stones = next(i for i in item_pool if i.name == "Sun Stone")
            item_pool.remove(sun_stones)
        return item_pool

    # If no Sun Stones are required for any bosses, we always want any that may be in the pool to be filler.
    # This is handled in a later function, so we can just quit out here.
    if prog_sun_stones == 0:
        return item_pool

    # Modifying the unneeded Sun Stones based on which option was chosen.
    if world.options.excess_sun_stones == 1:
        for _, item in zip(range(excess_sun_stones), total_sun_stones):
            item.classification = ItemClassification.useful
        return item_pool
    elif world.options.excess_sun_stones == 2:
        for _, item in zip(range(excess_sun_stones), total_sun_stones):
            item.classification = ItemClassification.filler
        return item_pool
    else:
        # By this point, all four valid options should have been accounted for, so we throw an error if it went wrong.
        raise Exception("Invalid value for option 'Excess Sun Stones'. Please report this to the maintainer.")

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
    stage_shuffle = get_option_value(multiworld, player, "stage_shuffle")
    boss_shuffle = get_option_value(multiworld, player, "boss_shuffle")
    # Stage Shuffle 4 and Boss Shuffle 3 are the default behavior, so we don't need to place anything here.
    # Stage Shuffle 0 doesn't need any items placed, so we also check for it.
    if (stage_shuffle == 0 or stage_shuffle == 4) and boss_shuffle == 3:
        return

    if stage_shuffle == 1 or stage_shuffle == 3:
        main_stage_locs = [loc for loc in multiworld.get_locations(player)
                           if "Unlock 1st Stage" in loc.name or "Unlock 2nd Stage" in loc.name
                           or "Unlock 3rd" in loc.name or "Unlock 4th" in loc.name or "Unlock 5th" in loc.name]
        main_stage_items = [i for i in multiworld.get_items() if i.player == player
                            and ("Stage 1" in i.name or "Stage 2" in i.name or "Stage 3" in i.name
                            or "Stage 4" in i.name or "Stage 5" in i.name)]
        for main_stage in main_stage_items:
            if len(main_stage_locs) == 0:
                break

            next_main_stage = world.random.choice(main_stage_locs)
            next_main_stage.place_locked_item(main_stage)
            multiworld.itempool.remove(main_stage)
            main_stage_locs.remove(next_main_stage)

    if stage_shuffle == 2 or stage_shuffle == 3:
        ex_stage_locs = [loc for loc in multiworld.get_locations(player)
                         if "Unlock EX" in loc.name or "Unlock 1st EX" in loc.name or "Unlock 2nd EX" in loc.name]
        ex_stage_items = [i for i in multiworld.get_items() if i.player == player
                          and "Stage EX" in i.name]

        for ex_stage in ex_stage_items:
            if len(ex_stage_locs) == 0:
                break

            next_ex_stage = world.random.choice(ex_stage_locs)
            next_ex_stage.place_locked_item(ex_stage)
            multiworld.itempool.remove(ex_stage)
            ex_stage_locs.remove(next_ex_stage)

    if boss_shuffle == 0:
        boss_stage_locs = [loc for loc in multiworld.get_locations(player)
                           if "Level 1 Boss" in loc.name or "Level 2 Boss" in loc.name or "Level 3 Boss" in loc.name
                           or "Level 4 Boss" in loc.name or "Level 5 Boss" in loc.name or "Level 6 Boss" in loc.name]
        boss_stage_items = [i for i in multiworld.get_items() if i.player == player and "VS" in i.name]
        for boss in boss_stage_items:
            if len(boss_stage_locs) == 0:
                break

            boss_locations = boss_stage_locs.pop(0)
            boss_locations.place_locked_item(boss)
            multiworld.itempool.remove(boss)

    if boss_shuffle == 1:
        masked_dedede_loc = [loc for loc in multiworld.get_locations(player) if "Level 6 Boss" in loc.name]
        masked_dedede_item = [i for i in multiworld.get_items() if i.player == player and i.name == "VS Masked Dedede"]
        for boss in masked_dedede_item:
            if len(masked_dedede_loc) == 0:
                break

            place_dedede = masked_dedede_loc.pop()
            place_dedede.place_locked_item(boss)
            multiworld.itempool.remove(boss)

    if boss_shuffle == 2:
        masked_dedede_loc = [loc for loc in multiworld.get_locations(player) if "Level 1 Boss" in loc.name]
        masked_dedede_item = [i for i in multiworld.get_items() if i.player == player and i.name == "VS Masked Dedede"]
        for boss in masked_dedede_item:
            if len(masked_dedede_loc) == 0:
                break

            place_dedede = masked_dedede_loc.pop()
            place_dedede.place_locked_item(boss)
            multiworld.itempool.remove(boss)


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
    pass
