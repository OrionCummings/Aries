from typing import Optional
from option import Err, Ok, Result
from Transformations import encode, decode, get_opcode
from PrettyPrinting import PrintMode, bold, green_bold, red_bold
from Constants import FL_ZERO, PC_INC, PC_OVERRUN, InstructionMode, TextRenderTarget
from RegisterFile import RegisterFile
from Memory import Memory
from CallStack import CallStack
from Utilities import get_opcode_from_id, p_exit

class CPU():
    """A CPU that supports the Aires Assembly Language."""
    
    def __init__(self, instruction_memory_size_in_bytes: int = 4096, data_memory_size_in_bytes: int = 4096) -> None:
        """Initializes a CPU instance with a given memory size in bytes."""
        
        # The essential parts a Harvard CPU
        self.register_file            = RegisterFile()
        self.instruction_memory       = Memory(instruction_memory_size_in_bytes)
        self.data_memory              = Memory(data_memory_size_in_bytes)
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
        builder: str = "PC: " + str(program_counter) + "\n"
        
        # Append the register file
        # builder += str(self.register_file)
        builder += self.register_file.to_string(TextRenderTarget.Widget)

        # Append the instruction memory
        builder += "Instruction Memory\n"
        builder += self.instruction_memory.to_string(TextRenderTarget.Terminal, self.register_file.get_pc())
        builder += "\n"

        # Append the data memory
        builder += "Data Memory\n"
        builder += self.data_memory.to_string(TextRenderTarget.Terminal, -4)
        
        return builder
    
    def load_program(self, program: list[int], program_name: str, base_address: int = 0) -> Result[bool, str]:
        """Loads a program into memory at the given address."""
        
        if base_address >= self.instruction_memory.capacity_in_bytes:
            print("Failed to load program: Base address '{}' exceeds the instruction memory address space of {}!".format(base_address, self.instruction_memory.capacity_in_bytes))
            exit(2)
        
        program_length = len(program)
        if program_length + base_address >= self.instruction_memory.capacity_in_bytes:
            print("Failed to load program: program size ({}) exceeds the instruction memory capacity ({})!".format(program_length, self.instruction_memory.capacity_in_bytes))
            exit(2)
        
        if program_length == 0: print("WARNING: Loading null program.")
        
        r_update = self.instruction_memory.load_instructions(program, base_address)
        if r_update.is_err: return Err(r_update.unwrap_err())
        
        print("Loaded '{}' starting at address {} ({:0X})".format(program_name, base_address, base_address))
        return Ok(True)
    
    def get_current_instruction(self):
        """Returns the current instruction."""
        return self.instruction_memory.get_instruction(self.register_file.get_pc()).unwrap()
    
    def execute_current_instruction(self) -> Result[bool, str]:
        """Executes the current instruction. On success, returns True. On failure, returns an
        error message string.
        """
        
        # Get the current instruction
        current_instruction = self.get_current_instruction()
        decoded_instruction = decode(current_instruction).unwrap()
        decoded_instruction_list = decoded_instruction.split(" ")
        (opcode, *arguments) = decoded_instruction_list

        # Get the instruction function
        function = CONSTANT_INSTRUCTION_FUNCTIONS[opcode]
        self = function(self, arguments).unwrap() # TODO: Reassigning 'self' is probably bad practice
        
        print(green_bold("Executed '{}'".format(decoded_instruction)))

        return Ok(True)
        
    def clock(self) -> bool:
        """Perform one clock cycle."""

        # Execute the current instruction
        execution_result = self.execute_current_instruction()
        if execution_result.is_err: p_exit(f"Failed to execute current instruction: {execution_result.unwrap_err()}")
        
        # Check if the current program counter is valid.
        if self.register_file.get_pc() >= self.instruction_memory.capacity_in_bytes - 1: p_exit("Program counter overrun!", PC_OVERRUN)

        return not self.halted

def nop(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes a 'nop' instruction."""

    # Just increment the program counter
    cpu.register_file.increment_program_counter()

    return Ok(cpu)

def hlt(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes a 'hlt' instruction."""

    # Halt the CPU
    cpu.halted = True

    cpu.register_file.increment_program_counter()

    return Ok(cpu)

def add(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes an 'add' instruction."""
    
    (reg1, reg2, reg3) = arguments
    reg1_value = cpu.register_file.get_reg(reg1).unwrap()
    reg2_value = cpu.register_file.get_reg(reg2).unwrap()
    reg3_value_new = reg1_value + reg2_value
    cpu.register_file.set_reg(reg3, reg3_value_new)

    cpu.register_file.increment_program_counter()

    return Ok(cpu)

def addi(cpu: CPU, arguments: list) -> Result[CPU, str]:
    
    (value_str, src_reg, dest_reg) = arguments
    value = int(value_str)
    src_value = cpu.register_file.get_reg(src_reg).unwrap()
    dest_value = value + src_value
    cpu.register_file.set_reg(dest_reg, dest_value)

    # Update the flags register
    if dest_value == 0:
        cpu.register_file.set_flag(FL_ZERO)
    else:
        cpu.register_file.reset_flag(FL_ZERO)


    cpu.register_file.increment_program_counter()
    
    return Ok(cpu)

def ldi(cpu: CPU, arguments: list) -> Result[CPU, str]:

    (value_str, reg) = arguments
    value = int(value_str)
    cpu.register_file.set_reg(reg, value)

    cpu.register_file.increment_program_counter()
    
    return Ok(cpu)

def j(cpu: CPU, arguments: list) -> Result[CPU, str]:

    (address_str,) = arguments
    address = int(address_str)

    cpu.register_file.set_reg("PC", address)
    
    return Ok(cpu)

def cmp(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes an 'cmp' instruction."""
    
    (reg1, reg2) = arguments
    reg1_value = cpu.register_file.get_reg(reg1).unwrap()
    reg2_value = cpu.register_file.get_reg(reg2).unwrap()
    value = bool(reg1_value - reg2_value)

    if value == 0:
        cpu.register_file.set_flag(FL_ZERO)
    else:
        cpu.register_file.reset_flag(FL_ZERO)

    cpu.register_file.increment_program_counter()

    return Ok(cpu)

def bne(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes an 'bne' instruction."""

    (address_str,) = arguments
    address = int(address_str)
    address_in_bytes = address * PC_INC

    zero_flag_set = cpu.register_file.get_flag(FL_ZERO)

    if zero_flag_set:
        cpu.register_file.set_reg("PC", address_in_bytes)
    else:
        cpu.register_file.increment_program_counter()
    
    return Ok(cpu)

# A list of all instruction functions
CONSTANT_INSTRUCTION_FUNCTIONS = {
    "nop":      nop,
    "hlt":      hlt,
    "add":      add,
    "addi":     addi,
    "ldi":      ldi,
    "bne":      bne,
    "j":        j,
    "cmp":      cmp,
}
