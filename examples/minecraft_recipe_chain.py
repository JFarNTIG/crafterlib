"""This example code file shows how crafterlib can be used to get
a sequence of steps needed to craft an item from an indirect ingredient,
another item that is not a direct ingredient to the first item.

If you have a Log for example and want to make a Pickaxe out of it,
then you can use the utility function get_recipe_chain to get a list
of ingredients and products for each crafting step inbetween these two
items.

This function is especially helpfull for getting complete recipes for
potions in minecraft which are made in multiple steps.

SPDX-License-Identifier: MIT
"""
import crafterlib
import crafterlib.craftutils as craftutils

game_data = crafterlib.load_data_for_game("minecraft")

# Get step by step instructions for crafting an Iron Pickaxe from Logs.
ingredient_name = "Logs"
product_name = "Iron Pickaxe"

# Get a list of recipes in short form.
recipe_chain = craftutils.get_recipe_chain(game_data,
                                           ingredient_name,
                                           product_name)

print(f"\nMake {product_name} from {ingredient_name}:")

# Loop through the recipes.
# Each recipe is one step in the crafting process.
for i, step in enumerate(recipe_chain):

    # Every step in this example only has one type of item as product.
    # Get the name of the product (key) and the amount of this product
    # that will be crafted (value).
    product_key, product_value = next(iter(step["products"].items()))
    print(f"Step {i+1}. Craft {product_value} {product_key} from ", end="")

    # Loop through and print the ingredients in a similar way.
    for ingredient in step["ingredients"].items():
        ingredient_key, ingredient_value = ingredient
        print(f"{ingredient_value} {ingredient_key}, ", end="")
    print()


# In this other example we will get instructions for brewing a
# Lingering Potion of Invisibility.
# Brewing is a little different than regular crafting because a potion is
# made in a brewing stand by adding ingredients to Water Bottles in a
# specific order. With the help of the get_recipe_chain function we can get
# all these ingredients in the correct order.
ingredient_name = "Water Bottle"
product_name = "Lingering Potion of Invisibility"

# Get a list of recipes in short form.
# When calling the function we can add the forth parameter `combine_ingredients`.
# Brewing a potion requires a little Blaze Powder as a second ingredient in
# every step, but all this can be added in the first step.´
# With `combine_ingredients` set, the function will calculate how much
# Blaze Powder that's needed for all steps and only return it as one ingredient
# in the first step.
recipe_chain = craftutils.get_recipe_chain(game_data,
                                           ingredient_name,
                                           product_name,
                                           combine_ingredients=True)

print(f"\nMake {product_name} from {ingredient_name}:")

# Loop through the recipes.
# Each recipe is one step in the brewing process.
for i, step in enumerate(recipe_chain):

    print(f"Step {i+1}.", end="")

    # Loop through and print the ingredients and their amount.
    for ingredient in step["ingredients"].items():
        ingredient_key, ingredient_value = ingredient
        print(f" {ingredient_value} {ingredient_key} +", end="")
    print("\b-> ", end="")

    # Print the product.
    product_key, product_value = next(iter(step["products"].items()))
    print(f"{product_value} {product_key}, ")