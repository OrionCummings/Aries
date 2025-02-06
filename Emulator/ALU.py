from __future__ import annotations
from typing import Optional
from Operation import Operation, OperationType
from ALU1Bit import ALU1Bit

class ALU():
    
    def __init__(self):

        # Create the inputs a and b
        self.a: Optional[int] = None
        self.b: Optional[int] = None

        # Create outputs s (result) and cout (carry out)
        self.s: Optional[int] = None
        self.cout: Optional[int] = None

        # Create the invert signals
        self.invert_a: Optional[bool] = None
        self.invert_b: Optional[bool] = None

        # Create the operation signal
        self.operation: Optional[Operation] = None

        # Create a list of 32 1-bit ALUs
        self.alus: list[ALU1Bit] = []
        for _ in range(0, 32):
            self.alus.append(ALU1Bit())

    def __str__(self) -> str:
        return "str(ALU)\n"

    def __eq__(self, other: ALU):
        pass

    @staticmethod
    def int_to_boolean_list(n: int) -> list[bool]:

        # Force the integer to be 32 bits
        n = n & 0xFFFFFFFF

        # Convert the int to a binary string
        s = format(n, "032b")

        bools: list[bool] = []
        for index in range(0, len(s)):
            bools.append(True) if s[index] == 1 else bools.append(False)

        return bools
    
    @staticmethod
    def boolean_list_to_int(bool_list: list[bool]) -> int:

        n = 0
        for index, b in enumerate(bool_list):
            n &= (b << index)

        return n

    def set_operation(self, op_type: OperationType):
        self.operation = Operation(op_type)
        for alu1bit in self.alus:
            alu1bit.set_operation(op_type)

    def eval(self):

        # Create a boolean input list
        a_bool_list = ALU.int_to_boolean_list(self.a)
        b_bool_list = ALU.int_to_boolean_list(self.b)

        # For ever bit in the inputs
        for index in reversed(range(0, 32)):
            (self.s, self.cout) = self.operation.eval(a_bool_list[index], b_bool_list[index])

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

if __name__ == '__main__':

    alu = ALU()
