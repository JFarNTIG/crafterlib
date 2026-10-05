"""This file is part of crafterlib.

SPDX-License-Identifier: MIT

"""

import pytest
from crafterlib.item import Item
from crafterlib.recipe import Recipe
from crafterlib import GameCraftingData
from crafterlib import load_data_for_game
from crafterlib.craftutils.crafting_plan import make_crafting_plan


def test_single_raw_item():
    game_data = load_data_for_game("test_game", "test_data")

    # Flour is a basic resource, so no crafting is required.
    plan = make_crafting_plan(game_data, {"Flour": 10})

    assert plan.ingredients == {"Flour": 10}
    assert plan.leftovers == {}

def test_single_crafted_item():
    game_data = load_data_for_game("test_game", "test_data")

    # Dough requires 2x Flour and 2x Water.
    plan = make_crafting_plan(game_data, {"Dough": 5})

    assert plan.ingredients == {
        "Flour": 10,
        "Water": 10,
        "Dough": 5,
    }
    assert plan.leftovers == {}

def test_batch_crafting_with_leftover():
    game_data = load_data_for_game("test_game", "test_data")

    # Cheese requires 3x Milk and 1x Vinegar and produces 2x Cheese.
    # 3 Cheese therefore requires 2 crafts and produces 1 leftover.
    plan = make_crafting_plan(game_data, {"Cheese": 3})

    assert plan.ingredients == {
        "Milk": 6,
        "Vinegar": 2,
        "Cheese": 4,
    }
    assert plan.leftovers == {
        "Cheese": 1,
    }

def test_batch_crafting_no_leftovers():

    game_data = load_data_for_game("test_game", "test_data")

    # Two Cheese exactly matches one recipe batch, so no leftover is produced.
    plan = make_crafting_plan(game_data, {"Cheese": 2})

    assert plan.ingredients == {
        "Milk": 3,
        "Vinegar": 1,
        "Cheese": 2,
    }

    assert plan.leftovers == {}

def test_multiple_leftovers():

    game_data = load_data_for_game("test_game", "test_data")

    # Extra Pepperoni and Cheese are both required, causing leftovers
    # from two different batch recipes.
    plan = make_crafting_plan(
        game_data,
        {"Pepperoni Pizza": 1, "Pepperoni": 1, "Cheese": 1},
    )

    assert plan.ingredients == {
        "Flour": 4,
        "Water": 4,
        "Meat": 1,
        "Salt": 3,
        "Milk": 9,
        "Vinegar": 3,
        "Tomato": 4,
        "Basil": 1,
        "Dough": 2,
        "Pepperoni": 4,
        "Cheese": 6,
        "Pizza Sauce": 1,
        "Pepperoni Pizza": 1,
    }

    assert plan.leftovers == {
        "Pepperoni": 1,
        "Cheese": 1,
    }

def test_recursive_crafting_with_leftover():
    game_data = load_data_for_game("test_game", "test_data")

    # A Pepperoni Pizza requires Dough, Pepperoni, Cheese, and Pizza Sauce.
    # Each of those items has its own recipe, so the full crafting chain must be included in the plan.
    plan = make_crafting_plan(game_data, {"Pepperoni Pizza": 1})

    assert plan.ingredients == {
        "Flour": 4,
        "Water": 4,
        "Meat": 1,
        "Salt": 3,
        "Milk": 6,
        "Vinegar": 2,
        "Tomato": 4,
        "Basil": 1,
        "Dough": 2,
        "Pepperoni": 4,
        "Cheese": 4,
        "Pizza Sauce": 1,
        "Pepperoni Pizza": 1,
    }
    assert plan.leftovers == {
        "Pepperoni": 2,
    }

def test_recursive_crafting_multiple_times_with_leftovers():
    game_data = load_data_for_game("test_game", "test_data")

    # Three pizzas require several crafting steps and produce
    # leftover Pepperoni from batch crafting.
    plan = make_crafting_plan(game_data, {"Pepperoni Pizza": 3})

    assert plan.ingredients == {
        "Flour": 12,
        "Water": 12,
        "Meat": 2,
        "Salt": 6,
        "Milk": 18,
        "Vinegar": 6,
        "Tomato": 12,
        "Basil": 3,
        "Dough": 6,
        "Pepperoni": 8,
        "Cheese": 12,
        "Pizza Sauce": 3,
        "Pepperoni Pizza": 3,
    }

    assert plan.leftovers == {
        "Pepperoni": 2,
    }

