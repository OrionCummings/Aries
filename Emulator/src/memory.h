#ifndef MEMORY_H
#define MEMORY_H

#include "defs.h"

#define MEMORY_SIZE_ZERO_BYTES (1)
#define MEMORY_SIZE_PROGRAM_BYTES (32768)
#define MEMORY_SIZE_SCRATCH_BYTES (32759)
#define MEMORY_SIZE_MEMMAP_BYTES (8)
#define MEMORY_SIZE_ALL_BYTES (MEMORY_SIZE_ZERO_BYTES + MEMORY_SIZE_PROGRAM_BYTES + MEMORY_SIZE_SCRATCH_BYTES + MEMORY_SIZE_MEMMAP_BYTES)
#define MEMORY_ZERO_START    ((address_t)(0))
#define MEMORY_PROGRAM_START ((address_t)(MEMORY_ZERO_START + MEMORY_SIZE_ZERO_BYTES))
#define MEMORY_SCRATCH_START ((address_t)(MEMORY_PROGRAM_START + MEMORY_SIZE_PROGRAM_BYTES))
#define MEMORY_MEMMAP_START ((address_t)(MEMORY_SCRATCH_START + MEMORY_SIZE_SCRATCH_BYTES))

#define MEMORY_PRINT_CHUCK_SIZE (8)

/// @brief The memory layout of the Aries CPU.
typedef struct {

    // The memory layout
    union {
        u8 memory[MEMORY_SIZE_ALL_BYTES];
        struct {
            u8 zero_memory[MEMORY_SIZE_ZERO_BYTES];
            u8 program_memory[MEMORY_SIZE_PROGRAM_BYTES];
            u8 scratch_memory[MEMORY_SIZE_SCRATCH_BYTES];
            u8 memmap_memory[MEMORY_SIZE_MEMMAP_BYTES];
        };
    };

    // The address to be read
    union {
        address_t address;
        struct {
            pin_t addr0 : 1;
            pin_t addr1 : 1;
            pin_t addr2 : 1;
            pin_t addr3 : 1;
            pin_t addr4 : 1;
            pin_t addr5 : 1;
            pin_t addr6 : 1;
            pin_t addr7 : 1;
            pin_t addr8 : 1;
            pin_t addr9 : 1;
            pin_t addr10 : 1;
            pin_t addr11 : 1;
            pin_t addr12 : 1;
            pin_t addr13 : 1;
            pin_t addr14 : 1;
            pin_t addr15 : 1;
            pin_t addr16 : 1;
            pin_t addr17 : 1;
            pin_t addr18 : 1;
            pin_t addr19 : 1;
            pin_t addr20 : 1;
            pin_t addr21 : 1;
            pin_t addr22 : 1;
            pin_t : 8;
            pin_t : 2;
        };
    };

    // The byte at the specified address
    union {
        u8 data;
        struct {
            pin_t data0 : 1;
            pin_t data1 : 1;
            pin_t data2 : 1;
            pin_t data3 : 1;
            pin_t data4 : 1;
            pin_t data5 : 1;
            pin_t data6 : 1;
            pin_t data7 : 1;
        };
    };

    union {
        u8 control;
        struct {
            pin_t vcc : 1;
            pin_t gnd : 1;
            pin_t clk : 1;
            pin_t enabled : 1;
            pin_t write : 1;
            pin_t read : 1;
            pin_t : 3;
        };
    };

} memory_t;

void memory_reset(memory_t* memory);

void memory_print(memory_t* const memory);

bool memory_read(const memory_t* memory, u8* data, address_t address);
bool memory_write(memory_t* memory, u8 data, address_t address);

/// @brief Private function. Prints a hex dump of the given object. Based on https://gist.github.com/ccbrown/9722406.
/// @param data The object to be dumped.
/// @param size The size of the object.
void _hex_dump(u8* data, size_t size);

#endif