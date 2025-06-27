"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
from typing import Dict, List, Iterable
import math
import networkx as nx
from crafterlib import Recipe

class ItemGraph:
    def __init__(self, graph: nx.DiGraph = None):
        self.graph: nx.DiGraph = graph if graph else nx.DiGraph()

    def add_items(self, items: Iterable[str]):
        self.graph.add_nodes_from(items)

    def add_recipes(self, recipes: Iterable[Recipe]):
        """Add new recipes to the collection.

        This function will only accept recipes for items
        that are not already covered by recipes in the collection.
        For example, say there is a recipe "2x Brick -> Pillar" and
        "3x Stone -> Pillar" then only the first recipe will be added,
        the second will be ignored.
        """
        for recipe in recipes:
            for output, output_count in recipe.products.items():
                if self.get_recipe_for(output):
                    # If the collection already contains a recipe
                    # for this particular output, skip, our collection
                    # already "covers" this item.
                    print(f"warning: skipping {recipe} because there was already a recipe for {output} in the database")
                    continue

                for ingredient, input_count in recipe.ingredients.items():
                    inputs_per_output = input_count / output_count
                    self.graph.add_edge(ingredient,
                                        output,
                                        weight=inputs_per_output)

    def num_items(self) -> int:
        return self.graph.number_of_nodes()
    
    def get_recipe_for(self, item: str) -> Dict[str, float]:
        ingredients: Dict[str, float] = {}
        for (ingredient, _, amount) in self.graph.in_edges(item, "weight"):
            ingredients[ingredient] = amount
        return ingredients
    
    def get_reverse_reachable_subgraph(self, item: str) -> "ItemGraph":
        """Get the subgraph induced by the set of all nodes
        that can reach `item`.
        """
        graph_reversed = nx.reverse(self.graph, copy=False)
        can_reach_item = nx.descendants(graph_reversed, item)
        can_reach_item.add(item)
        return ItemGraph(self.graph.subgraph(can_reach_item).copy())
    
    def draw_item_graph(self):
        nx.draw_networkx(self.graph, nx.spring_layout(self.graph, weight="weight"))
    
    def avg_unique_ingredients_per_item(self) -> float:
        """Get the average number of unique ingredients per item.

        Example: Say a database has two recipes:
        2x Sticks, 3x Iron Ingot -> 1x Iron Pickaxe, and
        0.25x Planks -> 1x Sticks,
        then the average number of unique ingredients is (2 + 1)/2 = 1.5.
        """
        # TODO: Finish this implementation.
        raise NotImplementedError
    
    def avg_ingredient_amount(self) -> float:
        """Get the average ingredient amount.

        Example: Say a database has two recipes:
        2x Sticks, 3x Iron Ingot -> 1x Iron Pickaxe, and
        0.25x Planks -> 1x Sticks,
        then the average ingredient amount would be (2 + 3 + 0.25)/3 = 1.75.
        """
        # TODO: Finish this implementation.
        raise NotImplementedError
    
    def max_ingredient_amount(self) -> float:
        """Get the max ingredient amount.

        Example: Say a database has two recipes:
        2x Sticks, 3x Iron Ingot -> 1x Iron Pickaxe, and
        0.25x Planks -> 1x Sticks,
        then the max ingredient amount would be 3.
        """
        # TODO: Finish this implementation.
        raise NotImplementedError
    
    def min_ingredient_amount(self) -> float:
        """Get the min ingredient amount.

        Example: Say a database has two recipes:
        2x Sticks, 3x Iron Ingot -> 1x Iron Pickaxe, and
        0.25x Planks -> 1x Sticks,
        then the min ingredient amount would be 0.25.
        """
        # TODO: Finish this implementation.
        raise NotImplementedError
