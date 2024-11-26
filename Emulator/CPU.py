from option import Err, Ok, Result
from Constants import ADDR_LENGTH, FF_LENGTH, FUNC_LENGTH, IMM_LENGTH, INS_LENGTH, OP_LENGTH, OPCODES, PC_OVERRUN, REG_LENGTH, REGISTERS, SHAMT_LENGTH, InstructionMode, PExit
from ProgramCounter import ProgramCounter
from RegisterFile import RegisterFile
from Memory import Memory
from Flags import Flags
from PrettyPrinting import PP, ParseMode, PrintMode
from CallStack import CallStack

class CPU():
    """A CPU implementing the Simple Aries Instruction Set Architecture."""
    
    def __init__(Self, InstructionMemorySize: int = 4096, DataMemorySize: int = 4096) -> None:
        """Initializes a CPU instance with a given memory size in bytes."""
        
        # The essential parts a Harvard CPU
        Self.ProgramCounter          = ProgramCounter()
        Self.RegisterFile            = RegisterFile()
        Self.InstructionMemory       = Memory(InstructionMemorySize)
        Self.DataMemory              = Memory(DataMemorySize)
        Self.CallStack               = CallStack()
        Self.Flags                   = Flags()

        # Auxilary metadata
        Self.Halt: bool              = False
        Self.LastUpdatedAddress: int = None
        Self.HPCBus: int             = 0

    def __str__(Self) -> str:
        
        # Begin the string builder by including the program counter
        Builder: str = "PC: " + str(Self.ProgramCounter)
        
        # TODO: Add some kind of 'CPU settings' similar to the assembler settings
        # to control things like the output format of this function.
        for Index in range(Self.InstructionMemory.Capacity):
            
            # If it's a 8 byte boundary, print some formatting
            if Index == 0 or Index % 8 == 0:
                Builder += "\n"
                Builder += str(Index)
                Builder += ":\t"
            
            # # Insert a space between each byte
            # Builder += " "
            
            # Get the full hex literal of the instruction
            Instruction = Self.InstructionMemory[Index]
            Hex = format(Instruction, "08X")
            HexList = [Hex[0:2], Hex[2:4], Hex[4:6], Hex[6:8]]
            
            x=1 # DEBUG LINE
            
            for Hex in HexList:
                
                # Insert a space between each byte
                Builder += " "
                
                if Index == Self.ProgramCounter: # Highlight the current instruction in bold red
                    Builder += PP.RedBold(Hex)
                elif Index == Self.LastUpdatedAddress: # Highlight the last recently updated address in bold green
                    Builder += PP.GreenBold(Hex)
                else: # Otherwise, just add the instruction data to the builder
                    Builder += Hex
            

            
        return Builder
    
    def Print(Self):
        print(str(Self))
    
    def LoadProgram(Self, Program: list[int], ProgramName: str, BaseAddress: int = 0) -> Result[bool, str]:
        """Loads a program into memory at the given address."""
        
        if BaseAddress >= Self.InstructionMemory.Capacity:
            print("Base address '{}' exceeds the instruction memory address space of {}!".format(BaseAddress, Self.InstructionMemory.Size))
            exit(2)
            #return Err("Base address '{}' exceeds the instruction memory address space of {}!".format(BaseAddress, Self.InstructionMemory.Size))
        
        if len(Program) == 0: print("WARNING: Loading null program.")
        
        RUpdate = Self.InstructionMemory.UpdateChunk(Program, BaseAddress)
        if RUpdate.is_err: return Err(RUpdate.unwrap_err())
        
        print("Loaded '{}' starting at address {} ({:0X})".format(ProgramName, BaseAddress, BaseAddress))
        return Ok(True)
    
    def GetCurrentInstruction(Self):
        """Returns the current instruction."""
        
        # TODO: Make this call safer!
        return Self.InstructionMemory.Memory[Self.ProgramCounter.Value]
    
    def Tick(Self) -> Result[int, str]:
        """Executes the current instruction and returns the address that was changed."""
        
        Address = None
        CurrentInstruction = Self.GetCurrentInstruction()
        
        ROpcode = GetOpcode(CurrentInstruction)
        if ROpcode.is_err: return Err(ROpcode.unwrap_err())
        OpcodeTuple = ROpcode.unwrap()
        
        OpcodeID = OpcodeTuple[0]
        OpcodeFunction = INSTRUCTIONS[OpcodeID]
        Self = OpcodeFunction(Self, CurrentInstruction)
        
        # TODO: Fix this (optional) feature!
        return Address
    
    def Clock(Self) -> bool:
        """Perform one clock cycle."""

        # If the CPU has been halted, then don't do anything!
        if Self.Halt: return False

        # Execute the instruction
        Self.Tick()
        
        # TODO: This only triggers when we go out of bounds (which is good!), but
        # it is possible to interact with uninitialized memory (index > size).
        # It may be a good idea to raise a warning of some kind, but there is no
        # such mechanism at the moment. 
        # Increment the program counter
        if Self.ProgramCounter.Value >= Self.InstructionMemory.Capacity - 1: PExit("Program counter overrun!", PC_OVERRUN)
            
        Self.ProgramCounter.Increment()
        
        return True

