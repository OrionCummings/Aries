
from enum import Enum

from option import Err, Ok, Result


def PExit(S: str, E: int = 0):
    """A function to print an error message and exit the assembler."""
    print(S)
    exit(E)

def IsValidOpcode(Opcode: str) -> bool:
    return Opcode in OPCODES

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

def OpcodeToInt(Opcode: str) -> Result[int, str]:
    """Converts the given opcode (as a string) to an integer."""
    try:
        OpcodeInt: int = int(Opcode)
    except (TypeError, ValueError):
        return Err("Failed to convert '{}' to a number".format(Opcode))
    return Ok(OpcodeInt)

def IsRegister(Reg: str) -> bool:
    return Reg in REGISTERS

########################################################################

# This is the character which should be interpreted as a comment in assembly
ASM_COMMENT_CHARACTER = ';'

# This is the character which should be interpreted as a test prefix in assembly
ASM_TEST_PREFIX_CHARACTER = ':'

# The length of full instructions in bits
INS_LENGTH = 32

# The length of opcode field in bits
OP_LENGTH = 6

# The length of register field in bits
REG_LENGTH = 4

# The length of immediate field in bits
IMM_LENGTH = 16

# The length of address field in bits
ADDR_LENGTH = 26

# The length of the (currently unused) future function field in bits
FF_LENGTH = 2

# The length of shift amount field in bits
SHAMT_LENGTH = 5

# The length of function field in bits
FUNC_LENGTH = 5

# Instruction modes determine the bit layout of the instruction
# 
# Simple
# OPCODE    [UNUSED]
# XXXXXX    XXXXXXXXXXXXXXXXXXXXXXXXXX
# 6         26
# 0-6       7-32
# 
# Register                        [UNUSED] [UNUSED]
# OPCODE    REGA    REGB    REGC    SHAMT   FUNC
# XXXXXX    XXXX    XXXX    XXXX    XXXXX   XXXXXXXXX
# 6         4       4       4       5       9
# 0-6       7-10    11-14   15-18   19-23   24-32
# 
# Immediate              [UNUSED]
# OPCODE    REGA    REGB    FF    VALUE
# XXXXXX    XXXX    XXXX    XX    XXXXXXXXXXXXXXXX
# 6         4       4       2     16
# 0-6       7-10    11-14   15-17 18-32
# 
# Jump
# OPCODE    ADDRESS
# XXXXXX    XXXXXXXXXXXXXXXXXXXXXXXXXX
# 6         26
# 0-6       7-32
# 
class InstructionMode(Enum):
    Register = 0
    Immediate = 1
    Jump = 2
    
# All valid opcodes and their information tuple (ID, ARGC, MODE, ALU?)
OPCODES = {
    "nop":      (0, 0, InstructionMode.Jump, False),
    "hlt":      (1, 0, InstructionMode.Jump, False),
    "add":      (2, 3, InstructionMode.Register, True),
    "addi":     (3, 2, InstructionMode.Immediate, True),
    # "sub":      (5, 3, InstructionMode.Register, True),
    # "subi":     (4, 2, InstructionMode.Immediate, True),
    # "not":      (6, 2, InstructionMode.Register, True),
    # "and":      (7, 3, InstructionMode.Register, True),
    # "nand":     (8, 3, InstructionMode.Register, True),
    # "or":       (9, 3, InstructionMode.Register, True),
    # "nor":     (10, 3, InstructionMode.Register, True),
    # "xor":     (11, 3, InstructionMode.Register, True),
    # "xnor":    (12, 3, InstructionMode.Register, True),
    # "shl":     (13, 2, InstructionMode.Register, True),
    # "shr":     (14, 2, InstructionMode.Register, True),
    "ldi":     (15, 2, InstructionMode.Immediate, True),    # TODO: May not use ALU
    # "lui":     (16, 2, InstructionMode.Immediate, True),  # TODO: May not use ALU
    # "lli":     (17, 2, InstructionMode.Immediate, True),  # TODO: May not use ALU
    # "ld":      (18, 2, InstructionMode.Register, True),   # TODO: May not use ALU
    # "sti":     (19, 2, InstructionMode.Immediate, False),
    # "str":     (20, 2, InstructionMode.Register, False),
    # "bne":     (21, 1, InstructionMode.Jump, False),
    # "jmp":     (22, 1, InstructionMode.Jump, False),
    # "jr":      (23, 1, InstructionMode.Jump, False),
    # "ret":     (24, 0, InstructionMode.Jump, False),
    # "hpc":     (25, 1, InstructionMode.Jump, False),
    # "syscall": (26, 1, InstructionMode.Register, False
    # ), # Bold move
}

# This is a dictionary containing all 16 registers.
# TODO: Could add indication of GPRs and SPRs
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

# The program counter increment value
PC_INC = 1

# Error codes
PC_OVERRUN = 0x30



