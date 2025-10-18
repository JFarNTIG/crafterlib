"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
import math
from typing import Dict
from crafterlib import GameCraftingData
import networkx as nx

def get_amount_craftable_with(game_data: GameCraftingData,
                              ingredients: Dict[str, float],
                              product: str,
                              recursive: bool = False) -> float:
    """Determine the maximum amount of a certain product that can be
    crafted with a set of available ingredients.

    If `recursive` is set, then intermediate recipes inbetween `ingredient` and `product`
    will also be considered.

    Example: If "1x Planks -> 4x Sticks" and "2x Sticks, 3x Iron Ingot -> 1x Iron Pickaxe"
    are recipes, and we have 1 Planks and 6 Iron Ingots, then we can craft
    a maximum of 2x Iron Pickaxes.
    """
    graph = game_data.item_graph.graph

    if not recursive:    
        if product not in graph:
            # If product isn't even in graph (it can't be crafted), return 0.
            return 0
        
        # Find items that can be directly crafted into product.
        predecessors = list(graph.predecessors(product))

        # Initialize list to store the number of products that
        # can be crafted from each ingredient.
        # So if you have 10 sticks you could craft 5 pickaxes,
        # since a pickaxe requires 2 sticks.
        # And if you have 6 iron Ingots you could craft 2 pickaxes,
        # since a pickaxe requires 3 ingots.
        possible = []

        # Iterate over each ingredient.
        for needed_ingreds in predecessors:
            # Get the "weight" or number of items needed to craft product.
            weight = graph.get_edge_data(needed_ingreds, product, {}).get("weight")
            # Skip if the edge has no valid weight.
            if weight is None or weight <= 0:
                continue

            # Store how many of the ingredient we have.
            available_ingreds = ingredients.get(needed_ingreds, 0.0)

            # Divide available ingredients by how many we need
            # to craft 1 of product, to get how many of product
            # we can craft with the available ingredients.
            
            # Add this value to possible.
            possible.append(available_ingreds / weight)

        if not possible:
            # If we couldn't find any availble ingredients,
            # return 0.
            return 0.0
        
        # min(possible) minimum amount of products you can craft.
        # Limited by the bottleneck ingredient.

        # So if you have 10 sticks and 6 ingots,
        # You could craft 5 pickaxes with the sticks and
        # 2 pickaxes with the ingots.
        # But in total you can only craft 2 pickaxes.
        # Which is why we get the smallest number in the list and
        # return the amount of complete products we can craft
        total_items = min(possible)

        # Determine output count per craft incase you get more
        # than one item per craft, default is 1
        output_count = 1
        for recipe in game_data.recipes:
            if product in recipe.products:
                output_count = recipe.products[product]
                break
            
        # Convert amount craftable to lowest whole amount of crafts
        # then multiply by the amount of product you get from a craft
        max_crafts = math.floor(total_items / output_count)
        return max_crafts * output_count