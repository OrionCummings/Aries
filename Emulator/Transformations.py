
from option import Result, Err, Ok
from BitManipulation import bit_mask
from Constants import CONSTANT_NO_ARG_OPCODES, CONSTANT_OPCODE_MAP, CONSTANT_REGISTER_MAP, FF_LENGTH, FUNC_LENGTH, IMM_LENGTH, INS_LENGTH, OP_LENGTH, REG_LENGTH, SHAMT_LENGTH, InstructionMode
from PrettyPrinting import PrintMode
from Utilities import get_opcode_from_id

def get_opcode(instruction: str | int) -> Result[int, str]:
    
    if isinstance(instruction, str):
        opcode = instruction.split(" ")[0]
        return Ok(opcode)
    elif isinstance(instruction, int):
        start_index = INS_LENGTH - OP_LENGTH
        end_index = INS_LENGTH
        mask = bit_mask(start_index, end_index)
        opcode = (instruction & mask) >> start_index
        return Ok(opcode)
    else:
        return Err("Unknown type passed to get_opcode()!")

def get_instruction_mode(instruction: str | int) -> Result[InstructionMode, str]:
    if isinstance(instruction, str):
        opcode = instruction.split(" ")[0]
    elif isinstance(instruction, int):
        decoded_instruction = decode(instruction).unwrap()
        opcode = decoded_instruction.split(" ")[0]
    else:
        return Err("Unknown type passed to get_instruction_mode()!")
    
    if opcode in CONSTANT_OPCODE_MAP:
        opcode_tuple = CONSTANT_OPCODE_MAP[opcode]
    else:
        return Err("Unknown opcode '{}' passed to get_instruction_mode()!".format(opcode))
    (_, _, i_mode, *_) = opcode_tuple

    return Ok(i_mode)

def is_valid_opcode(opcode: str) -> bool:
    return opcode in CONSTANT_OPCODE_MAP

def get_encoded_instruction_as_binary(encoded_instruction: int):
    return format(encoded_instruction, "032b")

def decode_register_instruction_as_list(binary_instruction: str) -> list:
    opcode = binary_instruction[:OP_LENGTH]
    reg_a  = binary_instruction[OP_LENGTH : OP_LENGTH + (1 * REG_LENGTH)]
    reg_b  = binary_instruction[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
    reg_c  = binary_instruction[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH)]
    shamt  = binary_instruction[OP_LENGTH + (3 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH) + SHAMT_LENGTH]
    func   = binary_instruction[-FUNC_LENGTH:]
    return [opcode, reg_a, reg_b, reg_c, shamt, func]

def decode_immediate_instruction_as_list(binary_instruction: str):
    opcode = binary_instruction[:OP_LENGTH]
    reg_a  = binary_instruction[OP_LENGTH : OP_LENGTH + REG_LENGTH]
    reg_b  = binary_instruction[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
    unk    = binary_instruction[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH) + FF_LENGTH]
    value  = binary_instruction[-IMM_LENGTH:]
    return [opcode, reg_a, reg_b, unk, value]

def decode_jump_instruction_as_list(binary_instruction: str):
    opcode  = binary_instruction[:OP_LENGTH]
    address = binary_instruction[OP_LENGTH:]
    return [opcode, address]

