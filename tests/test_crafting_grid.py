"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict
import pytest

from crafterlib.crafting_grid import CraftingGrid

test_crafting_grid_dict1 = {
    "id": 1,
    "products": {
        "Furnace": 1,
    },
    "crafting_coordinates": {
        "A1": "Cobblestone",
        "A2": "Cobblestone",
        "A3": "Cobblestone",
        "B1": "Cobblestone",
        "B2": "",
        "B3": "Cobblestone",
        "C1": "Cobblestone",
        "C2": "Cobblestone",
        "C3": "Cobblestone"
    }
}

test_crafting_grid_dict2 = {
    "id": 1,
    "products": {
        "Honey Block": 1,
        "Empty Bottle": 4
    },
    "crafting_coordinates": {
        "A1": "Honey Bottle",
        "A2": "Honey Bottle",
        "A3": "",
        "B1": "Honey Bottle",
        "B2": "Honey Bottle",
        "B3": "",
        "C1": "",
        "C2": "",
        "C3": ""
    }
}

def test_has_product_single():
    crafting_grid: CraftingGrid = CraftingGrid.from_dict(test_crafting_grid_dict1)

    item_name_true = "Furnace"
    item_name_false = "Grass"
    assert crafting_grid.has_product(item_name_true) == True
    assert crafting_grid.has_product(item_name_false) == False

def test_has_product_multiple():
    crafting_grid: CraftingGrid = CraftingGrid.from_dict(test_crafting_grid_dict2)

    item_name_true1 = "Honey Block"
    item_name_false1 = "Grass"
    assert crafting_grid.has_product(item_name_true1) == True
    assert crafting_grid.has_product(item_name_false1) == False

    item_name_true2 = "Empty Bottle"
    item_name_false2 = "Grass"
    assert crafting_grid.has_product(item_name_true2) == True
    assert crafting_grid.has_product(item_name_false2) == False


def test_crafting_grid_from_dict():
    crafting_grid: CraftingGrid = CraftingGrid.from_dict(test_crafting_grid_dict1)
    assert crafting_grid.id == 1
    assert crafting_grid.products == {
        "Furnace": 1
    }
    assert crafting_grid.crafting_coordinates == {
        "A1": "Cobblestone",
        "A2": "Cobblestone",
        "A3": "Cobblestone",
        "B1": "Cobblestone",
        "B2": "",
        "B3": "Cobblestone",
        "C1": "Cobblestone",
        "C2": "Cobblestone",
        "C3": "Cobblestone"
    }