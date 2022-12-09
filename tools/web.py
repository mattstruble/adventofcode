# -*- coding: utf-8 -*-
import json
import os
import time
from typing import Optional

import requests

from tools import CACHE_DIR, INPUT_FILE_NAME, INPUTS_DIR
from tools.config import get_configuration
from tools.utils import Singleton

# curl 'https://adventofcode.com/2022/day/7/answer' -X POST -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: https://adventofcode.com' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: https://adventofcode.com/2022/day/7' -H 'Cookie: session=XXX' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: same-origin' -H 'Sec-Fetch-User: ?1' -H 'Sec-GPC: 1' --data-raw 'level=2&answer=3866390'


class RequestLimiter(Singleton):
    """Be kind, and don't spam adventofcode.com"""

    GENERAL_RATE_SEC = 1
    DUPLICATE_RATE_SEC = 10

    def __init__(self) -> None:
        try:
            with open(os.path.join(CACHE_DIR, "requests.json"), "r") as f:
                self.requests = json.load(f)
        except FileNotFoundError:
            self.requests = {}

        self.last_request_time = 0

    def _save(self) -> None:
        with open(os.path.join(CACHE_DIR, "requests.json"), "w") as f:
            json.dump(self.requests, f)

    def get(self, url, **kwargs):
        now = time.time()

        if url in self.requests:
            time.sleep(max(0, self.DUPLICATE_RATE_SEC - (now - self.requests[url])))
        else:
            time.sleep(max(0, self.GENERAL_RATE_SEC - (now - self.last_request_time)))

        self.requests[url] = time.time()
        self.last_request_time = time.time()

        self._save()
        return requests.get(url, **kwargs)


class AOCWebInterface:
    """Interfaces with AOC"""

    def __init__(self, year: int, day: int) -> None:
        self.year = year
        self.day = day
        self.day_str = f"day_{day:02d}"
        self.request_limit = RequestLimiter()

        config = get_configuration()
        cookies = {}
        for key, value in config.items("requests.cookies"):
            cookies[key] = value

        self.request_kwargs = {"cookies": cookies}

    def download_input(self, path: Optional[str] = None) -> None:
        if path is None:
            path = os.path.join(INPUTS_DIR, self.day_str, INPUT_FILE_NAME)

        if os.path.exists(path):
            return

        response = self.request_limit.get(
            f"https://adventofcode.com/{self.year}/day/{self.day}/input",
            **self.request_kwargs,
        )

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "wb") as f:
            f.write(response.content)
