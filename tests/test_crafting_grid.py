"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict
import pytest

from crafterlib.crafting_grid import CraftingGrid

test_crafting_grid_dict = {
    "product": "Furnace",
    "crafting_coordinates": {
        "A1": "Cobblestone",
        "A2": "Cobblestone",
        "A3": "Cobblestone",
        "B1": "Cobblestone",
        "B2": "empty",
        "B3": "Cobblestone",
        "C1": "Cobblestone",
        "C2": "Cobblestone",
        "C3": "Cobblestone"
    }
}

def test_has_product():
    crafting_grid: CraftingGrid = CraftingGrid.from_dict(test_crafting_grid_dict)
    item_name1 = crafting_grid.product
    item_name2 = "Grass"

    assert crafting_grid.has_product(item_name1) == True
    assert crafting_grid.has_product(item_name2) == False


def test_crafting_grid_from_dict():
    crafting_grid: CraftingGrid = CraftingGrid.from_dict(test_crafting_grid_dict)
    assert crafting_grid.product == "Furnace"
    assert crafting_grid.crafting_coordinates == {
        "A1": "Cobblestone",
        "A2": "Cobblestone",
        "A3": "Cobblestone",
        "B1": "Cobblestone",
        "B2": "empty",
        "B3": "Cobblestone",
        "C1": "Cobblestone",
        "C2": "Cobblestone",
        "C3": "Cobblestone"
    }