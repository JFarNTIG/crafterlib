"""This file is part of crafterlib.

SPDX-License-Identifier: MIT

"""

import pytest

from crafterlib import load_data_for_game
from crafterlib.craftutils.crafting_plan import make_crafting_plan


def test_single_raw_item():
    game_data = load_data_for_game("test_game", "test_data")

    plan = make_crafting_plan(game_data, {"Flour": 10})

    assert plan.ingredients == {"Flour": 10}
    assert plan.leftovers == {}

def test_single_crafted_item():
    game_data = load_data_for_game("test_game", "test_data")

    plan = make_crafting_plan(game_data, {"Dough": 5})

    assert plan.ingredients == {
        "Flour": 10,
        "Water": 10,
        "Dough": 5,
    }
    assert plan.leftovers == {}

def test_batch_crafting():
    game_data = load_data_for_game("test_game", "test_data")

    plan = make_crafting_plan(game_data, {"Cheese": 3})

    assert plan.ingredients == {
        "Milk": 6,
        "Vinegar": 2,
        "Cheese": 4,
    }
    assert plan.leftovers == {
        "Cheese": 1,
    }