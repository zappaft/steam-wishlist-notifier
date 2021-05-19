import queue
import threading
import time
from typing import Any
from pynotifier import Notification
import requests
from argparse import ArgumentParser

PAGE_DELAY = 1
NOTIFICATION_DURATION = 4
notification_queue = queue.Queue()


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

    def get_discounts(self) -> str:
        return f"{[str(x) for x in self.sub_data]}"

    def __str__(self) -> str:
        return f"Name: {self.name} | Discounts: {[str(x) for x in self.sub_data]}"


def show_notification():
    while True:
        game_data: GameData = notification_queue.get()
        Notification(
            title=game_data.name,
            description=game_data.get_discounts(),
            duration=NOTIFICATION_DURATION
        ).send()
        time.sleep(NOTIFICATION_DURATION * 1.5)
        notification_queue.task_done()


def setup() -> None:
    parser = ArgumentParser()
    parser.add_argument("-user", required=True)
    parser.add_argument("-interval", required=True)
    parser.add_argument("-discount", required=True)
    args = parser.parse_args()
    profile_id: str = args.user
    interval: int = int(args.interval) * 60
    min_discount: int = int(args.discount)
    url: str = f"https://store.steampowered.com/wishlist/profiles/{profile_id}/wishlistdata"
    threading.Thread(target=show_notification, daemon=True).start()
    start(url, interval, min_discount)


def start(url: str, interval: int, min_discount: int) -> None:
    while True:
        has_next: bool = True
        page: int = 0
        while has_next:
            r: requests.Response = requests.get(f"{url}/?p={page}&v=2")
            wishlist: dict = r.json()
            if r.status_code == 200 and wishlist:
                for data in wishlist.values():
                    game_data: GameData = GameData(data)
                    game_data.add_subs(data["subs"])
                    if game_data.has_discount(min_discount):
                        notification_queue.put(game_data)
            else:
                has_next = False
            page += 1
            time.sleep(PAGE_DELAY)
        time.sleep(interval)


if __name__ == '__main__':
    setup()
