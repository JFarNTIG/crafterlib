"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from crafterlib import load_data_for_game

# Test min and max values
def test_min_max_test_game():
    game_data = load_data_for_game("test_game", "test_data")
    assert game_data.item_graph.min_ingredient_amount() == 0.25
    assert game_data.item_graph.max_ingredient_amount() == 4

# Test no recipes
def test_min_max_no_recipe():
    game_data = load_data_for_game("test_no_recipe", "test_data")
    assert game_data.item_graph.min_ingredient_amount() == 0
    assert game_data.item_graph.max_ingredient_amount() == 0

# Test single ingredients recipes
def test_min_max_single_ingredient():
    game_data = load_data_for_game("test_single_ingredient", "test_data")
    assert game_data.item_graph.min_ingredient_amount() == 2
    assert game_data.item_graph.max_ingredient_amount() == 2

# Test multiple ingredient recipes
def test_min_max_multiple_ingredient():
    game_data = load_data_for_game("test_multiple_ingredients", "test_data")
    assert game_data.item_graph.min_ingredient_amount() == 0.5
    assert game_data.item_graph.max_ingredient_amount() == 15
