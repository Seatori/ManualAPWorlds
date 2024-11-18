# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, ItemClassification


def shuffle_stages_early(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    stage_shuffle = world.options.stage_shuffle

    world.main_stage_order = {}
    if player not in world.main_stage_order:
        world.main_stage_order[player] = []

    world.ex_stage_order = {}
    if player not in world.ex_stage_order:
        world.ex_stage_order[player] = []

    world.stage_order = {}
    if player not in world.stage_order:
        world.stage_order[player] = []

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
        world.main_stage_order[player].append(first_stage.name)
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
        world.main_stage_order[player].append(first_stage.name)
        multiworld.push_precollected(first_stage)
        item_pool.remove(first_stage)
    elif stage_shuffle == 4:
        # Since stages are shuffled, we need to get one for the player to start with.
        # In this case, we can start with any stage since they can each be in any position.
        stages = [i for i in item_pool
                  if "Stage 1" in i.name or "Stage 2" in i.name or "Stage 3" in i.name
                  or "Stage 4" in i.name or "Stage 5" in i.name or "Stage EX" in i.name]
        first_stage = world.random.choice(stages)
        world.stage_order[player].append(first_stage.name)
        multiworld.push_precollected(first_stage)
        item_pool.remove(first_stage)
    else:
        raise Exception("Invalid value for option 'Stage Shuffle'. Please report this to the maintainer.")

    return item_pool


def shuffle_stages(world: World, multiworld: MultiWorld, player: int) -> list:
    stage_shuffle = world.options.stage_shuffle

    if stage_shuffle == 1 or stage_shuffle == 3:
        main_stage_locs = [loc for loc in multiworld.get_locations(player)
                           if "Unlock 1st Stage" in loc.name or "Unlock 2nd Stage" in loc.name
                           or "Unlock 3rd" in loc.name or "Unlock 4th" in loc.name or "Unlock 5th" in loc.name]
        main_stage_items = [i for i in multiworld.get_items() if i.player == player
                            and ("Stage 1" in i.name or "Stage 2" in i.name or "Stage 3" in i.name
                            or "Stage 4" in i.name or "Stage 5" in i.name)]

        for main_stage in main_stage_locs:
            main_stage_item = world.random.choice(main_stage_items)
            world.main_stage_order[player].append(main_stage_item.name)
            main_stage.place_locked_item(main_stage_item)
            multiworld.itempool.remove(main_stage_item)
            main_stage_items.remove(main_stage_item)

    if stage_shuffle == 2 or stage_shuffle == 3:
        ex_stage_locs = [loc for loc in multiworld.get_locations(player)
                         if "Unlock EX" in loc.name or "Unlock 1st EX" in loc.name or "Unlock 2nd EX" in loc.name]
        ex_stage_items = [i for i in multiworld.get_items() if i.player == player
                          and "Stage EX" in i.name]

        for ex_stage in ex_stage_locs:
            ex_stage_item = world.random.choice(ex_stage_items)
            world.ex_stage_order[player].append(ex_stage_item.name)
            ex_stage.place_locked_item(ex_stage_item)
            multiworld.itempool.remove(ex_stage_item)
            ex_stage_items.remove(ex_stage_item)

    if stage_shuffle == 4:
        stage_locs = [loc for loc in multiworld.get_locations(player)
                      if "Level" in loc.name and "Boss" not in loc.name]
        stage_items = [i for i in multiworld.get_items() if i.player == player
                       and "Stage" in i.name and "Key" not in i.name]

        for stage in stage_locs:
            stage_item = world.random.choice(stage_items)
            world.stage_order[player].append(stage_item.name)
            stage.place_locked_item(stage_item)
            multiworld.itempool.remove(stage_item)
            stage_items.remove(stage_item)


def shuffle_bosses(world: World, multiworld: MultiWorld, player: int) -> list:
    boss_shuffle = world.options.boss_shuffle

    world.boss_order = {}
    if player not in world.boss_order:
        world.boss_order[player] = []

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
        masked_dedede_loc = [loc for loc in multiworld.get_locations(player)
                             if "Level 6 Boss" in loc.name]
        masked_dedede_item = next(i for i in multiworld.get_items()
                                  if i.player == player and i.name == "VS Masked Dedede")
        place_dedede = masked_dedede_loc.pop()
        place_dedede.place_locked_item(masked_dedede_item)
        multiworld.itempool.remove(masked_dedede_item)

        boss_stage_locs = [loc for loc in multiworld.get_locations(player)
                           if "Level 1 Boss" in loc.name or "Level 2 Boss" in loc.name or "Level 3 Boss" in loc.name
                           or "Level 4 Boss" in loc.name or "Level 5 Boss" in loc.name]
        boss_stage_items = [i for i in multiworld.get_items()
                            if i.player == player and "VS" in i.name and "VS Masked Dedede" not in i.name]

        for boss_loc in boss_stage_locs:
            boss_item = world.random.choice(boss_stage_items)
            world.boss_order[player].append(boss_item.name)
            boss_loc.place_locked_item(boss_item)
            multiworld.itempool.remove(boss_item)
            boss_stage_items.remove(boss_item)

    if boss_shuffle == 2:
        masked_dedede_loc = [loc for loc in multiworld.get_locations(player) if "Level 1 Boss" in loc.name]
        masked_dedede_item = next(i for i in multiworld.get_items()
                                  if i.player == player and i.name == "VS Masked Dedede")
        world.boss_order[player].append(masked_dedede_item.name)
        place_dedede = masked_dedede_loc.pop()
        place_dedede.place_locked_item(masked_dedede_item)
        multiworld.itempool.remove(masked_dedede_item)

        boss_stage_locs = [loc for loc in multiworld.get_locations(player)
                           if "Level 2 Boss" in loc.name or "Level 3 Boss" in loc.name or "Level 4 Boss" in loc.name
                           or "Level 5 Boss" in loc.name or "Level 6 Boss" in loc.name]
        boss_stage_items = [i for i in multiworld.get_items()
                            if i.player == player and "VS" in i.name and "VS Masked Dedede" not in i.name]

        for boss_loc in boss_stage_locs:
            boss_item = world.random.choice(boss_stage_items)
            world.boss_order[player].append(boss_item.name)
            boss_loc.place_locked_item(boss_item)
            multiworld.itempool.remove(boss_item)
            boss_stage_items.remove(boss_item)

    if boss_shuffle == 3:
        boss_stage_locs = [loc for loc in multiworld.get_locations(player)
                           if "Level 1 Boss" in loc.name or "Level 2 Boss" in loc.name or "Level 3 Boss" in loc.name
                           or "Level 4 Boss" in loc.name or "Level 5 Boss" in loc.name or "Level 6 Boss" in loc.name]
        boss_stage_items = [i for i in multiworld.get_items() if i.player == player and "VS" in i.name]

        for boss_loc in boss_stage_locs:
            boss_item = world.random.choice(boss_stage_items)
            world.boss_order[player].append(boss_item.name)
            boss_loc.place_locked_item(boss_item)
            multiworld.itempool.remove(boss_item)
            boss_stage_items.remove(boss_item)
