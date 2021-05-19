import time
from typing import Any

import requests
from argparse import ArgumentParser


class GameData:
    class DiscountData:
        discount_pct: int
        price: int

        def __init__(self, dict_):
            self.__dict__.update(dict_)

        def __str__(self):
            return f"Discount: {self.discount_pct}% | Value: ~{self.price / 100}"

    name: str
    sub_data: list[DiscountData]

    def __init__(self, dict_):
        self.sub_data = []
        self.__dict__.update(dict_)

    def add_subs(self, subs: list[dict[str, Any]]) -> None:
        for sub in subs:
            self.sub_data.append(self.DiscountData(sub))

    def has_discount(self, min_discount: int) -> bool:
        return len(
            list(filter(lambda sub: sub.discount_pct >= min_discount, self.sub_data))
        ) > 0
        # for sub in self.sub_data:
        #     if sub.discount_pct >= min_discount:
        #         return True
        # return False

    def __str__(self):
        return f"{self.name}: {[str(x) for x in self.sub_data]}"


def show_notification(game_data: GameData):
    print(game_data)


def setup() -> None:
    parser = ArgumentParser()
    parser.add_argument("-user", required=True)
    parser.add_argument("-min", required=True)
    parser.add_argument("-discount", required=True)
    args = parser.parse_args()
    profile_id: str = args.user
    interval: int = int(args.min) * 60
    min_discount: int = int(args.discount)
    url: str = f"https://store.steampowered.com/wishlist/profiles/{profile_id}/wishlistdata"
    start(url, interval, min_discount)


def start(url: str, interval: int, min_discount: int) -> None:
    while True:
        has_next: bool = True
        page: int = 0
        while has_next:
            r: requests.Response = requests.get(f"{url}/?p={page}&v=2")
            if r.status_code == 200 and r.json():
                wishlist: dict = r.json()
                for _, data in wishlist.items():
                    game_data: GameData = GameData(data)
                    game_data.add_subs(data["subs"])
                    if game_data.has_discount(min_discount):
                        show_notification(game_data)
            else:
                has_next = False
            page += 1
            time.sleep(3)
        time.sleep(interval)


if __name__ == '__main__':
    setup()
