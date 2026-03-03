#ifndef BACKPLANE_H
#define BACKPLANE_H

#include "cpu.h"
#include "bus.h"

typedef struct {
    cpu_t* cpu;
    memory_t* memory;

    bus32_t address_bus;
    bus8_t data_bus;
} backplane_t;

void backplane_reset(backplane_t* backplane);
bool backplane_bus_active(backplane_t* backplane);
bool backplane_(backplane_t* backplane);

#endif