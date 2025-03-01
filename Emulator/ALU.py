from enum import Enum
from BinaryOperation import OperationType
from Utilities import trace

from option import Ok, Result

# NOTE: This does not work!

class ALU:

    def __init__(self, operation_type = OperationType.NONE, a = None, b = None, cin = None):
        self.operation_type = operation_type
        self.a = a
        self.b = b
        self.cin = cin

    def __str__(self) -> str:
        return f"{self.a} ~ {self.b} ({self.cin})"
    
    def set_op(self, op: OperationType) -> Result[None, str]:
        self.operation_type = op
        return Ok(None)

    def set_a(self, a) -> Result[None, str]:
        if a not in[0, 1]: return trace("attempted to set a to a non-binary value!")
        self.a = a
        return Ok(None)

    def set_b(self, b) -> Result[None, str]:
        if b not in[0, 1]: return trace("attempted to set b to a non-binary value!")
        self.b = b
        return Ok(None)
    
    def set_cin(self, cin) -> Result[None, str]:
        if cin not in[0, 1]: return trace("attempted to set cin to a non-binary value!")
        self.cin = cin
        return Ok(None)

    def eval(self) -> Result[tuple[int, int], str]:

        match self.operation_type:
            case OperationType.NONE:
                return trace("attempted to perform no operation")

            case OperationType.OR:
                (s, c) = OperationType.or_operation(self.a, self.b, self.cin)

                assert s in [0, 1]
                assert c in [0, 1]

                return Ok((s, c))

            case OperationType.AND:
                (s, c) = OperationType.and_operation(self.a, self.b, self.cin)

                assert s in [0, 1]
                assert c in [0, 1]

                return Ok((s, c))

            case OperationType.ADD:
                (s, c) = OperationType.full_add_operation(self.a, self.b, self.cin)

                assert s in [0, 1]
                assert c in [0, 1]

                return Ok((s, c))

class ALU2:

    def __init__(self, operation_type = OperationType.NONE, a = None, b = None, cin = None):

        assert a in range(0, 4)
        assert b in range(0, 4)
        assert cin in range(0, 1)

        self.operation_type = operation_type
        self.a = a
        self.b = b
        self.cin = cin

        self.alus: list[ALU] = [ALU(operation_type)] * 2

        # for a in self.alus:
        #     a.set_a(a_bin)
        #     a.set_b(b_bin)

    def set_operation(self, operation_type):
        self.operation_type = operation_type
        [a.set_op(operation_type) for a in self.alus]

    def set_a(self, a) -> Result[None, str]:
        self.a = a
        return Ok(None)
    
    def set_b(self, b) -> Result[None, str]:
        self.b = b
        return Ok(None)

    def set_cin(self, cin) -> Result[None, str]:
        self.cin = cin
        return Ok(None)

    def eval(self) -> Result[tuple[int, int], str]:

        sout = []
        cout = 0

        for (index, alu) in enumerate(self.alus):

            a = (self.a << index) & 1
            b = 0
            c = 0

            alu.set_a(a)
            alu.set_b(b)
            alu.set_cin(c)
            r_eval = alu.eval()
            if r_eval.is_err:
                return trace("failed to evaluate ALU", r_eval.unwrap_err())
            
            (sn, cn) = r_eval.unwrap()
            sout.append(sn)
        
        cout = cn

        # Convert the binary numbers to a single number
        n = sum(d << i for (i, d) in enumerate(sout))

        return Ok(n, cout)

if __name__ == "__main__":

    a = 1
    b = 1
    cin = 0

    alun = ALU2(OperationType.ADD, a, b, cin)


    r = alun.eval()
    if r.is_err:
        print(f"failed to evaluate: {r.unwrap_err()}")
        exit()
    
    (s, c) = r.unwrap()

    print(f"{a} + {b} ({cin}) = {s} ({c})")

##################
    # a = 1
    # b = 1
    # c = 0
    # d = 0
    # e = 1

    # answer = []

    # # Perform one addition
    # alu1 = ALU(OperationType.ADD, a, b, c)
    # (s1, c1) = alu1.eval().unwrap()
    # answer.append(s1)

    # # Perform the second addition
    # alu2 = ALU(OperationType.ADD, d, e, c1)
    # (s2, c2) = alu1.eval().unwrap()
    # answer.append(s2)

    # answer.append(c2)

    # n = sum(d << i for (i, d) in enumerate(answer))

    # print(f"{a} + {b} ({c}) = ({s1}, {c1})")
    # print(f"{d} + {e} ({c1}) = ({s2}, {c2})")
    # print(n)