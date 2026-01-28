#ifndef DEFS_H
#define DEFS_H

#include <stdint.h>

typedef uint32_t address;
typedef uint32_t instruction;
typedef uint32_t reg;

typedef enum : uint8_t {

    UNKNOWN = 0xFF,

    // Logical operations
    NOT = 0x00,
    AND,
    NAND,
    OR,
    NOR,
    XOR,
    XNOR,

    // Arithmetic operations
    ADD = 0x10,
    SUB,
    MUL,
    DIV,
    MOD,

} operation;

static const char* const OPERATION_NAMES[] = {
    [UNKNOWN] = "UNKNOWN",
    [NOT] = "NOT",
    [AND] = "AND",
    [NAND] = "NAND",
    [OR] = "OR",
    [NOR] = "NOR",
    [XOR] = "XOR",
    [XNOR] = "XNOR",
    [ADD] = "ADD",
    [SUB] = "SUB",
    [MUL] = "MUL",
    [DIV] = "DIV",
    [MOD] = "MOD",
};

static const char* const OPERATION_SYM[] = {
    [UNKNOWN] = "?",
    [NOT] = "!",
    [AND] = "&",
    [NAND] = "!&",
    [OR] = "|",
    [NOR] = "!|",
    [XOR] = "^",
    [XNOR] = "!^",
    [ADD] = "+",
    [SUB] = "-",
    [MUL] = "*",
    [DIV] = "/",
    [MOD] = "%%",
};

#endif