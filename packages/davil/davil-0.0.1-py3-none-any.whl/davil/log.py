from enum import Enum
from sty import fg


class Color(Enum):
    YELLOW = fg.yellow
    RED = fg.red
    GREEN = fg.green


def colorize(text, color):
    return color.value + text + fg.rs


def warn(msg):
    print(colorize('WARNING: ' + str(msg), Color.YELLOW))


def error(msg):
    print(colorize('ERROR: ' + str(msg), Color.RED))


def success(msg):
    print(colorize('SUCCESS: ' + str(msg), Color.GREEN))
