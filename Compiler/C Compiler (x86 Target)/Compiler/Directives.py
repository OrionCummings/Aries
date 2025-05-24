from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Self

class DirectiveType(Enum):
    NONE        = auto(),
    DEFINE      = auto(),
    INCLUDE     = auto(),
    IF          = auto(),
    IFDEF       = auto(),
    IFNDEF      = auto(),
    FUNCTION    = auto(), # TODO Implement

    @staticmethod
    def classify(directive: str) -> Optional[Self]:
        d = directive.upper()
        if   d == "NONE":       return DirectiveType.NONE
        elif d == "DEFINE":     return DirectiveType.DEFINE
        elif d == "INCLUDE":    return DirectiveType.INCLUDE
        elif d == "IF":         return DirectiveType.IF
        elif d == "IFDEF":      return DirectiveType.IFDEF
        elif d == "IFNDEF":     return DirectiveType.IFNDEF
        elif d == "FUNCTION":   return DirectiveType.FUNCTION
        else:                   return None

@dataclass
class Definition:
    name: str
    value = None