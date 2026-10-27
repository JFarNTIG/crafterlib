"""Usage: python item_parser.py <recipe file 1> <recipe file 2> ...

Output is a single items.json with all of the items.

If an item does not appear as a product in any recipe then it is
assigned a source "Gathering".

This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
import json
import sys

from typing import Dict, List

if len(sys.argv) < 2:
    print("Requires a path to recipes JSON file")
    exit()

num_files = len(sys.argv) - 1

recipes_paths = [sys.argv[i] for i in range(1, len(sys.argv))]

items = set()
sources: Dict[str, Dict[str]] = {}

for recipes_path in recipes_paths:
    with open(recipes_path) as file:
        recipes_json: List[Dict[str, str | int]] = json.load(file)

    for recipe in recipes_json:
        ingredients: Dict[str, float] = recipe.get("ingredients")
        products: Dict[str, float] = recipe.get("products")

        if not ingredients or not products:
            continue

        for item, _quantity in ingredients.items():
            items.add(item)

        for item, _quantity in products.items():
            items.add(item)

            if sources.get(item) is None:
                sources[item] = {recipe["category"]}
            else:
                sources[item].add(recipe["category"])

    for item, item_sources in sources.items():
        if item_sources is None or len(item_sources) == 0:
            sources[item] = ["Gathering"]

items = list(items)
item_objs = []

for idx, item in enumerate(items):
    item_objs.append(
        {
            "id": idx,
            "name": item,
            "sources": list(sources.get(item, ["Gathering"]))
        }
    )

with open("items.json", "w") as file:
    json.dump(list(item_objs), file, indent=2)