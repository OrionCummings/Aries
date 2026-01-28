#ifndef ALU_H
#define ALU_H

#include "defs.h"

typedef struct {
    uint32_t a;
    uint32_t b;
    uint32_t opcode;
    uint32_t input_status;
    uint32_t output_status;
    uint32_t result;
} alu;

#endif