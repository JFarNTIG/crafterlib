"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict
from crafterlib import GameCraftingData

def get_amount_craftable_with(game_data: GameCraftingData,
                              ingredients: Dict[str, float],
                              product: str,
                              recursive: True = False) -> float:
    """Determine the maximum amount of a certain product that can be
    crafted with a set of available ingredients.

    If `recursive` is set, then intermediate recipes inbetween `ingredient` and `product`
    will also be considered.

    Example: If "1x Planks -> 4x Sticks" and "2x Sticks, 3x Iron Ingot -> 1x Iron Pickaxe"
    are recipes, and we have 1 Planks and 6 Iron Ingots, then we can craft
    a maximum of 2x Iron Pickaxes.
    """
    graph = game_data.item_graph.graph

    # TODO: Finish this implementation.

    raise NotImplementedError