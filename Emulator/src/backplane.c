#include "backplane.h"

void backplane_init(backplane_t* backplane, bus32_t* address_bus, bus8_t* data_bus) {
    backplane->address_bus = address_bus;
    backplane->memory.address_bus = address_bus;

    backplane->data_bus = data_bus;
    backplane->memory.data_bus = data_bus;
}

void backplane_reset(backplane_t* backplane) {
    A_INFO("reset backplane");

    cpu_reset(&backplane->cpu);
    memory_reset(&backplane->memory);
}