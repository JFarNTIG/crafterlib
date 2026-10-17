"""Usage, run in terminal: python recipe_parser.py "<PATH>/mcmeta/data/minecraft/recipe"

This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List

import numpy as np

from crafterlib.recipe import Recipe

new_crafting_methods: List[str] = []
recipes_list: List[Dict] = []

class ParseSettings:
    """Return setting(s) from tools/config.json as an instance.

    ***Current adjustable setting(s):***
        - reskins_included: 1 / 0 (True / False)
    
    Arguments:
        None: call with no input

    Returns:
        settings: As a singleton instance

    Examples:
    Fetch settings with ParseSettings._instance.settings:
        ParseSettings._instance.settings.get("reskins_included"):
            -> Dict[str, int]: Reskins (woodtype or colors/dyes) included or not

    The setting reskins_included can be configured in config.json, by default it is set to 0,
    if given the value 1 it gives the option to include recipes for all woodtypes, 
    which means that instead of just `Planks` or `Door` we can also have `Oak Planks` or `Spruce Door`.

    Note: reskins_included = 1 has not been fully tested nor implemented.
    """
    _instance = None

    def __init__(self):
        self.get_settings_from_config()

    @staticmethod
    def get_instance() -> 'ParseSettings':
        """Return instance of setting(s)"""
        if ParseSettings._instance is None:
            ParseSettings._instance = ParseSettings()

        return ParseSettings._instance

    def get_settings_from_config(self):
        """Load setting(s) from config.json"""

        self.settings = load_data("tools/config.json")

        if self.settings == {}:
            self.settings = {"reskins_included", 0} # Default settings


def load_data(file_path: str) -> Dict[str, str | int]:
    """ Return ``Dict`` from a JSON file with the path *file_path*

    Args:
        file_path: Path to a JSON file

    Returns:
        dict: If the file could be loaded correctly, returns a dictionary containing data from the file.

    If the file could not be loaded correctly, prints out the error that occurred.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            loaded_file = json.load(file)

        return loaded_file

    except (FileNotFoundError, IsADirectoryError, PermissionError, json.JSONDecodeError) as e:
        print(f"An error occurred: {e}")

        return {}


def parse_item_name(external_item_name: str) -> str:
    """Parse the name of the item **external_item_name** and return it

    Args:
        external_item_name: Example `minecraft:acacia_planks`
    
    Returns:
        item_name: Example reskins_included = 0 -> `Planks`, 
            reskins_included = 1 -> `Acacia Planks`

    Examples:
        | **``external_item_name`` -> ``if reskins_included = 0``, ``if reskins_included = 1``**
        | -``minecraft:acacia_planks`` -> ``Planks``, ``Acacia Planks``
        | -``minecraft:tuff_brick_slab`` -> ``Tuff Brick Slab``, ``Tuff Brick Slab``
        | -``minecraft:light_blue_dye`` -> ``Light Blue Dye``, ``Light Blue Dye``
        | -``minecraft:blue_concrete_stairs`` -> ``Concrete Stairs``, ``Blue Concrete Stairs``
        | -``minecraft:bamboo_block`` -> ``Bamboo Block``, ``Bamboo Block`` (original recipe, thus, woodtype stays)
    """
    woodtypes: List[str] = [
        "acacia",
        "bamboo",
        "birch",
        "cherry",
        "crimson",
        "dark_oak",
        "jungle",
        "mangrove",
        "pale_oak",
        "oak",
        "poplar",
        "spruce",
        "warped",
    ]

    colors: List[str] = [
        "black",
        "light_blue",
        "light_gray",
        "blue",
        "brown",
        "cyan",
        "gray",
        "green",
        "lime",
        "magenta",
        "orange",
        "pink",
        "purple",
        "red",
        "white",
        "yellow",
    ]

    base_potions: List[str] = [
        "awkward",
        "mundane",
        "thick",
    ]
    
    if "tool_materials" in external_item_name:
        if "wooden" in external_item_name:
            return "Planks"

        if "diamond" in external_item_name:
            return "Diamond"

        if "stone" in external_item_name:
            return "Cobblestone"

        item_name = (((external_item_name.split(":")[1]).replace("tool_materials", "Ingot")).replace("_", " ")).title()

        return item_name

    if "potion" in external_item_name:
        if "water" in external_item_name:
            item_name = "Water Bottle"

        else:
            potion_effect = ((external_item_name.split(':')[1]).replace("_", " ")).title()
            if "master" in external_item_name:
                item_name = f"Potion of the {potion_effect}"

            else:
                item_name = f"Potion of {potion_effect}"

                for base_potion_name in base_potions:
                    if base_potion_name in external_item_name:
                        item_name = f"{potion_effect} Potion"

            if "strong" in external_item_name:
                item_name = f"{item_name.replace("Strong ", "")} II"

            elif "long" in external_item_name:
                item_name = f"{item_name.replace("Long ", "")} +"

            if "splash" in external_item_name:
                item_name = f"Splash {item_name}"

            elif "lingering" in external_item_name:
                item_name = f"Lingering {item_name}"

        return item_name
    
    # Removal of reskins of items
    if ParseSettings._instance.settings.get("reskins_included") == 0:
        for woodtype in woodtypes:
            if woodtype in external_item_name and "block" not in external_item_name:
                item_name = (((external_item_name.split(":")[1]).replace(f"{woodtype}_", "")).replace("_", " ")).title()

                return item_name

        for color in colors:
            if color in external_item_name and "dye" not in external_item_name and "slime" not in external_item_name:
                item_name = (((external_item_name.split(":")[1]).replace(f"{color}_", "")).replace("_", " ")).title()

                return item_name

    # If external_item_name does not have a reskin
    item_name = ((external_item_name.split(":")[1]).replace("_", " ")).title()

    return item_name


