import struct
from typing import Optional
from option import Err, Ok, Result
from Assembler import Assembler, AssemblerSettings, AssemblerSettingsSource
from Transformations import encode, decode, get_opcode
from PrettyPrinting import PrintMode, bold, green_bold, info, print_green, print_yellow, red_bold, warning
from Constants import CONSTANT_REGISTER_MAP, FL_ZERO, PC_INC, PC_OVERRUN, InstructionFormat, TextRenderTarget
from RegisterFile import RegisterFile
from Memory import Memory
from CallStack import CallStack
from Utilities import get_opcode_from_id, p_exit, debug, trace

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
        # self.last_updated_address: Optional[int] = None
        # self.hpc_bus: int                        = 0

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
        builder += "\n\n"

        # Append the data memory
        builder += "Data Memory\n"
        builder += self.data_memory.to_string(TextRenderTarget.Terminal, -4)
        
        return builder

    def load_program(self, program: list[int] | str, program_name: str, base_address_in_bytes: int = 0) -> Result[bool, str]:
        """Loads a program into memory at the given address.
        Can accept a list of instructions or a string as a program.
        """
        
        # If the input is a string, then assemble that string and reassign `program`
        if isinstance(program, str):

            settings = AssemblerSettings()
            settings.file_directory = None
            settings.file_name = program_name
            settings.print_mode = PrintMode.NoOutput
            settings.source = AssemblerSettingsSource.String

            assembler = Assembler(settings)

            r_run = assembler.run(program)
            if r_run.is_err:
                return trace(f"failed to run assembler:\n{r_run.unwrap_err()}")

            program = assembler.instructions

        if base_address_in_bytes > self.instruction_memory.capacity_in_bytes:
            return trace(f"failed to load program: base address '{base_address_in_bytes}' exceeds the instruction memory address space of {self.instruction_memory.capacity_in_bytes}!")
        
        program_length_in_bytes = len(program) * PC_INC
        if program_length_in_bytes + base_address_in_bytes > self.instruction_memory.capacity_in_bytes:
            return trace(f"failed to load program: program size ({program_length_in_bytes}) exceeds the instruction memory capacity ({self.instruction_memory.capacity_in_bytes})!")
        
        if program_length_in_bytes == 0: warning("Loading null program")
        
        r_update = self.instruction_memory.load_instructions(program, base_address_in_bytes)
        if r_update.is_err: return trace(f"failed to load instructions: {r_update.unwrap_err()}")

        info(f"Loaded '{program_name}' starting at address {base_address_in_bytes} ({base_address_in_bytes:0X})")
        return Ok(True)
    
    def get_current_instruction(self):
        """Returns the current instruction."""

        r_current_instruction = self.instruction_memory.get_instruction(self.register_file.get_pc())
        if r_current_instruction.is_err:
            return trace(r_current_instruction.unwrap_err())

        return r_current_instruction.unwrap()
    
    def execute_current_instruction(self) -> Result[bool, str]:
        """Executes the current instruction. On success, returns True. On failure, returns an
        error message string.
        """
        
        # Get the current instruction and line
        current_instruction = self.get_current_instruction()

        # TODO: Add this!
        current_line = -1

        # Given an instruction, attempt the decode it
        r_decoded_instruction = decode(current_instruction)
        if r_decoded_instruction.is_err:
            return trace(f"failed to decode instruction on line {current_line} '0x{format(current_instruction, '08x')}':\n{r_decoded_instruction.unwrap_err()}")
        decoded_instruction = r_decoded_instruction.unwrap()

        decoded_instruction_list = decoded_instruction.split(" ")
        (potential_opcode, *arguments) = decoded_instruction_list

        # If it exists, get the instruction function
        if potential_opcode not in CONSTANT_INSTRUCTION_FUNCTIONS.keys():
            return trace(f"found opcode '{potential_opcode}' without function definition")
        
        function = CONSTANT_INSTRUCTION_FUNCTIONS[potential_opcode]

        r_new_cpu_state = function(self, arguments)
        if r_new_cpu_state.is_err:
            return trace(f"invalid cpu state\n{r_new_cpu_state.unwrap_err()}")
        
        # TODO: Reassigning 'self' is probably bad practice. Should there be an object
        # that contains a CPU that handles CPU state changes?
        self = r_new_cpu_state.unwrap()
        
        print(green_bold(f"Executed '{decoded_instruction}'"))

        return Ok(True)
        
    def clock(self) -> bool:
        """Perform one clock cycle."""

        # Execute the current instruction
        execution_result = self.execute_current_instruction()
        if execution_result.is_err:
            p_exit(f"{debug()}: failed to execute current instruction:\n{execution_result.unwrap_err()}")
        
        # TODO: Refactor/remove p_exit and use a result type!
        # Check if the current program counter is valid.
        if self.register_file.get_pc() >= self.instruction_memory.capacity_in_bytes - 1: p_exit("Program counter overrun!", PC_OVERRUN)

        return not self.halted

    def run(self) -> Result[bool, str]:

        halted = False
        while not halted:
            halted = not self.clock()

        return Ok(True)

    def save_context(self) -> Result[bool, str]:
        """Saves the current CPU context to the Call Stack."""

        # Get the program counter
        pc = self.register_file.get_pc()

        # Save the program counter on the call stack
        r_push = self.call_stack.push(pc)
        if r_push.is_err:
            return trace(f"failed to push program counter '{pc}' to call stack:\n{r_push.unwrap_err()}")

        return Ok(r_push.unwrap())

    def restore_context(self) -> Result[bool, str]:
        """Restores the previous CPU context from the Call Stack."""

        # Save the program counter on the call stack
        r_pop = self.call_stack.pop()
        if r_pop.is_err:
            return trace(f"failed to pop program counter from call stack:\n{r_pop.unwrap_err()}")

        return Ok(r_pop.unwrap())

