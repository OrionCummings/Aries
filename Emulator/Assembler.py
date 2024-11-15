from re import search
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
    if not IsValidOpcode(PotentialOpcode):
        return Err("Unknown opcode '{}'".format(PotentialOpcode))
    
    OpcodeTuple = OPCODES[PotentialOpcode]
    Opcode = OpcodeTuple[0]
    NumArgs = OpcodeTuple[1]
    Mode = OpcodeTuple[2]
    
    # Check that the number of expected arguments matches
    # the number of actual arguments.
    if len(LineVector) == NumArgs:
        return Err("Expected number of arguments ({}) does not match the actual number of arguments ({})!".format(NumArgs, len(LineVector)))

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
            
        case InstructionMode.Simple:
            pass # Do nothing; opcode already captured
    
    return Ok(Instruction)

def Decode(Instruction: int) -> Result[(str, str, str, str, int), str]:
    print("Instruction decoding is not a priority and has not been implemented yet!")
    exit(-4)
    pass

class Assembler():
    
    def __init__(Self, FileName: str, TestFile: bool = True) -> None:
        """Assembles an Aires program from an Aries assembly (.aria) file ."""
        
        # Directory containing all test programs
        Self.ProgramDirectory = "Programs"
        
        # The name of the Aires assembly file (.aria) 
        Self.FileName: str = FileName
        
        # The raw .aria file contents
        Self.FileContents: List[str] = []
        
        # The contents of the file as a list of integers
        Self.Instructions: List[int] = []
        
        # The current line in the .aria file
        Self.CurrentLine: int = 0
        
        # Read the file into FileContents
        Self.Read().unwrap_or_else(lambda E: PExit(E))
        
        print()
        print("Read file '{}' into assembler buffer".format(FileName))
        
        # Assemble the file
        RInstructions = Self.Assemble(TestFile)
        if RInstructions.is_err:
            print()
            if TestFile: print("Failed to assemble file '{}' as a test file!".format(FileName))
            else:        print("Failed to assemble file '{}'!".format(FileName))
            print()
            print(RInstructions.Err)
        
        Self.Instructions = RInstructions.unwrap()
            
        print()
        print("Assembled file '{}'".format(FileName))
        print()
        
        # Update metadata post assembly
        Self.UpdateMetadata()
        
        print(Self)
        
    def __str__(Self) -> str:
        Builder: str = ""
        Builder += "\n[" + Self.FileName + " - " + str(Self.Size) + " Bytes]\n"
        if len(Self.Instructions) < 1:
            Builder = "No File Contents"
        else:
            Index = 0
            for Instruction in Self.Instructions:
                
                if Index != 0 and Index % 1 == 0:
                    Builder += "\n"
                
                InstructionBinary: str = format(Instruction, "032b")
                Builder += " ".join([InstructionBinary[i:i+8] for i in range(0, len(InstructionBinary), 8)])
                Builder += " "
                
                Index += 1
        return Builder
    
    def UpdateMetadata(Self):
        """Updates assembler metadata after a successful assembly."""
        
        # BUG: Magic number!
        # Program size in bytes
        Self.Size = len(Self.Instructions * 4)
        
        # Other metadata
        # ...
    
    def Assemble(Self, TestFile: bool = False) -> Result[List[int], str]:
        """Assembles the santized file into Aries machine code. Accepts a 
        boolean value to determine if the given file should be interpreted
        as a test file. Test files contain additional information such as
        manually compiled machine code prefixed by ':' that will be tested
        against the actual resulting machine code. An error will be thrown
        if these two do not match.
        """
        
        if len(Self.FileContents) == 0:
            return Ok(True)
        
        Instructions: List[int] = []
        TestInstructions: List[int] = []
        
        # For every line of assembly code
        for Line in Self.FileContents:
            
            # Parse the instruction
            if RInstruction := Encode(Line):
                
                # If parsing fails, propagate the error
                if RInstruction.is_err: return Err(RInstruction.Err)
                
                # Append the machine code instruction to the program
                Instructions.append(RInstruction.unwrap())
            
            # Check if the first non-whitespace character is a colon; if so,
            # this is a test file!
            # TODO: Could use decode here to add an additional check
            elif Line.strip()[0] == ':':
                
                InstructionStr = "".join(Line.split())
                InstructionStr = InstructionStr.replace(":", "")

                Instruction: int = int(InstructionStr, 2)

                TestInstructions.append(Instruction)
            
            else:
                PExit("Invalid instruction '{}'".format(Line))
        
        # If this is a test file, then compare the assembled
        # instructions and the test instructions
        if TestFile:
            if len(TestInstructions) != len(Instructions):
                return Err("Test instructions and assembled instructions differ in size ({} != {})".format(len(TestInstructions), len(Instructions)))
        
            for Index in range(0, len(TestInstructions)):
                if TestInstructions[Index] != Instructions[Index]:
                    return Err("Test instructions and assembled instructions differ at index {} ({} != {})".format(Index, format(TestInstructions[Index], "032b"), format(Instructions[Index], "032b")))
        
        return Ok(Instructions)
    
    def Read(Self, TestFile: bool = False) -> Result[bool, str]:
        """Reads the file into an internal buffer."""
        
        FullFileName = Self.ProgramDirectory + "/" + Self.FileName
        
        try:
            with open(FullFileName, "r") as File:
                while Line := File.readline():
                    
                    # BUG: Stripping out comments is good! But we lose
                    # line number information using this method!!!!!
                    # Error messages will never be good!!!!!!!!!!
                    # Idea: just stop adding to the FileContents
                    # if a comment character is found! Then, the index
                    # into the FileContents list will map to the line
                    # number of the source file!!!!!!!!!!!
                    Content = Line.partition(ASM_COMMENT_CHARACTER)[0].strip()
                    if Content != "":
                        Self.FileContents.append(Content)
        except FileNotFoundError:
            return Err("File '" + FullFileName + "' not found! Unable to parse program.")
        #except: 
        #    return Err("Unknown exception! Unable to parse program.")
        return Ok(True)

if __name__ == "__main__":
    
    A: Assembler = Assembler("Registers.aria", False)
    print()
