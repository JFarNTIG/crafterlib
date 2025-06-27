"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict, Iterable
from crafterlib import GameCraftingData

def get_basic_resources(game_data: GameCraftingData) -> Iterable[str]:
    """
    Find all basic resources, e.g. items that cannot be crafted,
    but are used in crafting recipes.

    Example: Dirt is a basic resource, since it is not possible
    to craft. However, Iron Pickaxe is not a basic resource,
    since it requires several intermediate crafting steps.
    """
    graph = game_data.item_graph.graph

    # TODO: Finish this implementation.
    
    raise NotImplementedError

def get_basic_resources_for(game_data: GameCraftingData,
                            item: str,
                            recursive: bool = False) -> Dict[str, float]:
    """Get all basic resources needed to craft a certain item.
    
    Example: Sticks are needed to craft an Iron Pickaxe,
    but they are not a basic resource because they can be crafted
    from Planks. Planks can be crafted from Logs, and Logs cannot
    be crafted, only gathered.
    So Logs are a basic resource needed to craft an Iron Pickaxe.
    """
    graph = game_data.item_graph.graph

    # TODO: Finish this implementation.

    raise NotImplementedError