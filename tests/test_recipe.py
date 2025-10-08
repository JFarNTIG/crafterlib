"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict
import pytest

from crafterlib import Recipe
from crafterlib import load_data_for_game

test_recipe_dict = {
    "id": 1,
    "category": "Crafting",
    "ingredients": {
        "Iron Ingot": 3,
        "Sticks": 2
    },
    "products": {
        "Iron Pickaxe": 1
    },
    "requirements": {
        "Crafting Table": 1
    }
}

test2_recipe_dict = {
    "id": 14,
    "category": "Crafting",
    "requirements": {},
    "ingredients": {
        "Coal": 1,
        "Sticks": 1
    },
    "products": {
        "Torch": 4
    }
}

def test_recipe_from_dict():
    recipe: Recipe = Recipe.from_dict(test_recipe_dict)

    # check if all the recipe's fields are correct,
    # i.e. if it was correctly parsed from the dict
    assert recipe.id == 1
    assert recipe.category == "Crafting"
    assert recipe.ingredients == {
        "Iron Ingot": 3,
        "Sticks": 2
    }
    assert recipe.products == {
        "Iron Pickaxe": 1
    }
    assert recipe.requirements == {
        "Crafting Table": 1
    }

def test_recipe_ingredients_for_1():
    recipe: Recipe = Recipe.from_dict(test_recipe_dict)

    # default (get_ingredients with no parameters) should be 1
    ingredients: Dict[str, float] = recipe.get_ingredients()

    assert len(ingredients) == 2
    assert ingredients["Iron Ingot"] == pytest.approx(3)
    assert ingredients["Sticks"] == pytest.approx(2)

def test_recipe_ingredients_for_several():
    recipe: Recipe = Recipe.from_dict(test_recipe_dict)

    ingredients: Dict[str, float] = recipe.get_ingredients(4)

    # should be 12 ingots, 8 sticks required for 4 pickaxes
    assert len(ingredients) == 2
    assert ingredients["Iron Ingot"] == pytest.approx(12)
    assert ingredients["Sticks"] == pytest.approx(8)

def test_recipe_ingredients_for_zero():
    recipe: Recipe = Recipe.from_dict(test_recipe_dict)

    # edge case: if we try to craft zero of an item,
    # it should return an empty dict
    ingredients: Dict[str, float] = recipe.get_ingredients(0)

    assert ingredients == {}

def test_recipe_ingredients_for_negative():
    recipe: Recipe = Recipe.from_dict(test_recipe_dict)

    # edge case: if we try to craft negative of an item, it should
    # raise ValueError
    with pytest.raises(ValueError):
        recipe.get_ingredients(-2)


def test_recipe_numcrafts():
    recipe: Recipe = Recipe.from_dict(test2_recipe_dict)
    game_data = load_data_for_game("minecraft")

    # Crafting 16 Torches should require 4 crafts
    assert recipe.get_num_crafts(game_data=game_data, item_name="Torch", amount=16) == 4


def test_recipe_numcrafts_for_zero():
    recipe: Recipe = Recipe.from_dict(test2_recipe_dict)
    game_data = load_data_for_game("minecraft")

    # edge case: trying to craft zero of an item
    # it should return an empty dict
    assert recipe.get_num_crafts(game_data=game_data, item_name="Torch", amount=0) == {}


def test_recipe_numcrafts_for_negative():
    recipe: Recipe = Recipe.from_dict(test2_recipe_dict)
    game_data = load_data_for_game("minecraft")
     
    # edge case: trying to craft negative of an item
    # raise ValueError
    with pytest.raises(ValueError):
        recipe.get_num_crafts(game_data=game_data, item_name="Torch", amount=-2)


def test_recipe_item_name_invalid_format():
    recipe: Recipe = Recipe.from_dict(test2_recipe_dict)
    game_data = load_data_for_game("minecraft")
    
    # edge case: invalid item name type (int instead of str)
    # raises TypeError
    with pytest.raises(TypeError):
        recipe.get_num_crafts(game_data=game_data, item_name=123456, amount=1)


def test_recipe_amount_invalid_format():
    recipe: Recipe = Recipe.from_dict(test2_recipe_dict)
    game_data = load_data_for_game("minecraft")
    
    # edge case: invalid amounttype (str instead of int)
    # raises TypeError
    with pytest.raises(TypeError):
        recipe.get_num_crafts(game_data=game_data, item_name="Torch", amount="NotAnIntegrer")


def test_recipe_amount_non_integer():
    recipe: Recipe = Recipe.from_dict(test2_recipe_dict)
    game_data = load_data_for_game("minecraft")
    
    # edge case: invalid amounttype (float instead of int)
    # raises TypeError
    with pytest.raises(TypeError):
        recipe.get_num_crafts(game_data=game_data, item_name="Torch", amount=1.5)


def test_recipe_not_in_game_data():
    recipe: Recipe = Recipe.from_dict(test2_recipe_dict)
    game_data = load_data_for_game("minecraft")
    
    # edge case: item not found in game data
    # raises ValueError
    with pytest.raises(ValueError):
        recipe.get_num_crafts(game_data=game_data, item_name="FakeItem.exe", amount=1)


def test_recipe_fake_game_data():
    recipe: Recipe = Recipe.from_dict(test2_recipe_dict)
    game_data = "NotRealGameData"

    # edge case: invalid game data type (str instead of class with proper structure)
    # raises TypeError
    with pytest.raises(TypeError):
        recipe.get_num_crafts(game_data=game_data, item_name="Torch", amount=1)


def test_not_product_of():
    recipe: Recipe = Recipe.from_dict(test2_recipe_dict)
    game_data = load_data_for_game("minecraft")

    # edge case: trying to craft an item that is not produced by this recipe
    # raises ValueError
    with pytest.raises(ValueError):
        recipe.get_num_crafts(game_data=game_data, item_name="Iron Pickaxe", amount=1)
