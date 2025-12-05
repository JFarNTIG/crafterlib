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
        subdir = resources.files("crafterlib").joinpath("data", "games", game)

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

    """Try to load fuels for this game"""
    try:
        fuel_data = load_fuel_data(game, root_dir)
        valid_fuels = {}
        for name, burn_time in fuel_data.items():
            item = crafting_data.get_item_by_name(name)
            if item:
                valid_fuels[item.name] = burn_time
            else:
                valid_fuels[name] = burn_time
        crafting_data.fuels = valid_fuels
    except FileNotFoundError:
        crafting_data.fuels = {}

    _crafting_data_cache[game] = crafting_data
    return crafting_data


def load_fuel_data(game: str, root_dir: str | Path | NoneType = None) -> dict[str, float]:
    """Load fuel burn values for the given game.

    Parameters
    ---
    game : str
        The game to load fuel data for, e.g. "minecraft".
    root_dir : str | Path | None
        Optional root directory override. If None, loads from crafterlib's built-in data.

    Returns
    ---
    dict[str, float]
        Dictionary mapping fuel names to how many items they can smelt.
    """
    if root_dir is not None:
        subdir = Path(root_dir) / "games" / game
    else:
        subdir = resources.files("crafterlib").joinpath("data", "games", game)

    fuel_path = subdir / "fuels.json"
    if not fuel_path.exists():
        raise FileNotFoundError(f"No fuels.json found for game {game}")

    with fuel_path.open("r", encoding="utf-8") as fp:
        return json.load(fp)
