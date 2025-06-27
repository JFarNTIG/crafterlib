"""This example code file shows how crafterlib can be used for more
advanced crafting-related math.

In Minecraft, you need to gather Logs to craft tools such as a pickaxe.
However, Logs aren't used directly in the recipe for crafting a pickaxe; rather,
Logs are needed to make Planks, which are needed to make Sticks,
which are needed to make the pickaxe.

crafterlib provides utility functions that can help answering questions such as:
  * If I start with 1 Logs, how many pickaxes can I craft?

SPDX-License-Identifier: MIT
"""
from fractions import Fraction
import crafterlib
import crafterlib.craftutils as craftutils

game_data = crafterlib.load_data_for_game("minecraft")

ingredient_name = "Logs"
product_name = "Iron Pickaxe"

# This utility function can calculate the amount of an ingredient
# needed to craft *one* of a certain item.
# If you set `recursive=True`, then this function will consider
# all intermediate recipes.
ingredients_per_product = craftutils.get_amount_needed_for(game_data, 
                                                           ingredient_name,
                                                           product_name,
                                                           True)

print(f"{ingredients_per_product:.4f} {ingredient_name} is needed to craft one {product_name}.")

# If one of an ingredient can produce more than one of an output, this
# information is not super valuable, because it is not possible to have fractional
# amounts of items in most games, including Minecraft.

# However, with the help of Python's `fractions` library, we can easily
# turn decimals into fractions. This allows us to reinterpret the decimal
# amount as a ratio of ingredient to product.

amount_as_frac = Fraction(ingredients_per_product)

amount_of_ingredient = amount_as_frac.numerator
amount_of_product = amount_as_frac.denominator

print("That means:")
print(f"{amount_of_ingredient} {ingredient_name} is enough to produce {amount_of_product} {product_name}!")