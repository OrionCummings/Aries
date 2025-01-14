
from option import Result, Err, Ok
from BitManipulation import bit_mask
from Constants import CONSTANT_OPCODE_MAP, CONSTANT_REGISTER_MAP, FF_LENGTH, FUNC_LENGTH, IMM_LENGTH, INS_LENGTH, OP_LENGTH, REG_LENGTH, SHAMT_LENGTH, InstructionFormat
from PrettyPrinting import PrintMode
from Utilities import get_opcode_from_id, debug, trace

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
        return trace(f"unknown type")

def get_instruction_mode(instruction: str | int) -> Result[InstructionFormat, str]:
    if isinstance(instruction, str):
        opcode = instruction.split(" ")[0]
    elif isinstance(instruction, int):
        decoded_instruction = decode(instruction).unwrap()
        opcode = decoded_instruction.split(" ")[0]
    else:
        return trace(f"unknown type '{type(instruction)}'")
    
    if opcode in CONSTANT_OPCODE_MAP:
        opcode_tuple = CONSTANT_OPCODE_MAP[opcode]
    else:
        return trace(f"unknown opcode '{opcode}'")
    (_, _, i_mode, *_) = opcode_tuple

    return Ok(i_mode)

def is_valid_opcode(opcode: str) -> bool:
    return opcode in CONSTANT_OPCODE_MAP

def get_encoded_instruction_as_binary(encoded_instruction: int):
    return format(encoded_instruction, "032b")

def decode_simple_instruction_as_list(binary_instruction: str) -> list:
    opcode  = binary_instruction[:OP_LENGTH]
    return [opcode]

def decode_register_instruction_as_list(binary_instruction: str) -> list:
    opcode = binary_instruction[:OP_LENGTH]
    reg_a  = binary_instruction[OP_LENGTH : OP_LENGTH + (1 * REG_LENGTH)]
    reg_b  = binary_instruction[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
    reg_c  = binary_instruction[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH)]
    shamt  = binary_instruction[OP_LENGTH + (3 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH) + SHAMT_LENGTH]
    func   = binary_instruction[-FUNC_LENGTH:]
    return [opcode, reg_a, reg_b, reg_c, shamt, func]

def decode_immediate_instruction_as_list(binary_instruction: str) -> list:
    opcode = binary_instruction[:OP_LENGTH]
    reg_a  = binary_instruction[OP_LENGTH : OP_LENGTH + REG_LENGTH]
    reg_b  = binary_instruction[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
    unk    = binary_instruction[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH) + FF_LENGTH]
    value  = binary_instruction[-IMM_LENGTH:]
    return [opcode, reg_a, reg_b, unk, value]

def decode_jump_instruction_as_list(binary_instruction: str) -> list:
    opcode  = binary_instruction[:OP_LENGTH]
    address = binary_instruction[OP_LENGTH:]
    return [opcode, address]

