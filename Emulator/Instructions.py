
from option import Err, Ok, Result
from Constants import ADDR_LENGTH, FF_LENGTH, FUNC_LENGTH, IMM_LENGTH, INS_LENGTH, OP_LENGTH, OPCODES, REG_LENGTH, REGISTERIDS, REGISTERS, SHAMT_LENGTH, InstructionMode
from PrettyPrinting import ParseMode, PrintMode
from CPU import CPU

def is_valid_opcode(opcode: str) -> bool:
    return opcode in OPCODES

def get_opcode(line: str | int) -> Result[tuple, str]:
    
    # If it's a string, the this call is likely parsing
    # an input file (i.e. Encode()).
    if isinstance(line, str):
        if line is not None:
            opcode_str = line.split(' ')[0]
            if opcode_str in OPCODES:
                return Ok(OPCODES[opcode_str])
            
    # If it's an int, then this call is likely decoding
    # a previously parsed instruction (i.e. Decode())
    elif isinstance(line, int):
        if line is not None:
            opcode_int = (line & 0xFC000000) >> (INS_LENGTH - OP_LENGTH) # TODO: Magic number!
            
            for opcode_tuple in OPCODES.values():# TODO: This is pretty stinky
                if opcode_int == opcode_tuple[0]:
                    return Ok(opcode_tuple)
    else:
        return Err("Invalid type passed to GetOpcode(Line: str | int)!")
    
    return Err("Line '{}' does not contain a valid opcode!")

def opcode_to_int(opcode: str) -> Result[int, str]:
    """Converts the given opcode (as a string) to an integer."""
    try:
        opcode_int: int = int(opcode)
    except (TypeError, ValueError):
        return Err("Failed to convert '{}' to a number".format(opcode))
    return Ok(opcode_int)

def instruction_string(instruction: int, p_mode: PrintMode) -> Result[str, str]:
    builder: str = ""
    
    r_opcode = get_opcode(instruction)
    if r_opcode.is_err: return Err(r_opcode.Err())
    opcode = r_opcode.unwrap()
    i_mode: InstructionMode = opcode[2]
    
    # Convert the intruction to a binary string
    instruction_str: str = format(instruction, "032b")
    
    match p_mode:
        
        case PrintMode.NoOutput:
            pass
        
        case PrintMode.Binary:
            builder += instruction_str
        
        case PrintMode.Bytes: # TODO: Magic numbers (but I think they are justified here)!
            byte0 = instruction_str[0:8]
            byte1 = instruction_str[8:16]
            byte2 = instruction_str[16:24]
            byte3 = instruction_str[24:32]
            builder += " ".join([byte0, byte1, byte2, byte3])
            
        case PrintMode.Hex:
            byte0 = "{:X}".format(int(instruction_str[0 : 4], 2))
            byte1 = "{:X}".format(int(instruction_str[4 : 8], 2))
            byte2 = "{:X}".format(int(instruction_str[8 :12], 2))
            byte3 = "{:X}".format(int(instruction_str[12:16], 2))
            byte4 = "{:X}".format(int(instruction_str[16:20], 2))
            byte5 = "{:X}".format(int(instruction_str[20:24], 2))
            byte6 = "{:X}".format(int(instruction_str[24:28], 2))
            byte7 = "{:X}".format(int(instruction_str[28:32], 2))
            builder += "".join([byte0, byte1, byte2, byte3, byte4, byte5, byte6, byte7])
        
        case PrintMode.Instructions:
            match i_mode:
                case instruction_mode.register:
                    opcode   = instruction_str[:OP_LENGTH]
                    reg_a    = instruction_str[OP_LENGTH : OP_LENGTH + (1 * REG_LENGTH)]
                    reg_b    = instruction_str[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
                    reg_c    = instruction_str[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH)]
                    shamt    = instruction_str[OP_LENGTH + (3 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH) + SHAMT_LENGTH]
                    func     = instruction_str[-FUNC_LENGTH:]
                    builder += " ".join([opcode, reg_a, reg_b, reg_c, shamt, func])
                    
                case InstructionMode.Immediate:
                    opcode  = instruction_str[:OP_LENGTH]
                    reg_a   = instruction_str[OP_LENGTH : OP_LENGTH + REG_LENGTH]
                    reg_b   = instruction_str[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
                    unk     = instruction_str[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH) + FF_LENGTH]
                    value   = instruction_str[-IMM_LENGTH:]
                    builder += " ".join([opcode, reg_a, reg_b, unk, value])
                    
                case InstructionMode.Jump:
                    opcode  = instruction_str[:OP_LENGTH]
                    address = instruction_str[OP_LENGTH:]
                    builder += " ".join([opcode, address])
    
    return Ok(builder)

