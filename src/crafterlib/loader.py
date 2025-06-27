"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
import importlib.resources as resources
import json
from pathlib import Path
from types import NoneType
from typing import Dict

from crafterlib.recipe import Recipe
from crafterlib.item import Item
from crafterlib.crafting_data import GameCraftingData

_crafting_data_cache: Dict[str, GameCraftingData] = {}

def load_data_for_game(
    game: str,
    root_dir: str | Path | NoneType = None,
) -> GameCraftingData:
    """Load item and crafting data for the specified game.

    Parameters
    --- 
    game : str
        The id of the game to load data for, example "minecraft".
    root_dir : str | Path | None
        Path to the root directory to search for the game data
        folder. If this is None, then crafterlib will search its
        built-in data for the game.

    Return
    --- 
    A GameCraftingData object containing item and recipe
    data for the game.
    """
    cache_entry = _crafting_data_cache.get(game)
    if cache_entry is not None:
        return cache_entry

    if root_dir is not None:
        subdir = Path(root_dir) / "games/" / game
    else:
        subdir = resources.files("crafterlib.data").joinpath("games/") / game

    if not subdir.is_dir():
        raise NotADirectoryError(f"No data folder for game {game}")
    
    items = []
    recipes = []

    def recipe_handler(recipe_json):
        if not isinstance(recipe_json, list):
            raise ValueError("Top-level JSON value must be an array")

        recipes.extend(Recipe.from_dict(obj) for obj in recipe_json if isinstance(obj, dict))
    
    def item_handler(item_json):
        if not isinstance(item_json, list):
            raise ValueError("Top-level JSON value must be an array")

        items.extend(Item.from_dict(obj) for obj in item_json if isinstance(obj, dict))

    root_json_path = subdir / "root.json"
    if not root_json_path.exists():
        raise Exception(f"No root.json found in data folder for {game}")

    with root_json_path.open("r", encoding="utf-8") as fp:
        root_data = json.load(fp)

    game_name = root_data.get("game", game)
    item_files = root_data.get("item_files", [])
    recipe_files = root_data.get("recipe_files", [])

    for filename in item_files:
        file_path = subdir / filename
        with file_path.open("r", encoding="utf-8") as fp:
            item_data = json.load(fp)

        item_handler(item_data)

    for filename in recipe_files:
        file_path = subdir / filename
        with file_path.open("r", encoding="utf-8") as fp:
            recipe_data = json.load(fp)

        recipe_handler(recipe_data)

    crafting_data = GameCraftingData(game_name, items, recipes)
    _crafting_data_cache[game] = crafting_data
    return crafting_data

