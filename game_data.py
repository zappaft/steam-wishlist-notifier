from typing import Any


class GameData:

    class DiscountData:

        def __init__(self, data: dict[str, Any]):
            self.discount_pct = data["discount_pct"]
            self.price = data["price"]

        def __repr__(self) -> str:
            return f"GameData.DiscountData({self.discount_pct}, {self.price})"

        def __str__(self) -> str:
            return f"Discount: {self.discount_pct}% | Value: ~{self.price / 100}"

        def __eq__(self, other: 'GameData.DiscountData') -> bool:
            return self.discount_pct == other.discount_pct and self.price == other.price

    def __init__(self, data: dict[str, Any], expiration_date: float = None):
        self.name = data["name"]
        if expiration_date is not None:
            self.expiration_date = expiration_date
        else:
            self.expiration_date = data["expiration_date"]
        self._add_subs(data["subs"])

    def _add_subs(self, subs: list[dict[str, Any]]) -> None:
        self.subs = list()
        for sub in subs:
            self.subs.append(self.DiscountData(sub))

    def has_discount(self, min_discount: int) -> bool:
        return len(list(filter(lambda sub: sub.discount_pct >= min_discount, self.subs))) > 0

    def get_discounts(self) -> str:
        return f"{[str(sub) for sub in self.subs]}\n"

    def __str__(self) -> str:
        return f"Name: {self.name} | Discounts: {[str(x) for x in self.subs]}"

    def __eq__(self, other: 'GameData') -> bool:
        if isinstance(other, GameData):
            return self.name == other.name and self.subs == other.subs
        raise ValueError(f"invalid comparison object: {type(other)}")
