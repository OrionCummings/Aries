from enum import Enum

from option import Err, Ok, Result
from Assembler import Assembler
from Constants import PC_OVERRUN, PExit
from ProgramCounter import ProgramCounter
from RegisterFile import RegisterFile
from Memory import Memory
from Flags import Flags
from PrettyPrinting import PP
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
    
    def LoadProgram(Self, Assembler: Assembler, BaseAddress: int = 0) -> Result[bool, str]:
        """Loads a program into memory at the given address."""
        
        if BaseAddress >= Self.InstructionMemory.Capacity:
            print("Base address '{}' exceeds the instruction memory address space of {}!".format(BaseAddress, Self.InstructionMemory.Size))
            exit(2)
            #return Err("Base address '{}' exceeds the instruction memory address space of {}!".format(BaseAddress, Self.InstructionMemory.Size))
        
        RUpdate = Self.InstructionMemory.UpdateChunk(Assembler.Instructions, BaseAddress)
        if RUpdate.is_err: return Err(RUpdate.unwrap_err())
        
        print("Loaded '{}' starting at address {} ({:0X})".format(Assembler.FileName, BaseAddress, BaseAddress))
        return Ok(True)
    
    def Tick(Self) -> int:
        """Executes the current instruction and returns the address that was changed."""
        pass
    
    def Clock(Self):
        """Perform one clock cycle."""

        # Execute the instruction
        Self.Tick()
        
        # TODO: This only triggers when we go out of bounds (which is good!), but
        # it is possible to interact with uninitialized memory (index > size).
        # It may be a good idea to raise a warning of some kind, but there is no
        # such mechanism at the moment. 
        # Increment the program counter
        if Self.ProgramCounter.Value >= Self.InstructionMemory.Capacity - 1: PExit("Program counter overrun!", PC_OVERRUN)
            
        Self.ProgramCounter.Increment()