def recipe_exists(external_recipe: Dict) -> bool:
    """Return ``True`` if the recipe already exists in recipes_list, 
    else ``False`` and add it to the list.

    Args:
        external_recipe: Dictionary of a recipe from the ./mcmeta/data/minecraft/recipe directory.

    Returns:
        bool: ``True`` if a match exists, else ``False``.
    """
    external_recipe_ingredients: List[str] = []

    if external_recipe["type"] == "minecraft:brewing":
        return False
    
    if "result" in external_recipe:
        external_recipe_products = parse_item_name(external_recipe["result"]["id"])

    if "ingredients" in external_recipe:
        for ingredient in external_recipe["ingredients"]:
            if isinstance(ingredient, list):
                ingredient = ingredient[0]
            external_recipe_ingredients.append(parse_item_name(ingredient))
    elif "key" in external_recipe:
        for key in external_recipe["key"]:
                    key_item = external_recipe["key"][key]
                    if isinstance(key_item, list):
                        for alternative_recipe_item in key_item:
                            external_recipe_ingredients.append(parse_item_name(alternative_recipe_item))
                    else:  
                        external_recipe_ingredients.append(parse_item_name(external_recipe["key"][key]))
    
    recipe_dict: Dict[str, List[str]]= {}
    recipe_dict[external_recipe_products] = external_recipe_ingredients

    for recipe in recipes_list:
            if recipe == recipe_dict:
                return True

    recipes_list.append(recipe_dict)
    return False


