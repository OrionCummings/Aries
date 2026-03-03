#ifndef DEFS_H
#define DEFS_H

#include <stdint.h>
#include "debug.h"
#include "util.h"

#define PAGE_SIZE (4096)

typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;

typedef u32 address_t;
typedef u32 instruction_t;
typedef u8 reg_t;

typedef u16 instr_value_t;

typedef u8 pin_t;

typedef u8 page_t[PAGE_SIZE];

#endif