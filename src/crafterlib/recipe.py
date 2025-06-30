"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict, Any

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