"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Iterable
from crafterlib import GameCraftingData

def get_possible_products(game_data: GameCraftingData,
                          ingredient: str, 
                          recursive: bool = False) -> Iterable[str]:
    """Get all possible items that can be crafted from
    a given ingredient.

    Example: Starting with Sticks, it is possible to craft an Iron Pickaxe,
    but also a Wood Pickaxe, so both are considered possible products.

    If `recursive` is set, then recipes beyond just what can be directly
    crafted from `ingredient` will also be considered.

    Example: Starting with Planks, it is possible to craft Sticks. However,
    from Sticks, one can craft an Iron Pickaxe. So one can also say that
    Iron Pickaxe is a possible product of Planks.
    """
    graph = game_data.item_graph.graph

    # TODO: Finish this implementation.

    raise NotImplementedError