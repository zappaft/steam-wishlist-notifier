import os
import json
import queue
import sys
import threading
import time
from typing import Any
from pynotifier import Notification
import requests

notification_queue = queue.Queue()
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")


def validate_data(data: dict[str, int]) -> bool:
    for value in data.values():
        if not isinstance(value, int):
            raise ValueError
    return True


class Settings:
    profile_id: int
    interval: int
    min_discount: int
    page_delay: int
    notification_duration: int
    url: str

    def __init__(self):
        try:
            with open(SETTINGS_FILE, "r") as settings_file:
                data: dict[str, int] = json.load(settings_file)
                if validate_data(data):
                    self.__dict__ = data
                    self.url = f"https://store.steampowered.com/wishlist/profiles/{self.profile_id}/wishlistdata"
        except (FileNotFoundError, ValueError) as e:
            if isinstance(e, FileNotFoundError):
                print(f"Please fill the {SETTINGS_FILE} with your data/preferences.")
                self.profile_id = None
                self.interval = 4
                self.min_discount = 30
                self.page_delay = 1
                self.notification_duration = 4
                with open(SETTINGS_FILE, "w") as settings_file:
                    json.dump(self.__dict__, settings_file, indent=2)
                sys.exit(1)
            else:
                print(f"Invalid data found at settings file: {SETTINGS_FILE}")
                sys.exit(1)


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
            duration=settings.notification_duration
        ).send()
        time.sleep(settings.notification_duration + 1)
        notification_queue.task_done()


def start() -> None:
    while True:
        has_next: bool = True
        page: int = 0
        while has_next:
            r: requests.Response = requests.get(f"{settings.url}/?p={page}&v=2")
            wishlist: dict = r.json()
            if r.status_code == 200 and wishlist:
                for data in wishlist.values():
                    game_data: GameData = GameData(data)
                    game_data.add_subs(data["subs"])
                    if game_data.has_discount(settings.min_discount):
                        notification_queue.put(game_data)
            else:
                has_next = False
            page += 1
            time.sleep(settings.page_delay)
        time.sleep(settings.interval * 60 * 60)


if __name__ == '__main__':
    settings = Settings()
    threading.Thread(target=show_notification, daemon=True).start()
    start()
