from dataclasses import dataclass

@dataclass
class SavedGift:
    id: str
    price: int
    upgrade_price: int | None
    remaining_count: int | None
    total_count: int | None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "price": self.price,
            "upgrade_price": self.upgrade_price,
            "remaining_count": self.remaining_count,
            "total_count": self.total_count,
        }