from enum import Enum

class TextFormatting():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[92m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    LIGHTGREY = '\033[37m'
    DARKGREY = '\033[90m'
    LIGHTRED = '\033[91m'
    LIGHTGREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHTBLUE = '\033[94m'
    PINK = '\033[95m'
    LIGHTCYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[01m'
    DISABLE = '\033[02m'
    UNDERLINE = '\033[04m'
    REVERSE = '\033[07m'
    STRIKETHROUGH = '\033[09m'
    INVISIBLE = '\033[08m'
    
def hex_literal(s: str) -> str:
    return "{:X}".format(s)

def red_bold(s: str) -> str:
    return red(bold(s))

def green_bold(s: str) -> str:
    return green(bold(s))

def yellow_bold(s: str) -> str:
    return yellow(bold(s))

def blue_bold(s: str) -> str:
    return blue(bold(s))

def bold(s: str) -> str:
    return str(TextFormatting.BOLD) + str(s) + str(TextFormatting.RESET)

def red(s: str) -> str:
    return str(TextFormatting.RED) + str(s) + str(TextFormatting.RESET)

def green(s: str) -> str:
    return str(TextFormatting.GREEN) + str(s) + str(TextFormatting.RESET)

def blue(s: str) -> str:
    return str(TextFormatting.BLUE) + str(s) + str(TextFormatting.RESET)

def yellow(s: str) -> str:
    return str(TextFormatting.YELLOW) + str(s) + str(TextFormatting.RESET)

def orange(s: str) -> str:
    return str(TextFormatting.ORANGE) + str(s) + str(TextFormatting.RESET)

def print_red(s: str) -> None:
    print(red(s))

def print_green(s: str) -> None:
    print(green(s))

def print_blue(s: str) -> None:
    print(blue(s))

def print_yellow(s: str) -> None:
    print(yellow(s))

def info(s: str) -> None:
    print_blue(f"[INFO] {s}")

def success(s: str) -> None:
    print_green(f"[SUCCESS] {s}")

def warning(s: str) -> None:
    print_yellow(f"[WARNING] {s}")

def error(s: str) -> None:
    print_red(f"[ERROR] {s}")

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
