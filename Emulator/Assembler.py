from typing import List

from option import Err, Ok, Result

from Constants import ASM_COMMENT_CHARACTER, OPCODES, PExit


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
    
    def ParseInstruction(Self, Line) -> Result[int, str]:
        PotentialOpcode = str(Line[0])
            
        if PotentialOpcode in OPCODES:
            Opcode = str(OPCODES[PotentialOpcode])
        else:
            return Err("Unknown opcode '{}' on line {}.".format(PotentialOpcode, "???")) 
        
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
            #Instruction = 
            
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
    
    A: Assembler = Assembler("Simple.aria")
    print()
