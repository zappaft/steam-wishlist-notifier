import getpass
import os
import json
from json import JSONEncoder
import queue
import sys
import threading
import time
from typing import Any
from pynotifier import Notification
from datetime import datetime, timedelta
import requests

notification_queue = queue.Queue()
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")
CACHE_FILE = os.path.join(os.path.dirname(__file__), "cached_data.json")
PYTHON_EXE = os.path.join(os.path.dirname(__file__), "venv", "Scripts", "python.exe")


class CacheEncoder(JSONEncoder):
    def default(self, obj: 'GameData') -> Any:
        return obj.__dict__


class CacheData:

    def __init__(self):
        try:
            self._load_cache()
        except FileNotFoundError:
            self.data = dict()

    def add(self, game_data: 'GameData'):
        self.data[game_data.name] = game_data
        self._save_cache()

    def __contains__(self, game_data: 'GameData') -> bool:
        return game_data.name in self.data.keys() and self.data[game_data.name] == game_data

    def _save_cache(self):
        with open(CACHE_FILE, "w") as cache_file:
            json.dump(self.data, cache_file, cls=CacheEncoder, indent=2)

    def _load_cache(self):
        with open(CACHE_FILE, "r") as cache_file:
            data: dict[str, Any] = json.load(cache_file)
            new_data = dict()
            for k, game_data in data.items():
                parsed_data: GameData = GameData(game_data)
                if parsed_data.expiration_date > datetime.now().timestamp():
                    new_data[k] = parsed_data
                    new_data[k].subs = list(map(lambda sub: GameData.DiscountData(sub), data[k]["subs"]))
            self.data = new_data


class Settings:

    def __init__(self):
        try:
            with open(SETTINGS_FILE, "r") as settings_file:
                data: dict[str, int] = json.load(settings_file)
                if validate_data(data):
                    self.__dict__ = data
        except (FileNotFoundError, ValueError) as e:
            if isinstance(e, FileNotFoundError):
                print(f"Please fill the {SETTINGS_FILE} with your data/preferences.")
                self.profile_id = None
                self.interval = 4
                self.min_discount = 30
                self.page_delay = 1
                self.notification_duration = 4
                self.expiration_days = 7
                self.start_delay = 3
                with open(SETTINGS_FILE, "w") as settings_file:
                    json.dump(self.__dict__, settings_file, indent=2)
                sys.exit(1)
            else:
                print(f"Invalid data found at settings file: {SETTINGS_FILE}")
                sys.exit(1)

    def wishlist_url(self) -> str:
        return f"https://store.steampowered.com/wishlist/profiles/{self.profile_id}/wishlistdata"


class GameData:

    class DiscountData:

        def __init__(self, data: dict[str, Any]):
            self.discount_pct = data["discount_pct"]
            self.price = data["price"]

        def __repr__(self):
            return f"GameData.DiscountData({self.discount_pct}, {self.price})"

        def __str__(self):
            return f"Discount: {self.discount_pct}% | Value: ~{self.price / 100}"

        def __eq__(self, other: 'GameData.DiscountData'):
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
        return len(
            list(filter(lambda sub: sub.discount_pct >= min_discount, self.subs))
        ) > 0

    def get_discounts(self) -> str:
        return f"{[str(sub) for sub in self.subs]}\n"

    def __str__(self) -> str:
        return f"Name: {self.name} | Discounts: {[str(x) for x in self.subs]}"

    def __eq__(self, other: 'GameData'):
        if isinstance(other, GameData):
            return self.name == other.name and self.subs == other.subs
        raise ValueError(f"invalid comparison object: {type(other)}")


def validate_data(data: dict[str, int]) -> bool:
    # TODO validate profile_id as a valid user
    # TODO improve validation to allow different types
    for value in data.values():
        if not isinstance(value, int):
            raise ValueError
    return True


def add_to_startup():
    user_name = getpass.getuser()
    bat_path = rf'C:\Users\{user_name}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
    bat_name = "wishlist-notifier.bat"
    bat_file = os.path.join(bat_path, bat_name)

    if os.path.exists(bat_file):
        return

    with open(bat_file, "w+") as file:
        file.write(f"{PYTHON_EXE} {__file__}")


def show_notification() -> None:
    while True:
        game_data: GameData = notification_queue.get()
        cache.add(game_data)
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
            r: requests.Response = requests.get(f"{settings.wishlist_url()}/?p={page}&v=2")
            wishlist: dict = r.json()
            if r.status_code == 200 and wishlist:
                for data in wishlist.values():
                    expiration: float = (datetime.now() + timedelta(settings.expiration_days)).timestamp()
                    game_data: GameData = GameData(data, expiration)
                    if game_data.has_discount(settings.min_discount) and game_data not in cache:
                        notification_queue.put(game_data)
            else:
                has_next = False
            page += 1
            time.sleep(settings.page_delay)
        time.sleep(settings.interval * 60 * 60)


if __name__ == '__main__':
    add_to_startup()
    settings = Settings()
    cache = CacheData()
    time.sleep(settings.start_delay * 60)
    threading.Thread(target=show_notification, daemon=True).start()
    start()
