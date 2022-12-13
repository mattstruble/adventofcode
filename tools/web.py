# -*- coding: utf-8 -*-
import json
import os
import re
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

        headers = {
            "User-Agent": "github.com/mattstruble/adventofcode by twitter.com/mestruble"
        }

        self.request_kwargs = {"cookies": cookies, "headers": headers}

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
    def _get_day_article(self, puzzle_num=1) -> str:
        cache_fname = os.path.join(CACHE_DIR, f"{self.day_str}.html")

        if os.path.exists(cache_fname):
            with open(cache_fname, "r") as f:
                html = f.read()

            # If we have both articles early return
            soup = BeautifulSoup(html, "html.parser")
            if len(soup.findAll("article")) >= puzzle_num:
                return html

        url = f"https://adventofcode.com/{self.year}/day/{self.day}"

        response = self.request_limit.get(url, **self.request_kwargs)

        soup = BeautifulSoup(response.content, "html.parser")
        article = "".join([str(article) for article in soup.findAll("article")])

        with open(cache_fname, "w") as f:
            f.write(article)

        return article

    def download_prompt(self, puzzle_num: int = 1, path: Optional[str] = None) -> None:
        if path is None:
            path = os.path.join(INPUTS_DIR, self.day_str, "README.md")

        article = self._get_day_article(puzzle_num)

        with open(path, "w") as f:
            f.write(markdownify.markdownify(str(article), heading_style="ATX"))

    def download_examples(
        self, puzzle_num: int = 1, path: Optional[str] = None
    ) -> None:
        if path is None:
            path = os.path.join(INPUTS_DIR, self.day_str)

        article = self._get_day_article(puzzle_num)

        soup = BeautifulSoup(article, "html.parser")
        articles = soup.findAll("article")

        for i, article in enumerate(articles):
            if os.path.exists(os.path.join(path, f"EXAMPLE_{i+1}.txt")):
                continue

            examples = article.findAll(
                "p", text=re.compile("(?:f|F)or (?:example|example:)", re.IGNORECASE)
            )
            for example in examples:
                try:
                    pre = example.find_next_sibling("pre")
                    with open(os.path.join(path, f"EXAMPLE_{i+1}.txt"), "w") as f:
                        f.write(str(pre.code.text.strip()))
                except Exception as e:
                    print(e)

    def submit(self, puzzle_num: int, solution: Union[str, int, float]) -> bool:
        data = {"level": puzzle_num, "answer": solution}

        url = f"https://adventofcode.com/{self.year}/day/{self.day}/answer"

        response = self.request_limit.post(url, data=data, **self.request_kwargs)

        soup = BeautifulSoup(response.content, "html.parser")
        article = soup.find("article")
        article_txt = article.getText(separator=" ", strip=True)
        correct = (
            "the right answer!" in article_txt.lower()
            and "one gold star" in article_txt.lower()
        )

        if not correct:
            print(article_txt)
        # hack for now, will change when get live response next day
        return correct
