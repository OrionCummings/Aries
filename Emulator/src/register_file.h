#ifndef reg_tISTER_FILE_H
#define reg_tISTER_FILE_H

#include <stdio.h>
#include <stdint.h>
#include "defs.h"

typedef struct {
    reg_t a;
    reg_t b;
    reg_t c;
    reg_t d;
    reg_t e;
    reg_t f;
    reg_t g;
    reg_t h;
    reg_t i;
    reg_t j;
    reg_t k;
    reg_t l;
    reg_t stack_pointer;
    reg_t base_pointer;
    reg_t program_counter;
    union {
        reg_t flags;
        struct {
            reg_t zero : 1;
            reg_t carry : 1;
            reg_t parity : 1;
            reg_t sign : 1;
            reg_t overflow : 1;
            reg_t interrupt : 1;
            reg_t trap : 1;
            reg_t _reserved : 1;
        };
    };
} register_file_t;

void register_file_print(const register_file_t reg_file, bool verbose);

#endif