# TODO: This should not be a thing: why are compare instruction treated differently??
# Just differentiate in encode()???
def decode_compare_instruction_as_list(binary_instruction: str) -> list:
    opcode = binary_instruction[:OP_LENGTH]
    reg_a  = binary_instruction[OP_LENGTH : OP_LENGTH + (1 * REG_LENGTH)]
    reg_b  = binary_instruction[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
    return [opcode, reg_a, reg_b]

def encode(line: str) -> Result[int, str]:
        
    # Create the line vector
    line_vector = line.split(' ')
    if len(line_vector) < 1: return Err(f"{debug()} malformed instruction '{line}' (too few arguments)")
    if len(line_vector) > 4: return Err(f"{debug()} malformed instruction '{line}' (too many arguments)")
    
    # Get the potential opcode
    potential_opcode = line_vector[0]
    
    # Check that it's a valid opcode
    if not is_valid_opcode(potential_opcode): return Err(f"{debug()} unknown opcode '{potential_opcode}'")
    
    # Get the opcode tuple and extract the important information
    opcode_tuple = CONSTANT_OPCODE_MAP[potential_opcode]
    (opcode, num_args, mode, *unused) = opcode_tuple
    
    # Check that the number of expected arguments matches the number of actual arguments.
    # The line vector includes the opcode, whereas the num_args constant does not => +1
    if len(line_vector) != num_args+1:
        return trace(f"expected number of arguments ({num_args+1}) does not match the actual number of arguments ({len(line_vector)})")

    instruction: int = 0
    instruction |= opcode << (INS_LENGTH - OP_LENGTH)
    
    match mode:
        
        case InstructionFormat.Simple:

            # Do nothing
            pass

        case InstructionFormat.Register:
            
            # Try to unpack the line vector. If this fails on a ValueError,
            # then we are likely trying to unpack something with the 
            # incorrect number of arguments, so return an error!
            try:
                _, reg_a_str, reg_b_str, reg_c_str = line_vector
            except ValueError:
                return trace(f"unexpected number of arguments in line '{line}'")
                
            reg_a = CONSTANT_REGISTER_MAP[reg_a_str]
            reg_b = CONSTANT_REGISTER_MAP[reg_b_str]
            reg_c = CONSTANT_REGISTER_MAP[reg_c_str]
            
            instruction |= reg_a << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 1))
            instruction |= reg_b << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 2))
            instruction |= reg_c << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 3))
            
            # TODO: SHAMT and FUNC are not implemented yet
            
        case InstructionFormat.Immediate:
            
            _, *arguments = line_vector
            
            # Immediate loads/stores have 2 arguments
            if len(arguments) == 2:
            
                potential_value_str = arguments[0]

                try:
                    potential_value = int(potential_value_str)
                except ValueError:
                    if isinstance(potential_value_str, str):
                        # If this is a register, then the programmer probably mixed up the order of arguments
                        if potential_value_str in CONSTANT_REGISTER_MAP.keys():
                            return trace(f"str value '{potential_value_str}' found; did you mix up the order or arguments?")
                        return trace(f"str value '{potential_value_str}' found")
                    return trace(f"unknown value '{potential_value_str}' found")

                # TODO: This could be handled with a psuedoinstruction!
                if potential_value >= 2**16:
                    return trace(f"failed to encode immediate value '{potential_value}' as it is too large (>= 2^16)")

                potential_reg = arguments[1]
                if potential_reg not in CONSTANT_REGISTER_MAP.keys():
                    return trace(f"parsed invalid register '{potential_reg}'")

                reg = CONSTANT_REGISTER_MAP[potential_reg]
                
                instruction |= reg << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 1))
                instruction |= potential_value
            
            # Immediate operations have 3 arguments
            elif len(arguments) == 3:
            
                value = int(arguments[0])
                src_reg = CONSTANT_REGISTER_MAP[arguments[1]]
                dest_reg = CONSTANT_REGISTER_MAP[arguments[2]]
                
                instruction |= src_reg  << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 1))
                instruction |= dest_reg << (INS_LENGTH - OP_LENGTH - (REG_LENGTH * 2))
                instruction |= value
            
            else:
                return trace(f"invalid number of arguments found in instruction '{line}'")
            
        case InstructionFormat.Jump:
            
            _, address_str = line_vector
            address = int(address_str)
            instruction |= address
                
    return Ok(instruction)

