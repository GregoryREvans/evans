import re


def to_digit(string):
    return int(string) if string.isdigit() else string


def sorted_keys(text):
    return [to_digit(_) for _ in re.split(r"(\d+)", text)]
