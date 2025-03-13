from __future__ import annotations
from option import Err, Ok, Result
from RegisterFile import RegisterFile
from Transformations import decode
from PrettyPrinting import green_bold
from Utilities import panic, debug, range_overlap, trace
from Constants import CONSTANT_REGISTER_MAP, DEFAULT_DATA_MEMORY_BASE_ADDRESS, DEFAULT_DATA_MEMORY_SIZE_IN_BYTES, DEFAULT_INSTRUCTION_MEMORY_BASE_ADDRESS, DEFAULT_INSTRUCTION_MEMORY_SIZE_IN_BYTES, DEFAULT_STACK_MEMORY_BASE_ADDRESS, DEFAULT_STACK_MEMORY_SIZE_IN_BYTES, DEFAULT_VIDEO_MEMORY_BASE_ADDRESS, DEFAULT_VIDEO_MEMORY_SIZE_IN_BYTES, FL_ZERO, PC_INC, EC_PC_OVERRUN, TextRenderTarget

class CPUSettings():

    def __init__(self):
        self.memory_size = 0
        self.instruction_memory_base = 0
        self.instruction_memory_size = 0
        self.data_memory_base = 0
        self.data_memory_size = 0
        self.video_memory_base = 0
        self.video_memory_size = 0
        self.stack_memory_base = 0
        self.stack_memory_size = 0

    @staticmethod
    def create_default_cpu_settings() -> Result[CPUSettings, str]:

        # Create a new instance of CPUSettings, set the defaults, 
        # and then validate it
        r_settings = (CPUSettings()
            .set_instruction_memory_size(DEFAULT_INSTRUCTION_MEMORY_SIZE_IN_BYTES)
            .set_instruction_memory_base(0)
            .set_data_memory_size(DEFAULT_DATA_MEMORY_SIZE_IN_BYTES)
            .set_data_memory_base(DEFAULT_INSTRUCTION_MEMORY_SIZE_IN_BYTES)
            .set_video_memory_size(DEFAULT_VIDEO_MEMORY_SIZE_IN_BYTES)
            .set_video_memory_base(DEFAULT_DATA_MEMORY_SIZE_IN_BYTES + DEFAULT_INSTRUCTION_MEMORY_SIZE_IN_BYTES)
            .set_stack_memory_size(DEFAULT_STACK_MEMORY_SIZE_IN_BYTES)
            .set_stack_memory_base(DEFAULT_DATA_MEMORY_SIZE_IN_BYTES + DEFAULT_INSTRUCTION_MEMORY_SIZE_IN_BYTES + DEFAULT_STACK_MEMORY_SIZE_IN_BYTES)
            .validate()
        )

        # If this failed, propagate the error
        if r_settings.is_err:
            return trace("failed to create default settings")

        return r_settings

    def set_instruction_memory_base(self, base_address: int) -> CPUSettings:
        self.instruction_memory_base = base_address
        return self

    def set_instruction_memory_size(self, size: int) -> CPUSettings:
        self.instruction_memory_size = size
        return self

    def set_data_memory_base(self, base_address: int) -> CPUSettings:
        self.data_memory_base = base_address
        return self

    def set_data_memory_size(self, size: int) -> CPUSettings:
        self.data_memory_size = size
        return self

    def set_video_memory_base(self, base_address: int) -> CPUSettings:
        self.video_memory_base = base_address
        return self
    
    def set_video_memory_size(self, size: int) -> CPUSettings:
        self.video_memory_size = size
        return self

    def set_stack_memory_base(self, base_address: int) -> CPUSettings:
        self.stack_memory_base = base_address
        return self

    def set_stack_memory_size(self, size: int) -> CPUSettings:
        self.stack_memory_size = size
        return self

    def validate(self) -> Result[CPU, str]:

        r_total_memory_size = self.calculate_total_memory_size()
        if r_total_memory_size.is_err:
            return trace("failed to calculate total memory size", r_total_memory_size.unwrap_err())
        self.memory_size = r_total_memory_size.unwrap()

        return Ok(self)

    # TODO: Make this real; fields are never None
    def set_default_values(self) -> None:
        if self.instruction_memory_base is None: self.instruction_memory_base = DEFAULT_INSTRUCTION_MEMORY_BASE_ADDRESS
        if self.instruction_memory_size is None: self.instruction_memory_size = DEFAULT_INSTRUCTION_MEMORY_SIZE_IN_BYTES
        if self.data_memory_base is None: self.data_memory_base = DEFAULT_DATA_MEMORY_BASE_ADDRESS
        if self.data_memory_size is None: self.data_memory_size = DEFAULT_DATA_MEMORY_SIZE_IN_BYTES
        if self.video_memory_base is None: self.video_memory_base = DEFAULT_VIDEO_MEMORY_BASE_ADDRESS
        if self.video_memory_size is None: self.video_memory_size = DEFAULT_VIDEO_MEMORY_SIZE_IN_BYTES
        if self.stack_memory_base is None: self.stack_memory_base = DEFAULT_STACK_MEMORY_BASE_ADDRESS
        if self.stack_memory_size is None: self.stack_memory_size = DEFAULT_STACK_MEMORY_SIZE_IN_BYTES

    def calculate_total_memory_size(self) -> Result[int, str] | int:
        return Ok(sum([self.instruction_memory_size, self.data_memory_size, self.video_memory_size, self.stack_memory_size]))

