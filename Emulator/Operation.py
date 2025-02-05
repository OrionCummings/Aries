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
    Subtract    = 9

def op_no_operation(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
    r = False
    c = False
    return (r, c)

def op_not(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
    r = not a
    c = False
    return (r, c)

def op_and(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
    r = a and b
    c = False
    return (r, c)

def op_nand(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
    r = not(a and b)
    c = False
    return (r, c)

def op_or(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
    r = a or b
    c = False
    return (r, c)

def op_xor(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
    r = (a or b) and not (a and b)
    c = False
    return (r, c)

def op_nor(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
    r = not (a or b)
    c = False
    return (r, c)

def op_xnor(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
    r = not ((a or b) and not (a and b))
    c = False
    return (r, c)

def op_add(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
    (r, _) = op_xor(a, b)
    (_, c) = op_and(a, b)
    return (r, c)

def op_subtract(a: bool, b: bool, cin: bool) -> tuple[bool, bool]:
    (r, _) = op_xor(a, b)
    (_, c) = op_and(a, b)
    return (r, c)

OPERATIONS = [
    op_no_operation,
    op_not,
    op_and,
    op_nand,
    op_or,
    op_xor,
    op_nor,
    op_xnor,
    op_and,
    op_add,
    op_subtract
]

class Operation:

    def __init__(self, operation_type: OperationType):
        self.set_operation(operation_type)

    def set_operation(self, operation_type: OperationType):
        self.operation_type = operation_type
        self.function = OPERATIONS[operation_type.value]

    def eval(self, a: bool, b: bool) -> tuple[bool, bool]:
        return self.function(a, b)
    
if __name__ == '__main__':

    op = Operation(OperationType.Add)

    (r, cout) = op.eval(True, True, True)

    print(r)
    print(cout)

