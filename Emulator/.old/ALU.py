from __future__ import annotations
from typing import Optional
from Operation import Operation, OperationType
from ALU1Bit import ALU1Bit

class ALU():

    def __init__(self):

        # Create the inputs a, b, and cin
        self.a: Optional[int] = None
        self.b: Optional[int] = None
        self.cin: Optional[int] = None

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

        bools: list[bool] = [False] * 32
        for index in range(0, len(s)):
            if s[index] == '1':
                bools[index] = True
            else:
                bools[index] = False

        return bools

    @staticmethod
    def boolean_list_to_int(bool_list: list[bool]) -> int:

        bool_list = list(reversed(bool_list))
        n = 0
        for index, b in enumerate(bool_list):
            b_int = int(b)
            mask = (b_int << index)
            n |= mask

        return n

    def set_operation(self, op_type: OperationType):

        # Set the overall ALU operation
        self.operation = Operation(op_type)

        # Set each 1 bit ALU operation
        [alu1bit.set_operation(op_type) for alu1bit in self.alus]

    def eval(self):

        # Invert inputs
        if self.invert_a: self.a = ~self.a
        if self.invert_b: self.b = ~self.b

        # Create a boolean input list
        a_bool_list = ALU.int_to_boolean_list(self.a)
        b_bool_list = ALU.int_to_boolean_list(self.b)
        cin_bool_list = ALU.int_to_boolean_list(self.cin)

        s_bool_list = []

        cout = False

        # For ever bit in the inputs
        for index in range(0, len(a_bool_list)):
            (a, b, cin) = (a_bool_list[index], b_bool_list[index], cin_bool_list[index])
            (s, cout) = self.operation.eval(a, b, cin)
            s_bool_list.append(s)
            

        self.s = ALU.boolean_list_to_int(s_bool_list)
        self.cout = cout

    def get_a(self) -> int:
        return self.a

    def set_a(self, a: int) -> None:
        self.a = a

    def get_b(self) -> int:
        return self.b
    
    def set_b(self, b: int) -> None:
        self.b = b

    def get_cin(self) -> int:
        return self.cin
    
    def set_cin(self, cin: int) -> None:
        self.cin = cin

    def get_s(self) -> int:
        return self.s

    def get_cout(self) -> int:
        return self.cout

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

    a = 3427
    b = 16892

    alu = ALU()
    alu.set_operation(OperationType.Add)
    alu.set_a(a)
    alu.set_b(b)
    alu.set_cin(0)
    alu.eval()
    x = alu.get_s()
    y = a + b
    assert x == y

    # TODO: Make ALU tests!!
    