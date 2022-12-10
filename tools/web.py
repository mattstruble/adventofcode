# -*- coding: utf-8 -*-
import json
import os
import time
from functools import lru_cache
from typing import Optional, Union

import markdownify
import requests
from bs4 import BeautifulSoup

from tools import CACHE_DIR, INPUT_FILE_NAME, INPUTS_DIR
from tools.config import get_configuration
from tools.utils import Singleton


class RequestLimiter(Singleton):
    """Be kind, and don't spam adventofcode.com"""

    GENERAL_RATE_SEC = 1
    GET_RATE_SEC = 10
    POST_RATE_SEC = 60

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

    def _wait(self, url: str, max_wait: int):
        now = time.time()

        if url in self.requests:
            time.sleep(max(0, max_wait - (now - self.requests[url])))
        else:
            time.sleep(max(0, self.GENERAL_RATE_SEC - (now - self.last_request_time)))

        self.requests[url] = time.time()
        self.last_request_time = time.time()

        self._save()

    def get(self, url, **kwargs):
        self._wait(url, self.GET_RATE_SEC)
        return requests.get(url, **kwargs)

    def post(self, url, **kwargs):
        self._wait(url, self.POST_RATE_SEC)
        return requests.post(url, **kwargs)


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

        url = f"https://adventofcode.com/{self.year}/day/{self.day}/input"

        response = self.request_limit.get(url, **self.request_kwargs)

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "wb") as f:
            f.write(response.content)

    @lru_cache()
    def _get_day_article(self) -> str:
        cache_fname = os.path.join(CACHE_DIR, f"{self.day_str}.html")

        if os.path.exists(cache_fname):
            with open(cache_fname, "r") as f:
                html = f.readlines()

            return html

        url = f"https://adventofcode.com/{self.year}/day/{self.day}"

        response = self.request_limit.get(url, **self.request_kwargs)

        soup = BeautifulSoup(response.content, "html.parser")
        article = "".join([str(article) for article in soup.findAll("article")])

        with open(cache_fname, "w") as f:
            f.write(article)

        return article

    def download_prompt(self, path: Optional[str] = None) -> None:
        if path is None:
            path = os.path.join(INPUTS_DIR, self.day_str, "README.md")

        if os.path.exists(path):
            return

        article = self._get_day_article()

        with open(path, "w") as f:
            f.write(markdownify.markdownify(str(article), heading_style="ATX"))

    def submit(self, puzzle_num: int, solution: Union[str, int, float]) -> bool:
        data = {"level": puzzle_num, "answer": solution}

        headers = {
            "Origin": "https://adventofcode.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": f"https://adventofcode.com/{self.year}/day/{self.day}",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
        }

        url = f"https://adventofcode.com/{self.year}/day/{self.day}/answer"

        response = self.request_limit.post(
            url, data=data, headers=headers, **self.request_kwargs
        )

        print(response.content)

        # hack for now, will change when get live response next day
        return (
            "that is right!" in response.content.decode("utf-8").lower()
            and "gold star" in response.content.decode("utf-8").lower()
        )