def crafting_method_implemented(external_recipe: Dict) -> bool:
    """Return ``True`` if external_recipe["type"] (crafting method) has been implemented, 
    else return ``False``. 
    If crafting method does not exist in either **implemented** or **not_implemented**, 
    add it to **new_crafting_methods**.

    Args:
        external_recipe: Dictionary of a recipe from the ./mcmeta/data/minecraft/recipe directory.

    Returns:
        bool: Return ``True`` if crafting method has been implemented, else return ``False``.
    """
    implemented: List[str] = [ # Keep track of what is implemented
        'minecraft:crafting_shaped', 
        'minecraft:crafting_shapeless',
        'minecraft:smelting',
        'minecraft:brewing',
    ]

    not_implemented: List[str] = [ # Keep track of what is not implemented
        'minecraft:stonecutting', # Not implemented (easy fix)
        'minecraft:crafting_transmute', # Not implemented (easy fix)
        'minecraft:campfire_cooking', # Useless (refer to smelting)
        'minecraft:smoking', # Useless (refer to smelting)
        'minecraft:crafting_special_bannerduplicate', # Completely useless 
        'minecraft:smithing_trim', # Not implemented
        'minecraft:crafting_special_bookcloning', # Completely useless
        'minecraft:blasting', # Useless (refer to smelting)
        'minecraft:crafting_decorated_pot', # Not implemented
        'minecraft:crafting_special_firework_rocket', # Not implemented
        'minecraft:crafting_special_firework_star', # Not implemented
        'minecraft:crafting_special_firework_star_fade', # Not implemented
        'minecraft:crafting_dye', # Completely useless
        'minecraft:crafting_special_mapextending', # Useless
        'minecraft:smithing_transform', # Not implemented (easy fix)
        'minecraft:crafting_special_repairitem', # Completety useless
        'minecraft:crafting_special_shielddecoration', # Useless
        'minecraft:crafting_imbue', # Not implemented (easy fix)
    ]

    if external_recipe["type"] in implemented:
        if "key" in external_recipe:
            for key in external_recipe["key"]:

                if isinstance(key, list):
                    for alternative_key in key:
                        if "dye" in alternative_key:
                            return new_crafting_methods, False
                if "dye" in external_recipe["key"][key]:
                    return False
                
        elif "ingredients" in external_recipe:
            for ingredient in external_recipe["ingredients"]:
                if isinstance(ingredient, list):
                    for alternative_ingredient in ingredient:
                        if "dye" in alternative_ingredient:
                            return new_crafting_methods, False
                elif "dye" in ingredient:
                    return False
            
        return True

    # If there's a new crafting method that the programmer probably does not know of 
    # (its contents should be added to not_implemented)
    elif external_recipe["type"] not in not_implemented and external_recipe["type"] not in new_crafting_methods:
        print(f"New crafting method `{external_recipe['type']}` discovered which has not been implemented!")
        new_crafting_methods.append(external_recipe["type"])

    return False
    

