from __future__ import annotations
from Operation import Operation, OperationType
from typing import Optional

class ALU1Bit():
    
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
    
    def __str__(self) -> str:
        return "str(ALU1Bit)\n"

    def __eq__(self, other: ALU1Bit):
        pass

    def eval(self) -> tuple[bool, bool]:
        return self.operation.eval(self.a, self.b, self.cin)

    def set_operation(self, op_type: OperationType):
        self.operation = Operation(op_type)

    def get_a(self) -> bool:
        return self.a
    
    def set_a(self, a: bool) -> bool:
        self.a = a

    def get_b(self) -> bool:
        return self.b
    
    def set_b(self, b: bool) -> bool:
        self.b = b

    def get_cin(self) -> bool:
        return self.cin
    
    def set_cin(self, cin: bool) -> bool:
        self.cin = cin

    def get_r(self) -> bool:
        return self.r
    
    def get_c(self) -> bool:
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

    alu = ALU1Bit()
    alu.set_operation(OperationType.Add)
    alu.set_a(False)
    alu.set_b(True)
    alu.set_cin(True)
    (s, cout) = alu.eval()
    print(f"{s} -- {cout}")