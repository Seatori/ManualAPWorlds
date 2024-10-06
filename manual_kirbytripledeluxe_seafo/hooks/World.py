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
    world.options.goal.value = get_option_value(multiworld, player, 'queen_sectonia_boss_requirement') - 1

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
    
    # atr = is_option_enabled(multiworld, player, "randomize_ability_testing_room")
    abilities = is_option_enabled(multiworld, player, "randomize_copy_abilities")
    archer = next(i for i in item_pool if i.name == "Archer")
    beam = next(i for i in item_pool if i.name == "Beam")
    beetle = next(i for i in item_pool if i.name == "Beetle")
    bell = next(i for i in item_pool if i.name == "Bell")
    bomb = next(i for i in item_pool if i.name == "Bomb")
    circus = next(i for i in item_pool if i.name == "Circus")
    crash = next(i for i in item_pool if i.name == "Crash")
    cutter = next(i for i in item_pool if i.name == "Cutter")
    fighter = next(i for i in item_pool if i.name == "Fighter")
    fire = next(i for i in item_pool if i.name == "Fire")
    hammer = next(i for i in item_pool if i.name == "Hammer")
    ice = next(i for i in item_pool if i.name == "Ice")
    leaf = next(i for i in item_pool if i.name == "Leaf")
    mike = next(i for i in item_pool if i.name == "Mike")
    needle = next(i for i in item_pool if i.name == "Needle")
    ninja = next(i for i in item_pool if i.name == "Ninja")
    parasol = next(i for i in item_pool if i.name == "Parasol")
    sleep = next(i for i in item_pool if i.name == "Sleep")
    spark = next(i for i in item_pool if i.name == "Spark")
    spear = next(i for i in item_pool if i.name == "Spear")
    stone = next(i for i in item_pool if i.name == "Stone")
    sword = next(i for i in item_pool if i.name == "Sword")
    wheel = next(i for i in item_pool if i.name == "Wheel")
    whip = next(i for i in item_pool if i.name == "Whip")
    wing = next(i for i in item_pool if i.name == "Wing")
    if not abilities:
        multiworld.push_precollected(archer)
        multiworld.push_precollected(beam)
        multiworld.push_precollected(beetle)
        multiworld.push_precollected(bell)
        multiworld.push_precollected(bomb)
        multiworld.push_precollected(circus)
        multiworld.push_precollected(crash)
        multiworld.push_precollected(cutter)
        multiworld.push_precollected(fighter)
        multiworld.push_precollected(fire)
        multiworld.push_precollected(hammer)
        multiworld.push_precollected(ice)
        multiworld.push_precollected(leaf)
        multiworld.push_precollected(mike)
        multiworld.push_precollected(needle)
        multiworld.push_precollected(ninja)
        multiworld.push_precollected(parasol)
        multiworld.push_precollected(sleep)
        multiworld.push_precollected(spark)
        multiworld.push_precollected(spear)
        multiworld.push_precollected(stone)
        multiworld.push_precollected(sword)
        multiworld.push_precollected(wheel)
        multiworld.push_precollected(whip)
        multiworld.push_precollected(wing)
        item_pool.remove(archer)
        item_pool.remove(beam)
        item_pool.remove(beetle)
        item_pool.remove(bell)
        item_pool.remove(bomb)
        item_pool.remove(circus)
        item_pool.remove(crash)
        item_pool.remove(cutter)
        item_pool.remove(fighter)
        item_pool.remove(fire)
        item_pool.remove(hammer)
        item_pool.remove(ice)
        item_pool.remove(leaf)
        item_pool.remove(mike)
        item_pool.remove(needle)
        item_pool.remove(ninja)
        item_pool.remove(parasol)
        item_pool.remove(sleep)
        item_pool.remove(spark)
        item_pool.remove(spear)
        item_pool.remove(stone)
        item_pool.remove(sword)
        item_pool.remove(wheel)
        item_pool.remove(whip)
        item_pool.remove(wing)

    keychains = get_option_value(multiworld, player, "keychain_locations")
    if keychains == 0:
        rare_keychains = [i.name for i in item_pool if " Keychain" in i.name]
        for keychains_to_remove in rare_keychains:
            remove_keychains = next(i for i in item_pool if i.name == keychains_to_remove)
            item_pool.remove(remove_keychains)

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
    if item.name == "Sleep":
        item.classification = ItemClassification.trap
    if item.name == "Wing":
        if world.options.logic_difficulty == 0:
            item.classification = ItemClassification.useful
    if item.name == "Bomb":
        if world.options.logic_difficulty == 0 and not world.options.enable_kirby_fighters_locations:
            item.classification = ItemClassification.useful
    if item.name == "Copy Ability Testing Room":
        if world.options.logic_difficulty < 2 or not world.options.randomize_copy_abilities:
            item.classification = ItemClassification.useful

    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    pass

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
