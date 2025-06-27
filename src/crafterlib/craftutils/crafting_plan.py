"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict, NamedTuple
from crafterlib import GameCraftingData

class CraftingPlan(NamedTuple):
    ingredients: Dict[str, float]
    leftovers: Dict[str, float]

def make_crafting_plan(game_data: GameCraftingData,
                       products: Dict[str, float]) -> CraftingPlan:
    """Given a dict of desired products, create a comprehensive crafting plan.

    The crafting plan consists of a dict of minimum necessary ingredients
    and a dict of leftovers.

    Moreover, the dict of ingredients is always sorted so that for any item,
    none of the item's prerequisites appear before it in the list, only after.
    This means that the ingredient dict can be followed step-by-step as a
    to-do list.

    Example: To craft 23x Iron Pickaxe you would need:
        *  9 Coal
        *  3 Logs
        * 12 Planks
        * 69 Raw Iron
        * 69 Iron Ingot
        * 48 Sticks
        * 23 Iron Pickaxe

    Leftovers would be:
        * 0.375000 Coal
        * 0.125000 Logs
        * 0.500000 Planks
        * 2.000000 Sticks
    """
    graph = game_data.item_graph.graph

    # TODO: Finish this implementation.

    raise NotImplementedError