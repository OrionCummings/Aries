
def PExit(S: str, E: int = 0):
    """A function to print an error message and exit the assembler."""
    print(S)
    exit(E)

def BitMask(Index: int) -> int:
    """Returns a 1-bit mask at the specified `Index`."""
    return (1 << Index)

def SetBit(Number: int, Index: int) -> int:
    """Sets bit `Index` in number `Number`."""
    return Number | BitMask(Index)

def GetBit(Number: int, Index: int) -> bool:
    """Gets bit `Index` in number `Number`."""
    return not not (Number & BitMask(Index))

def ToggleBit(Number: int, Index: int) -> int:
    """Toggles bit `Index` in number `Number`."""
    return (Number ^ (1 << (Index)))

################################################################################################################

# This is the character which should be interpreted as a comment in assembly
ASM_COMMENT_CHARACTER = ';'

# All valid opcodes
OPCODES = {
    "nop":       0,
    "hlt":       1,
    "add":       2,
    "addi":      3,
    "subi":      4,
    "sub":       5,
    "not":       6,
    "and":       7,
    "nand":      8,
    "or":        9,
    "nor":      10,
    "xor":      11,
    "xnor":     12,
    "shl":      13,
    "shr":      14,
    "ldi":      15,
    "sti":      16,
    "ldr":      17,
    "str":      18,
    "jmp":      19,
    "ret":      20,
    "hpe":      21,
    "hpd":      22,
    "syscall":  23,
}

# This is a dictionary containing all 16 16-bit registers.
REGISTERS = {
    "A":    0,
    "B":    1,
    "C":    2,
    "D":    3,
    "E":    4,
    "F":    5,
    "G":    6,
    "H":    7,
    "I":    8,
    "J":    9,
    "K":    10,
    "L":    11,
    "SP":   12, # Stack pointer
    "BP":   13, # Base pointer
    "IP":   14, # Instruction pointer
    "FL":   15  # Flags register
}

# Flag register bit positions
FL_ZERO              = 0 # Z
FL_CARRY             = 1 # C
FL_PARITY            = 2 # P
FL_SIGN              = 3 # S
FL_OVERFLOW          = 4 # O
FL_INTERRUPT         = 5 # I
FL_INTERRUPT_DISABLE = 6 # D
FL_TRAP              = 7 # T
FL_HPC               = 8 # H

# Flag bit masks
FL_ZERO_MASK              = BitMask(FL_ZERO)
FL_CARRY_MASK             = BitMask(FL_CARRY)
FL_PARITY_MASK            = BitMask(FL_PARITY)
FL_SIGN_MASK              = BitMask(FL_SIGN)
FL_OVERFLOW_MASK          = BitMask(FL_OVERFLOW)
FL_INTERRUPT_MASK         = BitMask(FL_INTERRUPT)
FL_INTERRUPT_DISABLE_MASK = BitMask(FL_INTERRUPT_DISABLE)
FL_TRAP_MASK              = BitMask(FL_TRAP)
FL_HPC_MASK               = BitMask(FL_HPC)

# The values to increment pointer registers
IP_INC = 1
BP_INC = 1
SP_INC = 1