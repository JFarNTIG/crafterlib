from crafterlib.loader import load_fuel_data

def convert_coal_to_fuel(game: str, fuel_name: str, coal_amount: float) -> float:
    """Convert a coal amount into an equivalent amount of another fuel type.

    Args:
        game: The game to load fuel data for (e.g. "minecraft").
        fuel_name: The name of the target fuel (e.g. "Logs").
        coal_amount: The number of coal units to convert.

    Returns:
        float: How much of the target fuel equals the given coal amount.
    """
    fuels = load_fuel_data(game)

    if "Coal" not in fuels:
        raise ValueError("Fuel data must contain a 'Coal' entry")
    if fuel_name not in fuels:
        raise ValueError(f"Unknown fuel type: {fuel_name}")

    coal_burn = fuels["Coal"]
    fuel_burn = fuels[fuel_name]
    return coal_amount * (coal_burn / fuel_burn)


def describe_fuel_conversion(game: str, fuel_name: str, coal_amount: float) -> str:
    """Return a readable description of a fuel conversion."""
    amount = convert_coal_to_fuel(game, fuel_name, coal_amount)
    return f"{coal_amount} coal ≈ {amount:.3f} {fuel_name.lower()}"

