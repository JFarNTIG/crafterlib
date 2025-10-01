"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict, Any

class CraftingGrid:
    """
    A class to use the crafting grid 

    Attributes
    ---
    id : int
        An integer ID for the crafting grid.
    product : str
        The name of the product attached to the crafting grid recipe
    crafting_coordinates : Dict[str, str]
        a representation of a crafting grid using coordinates (A1, A2, A3, B1...) in the form of a dictionary
    """

    def __init__(self, id: int, product: str, crafting_coordinates: Dict[str, str] = {}):
        self.id = id
        self.product = product
        self.crafting_coordinates = crafting_coordinates

    def has_product(self, product: str) -> bool:
        """
        Returns true if the crafting recipe contains the provided product
        """
        return product in self.product
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CraftingGrid":
        """
        Build a CraftingGrid instance from a plain dictionary.

        Parameters
        ---

        data : a representation of a crafting grid using coordinates (A1, A2, A3, B1...) in the form of a dictionary

        Returns
        ---
        A crafting grid instance built upon the dictionary provided

        """
        return cls(
            id=data.get("id", -1),
            product=data.get("product", ""),
            crafting_coordinates=data.get("crafting_coordinates", {})
        )
