#ifndef MEMORY_H
#define MEMORY_H

#include "defs.h"
#include "bus.h"

#define MEMORY_SIZE_ZERO_BYTES (1u)
#define MEMORY_SIZE_PROGRAM_BYTES (32768u)
#define MEMORY_SIZE_SCRATCH_BYTES (32759u)
#define MEMORY_SIZE_MEMMAP_BYTES (8u)
#define MEMORY_SIZE_ALL_BYTES (MEMORY_SIZE_ZERO_BYTES + MEMORY_SIZE_PROGRAM_BYTES + MEMORY_SIZE_SCRATCH_BYTES + MEMORY_SIZE_MEMMAP_BYTES)

#define MEMORY_ZERO_START    ((address_t)(0u))
#define MEMORY_PROGRAM_START ((address_t)(MEMORY_ZERO_START + MEMORY_SIZE_ZERO_BYTES))
#define MEMORY_SCRATCH_START ((address_t)(MEMORY_PROGRAM_START + MEMORY_SIZE_PROGRAM_BYTES))
#define MEMORY_MEMMAP_START ((address_t)(MEMORY_SCRATCH_START + MEMORY_SIZE_SCRATCH_BYTES))

#define MEMORY_SIZE_VIDEO_BYTES (32768u)

#define MEMORY_PRINT_CHUCK_SIZE (8u)

#define MEMORY_CONTROL_BIT_VCC          (0u)
#define MEMORY_CONTROL_BIT_GND          (1u)
#define MEMORY_CONTROL_BIT_CLK          (2u)
#define MEMORY_CONTROL_BIT_ENABLED      (3u)
#define MEMORY_CONTROL_BIT_ACTION       (4u)
#define MEMORY_CONTROL_BIT_VIDEO        (5u)

#define MEMORY_CONTROL_MASK_VCC         (1u << MEMORY_CONTROL_BIT_VCC)
#define MEMORY_CONTROL_MASK_GND         (1u << MEMORY_CONTROL_BIT_GND)
#define MEMORY_CONTROL_MASK_CLK         (1u << MEMORY_CONTROL_BIT_CLK)
#define MEMORY_CONTROL_MASK_ENABLED     (1u << MEMORY_CONTROL_BIT_ENABLED)
#define MEMORY_CONTROL_MASK_ACTION      (1u << MEMORY_CONTROL_BIT_ACTION)
#define MEMORY_CONTROL_MASK_VIDEO       (1u << MEMORY_CONTROL_BIT_VIDEO)

/// @brief The memory layout of the Aries CPU.
typedef struct {

    union {
        bus8_t control;
        struct {
            pin_t vcc : 1;
            pin_t gnd : 1;
            pin_t clk : 1;
            pin_t enabled : 1;
            pin_t action : 1;
            pin_t video : 1;
            pin_t : 3;
        };
    };

    // The memory layout
    union {
        u8 ram[MEMORY_SIZE_ALL_BYTES];
        struct {
            u8 zero_memory[MEMORY_SIZE_ZERO_BYTES];
            u8 program_memory[MEMORY_SIZE_PROGRAM_BYTES];
            u8 scratch_memory[MEMORY_SIZE_SCRATCH_BYTES];
            u8 memmap_memory[MEMORY_SIZE_MEMMAP_BYTES];
        };
    };

    union {
        u8 vram[MEMORY_SIZE_VIDEO_BYTES];
        // TODO: Create a VRAM memory map
    };

    // The address to be read
    bus32_t* address_bus;

    // The byte at the specified address
    bus8_t* data_bus;

} memory_t;

void memory_file_tick(memory_t* const memory);

void memory_reset(memory_t* memory);

void memory_print(memory_t* const memory);

bool memory_read(const memory_t* memory, u8* data, address_t address);
bool memory_write(memory_t* memory, u8 data, address_t address);

bool memory_load_bytes(memory_t* memory, u8* data, size_t num, address_t address);

/// @brief Private function. Prints a hex dump of the given object. Based on https://gist.github.com/ccbrown/9722406.
/// @param data The object to be dumped.
/// @param size The size of the object.
void _hex_dump(u8* data, size_t size);

#endif