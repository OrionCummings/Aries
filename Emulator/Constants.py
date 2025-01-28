from enum import Enum
from bidict import bidict
from BitManipulation import bit_mask

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
class InstructionFormat(Enum):
    Simple = 0,
    Register = 1,
    Immediate = 2,
    Jump = 3,

# All valid opcodes and their information tuple (ID, ARGC, FORMAT, ALU?)
# NOTE: ID is added later! This dict contains (ARGC, FORMAT, ALU?)
CONSTANT_OPCODE_MAP = {
    "nop":  (0, InstructionFormat.Simple, False),
    "ret":  (0, InstructionFormat.Simple, False),
    "hlt":  (0, InstructionFormat.Simple, False),
    "add":  (3, InstructionFormat.Register, True),
    "addi": (2, InstructionFormat.Immediate, True),
    "ldi":  (2, InstructionFormat.Immediate, True),
    "str":  (2, InstructionFormat.Immediate, True),
    "ld":   (2, InstructionFormat.Immediate, True),
    "bne":  (1, InstructionFormat.Jump, False),
    "j":    (1, InstructionFormat.Jump, False),
    "call": (1, InstructionFormat.Jump, False),
    "cmp":  (2, InstructionFormat.Register, False),
}

# Starting at 1, assign sequential IDs to each opcode in the order
# defined above. Leave zero open as an invalid opcode.
for index in range(0, len(CONSTANT_OPCODE_MAP)):
    (argc, mode, alu) = list(CONSTANT_OPCODE_MAP.values())[index]
    key = list(CONSTANT_OPCODE_MAP.keys())[index]

    # Add 1 to the index to avoid the zero opcode
    CONSTANT_OPCODE_MAP[key] = (index+1, argc, mode, alu)

# This is a dictionary containing all 16 registers.
CONSTANT_REGISTER_MAP = bidict({
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
    "PC":   14, # Program counter
    "FL":   15  # Flags register
})

# Flag register bit positions
FL_ZERO              = 0 # Z
FL_CARRY             = 1 # C
FL_PARITY            = 2 # P
FL_SIGN              = 3 # S
FL_OVERFLOW          = 4 # O
FL_INTERRUPT         = 5 # I
FL_TRAP              = 6 # T
FL_HPC               = 7 # H

# Flag bit masks
FL_ZERO_MASK              = bit_mask(FL_ZERO)
FL_CARRY_MASK             = bit_mask(FL_CARRY)
FL_PARITY_MASK            = bit_mask(FL_PARITY)
FL_SIGN_MASK              = bit_mask(FL_SIGN)
FL_OVERFLOW_MASK          = bit_mask(FL_OVERFLOW)
FL_INTERRUPT_MASK         = bit_mask(FL_INTERRUPT)
FL_TRAP_MASK              = bit_mask(FL_TRAP)
FL_HPC_MASK               = bit_mask(FL_HPC)

# The values to increment pointer registers
PC_INC = 4
BP_INC = 1
SP_INC = 1

# The total CPU memory size
CPU_MEMORY_SIZE_IN_BYTES = 2 ** INS_LENGTH

# Instruction memory parameters
DEFAULT_INSTRUCTION_MEMORY_BASE_ADDRESS     = 0x10
DEFAULT_INSTRUCTION_MEMORY_SIZE_IN_BYTES    = 64

# Data memory parameters
DEFAULT_DATA_MEMORY_BASE_ADDRESS            = DEFAULT_INSTRUCTION_MEMORY_BASE_ADDRESS + DEFAULT_INSTRUCTION_MEMORY_SIZE_IN_BYTES
DEFAULT_DATA_MEMORY_SIZE_IN_BYTES           = 64

# Video memory parameters
DEFAULT_VIDEO_MEMORY_BASE_ADDRESS           = DEFAULT_DATA_MEMORY_BASE_ADDRESS + DEFAULT_DATA_MEMORY_SIZE_IN_BYTES
DEFAULT_VIDEO_MEMORY_SIZE_IN_BYTES          = 0

# Stack memory parameters
DEFAULT_STACK_MEMORY_BASE_ADDRESS           = DEFAULT_VIDEO_MEMORY_BASE_ADDRESS + DEFAULT_VIDEO_MEMORY_SIZE_IN_BYTES
DEFAULT_STACK_MEMORY_SIZE_IN_BYTES          = 64

# Error codes
EC_ASSEMBLER_FAILURE = 0x20
EC_PC_OVERRUN        = 0x30

# TODO: Tidy this idea up!
class TextRenderTarget(Enum):
    Terminal = 0,
    Widget = 1,

