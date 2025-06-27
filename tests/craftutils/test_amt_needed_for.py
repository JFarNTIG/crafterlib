"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
import pytest
from crafterlib import load_data_for_game
from crafterlib.craftutils import get_amount_needed_for

def test_ingredients_positive():
    game_data = load_data_for_game("test_game", "test_data")

    # 2 Flour needed to make 1 Dough
    assert get_amount_needed_for(game_data, "Flour", "Dough", False) == pytest.approx(2)

    # 1 Vinegar needed to make 2 Cheese
    assert get_amount_needed_for(game_data, "Vinegar", "Cheese", False) == pytest.approx(0.5)

    # 1 Pizza Sauce needed to make 1 Pepperoni Pizza
    assert get_amount_needed_for(game_data, "Pizza Sauce", "Pepperoni Pizza", False) == pytest.approx(1)

def test_ingredients_not_found():
    game_data = load_data_for_game("test_game", "test_data")

    # Cornstarch is not even an item in the dataset.
    # If we try to get the amount needed to make a Pepperoni Pizza,
    # this should be None.
    assert get_amount_needed_for(game_data, "Cornstarch", "Pepperoni Pizza", False) == None

def test_ingredients_negative():
    game_data = load_data_for_game("test_game", "test_data")

    # Vinegar is not an ingredient to make Dough,
    # so we expect get_amount_needed_for to return None.
    assert get_amount_needed_for(game_data, "Vinegar", "Dough", False) == None

def test_ingredients_recursive_positive():
    game_data = load_data_for_game("test_game", "test_data")

    # 2 Flour needed to make 1 Dough
    # (Flour is used directly in the recipe for Dough,
    # should still be the same if recursive=True)
    assert get_amount_needed_for(game_data, "Flour", "Dough", True) == pytest.approx(2)

    # 1 Meat makes 4 Pepperoni, but we only need 2 Pepperoni
    # to make Pepperoni Pizza.
    # So actually, we need 0.5 Meat to make 1 Pepperoni Pizza.
    assert get_amount_needed_for(game_data, "Meat", "Pepperoni Pizza", True) == pytest.approx(0.5)

def test_ingredients_recursive_long_chain():
    game_data = load_data_for_game("test_game2", "test_data")

    # 9072 Silica Sand should be needed to craft one Computer.
    assert get_amount_needed_for(game_data, "Silica Sand", "Computer", True) == pytest.approx(9072)