def Parseargument(arg: str, parse_mode: ParseMode) -> Result[int, str]:
    """Parses a given argument as either a register value, immediate value, or an address."""
    
    ret = 0
    
    match parse_mode:
        case ParseMode.Register:
            
            if arg.isdigit():
                ret = int(arg)
                if ret < 0:
                    return Err("Invalid register '{}' (cannot be negative)!".format(ret))
                elif ret >= 2 ** REG_LENGTH:
                    return Err("Invalid register '{}' (cannot be greater or equal to {})!".format(ret, 2 ** REG_LENGTH))
            elif arg in REGISTERS:
                ret = REGISTERS[arg]
            else:
                return Err("Invalid non-numeric argument '{}'!".format(arg))
            
        case ParseMode.ImmediateValue:
            
            if arg.isdigit():
                ret = int(arg)
                if ret < 0: return Err("Invalid immediate value '{}' (cannot be negative)!".format(ret))
                elif ret >= 2 ** IMM_LENGTH: return Err("Invalid immediate value '{}' (cannot be greater or equal to {})!".format(ret, 2 ** IMM_LENGTH))
            elif len(arg) >= 2 and arg[0:2] == '0x':
                ret = int(arg, 16)
                if ret < 0: return Err("Invalid immediate value '{}' (cannot be negative)!".format(ret))
                elif ret >= 2 ** IMM_LENGTH: return Err("Invalid immediate value '{}' (cannot be greater or equal to {})!".format(ret, 2 ** IMM_LENGTH))
            elif len(arg) >= 2 and arg[0:2] == '0o':
                ret = int(arg, 8)
                if ret < 0: return Err("Invalid immediate value '{}' (cannot be negative)!".format(ret))
                elif ret >= 2 ** IMM_LENGTH: return Err("Invalid immediate value '{}' (cannot be greater or equal to {})!".format(ret, 2 ** IMM_LENGTH))
            elif len(arg) >= 2 and arg[0:2] == '0b':
                ret = int(arg, 2)
                if ret < 0: return Err("Invalid immediate value '{}' (cannot be negative)!".format(ret))
                elif ret >= 2 ** IMM_LENGTH: return Err("Invalid immediate value '{}' (cannot be greater or equal to {})!".format(ret, 2 ** IMM_LENGTH))
            else: return Err("Invalid non-numeric argument '{}'!".format(arg))
            
        case ParseMode.Address:
            
            if arg.isdigit():
                address = int(arg)
                if address < 0: return Err("Invalid address '{}' (cannot be negative)!".format(ret))
                elif address >= 2 ** ADDR_LENGTH: return Err("Invalid address '{}' (cannot be greater or equal to {})!".format(ret, 2 ** ADDR_LENGTH))
            else: return Err("Invalid non-numeric argument '{}'!".format(arg))
    
    return Ok(ret)

