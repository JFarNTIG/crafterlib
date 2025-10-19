"""This example code file shows how crafterlib can calculate
the number of items you can craft given a starting set of ingredients,
including recursive crafting.

In Minecraft, some recipes require multiple intermediate steps. For example:
Logs = Planks, Planks = Sticks, Sticks + Iron Ingot = Iron Pickaxe

crafterlib provides utility functions that can help determine how many final
products can be crafted from a given inventory of base ingredients.

SPDX-License-Identifier: MIT
"""

import crafterlib
import crafterlib.craftutils as craftutils

game_data = crafterlib.load_data_for_game("minecraft")

# Example: start with a given inventory of available items.
inventory = {
    "Logs": 10,
    "Iron Ingot": 7,
}

product_name = "Iron Pickaxe"

# This utility function can calculate the *max amount* of a given
# product you can craft given a dictionary of available items
# If you set `recursive=True`, then this function will consider
# all intermediate recipes.
max_products = craftutils.get_amount_craftable_with(game_data,
                                                    inventory,
                                                    product_name,
                                                    True
                                                    )

print(f"With the current inventory, you can craft {max_products} {product_name}(s).")