def IsValidOpcode(Opcode: str) -> bool:
    return Opcode in OPCODES

def GetOpcode(Line: str | int) -> Result[tuple, str]:
    
    # If it's a string, the this call is likely parsing
    # an input file (i.e. Encode()).
    if isinstance(Line, str):
        if Line is not None:
            OpcodeStr = Line.split(' ')[0]
            if OpcodeStr in OPCODES:
                return Ok(OPCODES[OpcodeStr])
            
    # If it's an int, then this call is likely decoding
    # a previously parsed instruction (i.e. Decode())
    elif isinstance(Line, int):
        if Line is not None:
            OpcodeInt = (Line & 0xFC000000) >> (INS_LENGTH - OP_LENGTH) # TODO: Magic number!
            
            for OpcodeTuple in OPCODES.values():# TODO: This is pretty stinky
                if OpcodeInt == OpcodeTuple[0]:
                    return Ok(OpcodeTuple)
    else:
        return Err("Invalid type passed to GetOpcode(Line: str | int)!")
    
    return Err("Line '{}' does not contain a valid opcode!")

def OpcodeToInt(Opcode: str) -> Result[int, str]:
    """Converts the given opcode (as a string) to an integer."""
    try:
        OpcodeInt: int = int(Opcode)
    except (TypeError, ValueError):
        return Err("Failed to convert '{}' to a number".format(Opcode))
    return Ok(OpcodeInt)

def InstructionString(Instruction: int, PMode: PrintMode) -> Result[str, str]:
    Builder: str = ""
    
    ROpcode = GetOpcode(Instruction)
    if ROpcode.is_err: return Err(ROpcode.Err())
    Opcode = ROpcode.unwrap()
    IMode: InstructionMode = Opcode[2]
    
    # Convert the intruction to a binary string
    InstructionStr: str = format(Instruction, "032b")
    
    match PMode:
        
        case PrintMode.NoOutput:
            pass
        
        case PrintMode.Binary:
            Builder += InstructionStr
        
        case PrintMode.Bytes: # TODO: Magic numbers (but I think they are justified here)!
            Byte0 = InstructionStr[0:8]
            Byte1 = InstructionStr[8:16]
            Byte2 = InstructionStr[16:24]
            Byte3 = InstructionStr[24:32]
            Builder += " ".join([Byte0, Byte1, Byte2, Byte3])
            
        case PrintMode.Hex:
            Byte0 = "{:X}".format(int(InstructionStr[0 : 4], 2))
            Byte1 = "{:X}".format(int(InstructionStr[4 : 8], 2))
            Byte2 = "{:X}".format(int(InstructionStr[8 :12], 2))
            Byte3 = "{:X}".format(int(InstructionStr[12:16], 2))
            Byte4 = "{:X}".format(int(InstructionStr[16:20], 2))
            Byte5 = "{:X}".format(int(InstructionStr[20:24], 2))
            Byte6 = "{:X}".format(int(InstructionStr[24:28], 2))
            Byte7 = "{:X}".format(int(InstructionStr[28:32], 2))
            Builder += "".join([Byte0, Byte1, Byte2, Byte3, Byte4, Byte5, Byte6, Byte7])
        
        case PrintMode.Instructions:
            match IMode:
                case InstructionMode.Register:
                    Opcode  = InstructionStr[:OP_LENGTH]
                    RegA    = InstructionStr[OP_LENGTH : OP_LENGTH + (1 * REG_LENGTH)]
                    RegB    = InstructionStr[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
                    RegC    = InstructionStr[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH)]
                    Shamt   = InstructionStr[OP_LENGTH + (3 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH) + SHAMT_LENGTH]
                    Func    = InstructionStr[-FUNC_LENGTH:]
                    Builder += " ".join([Opcode, RegA, RegB, RegC, Shamt, Func])
                    
                case InstructionMode.Immediate:
                    Opcode  = InstructionStr[:OP_LENGTH]
                    RegA    = InstructionStr[OP_LENGTH : OP_LENGTH + REG_LENGTH]
                    RegB    = InstructionStr[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
                    Unk     = InstructionStr[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH) + FF_LENGTH]
                    Value   = InstructionStr[-IMM_LENGTH:]
                    Builder += " ".join([Opcode, RegA, RegB, Unk, Value])
                    
                case InstructionMode.Jump:
                    Opcode  = InstructionStr[:OP_LENGTH]
                    Address = InstructionStr[OP_LENGTH:]
                    Builder += " ".join([Opcode, Address])
    
    return Ok(Builder)

