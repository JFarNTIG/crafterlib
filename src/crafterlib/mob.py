from typing import Dict, Set, Any


class Mob:
    def __init__(self,
                 id: int,
                 mob: str,
                 common_drops: Set[str],
                 rare_drops: Set[str],
                 farm_drops: Set[str],
                 equipped_items: Set[str]):
        self.id=id
        self.mob=mob
        self.common_drops=common_drops
        self.rare_drops=rare_drops
        self.farm_drops=farm_drops
        self.equipped_items=equipped_items
    
    def to_dict(self) -> Dict[str, Any]:
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
        return cls(
            id=data.get("id", -1),
            mob=data.get("mob", ""),
            common_drops=set(data.get("common_drops", [])),
            rare_drops=set(data.get("rare_drops", [])),
            farm_drops=set(data.get("farm_drops", [])),
            equipped_items=set(data.get("equipped_items", []))
        )

    def __hash__(self):
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
