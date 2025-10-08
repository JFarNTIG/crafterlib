"""This example code file shows how crafterlib can be used to load data
for a game (Minecraft) and do some basic queries related to items
and recipes.

It also shows how to calculate how many times a recipe must be crafted to get N desired item.

SPDX-License-Identifier: MIT
"""
import crafterlib

# crafterlib provides a function `load_data_for_game` to load item
# and crafting data for a certain game.
game_data = crafterlib.load_data_for_game("minecraft")

# Print some basic stats about the game data.
print(f"Loaded data for game: {game_data.name}")
print(f"Number of known items: {game_data.num_items()}")
print(f"Number of known recipes: {game_data.num_recipes()}")

# Query an item by name.
# Items are represented by the crafterlib.Item class.
item_name = "Iron Pickaxe"
item = game_data.get_item_by_name(item_name)

if item:
    # Determine sources of an item, i.e. different methods
    # for acquiring the item.
    sources_fmt = ", ".join(item.sources)
    print(f"You can obtain {item_name} by: {sources_fmt}")

# Query recipes for the item.
# This will return a list of recipes, which are represented
# in crafterlib by the crafterlib.Recipe class.
recipes = game_data.get_recipes_for_item(item_name)

for recipe in recipes:
    # Ingredients are items consumed when crafting the item.
    # crafterlib stores ingredients as a dict of the form:
    # {'item name': amount, 'item 2 name': amount}
    print(f"Ingredients needed to make {item_name}:")
    print(recipe.ingredients)

    # Requirements are items needed to craft the item,
    # but which are not consumed in the crafting process
    # (e.g. the crafting table itself)
    print(f"Requirements to make {item_name}:")
    print(recipe.requirements)

    # Calculate how many times this recipe needs to be crafted
    # To get the desired amount of items

    desired_amount = 10

    num_crafts = recipe.get_num_crafts(
        gameData=game_data,
        itemName=item_name,
        amount=10
    )

    print(f"To make {desired_amount} {item_name} you need to craft it {num_crafts} time(s)")