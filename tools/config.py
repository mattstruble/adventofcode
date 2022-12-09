
import configparser
from functools import lru_cache

@lru_cache(maxsize=1)
def get_configuration() ->configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read("adventofcode.cfg")

    return config 