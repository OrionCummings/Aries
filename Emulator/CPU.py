from enum import Enum
from Assembler import Assembler
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
        
        Self.ProgramCounter         = ProgramCounter()
        Self.RegisterFile           = RegisterFile()
        Self.InstructionMemory      = InstructionMemory(InstructionMemorySize)
        Self.DataMemory             = DataMemory(DataMemorySize)
        Self.CallStack              = CallStack()
        Self.Flags                  = Flags()
    
    def __str__(Self) -> str:
        Builder: str = "PC: " + str(Self.PC)
        for ByteIndex in range(0, len(Self.Memory)):
            if ByteIndex == 0 or ByteIndex % 16 == 0:
                Builder += "\n"
                Builder += str(ByteIndex)
                Builder += ":\t"
            if ByteIndex == Self.PC:
                Builder += PP.RedBold(PP.HexLiteral(Self.Memory[ByteIndex]))
            elif Self.IsByteInProgramMemory(ByteIndex):
                Builder += PP.BlueBold(PP.HexLiteral(Self.Memory[ByteIndex]))
            elif ByteIndex in Self.Delta:
                Builder += PP.GreenBold(PP.HexLiteral(Self.Memory[ByteIndex]))
            else:
                Builder += PP.HexLiteral(Self.Memory[ByteIndex])
            Builder += " "
        return Builder
    
    def Print(Self):
        print(Self)
    
    def LoadProgram(Self, Program: Program, BaseAddress: int = 0) -> bool:
        """Loads a program into memory at the given address."""
        
        if BaseAddress >= len(Self.Memory):
            print("Base address '{}' is too large!".format(BaseAddress))
            return False
        
        Self.ProgramMemory.append(BaseAddress)
        
        for Byte in Program.Bytes:
            Self.Memory[BaseAddress] = Byte
            BaseAddress += 1
        
        Self.ProgramMemory.append(BaseAddress)
        
        print("Loaded '{}' starting at address {}".format(Program.Filename, BaseAddress))
        return True
    
    def IsByteInProgramMemory(Self, Byte: int) -> bool:
        """Returns True if the given address/byte is in program memory."""
        return Self.ProgramMemory[0] <= Byte < Self.ProgramMemory[1]
    
    def ReadCurrentInstruction(Self) -> Instruction:
        """Reads the current instruction."""
        
        # Read the current opcode
        OpcodeStringHigh = str(Self.Memory[Self.PC])
        OpcodeStringLow = str(Self.Memory[Self.PC + 1])
        OpcodeString: str = OpcodeStringHigh + OpcodeStringLow
        Opcode = int(OpcodeString, 16)
        if not Self.ISA.IsValidOpcode(Opcode):
            print("Invalid opcode '{}' encountered!".format(OpcodeString))
            exit(Self.ExitCode.EMU_INVALID_OPCODE)
        
        # Read the data proceeding the opcode
        DataStringByte1High = Self.Memory[Self.PC + 2]
        DataStringByte1Low  = Self.Memory[Self.PC + 3]
        DataStringByte2High = Self.Memory[Self.PC + 4]
        DataStringByte2Low  = Self.Memory[Self.PC + 5]
        DataStringByte3High = Self.Memory[Self.PC + 6]
        DataStringByte3Low  = Self.Memory[Self.PC + 7]
        
        DataByte1 = int(DataStringByte1High + DataStringByte1Low, 16)
        DataByte2 = int(DataStringByte2High + DataStringByte2Low, 16)
        DataByte3 = int(DataStringByte3High + DataStringByte3Low, 16)
        
        I = Instruction()
        I.SetType(Opcode)
        I.Arg1 = DataByte1
        I.Arg2 = DataByte2
        I.Arg3 = DataByte3
        
        return I
    
    def ExecuteInstruction(Self, I: Instruction) -> int:
        """Executes the given instruction and returns the address that was changed."""
        pass
    
    def Clock(Self):
        """Perform one clock cycle."""
        
        # Read the current instruction
        CurrentInstruction: Instruction = Self.ReadCurrentInstruction()
        
        # Execute the instruction
        Self.ExecuteInstruction(CurrentInstruction)
        
        # Increment the program counter
        if Self.PC >= Self.MemorySize - 1:
            Self.Exit(Self.ExitCode.PC_OVERRUN)
        Self.PC += 1
    