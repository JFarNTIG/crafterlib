"""This file is part of crafterlib.

SPDX-License-Identifier: MIT
"""
import networkx as nx
from crafterlib import GameCraftingData

def get_amount_needed_for(game_data: GameCraftingData,
                          ingredient: str,
                          product: str,
                          recursive: bool = False) -> float | None:
    """Get the amount of a given item needed to craft one of a certain item.

    If `recursive` is set, then intermediate recipes inbetween `ingredient` and `product`
    will also be considered.

    Example: If "1x Planks -> 4x Sticks" and "2x Sticks, 3x Iron Ingot -> 1x Iron Pickaxe"
    are recipes, then we would need 0.5 Planks to craft one Iron Pickaxe.
    """
    graph = game_data.item_graph.graph

    if recursive:
        try:
            # Dijkstra's algorithm gives us the shortest path between
            # `ingredient` and `product`.
            path = nx.dijkstra_path(graph, ingredient, product, weight="weight")
        except nx.NodeNotFound:
            # can happen if `ingredient` is not in the graph
            return None
        except nx.NetworkXNoPath:
            # there is no way to get from `ingredient` to `product`
            return None
        
        # At this point, `path` is a list of nodes, such as: 
        # ["Iron Ore", "Iron Ingot", "Iron Pickaxe"].

        # To extract the amount data from the edges, we need
        # to turn this into a list of edges.
        # ("Iron Ore", "Iron Ingot")
        # ("Iron Ingot", "Iron Pickaxe")
        # .. and so on.
        edges = nx.utils.pairwise(path)

        total_amount = 1
        for edge in edges:
            total_amount *= graph.get_edge_data(*edge)["weight"]

        # After multiplying together all the amounts along
        # the path, now we have the total amount of `ingredient`
        # needed to craft `product`.
        return total_amount
    else:
        # If `recursive` is not set, then this is very simple.
        # We can just look at the edge between `ingredient` and
        # `product` and get the amount data from it.

        # If there is no such edge then this will just be None.
        weight = graph.get_edge_data(ingredient, product, {}).get("weight")
        return weight