def ParseArgument(Arg: str, Type: ParseMode) -> Result[int, str]:
    """Parses a given argument as either a register value, immediate value, or an address."""
    
    Ret = 0
    
    match Type:
        case ParseMode.Register:
            
            if Arg.isdigit():
                Ret = int(Arg)
                if Ret < 0:
                    return Err("Invalid register '{}' (cannot be negative)!".format(Ret))
                elif Ret >= 2 ** REG_LENGTH:
                    return Err("Invalid register '{}' (cannot be greater or equal to {})!".format(Ret, 2 ** REG_LENGTH))
            elif Arg in REGISTERS:
                Ret = REGISTERS[Arg]
            else:
                return Err("Invalid non-numeric argument '{}'!".format(Arg))
            
        case ParseMode.ImmediateValue:
            
            if Arg.isdigit():
                Ret = int(Arg)
                if Ret < 0: return Err("Invalid immediate value '{}' (cannot be negative)!".format(Ret))
                elif Ret >= 2 ** IMM_LENGTH: return Err("Invalid immediate value '{}' (cannot be greater or equal to {})!".format(Ret, 2 ** IMM_LENGTH))
            elif len(Arg) >= 2 and Arg[0:2] == '0x':
                Ret = int(Arg, 16)
                if Ret < 0: return Err("Invalid immediate value '{}' (cannot be negative)!".format(Ret))
                elif Ret >= 2 ** IMM_LENGTH: return Err("Invalid immediate value '{}' (cannot be greater or equal to {})!".format(Ret, 2 ** IMM_LENGTH))
            elif len(Arg) >= 2 and Arg[0:2] == '0o':
                Ret = int(Arg, 8)
                if Ret < 0: return Err("Invalid immediate value '{}' (cannot be negative)!".format(Ret))
                elif Ret >= 2 ** IMM_LENGTH: return Err("Invalid immediate value '{}' (cannot be greater or equal to {})!".format(Ret, 2 ** IMM_LENGTH))
            elif len(Arg) >= 2 and Arg[0:2] == '0b':
                Ret = int(Arg, 2)
                if Ret < 0: return Err("Invalid immediate value '{}' (cannot be negative)!".format(Ret))
                elif Ret >= 2 ** IMM_LENGTH: return Err("Invalid immediate value '{}' (cannot be greater or equal to {})!".format(Ret, 2 ** IMM_LENGTH))
            else: return Err("Invalid non-numeric argument '{}'!".format(Arg))
            
        case ParseMode.Address:
            
            if Arg.isdigit():
                Address = int(Arg)
                if Address < 0: return Err("Invalid address '{}' (cannot be negative)!".format(Ret))
                elif Address >= 2 ** ADDR_LENGTH: return Err("Invalid address '{}' (cannot be greater or equal to {})!".format(Ret, 2 ** ADDR_LENGTH))
            else: return Err("Invalid non-numeric argument '{}'!".format(Arg))
    
    return Ok(Ret)

