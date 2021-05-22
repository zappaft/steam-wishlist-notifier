import json
import os
from datetime import datetime
from json import JSONEncoder
from typing import Any

from game_data import GameData

CACHE_FILE = os.path.join(os.path.dirname(__file__), "cached_data.json")


class CacheEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:
        return obj.__dict__


class CacheData:

    def __init__(self):
        try:
            self._load_cache()
        except FileNotFoundError:
            self.data = dict()

    def add(self, game_data: GameData):
        self.data[game_data.name] = game_data
        self._save_cache()

    def __contains__(self, game_data: GameData) -> bool:
        return game_data.name in self.data.keys() and self.data[game_data.name] == game_data

    def _save_cache(self):
        with open(CACHE_FILE, "w", encoding="utf-8") as cache_file:
            json.dump(self.data, cache_file, cls=CacheEncoder, indent=2, ensure_ascii=False)

    def _load_cache(self):
        with open(CACHE_FILE, "r", encoding="utf-8") as cache_file:
            data: dict[str, Any] = json.load(cache_file)
            new_data = dict()
            for k, game_data in data.items():
                parsed_data: GameData = GameData(game_data)
                print(f"data: {parsed_data.expiration_date} > {datetime.now().timestamp()} = {parsed_data.expiration_date > datetime.now().timestamp()}")
                if parsed_data.expiration_date > datetime.now().timestamp():
                    new_data[k] = parsed_data
                    new_data[k].subs = list(map(lambda sub: GameData.DiscountData(sub), data[k]["subs"]))
            self.data = new_data
