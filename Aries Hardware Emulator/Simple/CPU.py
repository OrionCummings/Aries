from enum import Enum
from typing import List
from PrettyPrinting import PP

class CPU():
    """A CPU implementing the Simple Aries Instruction Set Architecture."""
    
    class Opcode(Enum):
        ADD = 0x00,
        SUB = 0x01,
        MOVE = 0x02,
        LOAD = 0x03,
        BNE = 0x04,
    
    def __init__(Self) -> None:
        Self.PC = 0
        Self.Memory: bytearray = bytearray(128)
        
        Self.Delta: List[int] = []
    
    def __str__(Self) -> str:
        Builder: str = "[SAISA CPU] PC: " + str(Self.PC)
        for ByteIndex in range(0, len(Self.Memory)):
            if ByteIndex == 0 or ByteIndex % 16 == 0:
                Builder += "\n"
                Builder += str(ByteIndex)
                Builder += ":\t"
            if ByteIndex == Self.PC:
                Builder += PP.RedBold(PP.HexLiteral(Self.Memory[ByteIndex]))
            else:
                Builder += PP.HexLiteral(Self.Memory[ByteIndex])
            Builder += " "
        return Builder
    
    def Print(Self):
        print(Self)
    
    def LoadProgram(Self, Program: Program):
        """Loads a program into memory."""
        pass
    
    def Clock(Self):
        """Perform one clock cycle."""
        pass
    
    def Add(Self, A: int, B: int, C: int):
        """Memory[A] + Memory[B] = Memory[C]"""
        pass
    
    def Sub(Self, A: int, B: int, C: int):
        """Memory[A] - Memory[B] = Memory[C]"""
        pass
    
    def Move(Self, A: int, B: int):
        """Memory[B] = Memory[A]"""
        pass
    
    def Load(Self, A: int, B: int, C: int):
        """Memory[A] + Memory[B] = Memory[C]"""
        pass
    
    def Bne(Self, A: int, B: int, L: int):
        """If A != B, then PC = L"""
        pass