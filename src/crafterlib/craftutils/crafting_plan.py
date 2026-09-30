"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""

import math
from typing import Dict, NamedTuple

import networkx as nx

from crafterlib import GameCraftingData


class CraftingPlan(NamedTuple):
    ingredients: Dict[str, float]
    leftovers: Dict[str, float]


def make_crafting_plan(game_data: GameCraftingData,
                       products: Dict[str, float]) -> CraftingPlan:
    """Create a crafting plan for the requested products.

    The crafting plan consists of a dict of minimum necessary ingredients
    and a dict of leftovers. The ingredients are ordered so that
    prerequisites appear before the items that depend on them.

    Args:
        game_data: The crafting data containing items and recipes.
        products: A dict mapping desired product names to required amounts.

    Returns:
        A CraftingPlan containing the required ingredients and leftovers.

    Raises:
        ValueError: If a requested item is unknown or an amount is negative.

    Example:
        To craft 23 Iron Pickaxes:

        >>> plan = make_crafting_plan(game_data, {"Iron Pickaxe": 23})
        >>> plan.ingredients["Iron Pickaxe"]
        23
    """
    graph = game_data.item_graph.graph
    required: Dict[str, float] = {}
    nodes = set()

    for item, amount in products.items():
        if item not in graph:
            raise ValueError(f"Unknown item: {item}")

        if amount < 0:
            raise ValueError(f"Amount cannot be negative: {amount}")

        if amount == 0:
            continue

        required[item] = required.get(item, 0) + amount
        nodes.add(item)
        nodes.update(nx.ancestors(graph, item))

    if not nodes:
        return CraftingPlan({}, {})

    # Order the graph topologically so prerequisites appear before
    # the items that depend on them.
    subgraph = graph.subgraph(nodes)
    ordered_items = list(nx.topological_sort(subgraph))

    ingredients: Dict[str, float] = {}
    leftovers: Dict[str, float] = {}

    # Process products before their prerequisites so each prerequisite 
    # is calculated from the actual amount that will be produced.
    for item in reversed(ordered_items):
        required_amount = required.get(item, 0)

        if required_amount == 0:
            continue

        recipes = game_data.get_recipes_for_item(item)

        if recipes:
            recipe = recipes[0]
            product_amount = recipe.products[item]
            num_crafts = math.ceil(required_amount / product_amount)
            actual_amount = num_crafts * product_amount

            for ingredient, amount_per_craft in recipe.ingredients.items():
                required[ingredient] = (
                    required.get(ingredient, 0)
                    + num_crafts * amount_per_craft
                )
        else:
            actual_amount = math.ceil(required_amount)

        ingredients[item] = actual_amount

        leftover = actual_amount - required_amount

        if leftover > 0:
            leftovers[item] = leftover

    ordered_ingredients = {
        item: ingredients[item]
        for item in ordered_items
        if item in ingredients
    }

    ordered_leftovers = {
        item: leftovers[item]
        for item in ordered_items
        if item in leftovers
    }

    return CraftingPlan(ordered_ingredients, ordered_leftovers)