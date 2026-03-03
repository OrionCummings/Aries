#ifndef INSTRUCTION_H
#define INSTRUCTION_H

#include "defs.h"

#define INSTR_WIDTH (32)
#define OPCODE_WIDTH (6)
#define JUMP_ADDR_WIDTH (INSTR_WIDTH - OPCODE_WIDTH)
#define REG_WIDTH (6)

typedef enum : u8 {
    IF_UNKNOWN,

    /// @brief A jump instruction.
    /// 
    /// OPCODE    ADDRESS
    /// XXXXXX    XXXXXXXXXXXXXXXXXXXXXXXXXX
    /// 6         26
    /// 0-6       7-32
    IF_JUMP,

    /// Register                        [UNUSED] [UNUSED]
    /// OPCODE    REGA    REGB    REGC    SHAMT   FUNC
    /// XXXXXX    XXXX    XXXX    XXXX    XXXXX   XXXXXXXXX
    /// 6         4       4       4       5       9
    /// 0-6       7-10    11-14   15-18   19-23   24-32
    IF_REGISTER,

    /// @brief An immediate instruction.
    /// Immediate              [UNUSED]
    /// OPCODE    REGA    REGB    FF    VALUE
    /// XXXXXX    XXXX    XXXX    XX    XXXXXXXXXXXXXXXX
    /// 6         4       4       2     16
    /// 0-6       7-10    11-14   15-17 18-32
    IF_IMMEDIATE,
} instruction_format_t;

typedef enum : u8 {
    OPC_NOP,
    OPC_RET,
    OPC_HLT,
    OPC_ADD,
    OPC_ADDI,
    OPC_LDI,
    OPC_LD,
    OPC_ST,
    OPC_BNE,
    OPC_J,
    OPC_CALL,
    OPC_CMP,
} opcode_t;

static const instruction_format_t OPCODE_FORMAT[] = {
    [OPC_NOP] = IF_JUMP,
    [OPC_RET] = IF_JUMP,
    [OPC_HLT] = IF_JUMP,
    [OPC_ADD] = IF_REGISTER,
    [OPC_ADDI] = IF_IMMEDIATE,
    [OPC_LDI] = IF_IMMEDIATE,
    [OPC_LD] = IF_UNKNOWN, // TODO
    [OPC_ST] = IF_UNKNOWN, // TODO
    [OPC_BNE] = IF_UNKNOWN, // TODO
    [OPC_J] = IF_JUMP,
    [OPC_CALL] = IF_JUMP,
    [OPC_CMP] = IF_REGISTER,
};

static const char* const OPCODE_NAMES[] = {
    [OPC_NOP] = "nop",
    [OPC_RET] = "ret",
    [OPC_HLT] = "hlt",
    [OPC_ADD] = "add",
    [OPC_ADDI] = "addi",
    [OPC_LDI] = "ldi",
    [OPC_LD] = "ld",
    [OPC_ST] = "st",
    [OPC_BNE] = "bne",
    [OPC_J] = "j",
    [OPC_CALL] = "call",
    [OPC_CMP] = "cmp",
};

opcode_t instr_get_opcode(instruction_t instr);
reg_t instr_get_reg_1(instruction_t instr);
reg_t instr_get_reg_2(instruction_t instr);
reg_t instr_get_reg_3(instruction_t instr);
instr_value_t instr_get_value(instruction_t instr);
address_t instr_get_address(instruction_t instr);

instruction_format_t instr_get_format(instruction_t instr);

#endif