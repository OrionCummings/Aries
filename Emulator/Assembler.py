from dataclasses import dataclass
from enum import Enum
from typing import List
from option import Err, Ok, Result
from CPU import Encode, InstructionString
from Constants import ASM_COMMENT_CHARACTER, ASM_TEST_PREFIX_CHARACTER, PExit
from PrettyPrinting import PrintMode

@dataclass
class AssemblerSettings:
    SelfTest: bool = False
    PrintMode      = PrintMode.NoOutput

class Assembler():
    
    def __init__(Self, FileName: str, Settings: AssemblerSettings) -> None:
        """Assembles an Aires program from an Aries assembly (.aria) file."""
        
        # Assembler settings
        Self.Settings: AssemblerSettings = Settings
        
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
        print("Reading file '{}' into assembler buffer.".format(FileName))
        RReal: Result[bool, str] = Self.Read(Settings)
        if RReal.is_err:
            PExit(RReal.Err(), -4)
        print("Read file '{}' into assembler buffer.".format(FileName))
        
        if Settings.SelfTest: print("Assembling file '{}' with self tests enabled.".format(FileName))
        else:        print("Assembling file '{}' with self tests enabled.".format(FileName))
            
        # Assemble the file
        RInstructions = Self.Assemble(Settings)
        if RInstructions.is_err:
            if Settings.SelfTest: print("Failed to assemble file '{}' as a test file!".format(FileName))
            else:        print("Failed to assemble file '{}'!".format(FileName))
            print(RInstructions.Err)
        
        Self.Instructions = RInstructions.unwrap()
            
        if Settings.SelfTest: print("Assembled file '{}' with self tests enabled.".format(FileName))
        else:        print("Assembled file '{}'.".format(FileName))
        
        # Update metadata post assembly
        Self.UpdateMetadata()
        
        if Settings.PrintMode != PrintMode.NoOutput:
            print()
            print(Self)
        
    def __str__(Self) -> str:
        
        if Self.Settings.PrintMode == PrintMode.NoOutput:
            return ""
        
        Builder: str = ""
        Builder += "[" + Self.FileName + " - " + str(Self.Size) + " Bytes]\n"
        
        if len(Self.Instructions) < 1:
            Builder += "No File Contents"
            return Builder
        
        Index = 0
        for Instruction in Self.Instructions:
            
            if Index != 0 and Index % 1 == 0:
                Builder += "\n"

            RInstruction: Result[str, str] = InstructionString(Instruction, Self.Settings.PrintMode)
            if RInstruction.is_err:
                Builder += "Failed to convert instruction '{}': {}".format(format(Instruction, "032b"), RInstruction.unwrap_err()) # TODO: Inconsistent use of 'format()'
                return Builder
            
            Builder += RInstruction.unwrap()
            
            Index += 1
            
        return Builder
    
    def UpdateMetadata(Self):
        """Updates assembler metadata after a successful assembly."""
        
        # BUG: Magic number!
        # Program size in bytes
        Self.Size = len(Self.Instructions * 4)
        
        # Other metadata
        # ...
    
    def Assemble(Self, Settings: AssemblerSettings) -> Result[List[int], str]:
        """Assembles the santized file into Aries machine code. Accepts a 
        boolean value to determine if the given file should be interpreted
        as a test file. Test files contain additional information such as
        manually compiled machine code prefixed by ASM_TEST_PREFIX_CHARACTER
        that will be tested against the actual resulting machine code. An 
        error will be thrown if these two do not match.
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
            elif Line.strip()[0] == ASM_TEST_PREFIX_CHARACTER:
                
                InstructionStr = "".join(Line.split())
                InstructionStr = InstructionStr.replace(ASM_TEST_PREFIX_CHARACTER, "")

                Instruction: int = int(InstructionStr, 2)

                TestInstructions.append(Instruction)
            
            else:
                PExit("Invalid instruction '{}'".format(Line))
        
        # If this is a test file, then compare the assembled
        # instructions and the test instructions
        if Settings.SelfTest:
            if len(TestInstructions) != len(Instructions):
                return Err("Test instructions and assembled instructions differ in size ({} != {})".format(len(TestInstructions), len(Instructions)))
        
            for Index in range(0, len(TestInstructions)):
                if TestInstructions[Index] != Instructions[Index]:
                    return Err("Test instructions and assembled instructions differ at index {} ({} != {})".format(Index, format(TestInstructions[Index], "032b"), format(Instructions[Index], "032b")))
        
        return Ok(Instructions)
    
    def Read(Self, Settings: AssemblerSettings) -> Result[bool, str]:
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
        return Ok(True)

if __name__ == "__main__":
    
    Settings = AssemblerSettings()
    Settings.PrintMode = PrintMode.Bytes
    Settings.SelfTest = True
    
    A: Assembler = Assembler("Example.aria", Settings=Settings)
