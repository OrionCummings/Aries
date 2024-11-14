from enum import Enum
from typing import List
from option import Err, Ok, Result
from Constants import ADDR_LENGTH, ASM_COMMENT_CHARACTER, IMM_LENGTH, INS_LENGTH, OP_LENGTH, OPCODES, REG_LENGTH, REGISTERS, InstructionMode, IsValidOpcode, PExit

def GetOpcode(Line: str) -> Result[int, str]:
    if Line is not None:
        Opcode = Line.split(' ')[0]
        if Opcode in OPCODES:
            return Ok(OPCODES[Opcode])
    return Err("Line '{}' does not contain a valid opcode!")

class ParseMode(Enum):
    Register = 0,
    ImmediateValue = 1,
    Address = 2,

def ParseArgument(Arg: str, Type: ParseMode = ParseMode.Register) -> Result[int, str]:
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

def Encode(OpcodeStr: str, Arg1Str: str = '0', Arg2Str: str = '0', Arg3Str: str = '0') -> Result[int, str]:
    
    if OpcodeStr not in OPCODES:
        return Err("Invalid opcode '{}'!".format(OpcodeStr))
    
    OpcodeInformation = OPCODES[OpcodeStr]
    Opcode = OpcodeInformation[0]
    Mode = OpcodeInformation[2]
    
    Instruction: int = 0
    Instruction |= Opcode << (INS_LENGTH - OP_LENGTH)
    
    match Mode:
        case InstructionMode.Register:
            
            RRegA = ParseArgument(Arg1Str, ParseMode.Register)
            if RRegA.is_err: return RRegA.Err()
            else: RegA = RRegA.unwrap()
            
            RRegB = ParseArgument(Arg2Str, ParseMode.Register)
            if RRegB.is_err: return RRegB.Err()
            else: RegB = RRegB.unwrap()
            
            RRegC = ParseArgument(Arg3Str, ParseMode.Register)
            if RRegC.is_err: return RRegC.Err()
            else: RegC = RRegC.unwrap()
            
            Instruction |= RegA << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 1))
            Instruction |= RegB << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 2))
            Instruction |= RegC << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 3))
            # TODO: SHAMT and FUNC are not implemented yet
            
        case InstructionMode.Immediate:
            
            RRegA = ParseArgument(Arg1Str, ParseMode.Register)
            if RRegA.is_err: return RRegA.Err()
            else: RegA = RRegA.unwrap()
            
            RValue = ParseArgument(Arg2Str, ParseMode.ImmediateValue)
            if RValue.is_err: return RValue.Err()
            else: Value = RValue.unwrap()
            
            Instruction |= RegA << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 1))
            Instruction |= Value
            
        case InstructionMode.Jump:
            
            Address = 0
            
            RAddress = ParseArgument(Arg3Str, ParseMode.Address)
            if RAddress.is_err: return RAddress.Err()
            else: Address = RAddress.unwrap()
            
            Instruction |= Address
    
    return Ok(Instruction)

def Decode(Instruction: int) -> Result[(str, str, str, str, int), str]:
    print("this no worko, bucko")
    exit(-4)
    pass

class Assembler():
    
    def __init__(Self, FileName: str) -> None:
        """Assembles an Aires program from an Aries assembly (.aria) file ."""
        
        # Directory containing all test programs
        Self.ProgramDirectory = "Programs"
        
        # The name of the Aires assembly file (.aria) 
        Self.FileName: str = FileName
        
        # The raw .aria file contents
        Self.FileContents: List[str] = []
        
        # The contents of the file as bytes
        Self.Bytes: bytearray = bytearray()
        
        # The current line in the .aria file
        Self.CurrentLine: int = 0
        
        # Read the file into FileContents
        Self.Read().unwrap_or_else(lambda E: PExit(E))
        
        print("Read file '{}' into assembler buffer.".format(FileName))
        
        # Assemble the file
        Self.Assemble().unwrap_or_else(lambda E: PExit(E))
            
        print("Assembled file '{}' into Aires Machine Code.".format(FileName))
        
        # Update metadata post assembly
        Self.UpdateMetadata()
        
        print(Self)
        
    def __str__(Self) -> str:
        Builder: str = ""
        Builder += "\n[" + Self.FileName + " - " + str(Self.Size) + " Bytes]\n"
        if len(Self.Bytes) < 1:
            Builder = "No File Contents"
        else:
            for Byte in Self.Bytes:
                Builder += str(Byte)
        return Builder
    
    def UpdateMetadata(Self):
        """Updates assembler metadata after a successful assembly."""
        
        # Program size in bytes
        Self.Size = len(Self.Bytes)
        
        # Other metadata
        # ...
    
    def ParseInstruction(Self, Line: List[str]) -> Result[int, str]:
        
        # Get the potential opcode
        PotentialOpcode = str(Line[0])
        
        # Check that it's a valid opcode
        if IsValidOpcode(PotentialOpcode):
            OpcodeTuple = OPCODES[PotentialOpcode]
        else:
            return Err("Unknown opcode '{}' on line {}.".format(PotentialOpcode, "???"))
        
        # Unpack the opcode tuple
        Opcode, Argc = OpcodeTuple
        
        # TEMP
        Arg1, Arg2, Arg3 = 0
        
        match Argc:
            case 0: return Encode(Opcode)
            case 1: return Encode(Opcode, Arg1)
            case 2: return Encode(Opcode, Arg1, Arg2)
            case 3: return Encode(Opcode, Arg1, Arg2, Arg3)
        
    def Assemble(Self) -> Result[bool, str]:
        """Assembles the santized file into Aries machine code."""
        
        if len(Self.FileContents) == 0:
            return Ok(True)
        
        # For every line of assembly code
        for Line in Self.FileContents:
            
            # Parse the instruction
            if Instruction := Self.ParseInstruction(Line.split(' ')):
                
                # Append the machine code instruction to the program
                Self.Bytes.append(Instruction)
            
            else:
                PExit("Invalid instruction '{}' on line {}".format(Line, '???'))
            
            # Create the full instruction
            
            print()
        
        return Ok(True)
    
    def Read(Self) -> Result[bool, str]:
        """Reads the file into an internal buffer."""
        
        FullFileName = Self.ProgramDirectory + "/" + Self.FileName
        
        try:
            with open(FullFileName, "r") as File:
                while Line := File.readline():
                    Content = Line.partition(ASM_COMMENT_CHARACTER)[0].strip()
                    if Content != "":
                        Self.FileContents.append(Content)
        except FileNotFoundError:
            return Err("File '" + FullFileName + "' not found! Unable to parse program.")
        #except: 
        #    return Err("Unknown exception! Unable to parse program.")
        return Ok(True)

if __name__ == "__main__":
    
    A: Assembler = Assembler("Example.aria")
    print()
