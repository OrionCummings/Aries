#ifndef CPU_H
#define CPU_H

#include <stdio.h>

#include "register_file.h"
#include "alu.h"
#include "control_unit.h"
#include "memory.h"

typedef struct {
    bus32_t bus;
    register_file_t regs;
    // control_unit_t cu;
    alu_t alu;
} cpu_t;

void cpu_reset(cpu_t* cpu);

void cpu_step(cpu_t* cpu, memory_t* mem);
instruction_t mem_get_byte(memory_t* mem, address_t addr); // why is this here?

#endif