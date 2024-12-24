from typing import Optional
from option import Err, Ok, Result
from Transformations import encode, decode, get_opcode
from PrettyPrinting import bold, green_bold
from Constants import PC_OVERRUN
from RegisterFile import RegisterFile
from Memory import Memory
from CallStack import CallStack

class CPU():
    """A CPU that supports the Aires Assembly Language."""
    
    def __init__(self, instruction_memory_size: int = 4096, data_memory_size: int = 4096) -> None:
        """Initializes a CPU instance with a given memory size in bytes."""
        
        # The essential parts a Harvard CPU
        self.register_file            = RegisterFile()
        self.instruction_memory       = Memory(instruction_memory_size)
        self.data_memory              = Memory(data_memory_size)
        self.call_stack               = CallStack()

        # Auxilary metadata
        self.halted: bool                        = False
        self.last_updated_address: Optional[int] = None
        self.hpc_bus: int                        = 0

    def __eq__(self, other):
        
        if not isinstance(other, CPU):
            return NotImplemented
        
        register_file_equal        = self.register_file == other.register_file
        instruction_memory_equal   = self.instruction_memory == other.instruction_memory
        data_memory_equal          = self.data_memory == other.data_memory
        call_stack                 = self.call_stack == other.call_stack
        
        halt_equal                 = self.halted == other.halted
        last_updated_address_equal = self.last_updated_address == other.last_updated_address
        hpc_bus_equal              = self.hpc_bus == other.hpc_bus
        
        return (register_file_equal and instruction_memory_equal and data_memory_equal and call_stack and halt_equal and last_updated_address_equal and hpc_bus_equal)

    def __str__(self) -> str:
        
        # Get the program counter
        program_counter = self.register_file.get_pc()
        
        # Begin the string builder by including the program counter
        builder: str = "PC: " + str(program_counter)
        
        # Print the register file
        print(str(self.register_file))
        
        # TODO: Add some kind of 'CPU settings' similar to the assembler settings
        # to control things like the output format of this function.
        for index in range(self.instruction_memory.capacity):
            
            # If it's a 8 byte boundary, print some formatting
            if index == 0 or index % 8 == 0:
                builder += "\n"
                builder += str(index)
                builder += ":\t"
            
            # Get the full hex literal of the instruction
            instruction = self.instruction_memory[index]
            hex_str = format(instruction, "08X")
            hex_list = [hex_str[0:2], hex_str[2:4], hex_str[4:6], hex_str[6:8]]
            
            for hex_s in hex_list:
                
                # Insert a space between each byte
                builder += " "
                
                if index == program_counter: # Highlight the current instruction in bold red
                    builder += bold(hex_s)
                elif index == self.last_updated_address: # Highlight the last recently updated address in bold green
                    builder += green_bold(hex_s)
                else: # otherwise, just add the instruction data to the builder
                    builder += hex_s
            
        return builder
    
    def load_program(self, program: list[int], program_name: str, base_address: int = 0) -> Result[bool, str]:
        """Loads a program into memory at the given address."""
        
        if base_address >= self.instruction_memory.capacity:
            print("Base address '{}' exceeds the instruction memory address space of {}!".format(base_address, self.instruction_memory.size))
            exit(2)
        
        if len(program) == 0: print("WARNING: Loading null program.")
        
        r_update = self.instruction_memory.update_chunk(program, base_address)
        if r_update.is_err: return Err(r_update.unwrap_err())
        
        print("Loaded '{}' starting at address {} ({:0X})".format(program_name, base_address, base_address))
        return Ok(True)
    
    def get_current_instruction(self):
        """Returns the current instruction."""
        return self.instruction_memory[self.register_file.get_pc()]
    
    def tick(self) -> Result[int, str]:
        """Executes the current instruction and returns the address that was changed."""
        
        from Instructions import INSTRUCTIONS, GetOpcode
        
        address = None
        current_instruction = self.get_current_instruction()
        
        r_opcode = get_opcode(current_instruction)
        if r_opcode.is_err: return Err(r_opcode.unwrap_err())
        opcode_tuple = r_opcode.unwrap()
        
        opcode_id = opcode_tuple[0]
        opcode_function = INSTRUCTIONS[opcode_id]
        self = opcode_function(self, current_instruction)
        
        print("Executed 'N/A'".format())
        
        # TODO: Fix this (optional) feature!
        return address
    
    def clock(self) -> bool:
        """Perform one clock cycle."""

        # Execute the instruction
        self.tick()
        
        # If the CPU has been halted, then don't do anything!
        if self.halt: return False
        
        # TODO: This only triggers when we go out of bounds (which is good!), but
        # it is possible to interact with uninitialized memory (index > size).
        # It may be a good idea to raise a warning of some kind, but there is no
        # such mechanism at the moment. 
        # Increment the program counter
        if self.register_file.get_pc() >= self.instruction_memory.capacity - 1: PExit("Program counter overrun!", PC_OVERRUN)
            
        self.register_file.increment_program_counter()
        
        return True