def Encode(Line: str) -> Result[int, str]:
    
    # Create the line vector
    LineVector = Line.split(' ')
    if len(LineVector) < 1: return Err("Malformed instruction '{}' (likely an empty line)".format(Line))
    if len(LineVector) > 4: return Err("Malformed instruction '{}' (too many arguments)".format(Line))
    
    # Get the potential opcode
    PotentialOpcode = LineVector[0]
    
    # Check that it's a valid opcode
    if not IsValidOpcode(PotentialOpcode): return Err("Unknown opcode '{}'".format(PotentialOpcode))
    
    OpcodeTuple = OPCODES[PotentialOpcode]
    Opcode = OpcodeTuple[0]
    NumArgs = OpcodeTuple[1]
    Mode = OpcodeTuple[2]
    
    # Check that the number of expected arguments matches
    # the number of actual arguments.
    if len(LineVector) == NumArgs: return Err("Expected number of arguments ({}) does not match the actual number of arguments ({})!".format(NumArgs, len(LineVector)))

    Instruction: int = 0
    Instruction |= Opcode << (INS_LENGTH - OP_LENGTH)
    
    match Mode:
        
        # TODO: ParseArgument also has a match on instruction mode. Consider refactoring! 
        
        case InstructionMode.Register:
            
            RegA, RegB, RegC = (0, 0, 0)
            
            if NumArgs > 0:
                RRegA = ParseArgument(LineVector[1], ParseMode.Register)
                if RRegA.is_err: return RRegA.Err()
                else: RegA = RRegA.unwrap()
            
            if NumArgs > 1:
                RRegB = ParseArgument(LineVector[2], ParseMode.Register)
                if RRegB.is_err: return RRegB.Err()
                else: RegB = RRegB.unwrap()
            
            if NumArgs > 2:
                RRegC = ParseArgument(LineVector[3], ParseMode.Register)
                if RRegC.is_err: return RRegC.Err()
                else: RegC = RRegC.unwrap()
            
            Instruction |= RegA << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 1))
            Instruction |= RegB << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 2))
            Instruction |= RegC << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 3))
            
            # TODO: SHAMT and FUNC are not implemented yet
            
        case InstructionMode.Immediate:
            
            Reg = 0
            
            if NumArgs > 0:
                RValue = ParseArgument(LineVector[1], ParseMode.ImmediateValue)
                if RValue.is_err: return RValue.Err()
                else: Value = RValue.unwrap()
            
            if NumArgs > 1:
                RReg = ParseArgument(LineVector[2], ParseMode.Register)
                if RReg.is_err: return RReg.Err()
                else: Reg = RReg.unwrap()
            
            Instruction |= Reg << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 1))
            Instruction |= Value
            
        case InstructionMode.Jump:
            
            Address = 0
            
            if NumArgs > 0:
                RAddress = ParseArgument(LineVector[1], ParseMode.Address)
                if RAddress.is_err: return RAddress.Err()
                else: Address = RAddress.unwrap()
            
            Instruction |= Address
            
    return Ok(Instruction)

def Decode(Instruction: int) -> Result[(str, str, str, str, int), str]:
    print("Instruction decoding is not a priority and has not been implemented yet!")
    exit(-4)
    pass