@dataclass
class NewRecipe(Recipe):
    """Class to structure new recipes with. Attributes set to ``None`` or ``0`` on default.

    **Has the following methods:**
        - ``get_id()``
        - ``get_category()``
        - ``get_requirements()``
        - ``get_ingredients()``
        - ``get_products()``
    """
    id: int = field(default=0)
    category: str = field(default=None)
    requirements: Dict[str, float] = field(default=None)
    ingredients: Dict[str, float] = field(default=None)
    products: Dict[str, float] = field(default=None)

    def get_id(self) -> int:
        """Add ``id`` to new recipe.

        Args:
            None: Call with no input.
        
        Returns:
            int: ``id`` (positive integer)
        """
        NewRecipe.id += 1
        self.id = NewRecipe.id

        return self.id

    def get_category(self, external_recipe: Dict) -> str:
        """Add ``category`` to new recipe.

        Args:
            external_recipe: Dictionary of a recipe from the ./mcmeta/data/minecraft/recipe directory.

        Returns:
            str: ``category``, for example ``"Crafting"`` or ``"Smelting"``.
        
        """

        if "crafting" in external_recipe["type"]:
            new_recipe_category = "Crafting"

        else:
            new_recipe_category = parse_item_name(external_recipe["type"])

        self.category = new_recipe_category

        return self.category

    def get_requirements(self, external_recipe: Dict) -> Dict[str, float]:
        """Add ``requirements`` to new recipe. 
        Recipes fitting in a 2x2 box can be crafted without a ``"Crafting Table"``.

        Args:
            external_recipe: Dictionary of a recipe from the ./mcmeta/data/minecraft/recipe directory.
        
        Returns:
            dict: Empty if a machine is not needed. Otherwise specifies machine.
            
        Example:
            - **Torch**: ``{}`` Empty, pattern is smaller than 2x2 (1x2)
            - **Bread**: ``{"Crafting Table": 1}`` Pattern is bigger than 2x2, (3x1)
            - **Bamboo Block**: ``{"Crafting Table": 1}`` Has more than 2x2 (= 4) items in recipe.
            - **Iron Ore** -> **Iron Ingot**: ``{"Furnace": 1}`` Crafting method is smelting -> "Furnace" needed.
        """
        if "crafting" in external_recipe["type"]:
            if "key" in external_recipe:
                matrix = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
                # Where chr in pattern -> 1, else -> 0
                for i, row in enumerate(external_recipe["pattern"]):
                    for j in range(len(row)):
                        if row[j] != ' ':
                            matrix[i][j] = 1

                sum_row1 = 0
                for j in range(3):
                    sum_row1 += matrix[0][j]
                    sum_row3 = 0
                for j in range(3):
                    sum_row3 += matrix[2][j]
                    sum_col1 = 0
                for i in range(3):
                    sum_col1 += matrix[i][0]
                    sum_col3 = 0
                for i in range(3):
                    sum_col3 += matrix[i][2]

                if (sum_row1 > 0 and sum_row3 > 0) or (sum_col1 > 0 and sum_col3 > 0):
                    new_recipe_requirements = {"Crafting Table": 1}

                else:
                    new_recipe_requirements = {}

            elif isinstance(external_recipe["ingredients"], list):
                if len(external_recipe["ingredients"]) > 4:
                    new_recipe_requirements = {"Crafting Table": 1}

                else:
                    new_recipe_requirements = {}

            else:
                new_recipe_requirements = {"Crafting Table": 1}

        elif external_recipe["type"] == "minecraft:smelting":
            new_recipe_requirements = {"Furnace": 1}

        elif external_recipe["type"] == "minecraft:brewing":
            new_recipe_requirements = {"Brewing Stand": 1}

        self.requirements = new_recipe_requirements

        return self.requirements

    def get_ingredients(self, external_recipe: Dict) -> Dict[str, float]:
        """ Add ``ingredients`` to new recipe.

        Args:
            external_recipe: Dictionary of a recipe from the ./mcmeta/data/minecraft/recipe directory.

        Returns:
            dict: Dictionary of items needed and their amounts.

        Example:
            - ``Fence Gate`` -> {{"Sticks": 4}, {"Planks": 2}} Count how many in **external_recipe["pattern"]**
            - ``Netherite Ingot`` -> {{"Netherite Scrap": 4}, {"Golden Ingot": 4}} Count how many times
            the item appears in **external_recipe["ingredients"]**
        """
        new_recipe_ingredients = {}

        if external_recipe["type"] == "minecraft:brewing":
            #"Awkward Potion": 3¨
            # Base (Water Bottle, Awkward Potion or some other Potion)
            base_potion = external_recipe["input"]["potion_contents"]["potions"]

            new_recipe_ingredients[parse_item_name(base_potion)] = 3

            # Reagent (Fermented Spider Eye, Glistering Melon Slice, Glowstone Dust etc..)
            new_recipe_ingredients[parse_item_name(external_recipe["reagent"]["item"])] = 1

            # Fuel
            if "Blaze Powder" not in new_recipe_ingredients:
                new_recipe_ingredients["Blaze Powder"] = 0.05

            else:
                new_recipe_ingredients["Blaze Powder"] = new_recipe_ingredients["Blaze Powder"] + 0.05

        elif "key" in external_recipe:
            for key in external_recipe["key"]:
                        key_item = external_recipe["key"][key]
                        if isinstance(key_item, list):
                            # TODO Implement alternative recipes (like using either charcoal or coal) using some kind of recursion
                                ingredients_amount = sum(key_in_pattern.count(key[0]) for key_in_pattern in external_recipe["pattern"])
                                # For now, just take the first alternative item in the list   
                                new_recipe_ingredients[parse_item_name(key_item[0])] = ingredients_amount
                        else:
                            ingredients_amount = sum(key_in_pattern.count(key[0]) for key_in_pattern in external_recipe["pattern"])   
                            new_recipe_ingredients[parse_item_name(external_recipe["key"][key])] = ingredients_amount

        elif "ingredients" in external_recipe:
            for ingredient in external_recipe["ingredients"]:
                if isinstance(ingredient, list):
                    # TODO Implement alternative recipes (like using either charcoal or coal)
                    # For now, just take the first alternative item in the list
                    ingredient = ingredient[0]

                if ingredient not in new_recipe_ingredients:
                    ingredients_amount = sum(key_in_pattern.count(ingredient) for key_in_pattern in external_recipe["ingredients"])  
                    new_recipe_ingredients[parse_item_name(ingredient)] = ingredients_amount

        elif "ingredient" in external_recipe:
            if isinstance(external_recipe["ingredient"], list):
                    # TODO Implement alternative recipes (like smelting down tools to get nuggets)
                    # For now, just take the first alternative item in the list
                    ingredient = external_recipe["ingredient"][0]

            else:
                ingredient = external_recipe["ingredient"]

            new_recipe_ingredients[parse_item_name(ingredient)] = 1

        if "cookingtime" in external_recipe:
            coal_amount = external_recipe["cookingtime"]/1600
            new_recipe_ingredients["Coal"] = coal_amount

        self.ingredients = new_recipe_ingredients

        return self.ingredients

    def get_products(self, external_recipe: Dict) -> Dict[str, float]:
        """Add ``products`` to new recipe.

        Args:
            external_recipe: Dictionary of a recipe from the ./mcmeta/data/minecraft/recipe directory.

        Returns:
            dict: Dictionary of the product created from the recipe and its amount.
        """
        if external_recipe["type"] == "minecraft:brewing":
            external_name = external_recipe["output"]["components"]["minecraft:potion_contents"]["potion"]
            external_name = f"potion{external_name}"

            # Potion of * II
            #"potion": "minecraft:strong_healing", glowstone dust, strength
            #new_recipe_products = {parse_item_name(external_name) : 3}
            
            # Potion of * +
            #"potion": "minecraft:long_strength", redstone dust, duration

            if external_recipe["output"]["id"] == "minecraft:splash_potion":
                # Splash Potion of *
                # Splash Mundane Potion" etc
                # Gunpowder
                product_name = parse_item_name(f"splash{external_name}")

            elif external_recipe["output"]["id"] == "minecraft:lingering_potion":
                # Lingering Potion of *
                #"Lingering Mundane Potion" (water + "anything"), 
                # "Lingering Awkward Potion" (water + nether warts), 
                # "Lingering Thick Potion" (water + glowstone)
                # Dragon's Breath
                product_name = parse_item_name(f"lingering{external_name}")

            else:
                product_name = parse_item_name(external_name)

            new_recipe_products = {product_name : 3}
            #There are: Potion of *, Potion of * II, Potion of * +, Splash Potion of * and Lingering Potion of *

        else:
            # If count does not exist, let it be 1
            if "count" in external_recipe["result"]:
                products_amount = external_recipe["result"]["count"]
            else:
                products_amount = 1

            new_recipe_products = {parse_item_name(external_recipe["result"]["id"]) : products_amount}
        
        self.products = new_recipe_products

        return self.products


