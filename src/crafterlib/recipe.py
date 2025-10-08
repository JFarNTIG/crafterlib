"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict, Any
import math

class Recipe:
    """
    A class representing some kind of crafting, cooking or smelting recipe.

    Attributes
    --
    id : int
        An integer ID for the recipe.
    category : str
        A category for the recipe (e.g. "Crafting", "Smelting").
    requirements : dict[str, int]
        Prerequisites that must be met in order for the player to be able
        to use this crafting recipe (e.g. "Furnace", "Crafting Table").
        Not consumed when the player crafts.
        Keys are item names; values are quantities.
    ingredients : dict[str, int]
        Resources that are consumed when the player crafts this recipe.
    products : dict[str, int]
        Output items produced by the recipe.
    """

    def __init__(
        self,
        id: int,
        category: str,
        requirements: Dict[str, float] = {},
        ingredients: Dict[str, float] = {},
        products: Dict[str, float] = {},
    ) -> None:
        self.id: int = id
        self.category: str = category
        self.requirements: Dict[str, float] = requirements
        self.ingredients: Dict[str, float] = ingredients
        self.products: Dict[str, float] = products
    
    def has_ingredient(self, ingredient: str) -> bool:
        return ingredient in self.ingredients
    
    def has_product(self, product: str) -> bool:
        return product in self.products
    
    def get_ingredients(self, num_crafts: float = 1) -> Dict[str, float]:
        """Calculate the ingredients required to craft
        this recipe `num_crafts` times.

        Args
        -- 
            num_crafts: The number of times the recipe will be crafted.
            If zero, an empty dict is always returned.
        
        Returns
        -- 
            Ingredient dict, example: `{"Item 1": 2, "Item 2": 4}`

        Raises
        --
            ValueError if num_crafts was negative
        """
        if num_crafts < 0:
            raise ValueError(f"Invalid number of crafts: {num_crafts}")
        elif num_crafts == 0:
            # edge case: just return the empty dict in this case
            return {}
        
        ingredients_for_n = {}
        for ingredient, amount in self.ingredients.items():
            ingredients_for_n[ingredient] = amount * num_crafts

        return ingredients_for_n

    def get_num_crafts(self, game_data, item_name: str, amount: float):
        """Calculate the amount of times you need to craft to get N of a certain item.
        Args
        --
            item_name: The name of the item you want to craft.
            amount: The total number of said item you want crafted.

        Returns
        --
            The amount of crafts needed to get N amount of item, example: `4`

        Raises
        --
            TypeError if item_name is not a string, amount is not a integer or game_data is invalid.
            ValueError if amount <= 0, item_name is not produced by this recipe or no recipe exists in game_data  

        Usage
        --
            num_crafts = recipe.get_num_crafts(game_data = game_data, item_name = "Torch", amount = 16)
            should return `4`
        """
        # Type Checks
        if not hasattr(game_data, "get_recipes_for_item"):
            raise TypeError(f"game_data must be a valid game data object with the get_recipes_for_item function")
        if not isinstance(item_name, str):
            raise TypeError(f"item_name must be a string, got `{type(item_name).__name__}`")
        if not isinstance(amount, int):
            raise TypeError(f"amount must be a integer, got `{type(amount).__name__}`")  

        # Value Check
        if amount < 0:
            raise ValueError(f"Amount must be greater then 0, got `{amount}`")
        if amount == 0:
            return {}
        
        # Check if recipe exists in game data
        recipes = game_data.get_recipes_for_item(item_name)
        if not recipes:
            raise ValueError(f"No recipe found for item `{item_name}`")

        # Check if recipe produces requested item
        if item_name not in self.products:
            raise ValueError(f"Item `{item_name}` is not produced by this recipe")

        product_value = self.products[item_name]

        return math.ceil(amount / product_value)
        
    def to_dict(self) -> Dict[str, Any]:
        """Return a representation of the recipe as a dictionary."""
        return {
            "id": self.id,
            "category": self.category,
            "requirements": self.requirements,
            "ingredients": self.ingredients,
            "products": self.products,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Recipe":
        """
        Build a Recipe instance from a plain dictionary.
        """
        return cls(
            id=data.get("id", -1),
            category=data.get("category", ""),
            requirements=data.get("requirements", {}),
            ingredients=data.get("ingredients", {}),
            products=data.get("products", {}),
        )

    def __repr__(self) -> str:
        return (
            f"Recipe(id={self.id!r}, "
            f"category={self.category!r}, "
            f"requirements={self.requirements!r}, "
            f"ingredients={self.ingredients!r}, "
            f"products={self.products!r})"
        )

    def __hash__(self) -> str:
        """Return a hash representation of this recipe."""
        return hash(self.id)    