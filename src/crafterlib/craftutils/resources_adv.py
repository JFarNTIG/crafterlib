"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Iterable
from crafterlib import GameCraftingData

def get_adv_resources(game_data: GameCraftingData) -> Iterable[str]:
    """Get a list of "advanced" resources, which are resources
    which can be crafted, but are not used in any other recipes.

    Example: Iron Pickaxe, since it is not used in any crafting
    recipes. However, Planks would not be an advanced resource,
    since it is used in many crafting recipes.
    """
    graph = game_data.item_graph.graph

    # TODO: Finish this implementation.

    raise NotImplementedError