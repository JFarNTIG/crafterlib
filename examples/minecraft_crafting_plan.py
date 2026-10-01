import crafterlib
from crafterlib.craftutils import make_crafting_plan


game_data = crafterlib.load_data_for_game("minecraft")

try:
    plan = make_crafting_plan(game_data,{"Iron Pickaxe": 23.0})

    print("ingredients:")
    for item, amount in plan.ingredients.items():
        print(f"  {item}: {amount}")

    print("\nleftovers:")
    for item, amount in plan.leftovers.items():
        print(f"  {item}: {amount}")
except ValueError as e:
    print(f"Error {e}")