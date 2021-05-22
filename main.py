import getpass
import os
import queue
import threading
import time
from typing import Any
from datetime import datetime, timedelta

from pynotifier import Notification
import requests
from requests import Response

from data_cache import CacheData
from game_data import GameData
from settings import Settings

PYTHON_EXE = os.path.join(os.path.dirname(__file__), "venv", "Scripts", "python.exe")


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
        has_next = True
        page = 0
        while has_next:
            r: Response = requests.get(f"{settings.wishlist_url()}/?p={page}&v=2")
            wishlist: dict[str, Any] = r.json()
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
        time.sleep(settings.get_request_interval())


if __name__ == '__main__':
    add_to_startup()
    settings = Settings(debug=True)
    cache = CacheData()
    notification_queue = queue.Queue()
    time.sleep(settings.get_start_delay())
    threading.Thread(target=show_notification, daemon=True).start()
    start()