class CPU():
    """A CPU that supports the Aries Assembly Language."""
    
    

    def __init__(self, settings: CPUSettings = None) -> None:
        """Initializes a CPU instance with a the given settings."""
        
        if settings is None:
            self.settings = CPU.create_default_cpu_settings()
        else:
            self.settings = settings

        # All CPUs have a notion of a halted state
        self.halted: bool = False

        # 
        self.register_file = RegisterFile()

        # TODO: Add cache, ALU, and FPU

    def __eq__(self, other: CPU):

        if not isinstance(other, CPU):
            return False
        
        register_file_equality = self.register_file == other.register_file

        return register_file_equality

    def __str__(self) -> str:
        
        return Err(abc_not_implemented())
    
    def load_program(self, program, program_name: str) -> Result[bool, str]:
        """Loads a program into memory at the given address.
        Can accept a list of instructions or a string as a program.
        """

        return Err(abc_not_implemented())
    
    def get_current_instruction(self):
        """Returns the current instruction."""

        return Err(abc_not_implemented())
    
    def execute_current_instruction(self) -> Result[None, str]:
        """Executes the current instruction. On success, returns True. On failure, returns an
        error message string.
        """
        
        # Get the current instruction and line
        r_current_instruction = self.get_current_instruction()
        if r_current_instruction.is_err:
            return trace("failed to get current instruction", r_current_instruction.unwrap_err())

        current_instruction = r_current_instruction.unwrap()

        # TODO: Add this!
        current_line = -1

        # Given an instruction, attempt the decode it
        r_decoded_instruction = decode(current_instruction)
        if r_decoded_instruction.is_err:
            return trace(f"failed to decode instruction on line {current_line} '0x{format(current_instruction, '08x')}'", r_decoded_instruction.unwrap_err())
        decoded_instruction = r_decoded_instruction.unwrap()

        decoded_instruction_list = decoded_instruction.split(" ")
        (potential_opcode, *arguments) = decoded_instruction_list

        # If it exists, get the instruction function
        if potential_opcode not in CONSTANT_INSTRUCTION_FUNCTIONS.keys():
            return trace(f"found opcode '{potential_opcode}' without function definition")
        
        function = CONSTANT_INSTRUCTION_FUNCTIONS[potential_opcode]

        r_new_cpu_state = function(self, arguments)
        if r_new_cpu_state.is_err:
            return trace("instruction invalidated cpu state", r_new_cpu_state.unwrap_err())
        
        # TODO: Reassigning 'self' is probably bad practice. Should there be an object
        # that contains a CPU that handles CPU state changes?
        self = r_new_cpu_state.unwrap()
        
        print(green_bold(f"Executed '{decoded_instruction}'"))

        return Ok(None)
        
    def clock(self) -> Result[bool, str]:
        """Perform one clock cycle."""

        # Execute the current instruction
        execution_result = self.execute_current_instruction()
        if execution_result.is_err:
            return trace("failed to execute current instruction", execution_result.unwrap_err())
        
        # Check if the current program counter is valid.
        pc = self.get_pc()
        if pc >= self.settings.memory_size - 1:
            return trace("program counter overrun")

        # Update the instruction memory range
        self.set_highlight_range(range(pc, pc + PC_INC))

        return Ok(not self.halted)

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
        r_push = self.push(pc)
        if r_push.is_err:
            return trace(f"failed to push program counter '{pc}' to call stack", r_push.unwrap_err())

        return Ok(r_push.unwrap())

    def restore_context(self) -> Result[bool, str]:
        """Restores the previous CPU context from the Call Stack."""

        # Save the program counter on the call stack
        r_pop = self.pop()
        if r_pop.is_err:
            return trace("failed to pop program counter from call stack", r_pop.unwrap_err())

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
        return trace("failed to get bytes", r_value_vector_bytes.unwrap_err())
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

