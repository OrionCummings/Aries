#ifndef REGISTER_FILE_H
#define REGISTER_FILE_H

#include <stdint.h>
#include "defs.h"

typedef struct {
    reg a;
    reg b;
    reg c;
    reg d;
    reg e;
    reg f;
    reg g;
    reg h;
    reg i;
    reg j;
    reg k;
    reg l;
    reg stack_pointer;
    reg base_pointer;
    reg program_counter;
    union {
        reg flags;
        struct {
            reg zero : 1;
            reg carry : 1;
            reg parity : 1;
            reg sign : 1;
            reg overflow : 1;
            reg interrupt : 1;
            reg trap : 1;
            reg hpc : 1;
        };
    } flags;
} register_file;

#endif