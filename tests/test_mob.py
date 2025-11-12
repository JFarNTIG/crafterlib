from crafterlib.mob import Mob

def test_mob_from_dict():
    mob_dict = {
        "id": 1,
        "mob": "Zombie",
        "common_drops": ["0-2 Rotten Flesh"],
        "rare_drops": ["1 Iron Ingot 0.83%", "1 Carrot 0.83%"],
        "farm_drops": ["None"],
        "equipped_items": ["Armor and tools 8.5% if killed by a player or a wolf"]
    }

    mob = Mob.from_dict(mob_dict)

    assert mob.id == 1
    assert mob.mob == "Zombie"

    assert isinstance(mob.common_drops, set)
    assert "0-2 Rotten Flesh" in mob.common_drops

    assert mob.rare_drops == {"1 Iron Ingot 0.83%", "1 Carrot 0.83%"}
    assert mob.farm_drops == {"None"}
    assert mob.equipped_items == {"Armor and tools 8.5% if killed by a player or a wolf"}


def test_mob_to_dict():
    mob = Mob(
        id=13,
        mob="Iron Golem",
        common_drops={"3-5 Iron Ingot", "0-2 Poppy"},
        rare_drops={"None"},
        farm_drops={"None"},
        equipped_items={"None"}
    )

    mob_dict = mob.to_dict()

    expected_keys = {"id", "mob", "common_drops", "rare_drops", "farm_drops", "equipped_items"}
    assert set(mob_dict.keys()) == expected_keys

    assert isinstance(mob_dict["common_drops"], list)
    assert "3-5 Iron Ingot" in mob_dict["common_drops"]

    assert mob_dict["mob"] == "Iron Golem"
    assert "None" in mob_dict["rare_drops"]
