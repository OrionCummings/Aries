from enum import Enum

class TextFormatting():
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
def hex_literal(s: str) -> str:
    return "{:X}".format(s)

def red_bold(s: str) -> str:
    return red(bold(s))

def green_bold(s: str) -> str:
    return green(bold(s))

def blue_bold(s: str) -> str:
    return blue(bold(s))

def bold(s: str) -> str:
    return str(TextFormatting.BOLD) + str(s) + str(TextFormatting.END)

def red(s: str) -> str:
    return str(TextFormatting.RED) + str(s) + str(TextFormatting.END)

def green(s: str) -> str:
    return str(TextFormatting.GREEN) + str(s) + str(TextFormatting.END)

def blue(s: str) -> str:
    return str(TextFormatting.BLUE) + str(s) + str(TextFormatting.END)

def print_red(s: str) -> None:
    print(red(s))

def print_green(s: str) -> None:
    print(green(s))

def print_blue(s: str) -> None:
    print(blue(s))

class ParseMode(Enum):
    Register = 0,
    ImmediateValue = 1,
    Address = 2,

class PrintMode(Enum):
    NoOutput        = 0,
    Bytes           = 1,
    Binary          = 2,
    Hex             = 3,
    Instructions    = 4,