def encode(line: str) -> Result[int, str]:
        
    # Create the line vector
    line_vector = line.split(' ')
    if len(line_vector) < 1: return Err("Malformed instruction '{}' (too few arguments)".format(line))
    if len(line_vector) > 4: return Err("Malformed instruction '{}' (too many arguments)".format(line))
    
    # Get the potential opcode
    potential_opcode = line_vector[0]
    
    # Check that it's a valid opcode
    if not is_valid_opcode(potential_opcode): return Err("Unknown opcode '{}'".format(potential_opcode))
    
    # Get the opcode tuple and extract the important information
    opcode_tuple = CONSTANT_OPCODE_MAP[potential_opcode]
    (opcode, num_args, mode, *unused) = opcode_tuple
    
    # Check that the number of expected arguments matches the number of actual arguments.
    if len(line_vector) == num_args: return Err("Expected number of arguments ({}) does not match the actual number of arguments ({})!".format(num_args, len(line_vector)))

    instruction: int = 0
    instruction |= opcode << (INS_LENGTH - OP_LENGTH)
    
    if potential_opcode not in CONSTANT_NO_ARG_OPCODES:
        match mode:
            
            case InstructionMode.Register:
                
                _, reg_a_str, reg_b_str, reg_c_str = line_vector
                
                reg_a = CONSTANT_REGISTER_MAP[reg_a_str]
                reg_b = CONSTANT_REGISTER_MAP[reg_b_str]
                reg_c = CONSTANT_REGISTER_MAP[reg_c_str]
                
                instruction |= reg_a << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 1))
                instruction |= reg_b << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 2))
                instruction |= reg_c << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 3))
                
                # TODO: SHAMT and FUNC are not implemented yet
                
            case InstructionMode.Immediate:
                
                _, *arguments = line_vector
                
                # Immediate loads/stores have 2 arguments
                if len(arguments) == 2:
                
                    value = int(arguments[0])
                    reg = CONSTANT_REGISTER_MAP[arguments[1]]
                    
                    instruction |= reg << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 1))
                    instruction |= value
                
                # Immediate operations have 3 arguments
                elif len(arguments) == 3:
                
                    value = int(arguments[0])
                    src_reg = CONSTANT_REGISTER_MAP[arguments[1]]
                    dest_reg = CONSTANT_REGISTER_MAP[arguments[2]]
                    
                    instruction |= src_reg  << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 1))
                    instruction |= dest_reg << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 2))
                    instruction |= value
                
                else:
                    return Err("Invalid number of arguments found in instruction '{}'!".format(line))
                
            case InstructionMode.Jump:
                
                _, address_str = line_vector
                
                address = int(address_str)
                
                instruction |= address
                
    return Ok(instruction)

def decode(encoded_instruction: int) -> Result[str, str]:
    """Decodes an integer-encoded instruction."""
    
    ret_list = []
    binary_instruction: str = get_encoded_instruction_as_binary(encoded_instruction)
    
    opcode_id = get_opcode(encoded_instruction).unwrap()
    opcode = get_opcode_from_id(opcode_id).unwrap()
    (_, argc, instruction_mode, *_) = CONSTANT_OPCODE_MAP[opcode]
    
    builder = ""
    builder += opcode

    if opcode not in CONSTANT_NO_ARG_OPCODES:
        builder += " "
        match instruction_mode:
            case InstructionMode.Register:
                ret_list = decode_register_instruction_as_list(binary_instruction)
                (_, bin_reg1, bin_reg2, bin_reg3, bin_shamt, bin_func) = ret_list
                reg1 = CONSTANT_REGISTER_MAP.inverse[int(bin_reg1, 2)]
                reg2 = CONSTANT_REGISTER_MAP.inverse[int(bin_reg2, 2)]
                reg3 = CONSTANT_REGISTER_MAP.inverse[int(bin_reg3, 2)]
                
                # TODO: Implement shift amount and function
                # shamt = int(bin_shamt, 2)
                # func = int(bin_func, 2)
                           
                builder += reg1
                builder += " "
                builder += reg2
                builder += " "
                builder += reg3
                
            case InstructionMode.Immediate:
                ret_list = decode_immediate_instruction_as_list(binary_instruction)
                (_, bin_src_reg, bin_dest_reg, _, bin_value) = ret_list
                src_reg_id = int(bin_src_reg, 2)
                src_reg = CONSTANT_REGISTER_MAP.inverse[src_reg_id]
                value = str(int(bin_value, 2))
                builder += value
                builder += " "
                builder += src_reg
                
                # If this is an immediate operator instruction, it has 3 arguments
                if argc == 3:
                    dest_reg_id = int(bin_dest_reg, 2)
                    dest_reg = CONSTANT_REGISTER_MAP.inverse[dest_reg_id]
                    builder += " "
                    builder += dest_reg
                
            case InstructionMode.Jump:
                ret_list = decode_jump_instruction_as_list(binary_instruction)
                (_, bin_address) = ret_list
                address = str(int(bin_address, 2))
                builder += address

    return Ok(builder)

def instruction_string(instruction: int, p_mode: PrintMode) -> Result[str, str]:
    builder: str = ""
    
    i_mode: InstructionMode = get_instruction_mode(instruction)
    
    # Convert the intruction to a binary string
    instruction_str: str = format(instruction, "032b")
    
    match p_mode:
        
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
                case InstructionMode.Register:
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