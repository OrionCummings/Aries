from typing import Optional
from option import Err, Ok, Result
from Transformations import encode, decode, get_opcode
from PrettyPrinting import bold, green_bold, red_bold
from Constants import PC_OVERRUN, InstructionMode
from RegisterFile import RegisterFile
from Memory import Memory
from CallStack import CallStack
from Utilities import get_opcode_from_id, p_exit

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
                    builder += red_bold(hex_s)
                elif index == self.last_updated_address: # Highlight the last recently updated address in bold green
                    builder += green_bold(hex_s)
                else: # otherwise, just add the instruction data to the builder
                    builder += hex_s
            
        return builder
    
    def load_program(self, program: list[int], program_name: str, base_address: int = 0) -> Result[bool, str]:
        """Loads a program into memory at the given address."""
        
        if base_address >= self.instruction_memory.capacity:
            print("Failed to load program: Base address '{}' exceeds the instruction memory address space of {}!".format(base_address, self.instruction_memory.capacity))
            exit(2)
        
        program_length = len(program)
        if program_length + base_address >= self.instruction_memory.capacity:
            print("Failed to load program: program size ({}) exceeds the instruction memory capacity ({})!".format(program_length, self.instruction_memory.capacity))
            exit(2)
        
        if program_length == 0: print("WARNING: Loading null program.")
        
        r_update = self.instruction_memory.update_chunk(program, base_address)
        if r_update.is_err: return Err(r_update.unwrap_err())
        
        print("Loaded '{}' starting at address {} ({:0X})".format(program_name, base_address, base_address))
        return Ok(True)
    
    def get_current_instruction(self):
        """Returns the current instruction."""
        return self.instruction_memory[self.register_file.get_pc()]
    
    def execute(self) -> Result[None, str]:
        """Executes the current instruction and returns the address that was changed."""
        
        address = None

        # Get the current instruction
        current_instruction = self.get_current_instruction()
        decoded_instruction = decode(current_instruction).unwrap()
        decoded_instruction_list = decoded_instruction.split(" ")
        (opcode, *arguments) = decoded_instruction_list

        function = CONSTANT_INSTRUCTION_FUNCTIONS[opcode]
        self = function(self, arguments).unwrap() # TODO: Reassigning 'self' is probably bad practice
        
        print(green_bold("Executed '{}'".format(decoded_instruction)))
        
        # TODO: Implement this (optional) feature!
        self.last_updated_address = address
    
    def clock(self) -> bool:
        """Perform one clock cycle."""

        # Execute the current instruction
        self.execute()
        
        # If the CPU has been halted, then don't do anything!
        if self.halted: return False
        
        # TODO: This only triggers when we go out of bounds (which is good!), but
        # it is possible to interact with uninitialized memory (index > size).
        # It may be a good idea to raise a warning of some kind, but there is no
        # such mechanism at the moment.
        
        # Increment the program counter
        if self.register_file.get_pc() >= self.instruction_memory.capacity - 1: p_exit("Program counter overrun!", PC_OVERRUN)
            
        self.register_file.increment_program_counter()
        
        return True


def nop(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes a 'nop' instruction."""

    # Do nothing

    return Ok(cpu)

def hlt(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes a 'hlt' instruction."""

    # Halt the CPU
    cpu.halted = True

    return Ok(cpu)

def add(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes an 'add' instruction."""
    
    (reg1, reg2, reg3) = arguments
    reg1_value = cpu.register_file.get_reg(reg1)
    reg2_value = cpu.register_file.get_reg(reg2)
    reg3_value_new = reg1_value + reg2_value
    cpu.register_file.set_reg(reg3, reg3_value_new)

    return Ok(cpu)

def addi(cpu: CPU, arguments: list) -> Result[CPU, str]:
    
    (value_str, src_reg, dest_reg) = arguments
    value = int(value_str)
    src_value = cpu.register_file.get_reg(src_reg).unwrap()
    dest_value = value + src_value
    cpu.register_file.set_reg(dest_reg, dest_value)
    
    return Ok(cpu)

def ldi(cpu: CPU, arguments: list) -> Result[CPU, str]:

    (value_str, reg) = arguments
    value = int(value_str)
    cpu.register_file.set_reg(reg, value)
    
    return Ok(cpu)

def j(cpu: CPU, arguments: list) -> Result[CPU, str]:

    (address_str,) = arguments
    address = int(address_str)
    cpu.register_file.set_reg("PC", address)
    
    return Ok(cpu)

# A list of all instruction functions
CONSTANT_INSTRUCTION_FUNCTIONS = {
    "nop":      nop,    # 0
    "hlt":      hlt,    # 1
    "add":      add,    # 2
    "addi":     addi,   # 3
    "ldi":      ldi,    # 15
    "j":        j,      # 22
}
