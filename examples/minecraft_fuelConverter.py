"""Example showing fuel conversion using GameCraftingData and fuel conversion functions.

SPDX-License-Identifier: MIT
"""
from crafterlib import load_data_for_game
from crafterlib.craftutils.fuel_conversion import convert_coal_to_fuel, describe_fuel_conversion

# Load Minecraft data, including fuels
crafting_data = load_data_for_game("minecraft")

coal_amount = 0.125
target_fuels = ["Logs", "Planks", "Charcoal", "Lava Bucket"]

for fuel_name in target_fuels:
    try:
        equivalent = convert_coal_to_fuel("minecraft", fuel_name, coal_amount)
        description = describe_fuel_conversion("minecraft", fuel_name, coal_amount)
        print(description)
    except ValueError as e:
        print(e)
