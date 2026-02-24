#ifndef INSTRUCTION_H
#define INSTRUCTION_H

#include "defs.h"

#define INSTR_WIDTH (32)
#define OPCODE_WIDTH (6)
#define JUMP_ADDR_WIDTH (INSTR_WIDTH - OPCODE_WIDTH)
#define REG_WIDTH (6)

typedef enum : u8 {
    IF_UNKNOWN,
    IF_JUMP,
    IF_REGISTER,
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

instruction_format_t get_instr_format(opcode_t opcode);
bool is_instr_format(instruction_t instr, instruction_format_t fmt);

#endif