def add_extra_recipes(new_recipes_potions: List[NewRecipe]) -> List[NewRecipe]:
    """Add missing recipes semi-manually.

    Args:
        new_recipes_potions: list of new potion recipes

    Returns:
        List[NewRecipes]: modified version of new_recipes_potions, added missing recipes.
    """
    missing_recipes: List[NewRecipe] = []

    water_bottle = NewRecipe(
        category="Filling", 
        requirements={"Water Source": 1}, 
        ingredients={"Glass Bottle": 1}, 
        products={"Water Bottle": 1},
        )

    missing_recipes.append(water_bottle)

    splash_water_bottle = NewRecipe(
        category="Brewing", 
        requirements={"Brewing Stand": 1}, 
        ingredients={"Water Bottle": 3, "Gunpowder": 1, "Blaze Powder": 0.05}, 
        products={"Splash Water Bottle": 3},
        )

    missing_recipes.append(splash_water_bottle)

    lingering_water_bottle = NewRecipe(
        category="Brewing", 
        requirements={"Brewing Stand": 1}, 
        ingredients={"Splash Water Bottle": 3, "Dragon's Breath": 1, "Blaze Powder": 0.05}, 
        products={"Lingering Water Bottle": 3},
        )

    missing_recipes.append(lingering_water_bottle)

    for recipe in missing_recipes:
        recipe.get_id()
        new_recipes_potions.append(recipe)

    print(f"Amount of semi-manually added recipes in crafterlib (not existing in external recipes): {len(missing_recipes)}")

    return new_recipes_potions


