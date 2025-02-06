from enum import Enum

class OperationType(Enum):
    NoOperation = 0
    Not         = 1
    And         = 2
    Nand        = 3
    Or          = 4
    Xor         = 5
    Nor         = 6
    Xnor        = 7
    Add         = 8

class Operations:

    @staticmethod
    def op_no_operation(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
        return (False, False)

    @staticmethod
    def op_not(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
        s = not a
        return (s, False)

    @staticmethod
    def op_and(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
        s = a and b
        return (s, False)

    @staticmethod
    def op_nand(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
        s = not(a and b)
        return (s, False)

    @staticmethod
    def op_or(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
        s = a or b
        return (s, False)

    @staticmethod
    def op_xor(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
        s = (a or b) and not (a and b)
        return (s, False)

    @staticmethod
    def op_nor(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
        s = not (a or b)
        return (s, False)

    @staticmethod
    def op_xnor(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
        s = not ((a or b) and not (a and b))
        return (s, False)

    @staticmethod
    def op_add(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:

        (d,    _) = Operations.op_xor(a, b,   False)
        (f,    _) = Operations.op_and(a, b,   False)
        (e,    _) = Operations.op_and(d, cin, False)
        (s,    _) = Operations.op_xor(d, cin, False)
        (cout, _) = Operations.op_or (e, f,   False)
        return (s, cout)

    operation_list = [
        op_no_operation,
        op_not,
        op_and,
        op_nand,
        op_or,
        op_xor,
        op_nor,
        op_xnor,
        op_add,
    ]

class Operation:

    def __init__(self, operation_type: OperationType):
        self.set_operation(operation_type)

    def set_operation(self, operation_type: OperationType):
        self.operation_type = operation_type
        self.function = Operations.operation_list[operation_type.value]

    def eval(self, a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
        return self.function(a, b, cin)
    
if __name__ == '__main__':

    op = Operation(OperationType.Add)

    (s, cout) = op.eval(False, False, True)
    print(f"expected: {True}\t{False}")
    print(f"actual:   {s}\t{cout}")

