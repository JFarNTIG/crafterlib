"""This example code file shows how crafterlib can be used to create a crafting plan.

In Minecraft, you sometimes want to gather a certain amount of an item. 
However, sometimes it's a bit complicated to calculate how much of each ingredient you need.
To make an iron pickaxe you need to go though multiple steps in order to craft it.

crafting_plan calculates what ingredients are needed and in which order they should be 
gathered/crafted in order to create a chosen amount of a chosen item, in this example iron pickaxes.

SPDX-License-Identifier: MIT
"""
import crafterlib
from crafterlib.craftutils import make_crafting_plan


game_data = crafterlib.load_data_for_game("minecraft")

try:
    plan = make_crafting_plan(game_data, {"Iron Pickaxe": 23.0})
    print("Crafting Plan for 23 Iron Pickaxes")
    print("\nObtain or craft items in this order:")
    for item, amount in plan.ingredients.items():
        print(f"  {item}: {amount}")

    print("\nLeftover ingredients:")
    for item, amount in plan.leftovers.items():
        print(f"  {item}: {amount}")
except ValueError as e:
    print(f"Error {e}")