def restructure_data(external_recipe: Dict) -> NewRecipe:
    """Add ``id``, ``category``, ``requirements``, 
    ``ingredients`` and ``products`` to new recipe.

    Args:
        external_recipe: Dictionary of a recipe from the ./mcmeta/data/minecraft/recipe directory.

    Returns:
        new_recipe: Object containing data parsed from **external_recipe**.

    Example:
    |    external_recipe: {
            "type": "minecraft:crafting_shaped",
            "key": {
                "#": "minecraft:redstone_torch",
                "S": "minecraft:stick",
                "X": "minecraft:iron_ingot"
            },
            "pattern": [
                "XSX",
                "X#X",
                "XSX"
            ],
            "result": {
                "count": 6,
                "id": "minecraft:activator_rail"
            }
        }
        ->
        NewRecipe(
            id = 1,
            category = 'Crafting',
            requirements = {'Crarfting Table': 1},
            ingredients = {
                {'Redstone Torch': 1}, 
                {'Stick': 2}, 
                {'Iron Ingot': 6},
            }
        )
    """
    new_recipe = NewRecipe()
    new_recipe.get_id() 
    new_recipe.get_category(external_recipe) 
    new_recipe.get_requirements(external_recipe) 
    new_recipe.get_ingredients(external_recipe) 
    new_recipe.get_products(external_recipe)

    return new_recipe


def parse_data(external_recipe: Dict) -> NewRecipe:
    """Check if the recipe-type (crafting method) is supported by this script
    and if the recipe already exists in the list of new recipes. 
    If it is supported and it does not exist in the list — parse it.

    Args:
        external_recipe: Dictionary of a recipe from the ./mcmeta/data/minecraft/recipe directory.

    Returns:
        new_recipe: Object containing data parsed from **external_recipe**.
    """
    implemented_result = crafting_method_implemented(external_recipe)

    if implemented_result == True and recipe_exists(external_recipe) == False:
            # Parse full recipe
            new_recipe = restructure_data(external_recipe)

            return new_recipe


def add_to_recipes_file(new_recipes: List[NewRecipe], file_path: str) -> None:
    """Add new recipes to new_recipes.json or new_recipes_potions.json
    Future plans: replace recipes.json's and recipes_potions.json's contents instead of new_recipes.json and new_recipes_potions.json

    Args:
        new_recipes: List of new recipes which have been parsed.

    Returns:
        None:
    """
    new_recipes_list = [asdict(new_recipe) for new_recipe in new_recipes]

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(new_recipes_list, file, indent=2)


def main() -> None:
    """Loop through external folder (mcmeta) containing recipes, parse it, 
    add it to crafterlib's recipe file and give a summary of this run.

    **Command line args:**
        external_recipes_path: Path to mcmeta's data (<PATH> + /mcmeta/data/minecraft/recipe), 
        given as a command line argument.
    """
    # Fetch external recipes from path given by user
    external_recipes_path = Path(sys.argv[1])
    
    # Fetch settings and create an instance for easy access
    ParseSettings.get_instance()

    count = 0
    new_recipes: List[NewRecipe] = []
    new_recipes_potions: List[NewRecipe] = []

    for external_recipe_file in external_recipes_path.rglob("*.json"):
        count += 1

        external_recipe: Dict = load_data(external_recipe_file)
        if external_recipe == {}:
            continue

        new_recipe = parse_data(external_recipe)

        # Check if the parsed recipe was returned (qualified) and if it was, add it to new_recipes.
        if new_recipe != None:
            if new_recipe.category == "Brewing":
                new_recipes_potions.append(new_recipe)

            else:
                new_recipes.append(new_recipe)

    # Add 3 potion recipes that don't exist in mcmeta that we should have in crafterlib
    new_recipes_potions = add_extra_recipes(new_recipes_potions)

    new_recipes_file = "src/crafterlib/data/games/minecraft/new_recipes.json"
    new_recipes_potions_file = "src/crafterlib/data/games/minecraft/new_recipes_potions.json"

    add_to_recipes_file(new_recipes, new_recipes_file)
    add_to_recipes_file(new_recipes_potions, new_recipes_potions_file)

    # Summary of new crafting methods found in this run
    if len(new_crafting_methods) != 0:
        print(f"Discovered new crafting methods: {new_crafting_methods}")

    print(f"Amount of recipes in external recipes: {count}")
    print(f"Amount of recipes in crafterlib: {NewRecipe.id}")

if __name__ == "__main__":
    main()