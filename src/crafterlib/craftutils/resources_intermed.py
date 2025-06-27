"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict, Iterable
from crafterlib import GameCraftingData

def get_intermed_resources(game_data: GameCraftingData) -> Iterable[str]:
    """Get a list of intermediate resources, which are resources
    which can both be crafted, and which are used in other crafting
    recipes.

    Example: Iron Ingot, since it is crafted from raw ingredients,
    and it is itself used in crafting recipes.
    """
    graph = game_data.item_graph.graph

    # TODO: Finish this implementation.

    raise NotImplementedError

def get_intermed_resources_for(game_data: GameCraftingData,
                               item: str,
                               recursive: bool = False) -> Dict[str, float]:
    """Get all intermediate resources needed to craft a certain item.
    
    Example: Sticks are an intermediate ingredient for
    crafting a Torch, but Coal is a basic resource, so Coal
    would not be included.
    """
    graph = game_data.item_graph.graph

    # TODO: Finish this implementation.

    raise NotImplementedError