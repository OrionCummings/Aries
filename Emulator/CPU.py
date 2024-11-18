from enum import Enum

from option import Err, Ok, Result
from Assembler import Assembler
from Constants import PC_OVERRUN
from ProgramCounter import ProgramCounter
from RegisterFile import RegisterFile
from DataMemory import DataMemory
from InstructionMemory import InstructionMemory
from Flags import Flags
from typing import List
from PrettyPrinting import PP
from CallStack import CallStack

class CPU():
    """A CPU implementing the Simple Aries Instruction Set Architecture."""
    
    def __init__(Self, InstructionMemorySize: int = 4096, DataMemorySize: int = 4096) -> None:
        """Initializes a CPU instance with a given memory size in bytes."""
        
        # The essential parts of the CPU
        Self.ProgramCounter          = ProgramCounter()
        Self.RegisterFile            = RegisterFile()
        Self.InstructionMemory       = InstructionMemory(InstructionMemorySize)
        Self.DataMemory              = DataMemory(DataMemorySize)
        Self.CallStack               = CallStack()
        Self.Flags                   = Flags()
    
        # Auxilary metadata
        Self.LastUpdatedAddress: int = 0
        Self.HPCBus: int             = 0
    
    def __str__(Self) -> str:
        
        # Begin the string builder by including the program counter
        Builder: str = "PC: " + str(Self.ProgramCounter)
        
        # For every byte in instruction memory
        for ByteAddress in range(len(Self.InstructionMemory)):
            
            # Get the hex literal of the instruction
            Hex = PP.HexLiteral(Self.InstructionMemory[ByteAddress])
            
            # If it's a 32 bit boundary, print some formatting
            if ByteAddress == 0 or ByteAddress % 32 == 0:
                Builder += "\n"
                Builder += str(ByteAddress)
                Builder += ":\t"
            
            if ByteAddress == Self.ProgramCounter: # Highlight the current instruction in bold red
                Builder += PP.RedBold(Hex)
            elif ByteAddress == Self.LastUpdatedAddress: # Highlight the last recently updated address in bold green
                Builder += PP.GreenBold(Hex)
            else: # Otherwise, just add the instruction data to the builder
                Builder += Hex
            
            # Insert a space between each byte
            Builder += " "
            
        return Builder
    
    def Print(Self):
        print(str(Self))
    
    def LoadProgram(Self, Assembler: Assembler, BaseAddress: int = 0) -> Result[bool, str]:
        """Loads a program into memory at the given address."""
        
        if BaseAddress >= len(Self.InstructionMemory):
            return Err("Base address '{}' exceeds the instruction memory address space of {}!".format(BaseAddress, Self.InstructionMemory.Size))
        
        for Byte in Assembler.Bytes:
            Self.InstructionMemory[BaseAddress] = Byte
            BaseAddress += 1
        
        print("Loaded '{}' starting at address {} ({:0X})".format(Assembler.FileName, BaseAddress, BaseAddress))
        return Ok(True)
    
    def ExecuteCurrentInstruction(Self) -> int:
        """Executes the current instruction and returns the address that was changed."""
        pass
    
    def Clock(Self):
        """Perform one clock cycle."""

        # Execute the instruction
        Self.ExecuteCurrentInstruction()
        
        # Increment the program counter
        if Self.ProgramCounter >= len(Self.InstructionMemory) - 1:
            exit(PC_OVERRUN)
        Self.ProgramCounter.Increment()
