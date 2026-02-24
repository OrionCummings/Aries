#ifndef ALU_H
#define ALU_H

#include "defs.h"

typedef struct {
    u32 a;
    u32 b;
    u32 opcode;
    u32 input_status;
    u32 output_status;
    u32 result;
} alu_t;

#endif