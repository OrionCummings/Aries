from __future__ import annotations
from enum import Enum
from typing import Optional
from Operation import OperationType

class ALU():
    
    def __init__(self):

        # Create the inputs a and b
        self.a: Optional[int] = None
        self.b: Optional[int] = None

        # Create outputs r (result) and c (carry)
        self.r: Optional[int] = None
        self.c: Optional[int] = None

        # Create the invert signals
        self.invert_a: Optional[bool] = None
        self.invert_b: Optional[bool] = None

        # Create the operation signal
        self.operation: Optional[OperationType] = None

    def __str__(self) -> str:
        return "str(ALU)\n"

    def __eq__(self, other: ALU):
        pass

    def get_a(self) -> int:
        return self.a
    
    def set_a(self, a: int) -> int:
        self.a = a

    def get_b(self) -> int:
        return self.b
    
    def set_b(self, b: int) -> int:
        self.b = b

    def get_r(self) -> int:
        return self.r
    
    def get_c(self) -> int:
        return self.c
    
    def set_invert_a(self) -> None:
        self.invert_a = True

    def reset_invert_a(self) -> None:
        self.invert_a = False

    def toggle_invert_a(self) -> None:
        self.invert_a = not self.invert_a

    def set_invert_b(self) -> None:
        self.invert_b = True

    def reset_invert_b(self) -> None:
        self.invert_b = False

    def toggle_invert_b(self) -> None:
        self.invert_b = not self.invert_b


