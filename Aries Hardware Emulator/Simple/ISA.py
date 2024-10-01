from dataclasses import dataclass
from typing import List
from enum import Enum
import returns
from returns.result import Result, Success, Failure

class Instruction():
    
    def __init__(Self) -> None:
        Self.InstructionStr: str    = None
        Self.Arg1: str              = None
        Self.Arg2: str              = None
        Self.Arg3: str              = None
        
    def __str__(Self) -> str:
        Builder: str = "0x"
        Builder += "{:04X}".format(Self.InstructionType)
        try:
            if Self.Arg1 is not None:
                Builder += Self.Arg1
            else:
                Builder += "0000"

            if Self.Arg2 is not None:
                Builder += Self.Arg2
            else:
                Builder += "0000"

            if Self.Arg3 is not None:
                Builder += Self.Arg3
            else:
                Builder += "0000"
                
        except ValueError:
            print("Invalid argument: unable to convert to integer!")
            exit(1)
        return Builder
    
    def AsBytes(Self) -> List[int]:

        # Get the string version of the instruction
        S: str = str(Self)
        
        # Remove the hex prefix
        S = S[2:]
        
        # Split every two characters
        # TODO: Always allocate 8 spaces! Instructions are fixed-width
        BytesAsStrings: List[str] = []
        while S:
            BytesAsStrings.append(S[:2])
            S = S[2:]
            
        # Convert each stringified byte into an actual byte
        Bytes: List[int] = []
        [Bytes.append(int(B, 16)) for B in BytesAsStrings]

        return Bytes
    
    def SetType(Self, IType: int):
        Self.InstructionType = IType

class SAISA():
    
    def __init__(Self) -> None:
        Self.Instructions: List[Instruction] = []
        Self.InstructionMap = {
            "ADD":  (0x00, 3),
            "SUB":  (0x01, 3),
            "MOVE": (0x02, 2),
            "LOAD": (0x03, 2),
            "BNE":  (0x04, 3),
            "EXIT": (0x05, 1)
        }
    
    def IsValidOpcode(Self, Opcode: int) -> bool:
        
        
        
        pass
    
    def ParseInstruction(Self, Line: str) -> Result[Instruction, str]:
        I: Instruction = Instruction()

        # Parse the instruction symbol
        FirstSpaceIndex: int = Line.find(' ')
        Symbol: str = Line[:FirstSpaceIndex]
        
        # If the symbol is not valid, return a failure
        if not Symbol in Self.InstructionMap.keys():
            return Failure("Unknown opcode '{}'".format(Symbol))
        
        # Extract information regarding this instruction
        (IType, NumArguments) = Self.InstructionMap[Symbol]
        
        # Set the instruction type
        I.SetType(IType)
        
        # If we are expecting one argument
        if NumArguments == 1:
            NewLineIndex: int = Line.find('\n')
            
            # If this instruction is the final one, then it has no newline!
            if NewLineIndex == -1:
                NewLineIndex = len(Line)
                
            A1 = Line[FirstSpaceIndex:NewLineIndex].strip()
            try:
                I.Arg1 = "{:04X}".format(int(A1, 16))
            except ValueError:
                print("Invalid first argument '" + Line + "'!")
                exit(1)
        
        # If we are expecting two arguments
        elif NumArguments == 2:
            CommaIndex: int = Line.find(',')
            NewLineIndex: int = Line.find('\n')
            
            # If this instruction is the final one, then it has no newline!
            if NewLineIndex == -1:
                NewLineIndex = len(Line)
                
            A1 = Line[FirstSpaceIndex:CommaIndex].strip()
            A2 = Line[CommaIndex+2:NewLineIndex].strip()
            
            try:
                I.Arg1 = "{:04X}".format(int(A1))
            except ValueError:
                print("Invalid second argument '" + Line + "'!")
                exit(1)
                
            try:
                I.Arg2 = "{:04X}".format(int(A2))
            except ValueError:
                print("Invalid second argument '" + Line + "'!")
                exit(1)
        
        # If we are expecting three arguments
        elif NumArguments == 3:
            FirstCommaIndex: int = Line.find(',')
            SecondCommaIndex: int = Line.find(',', FirstCommaIndex + 1)
            NewLineIndex: int = Line.find('\n')
            
            # If this instruction is the final one, then it has no newline!
            if NewLineIndex == -1:
                NewLineIndex = len(Line)
            
            A1 = Line[FirstSpaceIndex:FirstCommaIndex].strip()
            A2 = Line[FirstCommaIndex+1:SecondCommaIndex].strip()
            A3 = Line[SecondCommaIndex+1:NewLineIndex].strip()
            
            try:
                I.Arg1 = "{:04X}".format(int(A1))
            except ValueError:
                print("Invalid second argument '" + Line + "'!")
                exit(1)
                
            try:
                I.Arg2 = "{:04X}".format(int(A2))
            except ValueError:
                print("Invalid second argument '" + Line + "'!")
                exit(1)
                
            try:
                I.Arg3 = "{:04X}".format(int(A3))
            except ValueError:
                print("Invalid third argument '" + Line + "'!")
                exit(1)
        
        return Success(I)

        
