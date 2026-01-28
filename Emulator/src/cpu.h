#ifndef CPU_H
#define CPU_H

#include "register_file.h"
#include "alu.h"
#include "control_unit.h"

typedef struct {
    register_file regs;
    control_unit cu;
    alu alu;
} cpu;

void execute(address);

#endif