def encode(line: str) -> Result[int, str]:
    
    # Create the line vector
    line_vector = line.split(' ')
    if len(line_vector) < 1: return Err("Malformed instruction '{}' (likely an empty line)".format(line))
    if len(line_vector) > 4: return Err("Malformed instruction '{}' (too many arguments)".format(line))
    
    # Get the potential opcode
    potential_opcode = LineVector[0]
    
    # Check that it's a valid opcode
    if not is_valid_opcode(potential_opcode): return Err("Unknown opcode '{}'".format(potential_opcode))
    
    opcode_tuple = OPCODES[potential_opcode]
    opcode = opcode_tuple[0]
    num_args = opcode_tuple[1]
    mode = opcode_tuple[2]
    
    # Check that the number of expected arguments matches
    # the number of actual arguments.
    if len(line_vector) == num_args: return Err("Expected number of arguments ({}) does not match the actual number of arguments ({})!".format(num_args, len(line_vector)))

    instruction: int = 0
    Instruction |= opcode << (INS_LENGTH - OP_LENGTH)
    
    match Mode:
        
        # TODO: Parseargument also has a match on instruction mode. Consider refactoring! 
        
        case InstructionMode.Register:
            
            reg_a, reg_b, reg_c = (0, 0, 0)
            
            if num_args > 0:
                r_reg_a = parse_argument(line_vector[1], ParseMode.Register)
                if r_reg_a.is_err: return r_reg_a.Err()
                else: reg_a = r_reg_a.unwrap()
            
            if num_args > 1:
                r_reg_b = parse_argument(line_vector[2], ParseMode.Register)
                if r_reg_b.is_err: return r_reg_b.Err()
                else: reg_b = r_reg_b.unwrap()
            
            if num_args > 2:
                r_reg_c = parse_argument(line_vector[3], ParseMode.Register)
                if r_reg_c.is_err: return r_reg_c.Err()
                else: reg_c = r_reg_c.unwrap()
            
            instruction |= reg_a << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 1))
            instruction |= reg_b << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 2))
            instruction |= reg_c << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 3))
            
            # TODO: SHAMT and FUNC are not implemented yet
            
        case InstructionMode.Immediate:
            
            reg = 0
            
            if num_args > 0:
                r_value = parse_argument(line_vector[1], ParseMode.ImmediateValue)
                if r_value.is_err: return Err(r_value.Err())
                else: value = r_value.unwrap()
            
            if num_args > 1:
                r_reg = parse_argument(line_vector[2], ParseMode.Register)
                if r_reg.is_err: return Err(r_value.Err())
                else: reg = r_reg.unwrap()
            
            instruction |= reg << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 1))
            instruction |= value
            
        case InstructionMode.Jump:
            
            address = 0
            
            if num_args > 0:
                r_address = parse_argument(line_vector[1], ParseMode.Address)
                if r_address.is_err: return r_address.Err()
                else: address = r_address.unwrap()
            
            instruction |= address
            
    return Ok(instruction)

def decode(instruction: int) -> Result[(str, str, str, str, int), str]:
    print("Instruction decoding is not a priority and has not been implemented yet!")
    exit(-4)
    pass

def extract(instruction: int) -> Result[(InstructionMode, list), str]:
    
    r_opcode = get_opcode(instruction)
    if r_opcode.is_err: return Err(r_opcode.unwrap_err())
    opcode_tuple = r_opcode.unwrap()
    mode = opcode_tuple[2]
    
    binary_instruction = format(instruction, "032b")
    ret_list = []
    
    match Mode:
        
        case InstructionMode.Register:
            opcode  = binary_instruction[:OP_LENGTH]
            reg_a    = binary_instruction[OP_LENGTH : OP_LENGTH + (1 * REG_LENGTH)]
            reg_b    = binary_instruction[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
            reg_c    = binary_instruction[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH)]
            shamt   = binary_instruction[OP_LENGTH + (3 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH) + SHAMT_LENGTH]
            func    = binary_instruction[-FUNC_LENGTH:]
            ret_list = [opcode, reg_a, reg_b, reg_c, Shamt, Func]
            
        case InstructionMode.Immediate:
            opcode = binary_instruction[:OP_LENGTH]
            reg_a = binary_instruction[OP_LENGTH : OP_LENGTH + REG_LENGTH]
            reg_b = binary_instruction[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
            unk = binary_instruction[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH) + FF_LENGTH]
            value = binary_instruction[-IMM_LENGTH:]
            ret_list = [opcode, reg_a, reg_b, unk, value]
            
        case InstructionMode.Jump:
            opcode  = binary_instruction[:OP_LENGTH]
            address = binary_instruction[OP_LENGTH:]
            ret_list = [opcode, address]
    
    return Ok((mode, ret_list))

def verify_opcode(instruction: int, expected_opcode: str) -> Result[bool, str]:
    r_opcode = get_opcode(instruction)
    if r_opcode.is_err: return Err(r_opcode.unwrap_err())
    opcode_tuple = ROpcode.unwrap()
    actual_opcode_id = OpcodeTuple[0]
    expected_opcode_id = OPCODES[expected_opcode][0]
    if not expected_opcode_id == actual_opcode_id:
        return Err("Expected opcode '{}' does not match actual opcode '{}' from instruction {}".format(expected_opcode_id, actual_opcode_id, instruction))
    return Ok(True)
    