def test_recursive_crafting_multiple_times_no_leftovers():

    game_data = load_data_for_game("test_game", "test_data")

    # Two pizzas require several crafting steps, but every batch is exact,
    # so the complete recursive plan should have no leftovers.
    plan = make_crafting_plan(game_data, {"Pepperoni Pizza": 2})

    assert plan.ingredients == {
        "Flour": 8,
        "Water": 8,
        "Meat": 1,
        "Salt": 3,
        "Milk": 12,
        "Vinegar": 4,
        "Tomato": 8,
        "Basil": 2,
        "Dough": 4,
        "Pepperoni": 4,
        "Cheese": 8,
        "Pizza Sauce": 2,
        "Pepperoni Pizza": 2,
    }

    assert plan.leftovers == {}

def test_shared_dependency_between_products():
    game_data = load_data_for_game("test_game", "test_data")

    # The pizza requires 2x Dough, while the requested products also
    # include 1x Dough. The shared requirement should be combined.
    plan = make_crafting_plan(
        game_data,
        {"Dough": 1, "Pepperoni Pizza": 1},
    )

    assert plan.ingredients == {
        "Flour": 6,
        "Water": 6,
        "Meat": 1,
        "Salt": 3,
        "Milk": 6,
        "Vinegar": 2,
        "Tomato": 4,
        "Basil": 1,
        "Dough": 3,
        "Pepperoni": 4,
        "Cheese": 4,
        "Pizza Sauce": 1,
        "Pepperoni Pizza": 1,
    }
    assert plan.leftovers == {
        "Pepperoni": 2,
    }

def test_shared_crafting_dependency_with_leftovers():
    game_data = load_data_for_game("minecraft")

    # Fence needs Planks directly and also indirectly through Sticks.
    plan = make_crafting_plan(game_data, {"Fence": 1})

    assert plan.ingredients == {
        "Logs": 2,
        "Planks": 8,
        "Sticks": 4,
        "Fence": 3,
    }

    assert plan.leftovers == {
        "Planks": 2,
        "Sticks": 2,
        "Fence": 2,
    }

def test_zero_amount():
    game_data = load_data_for_game("test_game", "test_data")

    # Requesting zero items should not create any crafting steps.
    plan = make_crafting_plan(game_data, {"Dough": 0})

    assert plan.ingredients == {}
    assert plan.leftovers == {}

def test_empty_products():
    game_data = load_data_for_game("test_game", "test_data")

    plan = make_crafting_plan(game_data, {})

    assert plan.ingredients == {}
    assert plan.leftovers == {}

def test_negative_amount():
    game_data = load_data_for_game("test_game", "test_data")

    with pytest.raises(ValueError):
        make_crafting_plan(game_data, {"Dough": -1})

def test_unknown_item():
    game_data = load_data_for_game("test_game", "test_data")

    with pytest.raises(ValueError):
        make_crafting_plan(game_data, {"Unknown Item": 1})

def test_dependency_ordering():
    game_data = load_data_for_game("test_game", "test_data")

    plan = make_crafting_plan(game_data, {"Pepperoni Pizza": 1})

    items = list(plan.ingredients)

    # Every prerequisite must appear before the item that requires it.
    assert items.index("Flour") < items.index("Dough")
    assert items.index("Water") < items.index("Dough")

    assert items.index("Meat") < items.index("Pepperoni")
    assert items.index("Salt") < items.index("Pepperoni")

    assert items.index("Milk") < items.index("Cheese")
    assert items.index("Vinegar") < items.index("Cheese")

    assert items.index("Tomato") < items.index("Pizza Sauce")
    assert items.index("Basil") < items.index("Pizza Sauce")

    assert items.index("Dough") < items.index("Pepperoni Pizza")
    assert items.index("Pepperoni") < items.index("Pepperoni Pizza")
    assert items.index("Cheese") < items.index("Pepperoni Pizza")
    assert items.index("Pizza Sauce") < items.index("Pepperoni Pizza")

def test_zero_required_dependency():
    items = [
        Item(1, "Zero Item", set()),
        Item(2, "Water", set()),
        Item(3, "Dough", set()),
    ]

    # Zero Item is a dependency but requires zero items, so it should be skipped.
    recipes = [
        Recipe(
            1,
            "Crafting",
            ingredients={"Zero Item": 0, "Water": 2},
            products={"Dough": 1},
        )
    ]

    game_data = GameCraftingData(
        "Test Game",
        items=items,
        recipes=recipes,
    )

    plan = make_crafting_plan(game_data, {"Dough": 1})

    assert plan.ingredients == {
        "Water": 2,
        "Dough": 1,
    }
    assert plan.leftovers == {}