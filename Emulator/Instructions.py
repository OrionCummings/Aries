
from option import Err, Ok, Result
from Constants import CONSTANT_OPCODE_MAP, InstructionMode
from CPU import CPU
from Transformations import decode, encode

def nop(cpu: CPU, instruction: int) -> Result[CPU, str]:
    """Executes a 'nop' instruction."""
    
    instruction_mnemonic = 'nop'
    r_verification = verify_opcode(instruction, instruction_mnemonic)
    if r_verification.is_err: return Err(r_verification.unwrap_err())

    return Ok(cpu)

def hlt(cpu: CPU, instruction: int) -> Result[CPU, str]:
    """Executes a 'hlt' instruction."""
    
    instruction_mnemonic = 'hlt'
    r_verification = verify_opcode(instruction, instruction_mnemonic)
    if r_verification.is_err: return Err(r_verification.unwrap_err())

    # Halt the CPU
    cpu.halt = True

    return Ok(cpu)

def add(cpu: CPU, instruction: int) -> Result[CPU, str]:
    """Executes an 'add' instruction."""
    
    instruction_mnemonic = 'add'
    r_verification = verify_opcode(instruction, instruction_mnemonic)
    if r_verification.is_err: return Err(r_verification.unwrap_err())

    # TODO: This code probably already exists in this project, so find and reuse it!
    # Or make it generic!

    opcode_tuple = CONSTANT_OPCODE_MAP[instruction_mnemonic]
    mode = opcode_tuple[2]

    if mode != InstructionMode.Register: return Err("Expected nemonic '{}' to be Register!".format(instruction_mnemonic))
    
    r_decoded_instruction_list = decode(instruction)
    if r_decoded_instruction_list.is_err: return Err(r_decoded_instruction_list.unwrap_err())
    decoded_instruction_list = r_decoded_instruction_list.unwrap()
    
    if decoded_instruction_list[0] != InstructionMode.Register:
        return Err("Extracted instruction mode '{}' does not match expected instruction mode '{}'".format(extraction[0], InstructionMode.Register))
    
    # BUG: This is stupid lol. Use ya damn classes
    # Get each register
    reg_a = cpu.register_file.registers[REGISTERIDS[int(extraction[1][1])]]
    reg_b = cpu.register_file.registers[REGISTERIDS[int(extraction[1][2])]]
    reg_c = cpu.register_file.registers[REGISTERIDS[int(extraction[1][3])]]
    
    # Perform the operation
    res = reg_a + reg_b
    
    # Save the result to the source register
    cpu.register_file.set_reg(reg_c, res)

    return Ok(cpu)

def addi(cpu: CPU, instruction: int) -> Result[CPU, str]:
    
    instruction_mnemonic = 'addi'
    
    
    print("Performed a '{}' instruction!".format(instruction_mnemonic))

def ldi(cpu: CPU, instruction: int) -> Result[CPU, str]:
    
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

# A list of all instruction functions
CONSTANT_INSTRUCTIONS = {
    
    "nop":      nop,    # 0
    "hlt":      hlt,    # 1
    "add":      add,    # 2
    "addi":     addi,   # 3
    "ldi":      ldi,    # 15
}
