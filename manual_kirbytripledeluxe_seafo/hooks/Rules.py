from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_option_value
from BaseClasses import MultiWorld, CollectionState

import re


# Functions used to check the logic difficulty level.
def easy_logic(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.logic_difficulty == 0:
        return True
    else:
        return False


def normal_logic(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.logic_difficulty == 1:
        return True
    else:
        return False


def hard_logic(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.logic_difficulty == 2:
        return True
    else:
        return False


def not_easy_logic(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.logic_difficulty > 0:
        return True
    else:
        return False


# Functions used to check if the stage randomizer has been disabled.
def vanilla_main_stages(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return True
    else:
        return False


def vanilla_ex_stages(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle < 2:
        return True
    else:
        return False


# Sectonia's fight gives the player access to the following abilities:
# Archer, Beetle, Bomb, Fighter, Fire, Ice, Leaf, Spark, Stone, Whip, and Wing.
#
# If the Copy Ability Testing Room requires its vanilla conditions, this is used for that as well.
def can_fight_sectonia(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.queen_sectonia_boss_requirement == -1:
        return state.has("VS Masked Dedede", player)
    else:
        return state.has_group_unique("Bosses", player, world.options.queen_sectonia_boss_requirement.value)


def can_use_archer(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return (state.has("Archer", player)
                and (state.has("Grand Sun Stone", player, 1)
                     or state.has("Lollipop Land Stage EX", player)
                     or state.has("VS Coily Rattler", player)
                     or state.has("Endless Explosions Stage EX", player)
                     or state.has("VS Masked Dedede", player)
                     or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    elif world.options.stage_shuffle == 1:
        return (state.has("Archer", player)
                and (state.has("Lollipop Land Stage 2", player) or state.has("Lollipop Land Stage 3", player)
                     or (state.has("Grand Sun Stone", player, 1)
                         and (state.has("Progressive EX Stage Key", player, 2)
                              or state.has("Level 2 EX Stage Key", player)
                              )
                         )
                     or state.has("Old Odyssey Stage 1", player) or state.has("Old Odyssey Stage 2", player)
                     or state.has("Old Odyssey Stage 4", player) or state.has("Wild World Stage 1", player)
                     or state.has("VS Coily Rattler", player) or state.has("Endless Explosions Stage 4", player)
                     or state.has("Royal Road Stage 1", player) or state.has("Royal Road Stage 2", player)
                     or state.has("Royal Road Stage 4", player) or state.has("Royal Road Stage 5", player)
                     or state.has("VS Masked Dedede", player) or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    else:
        return (state.has("Archer", player)
                and (state.has("Lollipop Land Stage 2", player) or state.has("Lollipop Land Stage 3", player)
                     or state.has("Lollipop Land Stage EX", player) or state.has("Old Odyssey Stage 1", player)
                     or state.has("Old Odyssey Stage 2", player) or state.has("Old Odyssey Stage 4", player)
                     or state.has("Wild World Stage 1", player) or state.has("VS Coily Rattler", player)
                     or state.has("Endless Explosions Stage 4", player)
                     or state.has("Endless Explosions Stage EX", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 2", player) or state.has("Royal Road Stage 4", player)
                     or state.has("Royal Road Stage 5", player) or state.has("VS Masked Dedede", player)
                     or state.has("Royal Road Stage EX 1", player) or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )


def can_use_beam(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return state.has("Beam", player)
    elif world.options.stage_shuffle == 1:
        return (state.has("Beam", player)
                and (state.has("Fine Fields Stage 1", player) or state.has("Fine Fields Stage 4", player)
                     or state.has("VS Flowery Woods", player) or state.has("Progressive EX Stage Key", player, 1)
                     or state.has("Level 1 EX Stage Key", player) or state.has("Lollipop Land Stage 1", player)
                     or state.has("Lollipop Land Stage 3", player)
                     or (state.has("Grand Sun Stone", player, 1) and state.has("Level 2 EX Stage Key", player))
                     or state.has("Old Odyssey Stage 2", player) or state.has("Old Odyssey Stage 4", player)
                     or state.has("Old Odyssey Stage 5", player) or state.has("VS Kracko", player)
                     or state.has("Wild World Stage 1", player) or state.has("Wild World Stage 3", player)
                     or state.has("Wild World Stage 5", player) or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 4", player)
                     or state.has("VS Masked Dedede", player) or state.has("Copy Ability Testing Room", player)
                     )
                )
    else:
        return (state.has("Beam", player)
                and (state.has("Fine Fields Stage 1", player) or state.has("Fine Fields Stage 4", player)
                     or state.has("VS Flowery Woods", player) or state.has("Fine Fields Stage EX", player)
                     or state.has("Lollipop Land Stage 1", player) or state.has("Lollipop Land Stage 3", player)
                     or state.has("Lollipop Land Stage EX", player) or state.has("Old Odyssey Stage 2", player)
                     or state.has("Old Odyssey Stage 4", player) or state.has("Old Odyssey Stage 5", player)
                     or state.has("VS Kracko", player) or state.has("Wild World Stage 1", player)
                     or state.has("Wild World Stage 3", player) or state.has("Wild World Stage 5", player)
                     or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 4", player)
                     or state.has("VS Masked Dedede", player) or state.has("Copy Ability Testing Room", player)
                     )
                )


def can_use_beetle(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return state.has("Beetle", player)
    elif world.options.stage_shuffle == 1:
        return (state.has("Beetle", player)
                and (state.has("Fine Fields Stage 4", player) or state.has("VS Flowery Woods", player)
                     or state.has("Progressive EX Stage Key", player, 1) or state.has("Level 1 EX Stage Key", player)
                     or state.has("Wild World Stage 1", player) or state.has("Endless Explosions Stage 5", player)
                     or (state.has("Grand Sun Stone", player, 4) and state.has("Level 5 EX Stage Key", player))
                     or state.has("Royal Road Stage 1", player) or state.has("Royal Road Stage 5", player)
                     or state.has("VS Masked Dedede", player) or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    else:
        return (state.has("Beetle", player)
                and (state.has("Fine Fields Stage 4", player) or state.has("VS Flowery Woods", player)
                     or state.has("Fine Fields Stage EX", player) or state.has("Wild World Stage 1", player)
                     or state.has("Endless Explosions Stage 5", player)
                     or state.has("Endless Explosions Stage EX", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 5", player) or state.has("VS Masked Dedede", player)
                     or state.has("Royal Road Stage EX 1", player) or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )


def can_use_bell(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return state.has("Bell", player)
    # We don't need a dedicated case for only main stages being shuffled because the relevant EX stages always
    # become accessible only after the player is guaranteed to have encountered a Bell stage,
    # so we can just check the full list of Bell stages.
    else:
        return (state.has("Bell", player)
                and (state.has("Fine Fields Stage 2", player) or state.has("Fine Fields Stage 4", player)
                     or state.has("VS Paintra", player) or state.has("Old Odyssey Stage 1", player)
                     or state.has("Old Odyssey Stage 3", player) or state.has("Wild World Stage 2", player)
                     or state.has("VS Coily Rattler", player) or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage EX", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 4", player) or state.has("VS Masked Dedede", player)
                     or state.has("Royal Road Stage EX 1", player) or state.has("Copy Ability Testing Room", player)
                     )
                )


def can_use_bomb(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return (state.has("Bomb", player)
                and (state.has("Grand Sun Stone", player, 1)
                     or state.has("Lollipop Land Stage EX", player)
                     or state.has("Old Odyssey Stage EX", player)
                     or state.has("VS Pyribbit", player)
                     or state.has("Endless Explosions Stage EX", player)
                     or state.has("VS Masked Dedede", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    elif world.options.stage_shuffle == 1:
        return (state.has("Bomb", player)
                and (state.has("Lollipop Land Stage 3", player) or state.has("Lollipop Land Stage 4", player)
                     or (state.has("Grand Sun Stone", player, 1)
                         and (state.has("Progressive EX Stage Key", player, 2)
                              or state.has("Level 2 EX Stage Key", player)
                              )
                         )
                     or state.has("Old Odyssey Stage 2", player) or state.has("Old Odyssey Stage 3", player)
                     or state.has("Old Odyssey Stage 4", player)
                     or (state.has("Grand Sun Stone", player, 2) and state.has("Level 3 EX Stage Key", player))
                     or state.has("Wild World Stage 1", player) or state.has("Wild World Stage 2", player)
                     or state.has("Wild World Stage 3", player) or state.has("Wild World Stage 4", player)
                     or state.has("Wild World Stage 5", player) or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 4", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("VS Pyribbit", player)
                     or state.has("Royal Road Stage 2", player) or state.has("Royal Road Stage 5", player)
                     or state.has("VS Masked Dedede", player) or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    else:
        return (state.has("Bomb", player)
                and (state.has("Lollipop Land Stage 3", player) or state.has("Lollipop Land Stage 4", player)
                     or state.has("Lollipop Land Stage EX", player) or state.has("Old Odyssey Stage 2", player)
                     or state.has("Old Odyssey Stage 3", player) or state.has("Old Odyssey Stage 4", player)
                     or state.has("Old Odyssey Stage EX", player) or state.has("Wild World Stage 1", player)
                     or state.has("Wild World Stage 2", player) or state.has("Wild World Stage 3", player)
                     or state.has("Wild World Stage 4", player) or state.has("Wild World Stage 5", player)
                     or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 4", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("VS Pyribbit", player)
                     or state.has("Endless Explosions Stage EX", player) or state.has("Royal Road Stage 2", player)
                     or state.has("Royal Road Stage 5", player) or state.has("VS Masked Dedede", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )


def can_use_circus(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return (state.has("Circus", player)
                and (state.has("Grand Sun Stone", player, 1)
                     or state.has("Wild World Stage EX", player)
                     or state.has("VS Masked Dedede", player)
                     or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )
    elif world.options.stage_shuffle == 1:
        return (state.has("Circus", player)
                and (state.has("Lollipop Land Stage 4", player) or state.has("VS Paintra", player)
                     or state.has("Old Odyssey Stage 5", player) or state.has("Wild World Stage 4", player)
                     or (state.has("Grand Sun Stone", player, 3)
                         and (state.has("Progressive EX Stage Key", player, 4)
                              or state.has("Level 4 EX Stage Key", player)
                              )
                         )
                     or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 2", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 2", player) or state.has("VS Masked Dedede", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )
    else:
        return (state.has("Circus", player)
                and (state.has("Lollipop Land Stage 4", player) or state.has("VS Paintra", player)
                     or state.has("Old Odyssey Stage 5", player) or state.has("Wild World Stage 4", player)
                     or state.has("Wild World Stage EX", player) or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 2", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 2", player) or state.has("VS Masked Dedede", player)
                     or state.has("Royal Road Stage EX 1", player) or state.has("Copy Ability Testing Room", player)
                     )
                )


def can_use_crash(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return (state.has("Crash", player)
                and (state.has("Grand Sun Stone", player, 1)
                     or state.has("Old Odyssey Stage EX", player)
                     or state.has("Wild World Stage EX", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )
    elif world.options.stage_shuffle == 1:
        return (state.has("Crash", player)
                and (state.has("Lollipop Land Stage 3", player)
                     or (state.has("Grand Sun Stone", player, 2)
                         and (state.has("Progressive EX Stage Key", player, 3)
                              or state.has("Level 3 EX Stage Key", player)
                              )
                         )
                     or state.has("Wild World Stage 3", player) or state.has("Wild World Stage 4", player)
                     or (state.has("Grand Sun Stone", player, 3) and state.has("Level 4 EX Stage Key", player))
                     or state.has("Royal Road Stage 5", player) or state.has("Copy Ability Testing Room", player)
                     )
                )
    else:
        return (state.has("Crash", player)
                and (state.has("Lollipop Land Stage 3", player) or state.has("Old Odyssey Stage EX", player)
                     or state.has("Wild World Stage 3", player) or state.has("Wild World Stage 4", player)
                     or state.has("Wild World Stage EX", player) or state.has("Royal Road Stage 5", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )


def can_use_cutter(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return state.has("Cutter", player)
    elif world.options.stage_shuffle == 1:
        return (state.has("Cutter", player)
                and (state.has("Fine Fields Stage 3", player) or state.has("Fine Fields Stage 4", player)
                     or state.has("VS Flowery Woods", player) or state.has("Progressive EX Stage Key", player, 1)
                     or state.has("Level 1 EX Stage Key", player) or state.has("Lollipop Land Stage 1", player)
                     or state.has("Lollipop Land Stage 2", player) or state.has("Old Odyssey Stage 1", player)
                     or state.has("Old Odyssey Stage 2", player) or state.has("Old Odyssey Stage 3", player)
                     or state.has("Old Odyssey Stage 4", player) or state.has("Wild World Stage 1", player)
                     or state.has("Wild World Stage 4", player) or state.has("Wild World Stage 5", player)
                     or state.has("Endless Explosions Stage 2", player)
                     or state.has("Endless Explosions Stage 4", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 4", player)
                     or state.has("Royal Road Stage 5", player) or state.has("Copy Ability Testing Room", player)
                     )
                )
    else:
        return (state.has("Cutter", player)
                and (state.has("Fine Fields Stage 3", player) or state.has("Fine Fields Stage 4", player)
                     or state.has("VS Flowery Woods", player) or state.has("Fine Fields Stage EX", player)
                     or state.has("Lollipop Land Stage 1", player) or state.has("Lollipop Land Stage 2", player)
                     or state.has("Old Odyssey Stage 1", player) or state.has("Old Odyssey Stage 2", player)
                     or state.has("Old Odyssey Stage 3", player) or state.has("Old Odyssey Stage 4", player)
                     or state.has("Old Odyssey Stage EX", player) or state.has("Wild World Stage 1", player)
                     or state.has("Wild World Stage 4", player) or state.has("Wild World Stage 5", player)
                     or state.has("Endless Explosions Stage 2", player)
                     or state.has("Endless Explosions Stage 4", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 4", player)
                     or state.has("Royal Road Stage 5", player) or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )


def can_use_fighter(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0:
        return (state.has("Fighter", player)
                and (state.has("Grand Sun Stone", player, 2)
                     or (state.has("Grand Sun Stone", player, 1)
                         and (state.has("Progressive EX Stage Key", player, 2)
                              or state.has("Level 2 EX Stage Key", player)
                              )
                         )
                     or state.has("VS Pyribbit", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    elif world.options.stage_shuffle == 1:
        return (state.has("Fighter", player)
                and (state.has("Grand Sun Stone", player, 1)
                     and (state.has("Progressive EX Stage Key", player, 2)
                          or state.has("Level 2 EX Stage Key", player)
                          )
                     or state.has("Old Odyssey Stage 2", player) or state.has("Wild World Stage 4", player)
                     or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("VS Pyribbit", player)
                     or state.has("Royal Road Stage 2", player) or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    elif world.options.stage_shuffle == 2:
        return (state.has("Fighter", player)
                and (state.has("Grand Sun Stone", player, 2)
                     or state.has("Lollipop Land Stage EX", player)
                     or state.has("VS Pyribbit", player)
                     or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    else:
        return (state.has("Fighter", player)
                and (state.has("Lollipop Land Stage EX", player) or state.has("Old Odyssey Stage 2", player)
                     or state.has("Wild World Stage 4", player) or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("VS Pyribbit", player)
                     or state.has("Royal Road Stage 2", player) or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )


def can_use_fire(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return state.has("Fire", player)
    elif world.options.stage_shuffle == 1:
        return (state.has("Fire", player)
                and (state.has("Fine Fields Stage 1", player) or state.has("Fine Fields Stage 2", player)
                     or state.has("Fine Fields Stage 3", player) or state.has("Fine Fields Stage 4", player)
                     or state.has("VS Flowery Woods", player) or state.has("Progressive EX Stage Key", player, 1)
                     or state.has("Level 1 EX Stage Key", player) or state.has("Lollipop Land Stage 1", player)
                     or state.has("Lollipop Land Stage 3", player)
                     or (state.has("Grand Sun Stone", player, 1) and state.has("Level 2 EX Stage Key", player))
                     or state.has("Old Odyssey Stage 3", player) or state.has("Old Odyssey Stage 5", player)
                     or state.has("Wild World Stage 4", player) or state.has("Wild World Stage 5", player)
                     or state.has("VS Coily Rattler", player) or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("VS Pyribbit", player)
                     or state.has("Royal Road Stage 1", player) or state.has("Royal Road Stage 2", player)
                     or state.has("Royal Road Stage 4", player) or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    else:
        return (state.has("Fire", player)
                and (state.has("Fine Fields Stage 1", player) or state.has("Fine Fields Stage 2", player)
                     or state.has("Fine Fields Stage 3", player) or state.has("Fine Fields Stage 4", player)
                     or state.has("VS Flowery Woods", player) or state.has("Fine Fields Stage EX", player)
                     or state.has("Lollipop Land Stage 1", player) or state.has("Lollipop Land Stage 3", player)
                     or state.has("Lollipop Land Stage EX", player) or state.has("Old Odyssey Stage 3", player)
                     or state.has("Old Odyssey Stage 5", player) or state.has("Old Odyssey Stage EX", player)
                     or state.has("Wild World Stage 4", player) or state.has("Wild World Stage 5", player)
                     or state.has("VS Coily Rattler", player) or state.has("Wild World Stage EX", player)
                     or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("VS Pyribbit", player)
                     or state.has("Royal Road Stage 1", player) or state.has("Royal Road Stage 2", player)
                     or state.has("Royal Road Stage 4", player) or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )


def can_use_hammer(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return (state.has("Hammer", player)
                and (state.has("Grand Sun Stone", player, 2)
                     or state.has("Old Odyssey Stage EX", player)
                     or state.has("Wild World Stage EX", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )
    elif world.options.stage_shuffle == 1:
        return (state.has("Hammer", player)
                and (state.has("Old Odyssey Stage 2", player)
                     or (state.has("Grand Sun Stone", player, 2)
                         and (state.has("Progressive EX Stage Key", player, 3)
                              or state.has("Level 3 EX Stage Key", player)
                              )
                         )
                     or (state.has("Grand Sun Stone", player, 3) and state.has("Level 4 EX Stage Key", player))
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 4", player) or state.has("Royal Road Stage 5", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )
    else:
        return (state.has("Hammer", player)
                and (state.has("Old Odyssey Stage 2", player) or state.has("Old Odyssey Stage EX", player)
                     or state.has("Wild World Stage EX", player) or state.has("Endless Explosions Stage 5", player)
                     or state.has("Royal Road Stage 1", player) or state.has("Royal Road Stage 4", player)
                     or state.has("Royal Road Stage 5", player) or state.has("Copy Ability Testing Room", player)
                     )
                )


def can_use_ice(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return state.has("Ice", player)
    elif world.options.stage_shuffle == 1:
        return (state.has("Ice", player)
                and (state.has("Fine Fields Stage 2", player) or state.has("Lollipop Land Stage 3", player)
                     or state.has("Old Odyssey Stage 3", player) or state.has("Old Odyssey Stage 4", player)
                     or state.has("Old Odyssey Stage 5", player)
                     or (state.has("Grand Sun Stone", player, 2)
                         and (state.has("Progressive EX Stage Key", player, 3)
                              or state.has("Level 3 EX Stage Key", player)
                              )
                         )
                     or state.has("Wild World Stage 4", player) or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 4", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("VS Pyribbit", player)
                     or state.has("Royal Road Stage 4", player) or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    else:
        return (state.has("Ice", player)
                and (state.has("Fine Fields Stage 2", player) or state.has("Lollipop Land Stage 3", player)
                     or state.has("Old Odyssey Stage 3", player) or state.has("Old Odyssey Stage 4", player)
                     or state.has("Old Odyssey Stage 5", player) or state.has("Old Odyssey Stage EX", player)
                     or state.has("Wild World Stage 4", player) or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 4", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("VS Pyribbit", player)
                     or state.has("Endless Explosions Stage EX", player) or state.has("Royal Road Stage 4", player)
                     or state.has("Royal Road Stage EX 1", player) or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )


def can_use_leaf(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return (state.has("Leaf", player)
                and (state.has("Grand Sun Stone", player, 2)
                     or state.has("VS Kracko", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    else:
        return (state.has("Leaf", player)
                and (state.has("Old Odyssey Stage 1", player) or state.has("VS Kracko", player)
                     or state.has("Wild World Stage 1", player) or state.has("Wild World Stage 4", player)
                     or state.has("Wild World Stage 5", player) or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 4", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 4", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )


def can_use_mike(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return (state.has("Mike", player)
                and (state.has("Grand Sun Stone", player, 2)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )
    else:
        return (state.has("Mike", player)
                and (state.has("Old Odyssey Stage 2", player) or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 2", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )


def can_use_needle(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return state.has("Needle", player)
    elif world.options.stage_shuffle == 1:
        return (state.has("Needle", player)
                and (state.has("Fine Fields Stage 4", player) or state.has("Progressive EX Stage Key", player, 1)
                     or state.has("Level 1 EX Stage Key", player) or state.has("Old Odyssey Stage 2", player)
                     or state.has("Wild World Stage 4", player)
                     or (state.has("Grand Sun Stone", player, 3) and state.has("Level 4 EX Stage Key", player))
                     or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 4", player)
                     or state.has("Royal Road Stage 5", player) or state.has("Copy Ability Testing Room", player)
                     )
                )
    else:
        return (state.has("Needle", player)
                and (state.has("Fine Fields Stage 4", player) or state.has("Fine Fields Stage EX", player)
                     or state.has("Old Odyssey Stage 2", player) or state.has("Wild World Stage 4", player)
                     or state.has("Wild World Stage EX", player) or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 4", player)
                     or state.has("Royal Road Stage 5", player) or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )


def can_use_ninja(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return (state.has("Ninja", player)
                and (state.has("Grand Sun Stone", player, 1)
                     or state.has("VS Kracko", player)
                     or state.has("Old Odyssey Stage EX", player)
                     or state.has("Endless Explosions Stage EX", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )
    elif world.options.stage_shuffle == 1:
        return (state.has("Ninja", player)
                and (state.has("Lollipop Land Stage 3", player) or state.has("Lollipop Land Stage 4", player)
                     or state.has("VS Kracko", player)
                     or (state.has("Grand Sun Stone", player, 2)
                         and (state.has("Progressive EX Stage Key", player, 3)
                              or state.has("Level 3 EX Stage Key", player)
                              )
                         )
                     or state.has("Wild World Stage 2", player) or state.has("Wild World Stage 3", player)
                     or state.has("Endless Explosions Stage 2", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 4", player) or state.has("Copy Ability Testing Room", player)
                     )
                )
    else:
        return (state.has("Ninja", player)
                and (state.has("Lollipop Land Stage 3", player) or state.has("Lollipop Land Stage 4", player)
                     or state.has("VS Kracko", player) or state.has("Old Odyssey Stage EX", player)
                     or state.has("Wild World Stage 2", player) or state.has("Wild World Stage 3", player)
                     or state.has("Endless Explosions Stage 2", player)
                     or state.has("Endless Explosions Stage EX", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 4", player) or state.has("Copy Ability Testing Room", player)
                     )
                )


def can_use_parasol(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return (state.has("Parasol", player)
                and (state.has("Grand Sun Stone", player, 1)
                     or state.has("Lollipop Land Stage EX", player)
                     or state.has("VS Kracko", player)
                     or state.has("Endless Explosions Stage EX", player)
                     or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )
    elif world.options.stage_shuffle == 1:
        return (state.has("Parasol", player)
                and (state.has("Lollipop Land Stage 1", player) or state.has("Lollipop Land Stage 4", player)
                     or (state.has("Grand Sun Stone", player, 1)
                         and (state.has("Progressive EX Stage Key", player, 2)
                              or state.has("Level 2 EX Stage Key", player)
                              )
                         )
                     or state.has("Old Odyssey Stage 1", player) or state.has("Old Odyssey Stage 4", player)
                     or state.has("VS Kracko", player) or state.has("Wild World Stage 2", player)
                     or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 4", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 2", player)
                     or state.has("Royal Road Stage 4", player) or state.has("Copy Ability Testing Room", player)
                     )
                )
    else:
        return (state.has("Parasol", player)
                and (state.has("Lollipop Land Stage 1", player) or state.has("Lollipop Land Stage 4", player)
                     or state.has("Lollipop Land Stage EX", player) or state.has("Old Odyssey Stage 1", player)
                     or state.has("Old Odyssey Stage 4", player) or state.has("VS Kracko", player)
                     or state.has("Wild World Stage 2", player) or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 4", player)
                     or state.has("Endless Explosions Stage 5", player)
                     or state.has("Endless Explosions Stage EX", player) or state.has("Royal Road Stage 2", player)
                     or state.has("Royal Road Stage 4", player) or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )


def can_use_spark(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return state.has("Spark", player)
    elif world.options.stage_shuffle == 1:
        return (state.has("Spark", player)
                and (state.has("Fine Fields Stage 1", player) or state.has("Fine Fields Stage 4", player)
                     or state.has("Progressive EX Stage Key", player, 1) or state.has("Level 1 EX Stage Key", player)
                     or state.has("Lollipop Land Stage 1", player) or state.has("Lollipop Land Stage 3", player)
                     or state.has("Lollipop Land Stage 4", player) or state.has("Old Odyssey Stage 2", player)
                     or state.has("Old Odyssey Stage 3", player)
                     or (state.has("Grand Sun Stone", player, 2) and state.has("Level 3 EX Stage Key", player))
                     or state.has("Wild World Stage 5", player)
                     or (state.has("Grand Sun Stone", player, 3) and state.has("Level 4 EX Stage Key", player))
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    else:
        return (state.has("Spark", player)
                and (state.has("Fine Fields Stage 1", player) or state.has("Fine Fields Stage 4", player)
                     or state.has("Fine Fields Stage EX", player) or state.has("Lollipop Land Stage 1", player)
                     or state.has("Lollipop Land Stage 3", player) or state.has("Lollipop Land Stage 4", player)
                     or state.has("Old Odyssey Stage 2", player) or state.has("Old Odyssey Stage 3", player)
                     or state.has("Old Odyssey Stage EX", player) or state.has("Wild World Stage 5", player)
                     or state.has("Wild World Stage EX", player) or state.has("Endless Explosions Stage 5", player)
                     or state.has("Royal Road Stage 1", player) or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )


def can_use_spear(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return (state.has("Spear", player)
                and (state.has("Grand Sun Stone", player, 1)
                     or state.has("VS Paintra", player)
                     or state.has("Lollipop Land Stage EX", player)
                     or state.has("VS Coily Rattler", player)
                     or state.has("Endless Explosions Stage EX", player)
                     or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )
    elif world.options.stage_shuffle == 1:
        return (state.has("Spear", player)
                and (state.has("Lollipop Land Stage 2", player) or state.has("Lollipop Land Stage 3", player)
                     or state.has("VS Paintra", player)
                     or (state.has("Grand Sun Stone", player, 1)
                         and (state.has("Progressive EX Stage Key", player, 2)
                              or state.has("Level 2 EX Stage Key", player)
                              )
                         )
                     or state.has("Old Odyssey Stage 2", player) or state.has("Old Odyssey Stage 4", player)
                     or state.has("Old Odyssey Stage 5", player) or state.has("Wild World Stage 1", player)
                     or state.has("Wild World Stage 2", player) or state.has("Wild World Stage 5", player)
                     or state.has("VS Coily Rattler", player) or state.has("Endless Explosions Stage 2", player)
                     or state.has("Endless Explosions Stage 4", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 2", player) or state.has("Royal Road Stage 4", player)
                     or state.has("Royal Road Stage 5", player) or state.has("Copy Ability Testing Room", player)
                     )
                )
    else:
        return (state.has("Spear", player)
                and (state.has("Lollipop Land Stage 2", player) or state.has("Lollipop Land Stage 3", player)
                     or state.has("VS Paintra", player) or state.has("Lollipop Land Stage EX", player)
                     or state.has("Old Odyssey Stage 2", player) or state.has("Old Odyssey Stage 4", player)
                     or state.has("Old Odyssey Stage 5", player) or state.has("Wild World Stage 1", player)
                     or state.has("Wild World Stage 2", player) or state.has("Wild World Stage 5", player)
                     or state.has("VS Coily Rattler", player) or state.has("Endless Explosions Stage 2", player)
                     or state.has("Endless Explosions Stage 4", player)
                     or state.has("Endless Explosions Stage 5", player)
                     or state.has("Endless Explosions Stage EX", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 2", player) or state.has("Royal Road Stage 4", player)
                     or state.has("Royal Road Stage 5", player) or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )


def can_use_stone(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0:
        return (state.has("Stone", player)
                and (state.has("Grand Sun Stone", player, 2)
                     or state.has("Progressive EX Stage Key", player, 1)
                     or state.has("Level 1 EX Stage Key", player)
                     or (state.has("Grand Sun Stone", player, 1)
                         and state.has("Level 2 EX Stage Key", player)
                         )
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    elif world.options.stage_shuffle == 1:
        return (state.has("Stone", player)
                and (state.has("Progressive EX Stage Key", player, 1) or state.has("Level 1 EX Stage Key", player)
                     or (state.has("Grand Sun Stone", player, 1) and state.has("Level 2 EX Stage Key", player))
                     or state.has("Old Odyssey Stage 1", player) or state.has("Old Odyssey Stage 2", player)
                     or state.has("Old Odyssey Stage 3", player) or state.has("Wild World Stage 1", player)
                     or state.has("Wild World Stage 4", player)
                     or state.has("Grand Sun Stone", player, 3) and state.has("Level 4 EX Stage Key", player)
                     or state.has("Endless Explosions Stage 2", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    elif world.options.stage_shuffle == 2:
        return (state.has("Stone", player)
                and (state.has("Grand Sun Stone", player, 2)
                     or state.has("Fine Fields Stage EX", player)
                     or state.has("Lollipop Land Stage EX", player)
                     or state.has("Wild World Stage EX", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    else:
        return (state.has("Stone", player)
                and (state.has("Fine Fields Stage EX", player) or state.has("Lollipop Land Stage EX", player)
                     or state.has("Old Odyssey Stage 1", player) or state.has("Old Odyssey Stage 2", player)
                     or state.has("Old Odyssey Stage 3", player) or state.has("Wild World Stage 1", player)
                     or state.has("Wild World Stage 4", player) or state.has("Wild World Stage EX", player)
                     or state.has("Endless Explosions Stage 2", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )


def can_use_sword(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return state.has("Sword", player)
    elif world.options.stage_shuffle == 1:
        return (state.has("Sword", player)
                and (state.has("Fine Fields Stage 1", player) or state.has("Fine Fields Stage 2", player)
                     or state.has("Fine Fields Stage 3", player) or state.has("Fine Fields Stage 4", player)
                     or state.has("Lollipop Land Stage 3", player) or state.has("Old Odyssey Stage 1", player)
                     or state.has("Old Odyssey Stage 4", player)
                     or (state.has("Grand Sun Stone", player, 2)
                         and (state.has("Progressive EX Stage Key", player, 3)
                              or state.has("Level 3 EX Stage Key", player))
                         )
                     or state.has("Wild World Stage 2", player) or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 5", player) or state.has("Copy Ability Testing Room", player)
                     )
                )
    else:
        return (state.has("Sword", player)
                and (state.has("Fine Fields Stage 1", player) or state.has("Fine Fields Stage 2", player)
                     or state.has("Fine Fields Stage 3", player) or state.has("Fine Fields Stage 4", player)
                     or state.has("Lollipop Land Stage 3", player) or state.has("Old Odyssey Stage 1", player)
                     or state.has("Old Odyssey Stage 4", player) or state.has("Old Odyssey Stage EX", player)
                     or state.has("Wild World Stage 2", player) or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 5", player)
                     or state.has("Endless Explosions Stage EX", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 5", player) or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )


def can_use_wheel(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return (state.has("Wheel", player)
                and (state.has("Grand Sun Stone", player, 1)
                     or state.has("Lollipop Land Stage EX", player)
                     or state.has("Endless Explosions Stage EX", player)
                     or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )
    elif world.options.stage_shuffle == 1:
        return (state.has("Wheel", player)
                and (state.has("Lollipop Land Stage 1", player)
                     or (state.has("Grand Sun Stone", player, 1)
                         and (state.has("Progressive EX Stage Key", player, 2)
                              or state.has("Level 2 EX Stage Key", player)
                              )
                         )
                     or state.has("Wild World Stage 2", player) or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 4", player) or state.has("Copy Ability Testing Room", player)
                     )
                )
    else:
        return (state.has("Wheel", player)
                and (state.has("Lollipop Land Stage 1", player) or state.has("Lollipop Land Stage EX", player)
                     or state.has("Wild World Stage 2", player) or state.has("Endless Explosions Stage 1", player)
                     or state.has("Endless Explosions Stage 5", player)
                     or state.has("Endless Explosions Stage EX", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 4", player) or state.has("Royal Road Stage EX 1", player)
                     or state.has("Copy Ability Testing Room", player)
                     )
                )


def can_use_whip(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        return state.has("Whip", player)
    elif world.options.stage_shuffle == 1:
        return (state.has("Whip", player)
                and (state.has("Fine Fields Stage 2", player) or state.has("Fine Fields Stage 3", player)
                     or state.has("Lollipop Land Stage 1", player) or state.has("Lollipop Land Stage 3", player)
                     or (state.has("Grand Sun Stone", player, 1)
                         and (state.has("Progressive EX Stage Key", player, 2)
                              or state.has("Level 2 EX Stage Key", player)
                              )
                         )
                     or state.has("Old Odyssey Stage 2", player) or state.has("Old Odyssey Stage 3", player)
                     or state.has("Wild World Stage 5", player) or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 2", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    else:
        return (state.has("Whip", player)
                and (state.has("Fine Fields Stage 2", player) or state.has("Fine Fields Stage 3", player)
                     or state.has("Lollipop Land Stage 1", player) or state.has("Lollipop Land Stage 3", player)
                     or state.has("Lollipop Land Stage EX", player) or state.has("Old Odyssey Stage 2", player)
                     or state.has("Old Odyssey Stage 3", player) or state.has("Wild World Stage 5", player)
                     or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 2", player)
                     or state.has("Royal Road Stage EX 1", player) or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )


def can_use_wing(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0:
        return (state.has("Wing", player)
                and (state.has("Grand Sun Stone", player, 2)
                     or state.has("Progressive EX Stage Key", player, 1)
                     or state.has("Level 1 EX Stage Key", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    elif world.options.stage_shuffle == 1:
        return (state.has("Wing", player)
                and (state.has("Progressive EX Stage Key", player, 1) or state.has("Level 1 EX Stage Key", player)
                     or state.has("Old Odyssey Stage 4", player) or state.has("Wild World Stage 1", player)
                     or (state.has("Grand Sun Stone", player, 3) and state.has("Level 4 EX Stage Key", player))
                     or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 2", player) or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    elif world.options.stage_shuffle == 2:
        return (state.has("Wing", player)
                and (state.has("Grand Sun Stone", player, 2)
                     or state.has("Fine Fields Stage EX", player)
                     or state.has("Wild World Stage EX", player)
                     or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )
    else:
        return (state.has("Wing", player)
                and (state.has("Fine Fields Stage EX", player) or state.has("Old Odyssey Stage 4", player)
                     or state.has("Wild World Stage 1", player) or state.has("Wild World Stage EX", player)
                     or state.has("Endless Explosions Stage 3", player)
                     or state.has("Endless Explosions Stage 5", player) or state.has("Royal Road Stage 1", player)
                     or state.has("Royal Road Stage 2", player) or state.has("Copy Ability Testing Room", player)
                     or can_fight_sectonia(world, multiworld, state, player)
                     )
                )


def fine_fields_hal_room(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    if world.options.stage_shuffle == 0 or world.options.stage_shuffle == 2:
        # Hammer is never logically relevant for abilities without stage rando, but this function is used elsewhere too.
        return (can_use_archer(world, multiworld, state, player) or state.has("Beetle", player)
                or can_use_circus(world, multiworld, state, player) or state.has("Cutter", player)
                or can_use_fighter(world, multiworld, state, player) or state.has("Fire", player)
                or can_use_hammer(world, multiworld, state, player) or can_use_leaf(world, multiworld, state, player)
                or can_use_ninja(world, multiworld, state, player) or can_use_spear(world, multiworld, state, player)
                or state.has("Sword", player) or can_use_wing(world, multiworld, state, player)
                )
    else:
        return (state.has("Fine Fields Stage 3", player)
                and (can_use_archer(world, multiworld, state, player)
                     or can_use_beetle(world, multiworld, state, player)
                     or can_use_circus(world, multiworld, state, player)
                     or state.has("Cutter", player)
                     or can_use_fighter(world, multiworld, state, player)
                     or state.has("Fire", player)
                     or can_use_hammer(world, multiworld, state, player)
                     or can_use_leaf(world, multiworld, state, player)
                     or can_use_ninja(world, multiworld, state, player)
                     or can_use_spear(world, multiworld, state, player)
                     or state.has("Sword", player)
                     or can_use_wing(world, multiworld, state, player)
                     )
                )


# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def overfishedAnywhere(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player collected all fish from any fishing log?"""
    for cat, items in world.item_name_groups:
        if cat.endswith("Fishing Log") and state.has_all(items, player):
            return True
    return False

# You can also pass an argument to your function, like {function_name(15)}
# Note that all arguments are strings, so you'll need to convert them to ints if you want to do math.
def anyClassLevel(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    for item in ["Figher Level", "Black Belt Level", "Thief Level", "Red Mage Level", "White Mage Level", "Black Mage Level"]:
        if state.count(item, player) >= int(level):
            return True
    return False

# You can also return a string from your function, and it will be evaluated as a requires string.
def requiresMelee(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player has unlocked the tank."""
    return "|Figher Level:15| or |Black Belt Level:15| or |Thief Level:15|"
