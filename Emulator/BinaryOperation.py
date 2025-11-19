from enum import Enum

class BinaryOperation():

    @staticmethod
    def and_operation(a, b) -> int:
        return a & b

    @staticmethod
    def or_operation(a, b) -> int:
        return (a | b)
    
    @staticmethod
    def xor_operation(a, b) -> int:
        return (a ^ b)

    @staticmethod
    def half_add_operation(a, b) -> tuple[int, int]:
        s = a ^ b
        c = a and b
        return (s, c)
    
    @staticmethod
    def full_add_operation(a, b, cin) -> tuple[int, int]:
        s1, c1 = BinaryOperation.half_add_operation(cin, a)
        s2, c2 = BinaryOperation.half_add_operation(s1, b)
        c = c1 or c2
        return (s2, c)
    
    # TODO: Do this later lmao
    @staticmethod
    def intel74181():
        pass

class OperationType(Enum):
    NONE = 0,
    AND = 1,
    OR = 2,
    ADD = 3
