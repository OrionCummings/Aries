from enum import Enum

class PP():
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
    
    def HexLiteral(s: str) -> str:
        return "{:X}".format(s)
    
    def RedBold(s: str) -> str:
        return PP.Red(PP.Bold(s))

    def GreenBold(s: str) -> str:
        return PP.Green(PP.Bold(s))
    
    def BlueBold(s: str) -> str:
        return PP.Blue(PP.Bold(s))
    
    def Bold(s: str) -> str:
        return str(PP.BOLD) + str(s) + str(PP.END)

    def Red(s: str) -> str:
        return str(PP.RED) + str(s) + str(PP.END)
    
    def Green(s: str) -> str:
        return str(PP.GREEN) + str(s) + str(PP.END)
    
    def Blue(s: str) -> str:
        return str(PP.BLUE) + str(s) + str(PP.END)

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
