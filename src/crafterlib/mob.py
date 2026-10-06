from typing import Dict, Set, Any


class Mob:
    def __init__(self,
                 id: int,
                 mob: str,
                 common_drops: Set[str],
                 rare_drops: Set[str],
                 farm_drops: Set[str],
                 equipped_items: Set[str]):
        # identifier for the mob class
        self.id=id

        # name of the mob
        self.mob=mob

        # items the mob commonly drops
        self.common_drops=common_drops

        # items the mob rarely drops
        self.rare_drops=rare_drops

        # items dropped when the mob is farmed
        self.farm_drops=farm_drops

        # items the mob has equipped
        self.equipped_items=equipped_items
    
    def to_dict(self) -> Dict[str, Any]:
        # convert the mob data into a dictionary for JSON serialization.
        return {
            "id": self.id,
            "mob": self.mob,
            "common_drops": list(self.common_drops),
            "rare_drops": list(self.rare_drops),
            "farm_drops": list(self.farm_drops),
            "equipped_items": list(self.equipped_items)
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Mob":
        # create a Mob instance from a dictionary
        return cls(
            id=data.get("id", -1), # fallback ID if missing
            mob=data.get("mob", ""), # empty string if name missing
            common_drops=set(data.get("common_drops", [])),
            rare_drops=set(data.get("rare_drops", [])),
            farm_drops=set(data.get("farm_drops", [])),
            equipped_items=set(data.get("equipped_items", []))
        )

    def __hash__(self):
        # enables using Mob objects in sets or as dictionary keys.
        # hash is based solely on the mob's ID.
        return hash(self.id)
    
    def __repr__(self) -> str:
        return (
            f"Mob(id={self.id!r}, "
            f"mob={self.mob!r}, "
            f"common_drops={self.common_drops!r}, "
            f"rare_drops={self.rare_drops!r})"
            f"farm_drops={self.farm_drops!r})"
            f"equipped_items={self.equipped_items!r})"
        )
