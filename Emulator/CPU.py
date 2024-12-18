from option import Err, Ok, Result
from PrettyPrinting import PP, ParseMode, PrintMode
from Constants import ADDR_LENGTH, FF_LENGTH, FUNC_LENGTH, IMM_LENGTH, INS_LENGTH, OP_LENGTH, OPCODES, PC_OVERRUN, REG_LENGTH, REGISTERS, SHAMT_LENGTH, InstructionMode, PExit
from RegisterFile import RegisterFile
from Memory import Memory
from CallStack import CallStack

class CPU():
    """A CPU implementing the Simple Aries Instruction Set Architecture."""
    
    def __init__(Self, InstructionMemorySize: int = 4096, DataMemorySize: int = 4096) -> None:
        """Initializes a CPU instance with a given memory size in bytes."""
        
        # The essential parts a Harvard CPU
        Self.RegisterFile            = RegisterFile()
        Self.InstructionMemory       = Memory(InstructionMemorySize)
        Self.DataMemory              = Memory(DataMemorySize)
        Self.CallStack               = CallStack()

        # Auxilary metadata
        Self.Halt: bool              = False
        Self.LastUpdatedAddress: int = None
        Self.HPCBus: int             = 0

    def __eq__(Self, Other):
        
        if not isinstance(Other, CPU):
            raise NotImplementedError
        
        RegisterFileEqual       = Self.RegisterFile == Other.RegisterFile
        InstructionMemoryEqual  = Self.InstructionMemory == Other.InstructionMemory
        DataMemoryEqual         = Self.DataMemory == Other.DataMemory
        CallStack               = Self.CallStack == Other.CallStack
        
        HaltEqual               = Self.Halt == Other.Halt
        LastUpdatedAddressEqual = Self.LastUpdatedAddress == Other.LastUpdatedAddress
        HPCBusEqual             = Self.HPCBus == Other.HPCBus
        
        return (RegisterFileEqual and InstructionMemoryEqual and DataMemoryEqual and CallStack and HaltEqual and LastUpdatedAddressEqual and HPCBusEqual)

    def __str__(Self) -> str:
        
        # Get the program counter
        ProgramCounter = Self.RegisterFile.GetPC()
        
        # Begin the string builder by including the program counter
        Builder: str = "PC: " + str(ProgramCounter)
        
        # Print the register file
        print(str(Self.RegisterFile))
        
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
                
                if Index == ProgramCounter: # Highlight the current instruction in bold red
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
        return Self.InstructionMemory.Memory[Self.RegisterFile.GetPC()]
    
    def Tick(Self) -> Result[int, str]:
        """Executes the current instruction and returns the address that was changed."""
        
        from Instructions import INSTRUCTIONS, GetOpcode
        
        Address = None
        CurrentInstruction = Self.GetCurrentInstruction()
        
        ROpcode = GetOpcode(CurrentInstruction)
        if ROpcode.is_err: return Err(ROpcode.unwrap_err())
        OpcodeTuple = ROpcode.unwrap()
        
        OpcodeID = OpcodeTuple[0]
        OpcodeFunction = INSTRUCTIONS[OpcodeID]
        Self = OpcodeFunction(Self, CurrentInstruction)
        
        print("Executed '{}'".format()  )
        
        # TODO: Fix this (optional) feature!
        return Address
    
    def Clock(Self) -> bool:
        """Perform one clock cycle."""

        # Execute the instruction
        Self.Tick()
        
        # If the CPU has been halted, then don't do anything!
        if Self.Halt: return False
        
        # TODO: This only triggers when we go out of bounds (which is good!), but
        # it is possible to interact with uninitialized memory (index > size).
        # It may be a good idea to raise a warning of some kind, but there is no
        # such mechanism at the moment. 
        # Increment the program counter
        if Self.RegisterFile.GetPC() >= Self.InstructionMemory.Capacity - 1: PExit("Program counter overrun!", PC_OVERRUN)
            
        Self.RegisterFile.IncrementProgramCounter()
        
        return True
