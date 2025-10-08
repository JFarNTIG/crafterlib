"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from crafterlib import load_data_for_game
from crafterlib.craftutils import get_recipe_chain

def test_direct_ingredient():
    game_data = load_data_for_game("test_game2", "test_data")

    output = get_recipe_chain(game_data, "Silica Sand", "Silicon", False)
    assert output == [{
            "ingredients": { "Silica Sand": 36 },
            "products": { "Silicon": 1 }
        }]
    
def test_direct_ingredient_combine_ingredients():
    game_data = load_data_for_game("test_game2", "test_data")

    output = get_recipe_chain(game_data, "Silica Sand", "Silicon", True)
    assert output == [{
            "ingredients": { "Silica Sand": 36 },
            "products": { "Silicon": 1 }
        }]
    
def test_indirect_ingredient():
    game_data = load_data_for_game("test_game2", "test_data")

    output = get_recipe_chain(game_data, "Silica Sand", "Computer", False)
    assert output == [
    {
        "ingredients": { "Silica Sand": 36 },
        "products": { "Silicon": 1 }
    },
    {
        "ingredients": { "Silicon": 2 },
        "products": { "Polysilicon": 1 }
    },
    {
        "ingredients": { "Polysilicon": 3 },
        "products": { "Silicon Wafers": 2 }
    },
    {
        "ingredients": { "Silicon Wafers": 3 },
        "products": { "Integrated Circuit": 1 }
    },
    {
        "ingredients": { "Integrated Circuit": 4 },
        "products": { "Electronics Module": 1 }
    },
    {
        "ingredients": { "Electronics Module": 7 },
        "products": {"Computer": 1 }
    }
]
    
def test_ingredient_not_found():
    game_data = load_data_for_game("test_game2", "test_data")

    # Test with string that doesn't match
    output = get_recipe_chain(game_data, "-", "Silicon", False)
    assert output == None

    # Test with empty string
    output = get_recipe_chain(game_data, "", "Silicon", False)
    assert output == None

def test_product_not_found():
    game_data = load_data_for_game("test_game2", "test_data")

    # Test with string that doesn't match
    output = get_recipe_chain(game_data, "Silicon", "-", False)
    assert output == None

    # Test with empty string
    output = get_recipe_chain(game_data, "Silicon", "", False)
    assert output == None

def test_connection_not_found():
    game_data = load_data_for_game("test_game2", "test_data")

    # Test with inverted parameters
    output = get_recipe_chain(game_data, "Silicon", "Silica Sand", False)
    assert output == None

    # Test with the same item for both parameters
    output = get_recipe_chain(game_data, "Silicon", "Silicon", False)
    assert output == None


def test_recyclables():
    game_data = load_data_for_game("minecraft")

    # Gold Ingot and Gold Nugget can be crafted into each other
    # and are therefore each other's ingredients.
    output = get_recipe_chain(game_data, "Gold Ingot", "Gold Nugget", False)
    assert output == [{
            "ingredients": { "Gold Ingot": 1 },
            "products": { "Gold Nugget": 9 }
        }]
    
    # Test the other way around
    output = get_recipe_chain(game_data, "Gold Nugget", "Gold Ingot", False)
    assert output == [{
            "ingredients": { "Gold Nugget": 9 },
            "products": { "Gold Ingot": 1 }
        }]
    
def test_equal_recyclables():
    game_data = load_data_for_game("minecraft")

    # Test with the same ingredient and product.
    # There is a recipe chain through Gold Nugget
    # but the function should return None
    # since the parameters are the same.
    output = get_recipe_chain(game_data, "Gold Ingot", "Gold Ingot", False)
    assert output == None

def test_combine_ingredients():
    game_data = load_data_for_game("minecraft")

    # Test with a potion that needs Blaze Powder
    # in multiple recipes.
    output = get_recipe_chain(game_data, "Water Bottle", "Splash Potion of Invisibility", True)
    assert output == [
        {
            "ingredients": { "Water Bottle": 3, "Nether Wart": 1, "Blaze Powder": 0.2 },
            "products": { "Awkward Potion": 3 } 
        },
        {
            "ingredients": { "Awkward Potion": 3, "Golden Carrot": 1 },
            "products": { "Potion of Night Vision": 3 }
        },
        {
            "ingredients": { "Potion of Night Vision": 3, "Fermented Spider Eye": 1 },
            "products": { "Potion of Invisibility": 3 }
        },
        {
            "ingredients": { "Potion of Invisibility": 3, "Gunpowder": 1 },
            "products": { "Splash Potion of Invisibility": 3 }
        }
    ]

def test_combine_ingredients_complex():
    game_data = load_data_for_game("test_game3", "test_data")

    # Test with a game that needs the same ingredients in multiple steps
    output = get_recipe_chain(game_data, "Shovel", "Large Sand Castle", True)
    assert output == [
        {
            "ingredients": { "Sand": 3, "Water": 6, "Shovel": 1 },
            "products": { "Sand Pile": 1 }
        },
        {
            "ingredients": { "Sand Pile": 1, "Bucket": 2 },
            "products": { "Sand Castle": 1 }
        },
        {
            "ingredients": { "Sand Castle": 1 },
            "products": { "Large Sand Castle": 1 }
        }
    ]