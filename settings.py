import logging
import sys
import json
import os
from typing import Union

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")
SECS_IN_HOUR = 3600


def validate_data(data: dict[str, Union[int, float]]) -> bool:
    # TODO validate profile_id as a valid user
    # TODO improve validation to allow different types
    for k, value in data.items():
        if not isinstance(value, (int, float)):
            logging.error(f"settings.validate_data :: invalid data {value} for key {k}")
            raise ValueError
    return True


class Settings:

    def __init__(self, debug=False):
        self.debug = debug
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as settings_file:
                data: dict[str, int] = json.load(settings_file)
                if validate_data(data):
                    if "debug" in data:
                        del data["debug"]
                    self.__dict__.update(data)
        except (FileNotFoundError, ValueError) as e:
            if isinstance(e, FileNotFoundError):
                logging.warning(f"settings.Settings.__init__ :: Please fill the {SETTINGS_FILE} with your data.")
                self.profile_id = None
                self.interval = 4
                self.min_discount = 30
                self.page_delay = 1
                self.notification_duration = 5
                self.expiration_days = 7
                self.start_delay = 3
                with open(SETTINGS_FILE, "w", encoding="utf-8") as settings_file:
                    logging.debug(f"settings.Settings.__init__ :: Writing default settings to {SETTINGS_FILE}")
                    del self.debug
                    json.dump(self.__dict__, settings_file, indent=2, ensure_ascii=False)
                sys.exit(1)
            else:
                logging.error(f"settings.Settings.__init__ :: Invalid data found at settings file {SETTINGS_FILE}")
                sys.exit(1)

    def wishlist_url(self) -> str:
        return f"https://store.steampowered.com/wishlist/profiles/{self.profile_id}/wishlistdata"

    def get_request_interval(self) -> int:
        return self.interval * SECS_IN_HOUR if not self.debug else 10

    def get_start_delay(self) -> int:
        return self.start_delay * 60 if not self.debug else 0

    def get_expiration_days(self):
        return self.expiration_days if not self.debug else -1
