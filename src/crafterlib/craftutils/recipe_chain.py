"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
import networkx as nx
from crafterlib import GameCraftingData

def get_recipe_chain(game_data: GameCraftingData,
                     ingredient: str,
                     product: str,
                     combine_ingredients: bool = False) -> list:
    """Get a chain of recipes that connect `ingredient` to `product`.

    Returns a list of dictionaries with ingredients and products
    for every recipe inbetween `ingredient` and `product`.
    The recipes' `id`, `category` and `requirements` will not be
    included.

    Example: `ingredient='Logs', product='Iron Pickaxe'` -> 
    ```
    [
      {
        "ingredients": {
          "Logs": 1
        },
        "products": {
          "Planks": 2
        }
      },
      {
        "ingredients": {
          "Planks": 2
        },
        "products": {
          "Sticks": 4
        }
      },
      {
        "ingredients": {
          "Iron Ingot": 3,
          "Sticks": 2
        },
        "products": {
          "Iron Pickaxe": 1
        }
      }
    ]
    ```
    If `combine_ingredients` is set, the ingredients of
    different recipes will be summed up if they're the same
    and be accounted for in the first step in which they occur.

    Returns None if no connection between `ingredient` and `product` is found.
    """
    # If `ingredient` and `product` are the same,
    # this funciton should return None.
    if ingredient == product:
        return None

    graph = game_data.item_graph.graph

    try:
        # Dijkstra's algorithm gives us the shortest path between
        # `ingredient` and `product`.
        path = nx.dijkstra_path(graph, ingredient, product, weight="weight")
    except nx.NodeNotFound:
        # can happen if `ingredient` is not in the graph
        return None
    except nx.NetworkXNoPath:
        # there is no way to get from `ingredient` to `product`
        return None

    chain = []

    # Loop through every product in the path and collect their recipes
    for i, item in enumerate(path[1:]):
        recipes = game_data.get_recipes_for_item(item)
        for recipe in recipes:
            recipe = recipe.to_dict()

            # Find the recipe with the previous product as an ingredient
            # and remove unwanted data.
            if path[i] in recipe['ingredients'].keys():
                recipe.pop("id")
                recipe.pop("category")
                recipe.pop("requirements")
                chain.append(recipe)
                break
        
        # If combine ingredients is set and there are more than one
        # recipe/step in the chain list.
        if combine_ingredients and i > 0:
            ingredients_to_remove = []

            # Loop through the ingredients in the new step
            for new_ingredient in chain[-1]['ingredients']:

                # Loop through the previous steps i the chain
                for index, step in enumerate(chain[:-1]):

                    # and loop through their ingredients
                    for step_ingredient in step['ingredients']:

                        # If a new ingredient is used in a previous step,
                        # add it to the previous step and save so it can be
                        # removed from the new step later.
                        if new_ingredient == step_ingredient:
                            chain[index]['ingredients'][step_ingredient] += chain[-1]['ingredients'][new_ingredient]
                            ingredients_to_remove.append(step_ingredient)
                            break
                    else:
                        continue
                    break
            
            # Remove ingredients that have been combined from the new step
            for _ingredient in ingredients_to_remove:
                chain[-1]['ingredients'].pop(_ingredient)

    return chain