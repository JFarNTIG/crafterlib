"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from crafterlib import Item

def test_item_from_dict():
    item_dict = {
        "id": 1,
        "name": "Iron Ingot",
        "sources": {"Smelting", "Looting"}
    }

    item = Item.from_dict(item_dict)
    assert item.id == 1
    assert item.name == "Iron Ingot"
    assert len(item.sources) == 2
    assert item.sources == {"Smelting", "Looting"}