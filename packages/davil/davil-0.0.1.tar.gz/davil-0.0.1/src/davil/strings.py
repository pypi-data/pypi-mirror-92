import re


def get_number_of_chars(path, char):
    n = 0
    for c in path:
        if c is char:
            n = n + 1
    return n


def get_number_of_underscores(path):
    return get_number_of_chars(path, '_')


def nums_from_string(text: str):
    return [s for s in re.findall(r'\d+', text)]
