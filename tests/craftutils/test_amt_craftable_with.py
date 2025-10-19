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
    ingredients = {"Flour": 10, "Peperoni": 2}
    assert get_amount_craftable_with(game_data, ingredients, "Dough", recursive=False) == 0

def test_craftable_zero_ingredients():
    game_data = load_data_for_game("test_game", "test_data")
    
    ingredients = {}  # empty inventory
    assert get_amount_craftable_with(game_data, ingredients, "Dough", recursive=False) == 0

def test_craftable_non_recursive_bottleneck():
    game_data = load_data_for_game("test_game", "test_data")

    # 10x Flour, but only 4x Water, limits us to only 2x Dough
    ingredients = {"Flour": 10, "Water": 4}
    assert get_amount_craftable_with(game_data, ingredients, "Dough", recursive=False) == pytest.approx(2)

def test_craftable_non_recursive_multi_output():
    game_data = load_data_for_game("test_game", "test_data")

    # 1x Vinegar + 3x Milk = 2x Cheese

    # 3x Vinegar and 6x Milk limits us to being able to craft
    # cheese 2 times which returns 4x Cheese
    ingredients = {"Vinegar": 3, "Milk": 6}
    assert get_amount_craftable_with(game_data, ingredients, "Cheese", recursive=False) == pytest.approx(4)

    # 3x Vinegar and 10x Milk lets us craft cheese
    # 3 times which returns 6x Cheese
    ingredients = {"Vinegar": 3, "Milk": 10}
    assert get_amount_craftable_with(game_data, ingredients, "Cheese", recursive=False) == pytest.approx(6)

    # 3x Vinegar and 5x Milk limits us to craft cheese
    # 1x time which returns 2 cheese.
    ingredients = {"Vinegar": 3, "Milk": 5}
    assert get_amount_craftable_with(game_data, ingredients, "Cheese", recursive=False) == pytest.approx(2)

def test_craftable_recursive_pizza():
    game_data = load_data_for_game("test_game", "test_data")

    # Recursive case:
    # To craft Pepperoni Pizza, we need:
    #   - 2x Dough  (from 2x Flour + 2x Water per Dough)
    #   - 4x Cheese (from 3x Milk + 1x Vinegar per 2x Cheese)
    #   - 2x Pepperoni (from 1x Meat + 3x Salt per 4x Pepperoni)
    #   - 1x Pizza Sauce (from 4x Tomato + 1x Basil)
    #
    # We'll give enough base ingredients to make exactly 1 pizza.

    ingredients = {
        "Flour": 8,     # enough for 4 Dough (2 Flour each)
        "Water": 8,     # enough for 4 Dough (2 Water each)
        "Milk": 12,      # enough for 8 Cheese (3 Milk per 2 Cheese)
        "Vinegar": 4,   # enough for 8 Cheese
        "Meat": 2,      # enough for 8 Pepperoni
        "Salt": 6,      # enough for 8 Pepperoni
        "Tomato": 8,    # enough for 2 Pizza Sauce
        "Basil": 2      # enough for 2 Pizza Sauce
    }

    # With recursive crafting, we should be able to make exactly 2 pizzas
    assert get_amount_craftable_with(game_data, ingredients, "Pepperoni Pizza", recursive=True) == pytest.approx(2)

def test_craftable_recursive_pizza_missing_base():
    game_data = load_data_for_game("test_game", "test_data")

    # Missing basil which means we can't craft any pizzas since
    # we don't have Pizza Sauce

    ingredients = {
        "Flour": 4,     # enough for 2 Dough (2 Flour each)
        "Water": 4,     # enough for 2 Dough (2 Water each)
        "Milk": 6,      # enough for 4 Cheese (3 Milk per 2 Cheese)
        "Vinegar": 2,   # enough for 4 Cheese
        "Meat": 1,      # enough for 4 Pepperoni
        "Salt": 3,      # enough for 4 Pepperoni
        "Tomato": 4,    # enough for 1 Pizza Sauce
    }

    assert get_amount_craftable_with(game_data, ingredients, "Pepperoni Pizza", recursive=True) == 0

def test_craftable_recursive_pizza_mixed_ingredients():
    game_data = load_data_for_game("test_game", "test_data")

    # Recursive case:
    # To craft Pepperoni Pizza, we need:
    #   - 2x Dough  (from 2x Flour + 2x Water per Dough)
    #   - 4x Cheese (from 3x Milk + 1x Vinegar per 2x Cheese)
    #   - 2x Pepperoni (from 1x Meat + 3x Salt per 4x Pepperoni)
    #   - 1x Pizza Sauce (from 4x Tomato + 1x Basil)
    #
    # We'll give enough base ingredients to make exactly 1 pizza.

    ingredients = {
        "Flour": 8,     # enough for 4 Dough (2 Flour each)
        "Dough": 3,     # enough for 1 Pizza (2 Dough per 1 Pizza)
        "Milk": 12,     # enough for 8 Cheese (3 Milk per 2 Cheese)
        "Vinegar": 4,   # enough for 8 Cheese
        "Pepperoni": 8, # enough for 4 Pizzas (2 Pepperoni per 1 Pizza)
        "Tomato": 8,    # enough for 2 Pizza Sauce
        "Basil": 2      # enough for 2 Pizza Sauce
    }

    # With recursive crafting, we should be able to make exactly 1 pizza
    assert get_amount_craftable_with(game_data, ingredients, "Pepperoni Pizza", recursive=True) == pytest.approx(1)

def test_recursive_unreachable_product():
    game_data = load_data_for_game("test_game", "test_data")

    ingredients = {"Flour": 10, "Water": 10}
    # There’s no chain that can produce "Basil"
    assert get_amount_craftable_with(game_data, ingredients, "Basil", recursive=True) == 0

def test_craftable_product_not_in_graph():
    game_data = load_data_for_game("test_game", "test_data")
    ingredients = {"Flour": 10}
    # "Bread" does not exist in the crafting graph
    assert get_amount_craftable_with(game_data, ingredients, "Bread", recursive=False) == 0







