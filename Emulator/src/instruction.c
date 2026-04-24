#include "instruction.h"

opcode_t instr_get_opcode(instruction_t instr) {
    return (opcode_t)extract_bits(instr, INSTR_WIDTH - OPCODE_WIDTH, INSTR_WIDTH);
}

instr_reg_t instr_get_reg_1(instruction_t instr) {
    return (instr_reg_t)extract_bits(instr, INSTR_WIDTH - OPCODE_WIDTH - REG_WIDTH, INSTR_WIDTH - OPCODE_WIDTH);
}

instr_reg_t instr_get_reg_2(instruction_t instr) {
    return (instr_reg_t)extract_bits(instr, INSTR_WIDTH - OPCODE_WIDTH - REG_WIDTH - REG_WIDTH, INSTR_WIDTH - OPCODE_WIDTH - REG_WIDTH);
}

instr_reg_t instr_get_reg_3(instruction_t instr) {
    return (instr_reg_t)extract_bits(instr, INSTR_WIDTH - OPCODE_WIDTH - REG_WIDTH - REG_WIDTH - REG_WIDTH, INSTR_WIDTH - OPCODE_WIDTH - REG_WIDTH - REG_WIDTH);
}

instr_value_t instr_get_value(instruction_t instr) {
    return (instr_value_t)extract_bits(instr, 0, 16);
}

address_t instr_get_address(instruction_t instr) {
    return (address_t)extract_bits(instr, 0, 26);
}

instruction_format_t instr_get_format(instruction_t instr) {
    opcode_t opcode = instr_get_opcode(instr);
    return OPCODE_FORMAT[opcode];
}

