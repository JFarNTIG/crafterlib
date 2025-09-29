"""This example code file shows how crafterlib can be used ...

SPDX-License-Identifier: MIT
"""

import crafterlib

game_data = crafterlib.load_data_for_game("minecraft")

item_name = "Furnace"

crafting_grids = game_data.get_crafting_grid_for_item(item_name)

for crafting_grid in crafting_grids:
    print("The crafting grid for",item_name,"is: \n")
    for coordinate,item in crafting_grid.crafting_coordinates.items():
        print(coordinate,item)

# Very simple visual representation of the crafting grid, this could be implemented in a 
# more user friendly way by having a graphic display of the data.
for crafting_grid in crafting_grids:
    print("\nThe crafting grid for",item_name,"is: \n")
    print("___________________________________________")
    print("|",crafting_grid.crafting_coordinates["A1"], "|",crafting_grid.crafting_coordinates["A2"], "|",crafting_grid.crafting_coordinates["A3"], "|" )
    print("___________________________________________")
    print("|",crafting_grid.crafting_coordinates["B1"], "|",crafting_grid.crafting_coordinates["B2"], "|",crafting_grid.crafting_coordinates["B3"], "|" )
    print("___________________________________________")
    print("|",crafting_grid.crafting_coordinates["C1"], "|",crafting_grid.crafting_coordinates["C2"], "|",crafting_grid.crafting_coordinates["C3"], "|" )
    print("___________________________________________")

