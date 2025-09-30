"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict, List, Optional
from crafterlib.item import Item
from crafterlib.recipe import Recipe
from crafterlib.crafting_grid import CraftingGrid
from crafterlib.graph import ItemGraph

def _make_item_id_map(items: List[Item]):
    item_id_map: Dict[str, Item] = {}
    for item in items:
        existing_item = item_id_map.get(item.id)
        if existing_item:
            raise ValueError(f"Can't add item {item.name}[id={item.id}], "
                             f"ID conflict with {existing_item.name}[id={existing_item.id}]")
        item_id_map[item.id] = item
    return item_id_map

def _make_item_name_map(items: List[Item]):
    item_name_map: Dict[str, Item] = {}
    for item in items:
        existing_item = item_name_map.get(item.name)
        if existing_item:
            raise ValueError(f"Can't add item {item.name}[id={item.id}], "
                             f"name conflict with {existing_item.name}[id={existing_item.id}]")
        item_name_map[item.name] = item
    return item_name_map

def _make_recipe_id_map(recipes: List[Recipe]):
    recipe_id_map: Dict[str, Recipe] = {}
    for recipe in recipes:
        existing_recipe = recipe_id_map.get(recipe.id)
        if existing_recipe:
            raise ValueError(f"Can't add recipe[id={recipe.id}], "
                             f"ID conflict with recipe[id={existing_recipe.id}]")
        recipe_id_map[recipe.id] = recipe
    return recipe_id_map

class GameCraftingData:
    def __init__(self, name: str, items: List[Item] = [], recipes: List[Recipe] = [], crafting_grids: List[CraftingGrid] = []):
        self.name = name
        self.items = items
        self.recipes = recipes
        self.crafting_grids = crafting_grids
        self.item_id_map = _make_item_id_map(items)
        self.item_name_map = _make_item_name_map(items)
        self.recipe_id_map = _make_recipe_id_map(recipes)
        self.item_graph = ItemGraph()
        self.item_graph.add_items([item.name for item in items])
        self.item_graph.add_recipes(recipes)

    def num_items(self):
        return len(self.items)
    
    def num_recipes(self):
        return len(self.recipes)
    
    def num_crafting_grids(self):
        return len(self.crafting_grids)
    
    def get_item_by_id(self, id: int) -> Optional[Item]:
        return self.item_id_map.get(id)
    
    def get_item_by_name(self, item_name: str) -> Optional[Item]:
        return self.item_name_map.get(item_name)
    
    def get_recipe_by_id(self, id: int) -> Optional[Item]:
        return self.recipe_id_map.get(id)
    
    def get_recipes_for_item(self, item_name: str) -> List[Recipe]:
        """Get all recipes in which the specified
        item appears as a product.
        """
        recipes_for_item = []

        for recipe in self.recipes:
            if recipe.has_product(item_name):
                recipes_for_item.append(recipe)
        return recipes_for_item
    
    def get_crafting_grid_for_item(self, item_name: str) -> List[CraftingGrid]:
       """Get all crafting grid recipes in which the specified
       item appears as a product.
       """
       crafting_grids_for_item = []

       for crafting_grid in self.crafting_grids:
           if crafting_grid.has_product(item_name):
               crafting_grids_for_item.append(crafting_grid )
       return crafting_grids_for_item