def i_nop(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes a 'No Operation' instruction."""

    # Just increment the program counter
    cpu.register_file.increment_program_counter()

    return Ok(cpu)

def i_hlt(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes a 'Halt' instruction."""

    # Halt the CPU
    cpu.halted = True

    cpu.register_file.increment_program_counter()

    return Ok(cpu)

def i_add(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes an 'Addition' instruction."""
    
    (reg1, reg2, reg3) = arguments
    reg1_value = cpu.register_file.get_reg(reg1).unwrap()
    reg2_value = cpu.register_file.get_reg(reg2).unwrap()
    reg3_value_new = reg1_value + reg2_value
    cpu.register_file.set_reg(reg3, reg3_value_new)

    cpu.register_file.increment_program_counter()

    return Ok(cpu)

def i_addi(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes a 'Addition Immediate' instruction."""
    
    (value_str, reg) = arguments
    try:
        value = int(value_str)
    except ValueError:
        return trace(f"failed to convert '{value_str}' to an integer")

    r_reg_value = cpu.register_file.get_reg(reg)
    if r_reg_value.is_err:
        return trace(f"failed to get value of register '{reg}'")
    
    dest_value = value + r_reg_value.unwrap()
    cpu.register_file.set_reg(reg, dest_value)

    # Update the flags register
    if dest_value == 0:
        cpu.register_file.set_flag(FL_ZERO)
    else:
        cpu.register_file.reset_flag(FL_ZERO)


    cpu.register_file.increment_program_counter()
    
    return Ok(cpu)

def i_ldi(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes a 'Load Immediate' instruction."""

    (value_str, potential_reg) = arguments
    potential_value = int(value_str)

    if potential_reg not in CONSTANT_REGISTER_MAP.keys():
        return trace(f"invalid register '{potential_reg}' parsed")

    # 2^16-1 = 65535 is the largest value these instructions can hold,
    # so attempting to load any larger number should fail!
    if potential_value >= 2**16:
        return trace(f"failed to load immediate '{potential_value}' into register '{potential_reg}' (value is too large for 16 bits!)")

    cpu.register_file.set_reg(potential_reg, potential_value)

    cpu.register_file.increment_program_counter()
    
    return Ok(cpu)

def i_j(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes a 'Jump' instruction."""

    (address_str,) = arguments
    address = int(address_str)
    address_in_bytes = address * PC_INC

    cpu.register_file.set_reg("PC", address_in_bytes)
    
    return Ok(cpu)

def i_cmp(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes an 'Compare' instruction."""
    
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

def i_bne(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes a 'Branch Not Equal' instruction."""

    (address_str,) = arguments
    address = int(address_str)
    address_in_bytes = address * PC_INC

    zero_flag_set = cpu.register_file.get_flag(FL_ZERO)

    # If the zero flag is set (the value ARE equal), then inc and reset
    if zero_flag_set:
        cpu.register_file.increment_program_counter()
        cpu.register_file.reset_flag(FL_ZERO)

    # If the zero flag is not set (the value ARE NOT equal), then jump
    else:
        cpu.register_file.set_reg("PC", address_in_bytes)
    
    return Ok(cpu)

def i_ld(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Execute a 'Load' instruction."""

    # Get the memory address
    potential_address = arguments[0]
    try:
        address = int(potential_address)
    except ValueError:
        return trace(f"failed to convert address '{potential_address}' to an integer")

    # Get the value at that memory address
    # TODO: Magic numbers!
    r_value_vector_bytes = cpu.data_memory.get_bytes(address, address+3)
    if r_value_vector_bytes.is_err:
        return trace(f"failed to get bytes\n{r_value_vector_bytes.unwrap_err()}")
    value_vector_bytes = r_value_vector_bytes.unwrap()
    value = int.from_bytes(value_vector_bytes, byteorder='little')

    # Get the register
    potential_reg = arguments[1]
    if potential_reg not in CONSTANT_REGISTER_MAP.keys():
        return trace(f"parsed unknown register '{potential_reg}'")

    # Set the register value to the value in memory
    cpu.register_file.set_reg(potential_reg, value)

    # Increment the program counter
    cpu.register_file.increment_program_counter()

    return Ok(cpu)

def i_str(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Execute a 'Store' instruction."""

    # Get the register
    potential_reg = arguments[1]
    if potential_reg not in CONSTANT_REGISTER_MAP.keys():
        return trace(f"parsed unknown register '{potential_reg}'")
    
    # Get the value of the register and split it into 4 bytes
    r_reg_value = cpu.register_file.get_reg(potential_reg)
    if r_reg_value.is_err:
        return trace(f"failed to get register '{potential_reg}'")
    
    # This value may be 1-4 bytes in size, so we need to treat it accordingly!
    reg_value = r_reg_value.unwrap()

    # This assumes all loaded values are 4 bytes!
    # Create a list of each byte of the value (little endian!)
    parts = []
    for _ in range(0, 4):
        parts.append(reg_value & 255)
        reg_value >>= 8

    # Pack the bytes into a single number.
    # '<' => little endian
    # 'B' => one unsigned char (duplicated four times!)
    try:
        packed_bytes = struct.pack('>BBBB', *parts)
    except struct.error as _:
        return trace(f"failed to pack bytes")

    # Get the memory address
    potential_address = arguments[0]
    try:
        address = int(potential_address)
    except ValueError:
        return trace(f"failed to convert address '{potential_address}' to an integer")

    # Set the value in memory to the register value
    # TODO: Magic numbers!
    r_set_bytes = cpu.data_memory.set_bytes(packed_bytes, range(address, address+4))
    if r_set_bytes.is_err:
        return trace(f"failed to set bytes\n{r_set_bytes.unwrap_err()}")

    # Increment the program counter
    cpu.register_file.increment_program_counter()
    
    return Ok(cpu)

def i_call(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes a 'Call' instruction."""
    
    # Labels are resolved during assembly, so the single argument
    # of a call instruction will be a precomputed address
    (address_str,) = arguments
    address = int(address_str)
    address_in_bytes = address * PC_INC

    # Increment the program counter and save the CPU context to the top of the call stack
    cpu.register_file.increment_program_counter()
    r_save = cpu.save_context()
    if r_save.is_err:
        return trace(f"failed to save cpu context:\n{r_save.unwrap_err()}")

    # Set the program counter
    cpu.register_file.set_reg("PC", address_in_bytes)

    return Ok(cpu)

def i_ret(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes a 'Return' instruction."""
    
    # Restore the CPU context that is on the top of the call stack
    r_restore_address = cpu.restore_context()
    if r_restore_address.is_err:
        return trace(f"failed to restore cpu context:\n{r_restore_address.unwrap_err()}")

    restore_address = r_restore_address.unwrap()
    cpu.register_file.set_reg("PC", restore_address)

    return Ok(cpu)

# A list of all instruction functions
CONSTANT_INSTRUCTION_FUNCTIONS = {
    "nop":      i_nop,
    "hlt":      i_hlt,
    "add":      i_add,
    "addi":     i_addi,
    "ldi":      i_ldi,
    "bne":      i_bne,
    "j":        i_j,
    "cmp":      i_cmp,
    "ld":       i_ld,
    "str":      i_str,
    "call":     i_call,
    "ret":     i_ret,
}

if __name__ == '__main__':
    c = CPU(8,8)
    program = ";test\nldi 255 A    ;   test    \nhlt\n"

    c.load_program(program, "Test String Program")

    c.clock()
    print(c)