def Extract(Instruction: int) -> Result[(InstructionMode, list), str]:
    
    ROpcode = GetOpcode(Instruction)
    if ROpcode.is_err: return Err(ROpcode.unwrap_err())
    OpcodeTuple = ROpcode.unwrap()
    Mode = OpcodeTuple[2]
    
    BinaryInstruction = format(Instruction, "032b")
    RetList = []
    
    match Mode:
        
        case InstructionMode.Register:
            Opcode  = BinaryInstruction[:OP_LENGTH]
            RegA    = BinaryInstruction[OP_LENGTH : OP_LENGTH + (1 * REG_LENGTH)]
            RegB    = BinaryInstruction[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
            RegC    = BinaryInstruction[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH)]
            Shamt   = BinaryInstruction[OP_LENGTH + (3 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH) + SHAMT_LENGTH]
            Func    = BinaryInstruction[-FUNC_LENGTH:]
            RetList = [Opcode, RegA, RegB, RegC, Shamt, Func]
            
        case InstructionMode.Immediate:
            Opcode  = BinaryInstruction[:OP_LENGTH]
            RegA    = BinaryInstruction[OP_LENGTH : OP_LENGTH + REG_LENGTH]
            RegB    = BinaryInstruction[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
            Unk     = BinaryInstruction[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH) + FF_LENGTH]
            Value   = BinaryInstruction[-IMM_LENGTH:]
            RetList = [Opcode, RegA, RegB, Unk, Value]
            
        case InstructionMode.Jump:
            Opcode  = BinaryInstruction[:OP_LENGTH]
            Address = BinaryInstruction[OP_LENGTH:]
            RetList = [Opcode, Address]
    
    return Ok((Mode, RetList))

def VerifyOpcode(Instruction: int, ExpectedOpcode: str) -> Result[bool, str]:
    ROpcode = GetOpcode(Instruction)
    if ROpcode.is_err: return Err(ROpcode.unwrap_err())
    ActualOpcode = ROpcode.unwrap()
    if not ActualOpcode == OPCODES[ExpectedOpcode][0]:
        return Err("Expected opcode '{}' does not match actual opcode '{}' from instruction {}".format(ExpectedOpcode, ActualOpcode, Instruction))
    return True
    
def NOP(CPU: CPU, Instruction: int) -> Result[CPU, str]:
    """Executes a 'nop' instruction."""
    
    InstructionMnemonic = 'nop'
    RVerification = VerifyOpcode(Instruction, InstructionMnemonic)
    if RVerification.is_err: return Err(RVerification.unwrap_err())

    return Ok(CPU)

def HLT(CPU: CPU, Instruction: int) -> Result[CPU, str]:
    """Executes a 'hlt' instruction."""
    
    InstructionMnemonic = 'hlt'
    RVerification = VerifyOpcode(Instruction, InstructionMnemonic)
    if RVerification.is_err: return Err(RVerification.unwrap_err())

    # Set the program counter to None and halt the CPU
    CPU.ProgramCounter = None
    CPU.Halt = True

    return Ok(CPU)

def ADD(CPU: CPU, Instruction: int) -> Result[CPU, str]:
    """Executes an 'add' instruction."""
    
    InstructionMnemonic = 'add'
    RVerification = VerifyOpcode(Instruction, InstructionMnemonic)
    if RVerification.is_err: return Err(RVerification.unwrap_err())

    # TODO: This code probably already exists in this project, so find and reuse it!
    # Or make it generic!

    OpcodeTuple = OPCODES[InstructionMnemonic]
    Mode = OpcodeTuple[2]

    if not Mode == InstructionMode.Register: return Err("Expected nemonic '{}' to be Register!".format(InstructionMnemonic))
    
    RExtraction = Extract(Instruction)
    if RExtraction.is_err: return Err(RExtraction.unwrap_err())
    Extraction = RExtraction.unwrap()
    
    x=1 # debug line


    return Ok(CPU)

def ADDI(CPU: CPU, Instruction: int) -> Result[CPU, str]:
    pass

def LDI(CPU: CPU, Instruction: int) -> Result[CPU, str]:
    pass

def PLACEHOLDER_INSTRUCTION_FUNCTION() -> Result[CPU, str]:
    return Err("Unimplemented instruction function called!")
    
INSTRUCTIONS = [
    NOP,    # 0
    HLT,    # 1
    ADD,    # 2
    ADDI,   # 3
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 4
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 5
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 6
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 7
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 8
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 9
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 10
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 11
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 12
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 13
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 14
    LDI,    # 15
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 16
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 17
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 18
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 19
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 20
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 21
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 22
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 23
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 24
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 25
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 26
]