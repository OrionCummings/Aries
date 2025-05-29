from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Self

@dataclass
class Definition:
    name: str
    value = None

    def __str__(self):
        return f"{{name: '{self.name}', value: '{self.value}'}}"

class DirectiveType(Enum):
    INCLUDE     = auto(),
    DEFINE      = auto(),
    IF          = auto(),
    ENDIF       = auto(),
    IFDEF       = auto(),
    IFNDEF      = auto(),

    def __str__(self) -> str:
        return super().__str__()

    @staticmethod
    def classify(directive: str) -> Optional[Self]:
        d = directive.upper()
        if   d == "DEFINE":     return DirectiveType.DEFINE
        elif d == "INCLUDE":    return DirectiveType.INCLUDE
        elif d == "IF":         return DirectiveType.IF
        elif d == "ENDIF":      return DirectiveType.ENDIF
        elif d == "IFDEF":      return DirectiveType.IFDEF
        elif d == "IFNDEF":     return DirectiveType.IFNDEF
        else:                   return None

@dataclass
class DirectiveInstance:
    directive_type: DirectiveType
    line: int
    included_file: Optional[str] = None
    definition: Optional[Definition] = None

    def __str__(self) -> str:
        return f"{{type: {self.directive_type}, line: {self.line}, include: '{self.included_file}', definition: '{self.definition}'}}"

