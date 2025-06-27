"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Iterable
from crafterlib import GameCraftingData

def get_recyclables(game_data: GameCraftingData) -> Iterable[str]:
    """Get all possible items that can be "recycled"
    aka turned back into the same ingredients that they're
    crafted from.

    Example: Gold Nuggets can be turned into Gold Ingots,
    which can be turned back into Gold Nuggets.
    """
    graph = game_data.item_graph.graph

    # TODO: Finish this implementation.

    raise NotImplementedError