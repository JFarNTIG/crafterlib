"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
import pytest
from crafterlib import load_data_for_game
from crafterlib.craftutils import get_amount_craftable_with

def test_craftable_non_recursive_basic():
    game_data = load_data_for_game("test_game", "test_data")

    # Dough requires 2x Flour and 2x Water
    # So with 10x Flour and 10x Water, we can make 5 Dough
    ingredients = {"Flour": 10, "Water": 10}
    assert get_amount_craftable_with(game_data, ingredients, "Dough", recursive=False) == pytest.approx(5)

def test_craftable_large_inventory():
    game_data = load_data_for_game("test_game", "test_data")
    
    ingredients = {"Flour": 1_000_000, "Water": 500_000}
    # Dough requires 2x Flour + 2x Water
    # so with 1,000,000x Flour and 500,000x Water, we can make 250,000x Dough
    assert get_amount_craftable_with(game_data, ingredients, "Dough", recursive=False) == 250_000

def test_craftable_non_recursive_missing_ingredient():
    game_data = load_data_for_game("test_game", "test_data")

    # Dough requires 2x Flour and 2x Water
    # So with only 10x Flour, we can't make dough at all
    ingredients = {"Flour": 10}
    assert get_amount_craftable_with(game_data, ingredients, "Dough", recursive=False) == pytest.approx(0)

def test_craftable_zero_ingredients():
    game_data = load_data_for_game("test_game", "test_data")
    
    ingredients = {}  # empty inventory
    assert get_amount_craftable_with(game_data, ingredients, "Dough", recursive=False) == 0

def test_craftable_non_recursive_bottleneck():
    game_data = load_data_for_game("test_game", "test_data")

    # 10 Flour, but only 4 Water, limits us to only 2 Dough
    ingredients = {"Flour": 10, "Water": 4}
    assert get_amount_craftable_with(game_data, ingredients, "Dough", recursive=False) == pytest.approx(2)

def test_craftable_non_recursive_multi_output():
    game_data = load_data_for_game("test_game", "test_data")

    # 1x Vinegar + 3x Milk = 2x Cheese

    ingredients = {"Vinegar": 3, "Milk": 6}
    assert get_amount_craftable_with(game_data, ingredients, "Cheese", recursive=False) == pytest.approx(4)
#
    ingredients = {"Vinegar": 3, "Milk": 10}
    assert get_amount_craftable_with(game_data, ingredients, "Cheese", recursive=False) == pytest.approx(6)
#
    ingredients = {"Vinegar": 3, "Milk": 5}
    assert get_amount_craftable_with(game_data, ingredients, "Cheese", recursive=False) == pytest.approx(2)







