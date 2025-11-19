"""This example code file shows how crafterlib can draw a diagram
of items in a game as a way of visualizing a crafting "ecosystem".

SPDX-License-Identifier: MIT
"""
from crafterlib import load_data_for_game


#test min and max values
def test_item_from_item_graph_min_max_testgame():
    game_data = load_data_for_game("test_game", "test_data")
    assert game_data.item_graph.min_ingredient_amount() == 0.25
    assert game_data.item_graph.max_ingredient_amount() == 4


#test no recepies 
def test_item_from_item_graph_min_max_no_recipe_testgame():
    game_data = load_data_for_game("test_no_recipe", "test_data")
    assert game_data.item_graph.min_ingredient_amount() == 0
    assert game_data.item_graph.max_ingredient_amount() == 0


#test with singel ingredients recepies
def test_item_from_item_graph_min_max_single_ingredient_testgame():
    game_data = load_data_for_game("test_single_ingredient", "test_data")
    assert game_data.item_graph.min_ingredient_amount() == 2
    assert game_data.item_graph.max_ingredient_amount() == 2


#test with multiple ingredient recepies
def test_item_from_item_graph_min_max_mutiple_ingredient_testgame():
    game_data = load_data_for_game("test_mutiple_ingredients", "test_data")
    assert game_data.item_graph.min_ingredient_amount() == 0.5
    assert game_data.item_graph.max_ingredient_amount() == 15