def i_st(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Execute a 'Store' instruction."""

    # Get the value register
    potential_value_reg = arguments[0]
    if potential_value_reg not in CONSTANT_REGISTER_MAP.keys():
        return trace(f"parsed unknown value register '{potential_value_reg}'")
    value_reg = potential_value_reg
    
    # Get the value of the register and split it into 4 bytes
    r_reg_value = cpu.register_file.get_reg(value_reg)
    if r_reg_value.is_err:
        return trace(f"failed to get register '{value_reg}'")
    
    # This value may be 1-4 bytes in size, so we need to treat it accordingly!
    reg_value = r_reg_value.unwrap()

    # TODO: Magic numbers! This assumes all loaded values are 4 bytes!
    # Create a list of each byte of the value (little endian!)
    value_bytes = []
    for _ in range(0, 4):
        value_bytes.append(reg_value & 255)
        reg_value >>= 8

    # Overwrite this variable so it's more difficult to misuse!
    reg_value = None
    
    # Get the address register
    potential_address_reg = arguments[1]
    if potential_address_reg not in CONSTANT_REGISTER_MAP.keys():
        return trace(f"parsed unknown address register '{potential_address_reg}'")
    address_reg = potential_address_reg
    
    # Get the value of the register and split it into 4 bytes
    r_address = cpu.register_file.get_reg(address_reg)
    if r_address.is_err:
        return trace(f"failed to get register '{address_reg}'")
    
    # This value may be 1-4 bytes in size, so we need to treat it accordingly!
    address = r_address.unwrap()
    
    # TODO: Magic numbers!
    # Set the address in memory
    address_range = range(address, address + 4)
    r_set_bytes = cpu.data_memory.set_bytes(address_range, value_bytes)
    if r_set_bytes.is_err:
        return trace("failed to set bytes", r_set_bytes.unwrap_err())
    
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
        return trace("failed to save cpu context", r_save.unwrap_err())

    # Set the program counter
    cpu.register_file.set_reg("PC", address_in_bytes)

    return Ok(cpu)

def i_ret(cpu: CPU, arguments: list) -> Result[CPU, str]:
    """Executes a 'Return' instruction."""
    
    # Restore the CPU context that is on the top of the call stack
    r_restore_address = cpu.restore_context()
    if r_restore_address.is_err:
        return trace("failed to restore cpu context", r_restore_address.unwrap_err())

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
    "st":       i_st,
    "call":     i_call,
    "ret":      i_ret,
}

