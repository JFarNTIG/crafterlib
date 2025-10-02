"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
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
    and be accounted for in the first step which they occur.

    Returns None if no connection between `ingredient` and `product` is found.
    """
    # TODO: Finish this implementation.

    raise NotImplementedError