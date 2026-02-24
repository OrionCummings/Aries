#include "backplane.h"

void backplane_reset(backplane_t* backplane) {
    A_INFO("reset backplane");

    cpu_reset(backplane->cpu);
    memory_reset(backplane->memory);
}