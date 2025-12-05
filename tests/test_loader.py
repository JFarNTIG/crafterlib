"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from crafterlib import load_data_for_game

def test_load_data():
    game_data = load_data_for_game("test_game", "test_data")
    assert game_data.num_items() == 13
    assert game_data.num_recipes() == 5

def test_item_parsing():
    game_data = load_data_for_game("test_game", "test_data")
    item = game_data.get_item_by_name("Milk")

    assert item.id == 7
    assert item.name == "Milk"
    assert item.sources == []

def test_load_data_cached():
    game_data = load_data_for_game("test_game", "test_data")
    
    # Try loading data for the same game a second time.
    game_data_2 = load_data_for_game("test_game", "test_data")

    # If caching is working properly, both loads
    # should actually return the same GameCraftingData object.
    # We can test if two variables refer to the same object
    # with the `is` operator in Python.
    assert game_data is game_data_2

def test_fuels_loaded():
    game_data = load_data_for_game("minecraft")
    
    # Basic check: Coal should exist
    assert "Coal" in game_data.fuels
    assert game_data.get_fuel_burn_time("Coal") == game_data.fuels["Coal"]
    
    # Check other fuels
    for fuel in ["Logs", "Planks", "Charcoal", "Lava Bucket"]:
        burn_time = game_data.get_fuel_burn_time(fuel)
        assert burn_time is not None
        assert burn_time > 0    