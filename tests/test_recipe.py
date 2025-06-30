"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict
import pytest

from crafterlib import Recipe

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