def NOP(cpu: CPU, instruction: int) -> Result[CPU, str]:
    """Executes a 'nop' instruction."""
    
    instruction_mnemonic = 'nop'
    r_verification = verify_opcode(instruction, instruction_mnemonic)
    if r_verification.is_err: return Err(r_verification.unwrap_err())

    return Ok(cpu)

def HLT(cpu: CPU, instruction: int) -> Result[CPU, str]:
    """Executes a 'hlt' instruction."""
    
    instruction_mnemonic = 'hlt'
    r_verification = verify_opcode(instruction, instruction_mnemonic)
    if r_verification.is_err: return Err(r_verification.unwrap_err())

    # Halt the CPU
    cpu.halt = True

    return Ok(cpu)

def ADD(cpu: CPU, instruction: int) -> Result[CPU, str]:
    """Executes an 'add' instruction."""
    
    instruction_mnemonic = 'add'
    r_verification = verify_opcode(instruction, instruction_mnemonic)
    if r_verification.is_err: return Err(r_verification.unwrap_err())

    # TODO: This code probably already exists in this project, so find and reuse it!
    # Or make it generic!

    opcode_tuple = OPCODES[instruction_mnemonic]
    mode = opcode_tuple[2]

    if mode != InstructionMode.Register: return Err("Expected nemonic '{}' to be Register!".format(instruction_mnemonic))
    
    r_extraction = extract(instruction)
    if r_extraction.is_err: return Err(r_extraction.unwrap_err())
    extraction = r_extraction.unwrap()
    
    if extraction[0] != InstructionMode.Register:
        return Err("Extracted instruction mode '{}' does not match expected instruction mode '{}'".format(extraction[0], InstructionMode.Register))
    
    # BUG: This is stupid lol. Use ya damn classes
    # Get each register
    reg_a = cpu.register_file.registers[REGISTERIDS[int(extraction[1][1])]]
    reg_b = cpu.register_file.registers[REGISTERIDS[int(extraction[1][2])]]
    reg_c = cpu.register_file.registers[REGISTERIDS[int(extraction[1][3])]]
    
    # Perform the operation
    res = reg_a + reg_b
    
    # Save the result to the source register
    cpu.register_file.set_reg(reg_c, Res)

    return Ok(cpu)

def ADDI(cpu: CPU, instruction: int) -> Result[CPU, str]:
    
    instruction_mnemonic = 'addi'
    
    
    print("Performed a '{}' instruction!".format(instruction_mnemonic))

def LDI(cpu: CPU, instruction: int) -> Result[CPU, str]:
    
    instruction_mnemonic = 'ldi'
    r_verification = verify_opcode(instruction, instruction_mnemonic)
    if r_verification.is_err: return Err(r_verification.unwrap_err())

    opcode_tuple = OPCODES[instruction_mnemonic]
    mode = opcode_tuple[2]

    if mode != InstructionMode.Immediate: return Err("Expected nemonic '{}' to be Immediate!".format(instruction_mnemonic))
    
    r_extraction = extract(instruction)
    if r_extraction.is_err: return Err(r_extraction.unwrap_err())
    extraction = r_extraction.unwrap()
    
    if extraction[0] != InstructionMode.Immediate:
        return Err("Extracted instruction mode '{}' does not match expected instruction mode '{}'".format(extraction[0], InstructionMode.Immediate))
    
    # Get the register and the value
    reg_a = extraction[1][1]
    value = extraction[1][4]
    
    # Save the result to the source register
    cpu.register_file.set_reg(reg_a, value)
    
    print("Performed a '{}' instruction!".format(instruction_mnemonic))
    
    return Ok(cpu)

def placeholder_instruction_function() -> Result[CPU, str]:
    return Err("Unimplemented instruction function called!")

# A list of all instruction functions
INSTRUCTIONS = [
    NOP,    # 0
    HLT,    # 1
    ADD,    # 2
    ADDI,   # 3
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 4
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 5
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 6
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 7
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 8
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 9
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 10
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 11
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 12
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 13
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 14
    LDI,    # 15
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 16
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 17
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 18
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 19
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 20
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 21
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 22
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 23
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 24
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 25
    PLACEHOLDER_INSTRUCTION_FUNCTION, # 26
]
