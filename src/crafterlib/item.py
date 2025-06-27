"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict, Set, Any

class Item:
    def __init__(self,
                 id: int,
                 name: str,
                 sources: Set[str]):
        self.id = id
        self.name = name
        self.sources = sources

    def to_dict(self) -> Dict[str, Any]:
        """Return a representation of the item as a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "sources": self.sources
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Item":
        """
        Build an Item instance from a plain dictionary.
        """
        return cls(
            id=data.get("id", -1),
            name=data.get("name", ""),
            sources=data.get("sources", set())
        )

    def __hash__(self):
        return hash(self.id)
    
    def __repr__(self) -> str:
        return (
            f"Item(id={self.id!r}, "
            f"name={self.name!r}, "
            f"sources={self.sources!r})"
        )
