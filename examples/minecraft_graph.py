"""This example code file shows how crafterlib can draw a diagram
of items in a game as a way of visualizing a crafting "ecosystem".

SPDX-License-Identifier: MIT
"""
import matplotlib.pyplot as plt
from crafterlib import load_data_for_game

# Use `load_data_for_game` to load data for a certain game.
minecraft_data = load_data_for_game("minecraft")

minecraft_data.item_graph.draw_item_graph()
plt.show()