def decode(encoded_instruction: int) -> Result[str, str]:
    """Decodes an integer-encoded instruction."""
    
    ret_list = []
    binary_instruction: str = get_encoded_instruction_as_binary(encoded_instruction)
    
    # Given an encoded instruction, attempt to get the opcode
    r_opcode_id = get_opcode(encoded_instruction)
    if r_opcode_id.is_err:
        return Err(r_opcode_id.unwrap_err())
    opcode_id = r_opcode_id.unwrap()

    # Given an opcode id, attempt to get the opcode
    r_opcode = get_opcode_from_id(opcode_id)
    if r_opcode.is_err:
        return Err(r_opcode.unwrap_err())
    opcode = r_opcode.unwrap()

    # Use the opcode to look up in the dictionary of opcodes for
    # the relavent information
    (_, argc, instruction_mode, *_) = CONSTANT_OPCODE_MAP[opcode]
    
    builder = ""
    builder += opcode

    match instruction_mode:
        case InstructionFormat.Simple:

            # Do nothing; the opcode is already appended above
            pass

        case InstructionFormat.Register:
            ret_list = decode_register_instruction_as_list(binary_instruction)
            (_, bin_reg1, bin_reg2, bin_reg3, bin_shamt, bin_func) = ret_list
            reg1 = CONSTANT_REGISTER_MAP.inverse[int(bin_reg1, 2)]
            reg2 = CONSTANT_REGISTER_MAP.inverse[int(bin_reg2, 2)]
            reg3 = CONSTANT_REGISTER_MAP.inverse[int(bin_reg3, 2)]
            
            # TODO: Implement shift amount and function
            # shamt = int(bin_shamt, 2)
            # func = int(bin_func, 2)
            
            builder += " "
            builder += reg1
            builder += " "
            builder += reg2
            builder += " "
            builder += reg3
            
        case InstructionFormat.Immediate:
            ret_list = decode_immediate_instruction_as_list(binary_instruction)
            (_, bin_src_reg, bin_dest_reg, _, bin_value) = ret_list
            src_reg_id = int(bin_src_reg, 2)
            src_reg = CONSTANT_REGISTER_MAP.inverse[src_reg_id]
            value = str(int(bin_value, 2))

            builder += " "
            builder += value
            builder += " "
            builder += src_reg
            
            # If this is an immediate operator instruction, it has 3 arguments
            if argc == 3:
                dest_reg_id = int(bin_dest_reg, 2)
                dest_reg = CONSTANT_REGISTER_MAP.inverse[dest_reg_id]
                builder += " "
                builder += dest_reg
            
        case InstructionFormat.Jump:
            ret_list = decode_jump_instruction_as_list(binary_instruction)
            (_, bin_address) = ret_list
            address = str(int(bin_address, 2))
            builder += " "
            builder += address

        case InstructionFormat.Compare:
            ret_list = decode_compare_instruction_as_list(binary_instruction)
            (_, bin_reg1, bin_reg2) = ret_list
            reg1 = CONSTANT_REGISTER_MAP.inverse[int(bin_reg1, 2)]
            reg2 = CONSTANT_REGISTER_MAP.inverse[int(bin_reg2, 2)]

            builder += " "
            builder += reg1
            builder += " "
            builder += reg2

    return Ok(builder)

def instruction_string(instruction: int, p_mode: PrintMode) -> Result[str, str]:
    builder: str = ""
    
    i_mode: InstructionFormat = get_instruction_mode(instruction)
    
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
                case InstructionFormat.Register:
                    opcode   = instruction_str[:OP_LENGTH]
                    reg_a    = instruction_str[OP_LENGTH : OP_LENGTH + (1 * REG_LENGTH)]
                    reg_b    = instruction_str[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
                    reg_c    = instruction_str[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH)]
                    shamt    = instruction_str[OP_LENGTH + (3 * REG_LENGTH) : OP_LENGTH + (3 * REG_LENGTH) + SHAMT_LENGTH]
                    func     = instruction_str[-FUNC_LENGTH:]
                    builder += " ".join([opcode, reg_a, reg_b, reg_c, shamt, func])
                    
                case InstructionFormat.Immediate:
                    opcode  = instruction_str[:OP_LENGTH]
                    reg_a   = instruction_str[OP_LENGTH : OP_LENGTH + REG_LENGTH]
                    reg_b   = instruction_str[OP_LENGTH + (1 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH)]
                    unk     = instruction_str[OP_LENGTH + (2 * REG_LENGTH) : OP_LENGTH + (2 * REG_LENGTH) + FF_LENGTH]
                    value   = instruction_str[-IMM_LENGTH:]
                    builder += " ".join([opcode, reg_a, reg_b, unk, value])
                    
                case InstructionFormat.Jump:
                    opcode  = instruction_str[:OP_LENGTH]
                    address = instruction_str[OP_LENGTH:]
                    builder += " ".join([opcode, address])
    
    return Ok(builder)