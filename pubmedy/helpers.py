"""Simple helper functions.
"""
import logging
import re
from typing import List, Sequence, Union


def unique(sequence: Sequence) -> List:
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


def find_email(string: str) -> Union[str, None]:
    # https://stackoverflow.com/questions/3965104/not-none-test-in-python
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", string)
    if match:
        return match.group(0)
    else:
        return None


def clean_html(raw_html):
    # https://stackoverflow.com/a/12982689/8674856
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


def config_basicLogger(logfile: str) -> None:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.FileHandler(logfile + ".log", mode="w"), stream_handler],
    )
