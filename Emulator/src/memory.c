#include "memory.h"

void memory_reset(memory_t* memory) {
    A_INFO("memory reset");

    // memset(memory->memory, 0, MEMORY_SIZE_ALL); // Segfaults; why?
}

bool memory_read(const memory_t* memory, u8* data, address_t address) {
    if (memory == NULL) { return false; }
    if (data == NULL) { return false; }
    if (address > MEMORY_SIZE_ALL_BYTES) { return false; }
    *data = memory->memory[address];
    return true;
}

bool memory_write(memory_t* memory, u8 data, address_t address) {
    if (memory == NULL) { return false; }
    if (address > MEMORY_SIZE_ALL_BYTES) { return false; }
    memcpy(memory->memory + address, &data, sizeof(data));
    return true;
}

void memory_print(memory_t* const memory) {
    _hex_dump(memory->memory, MEMORY_SIZE_ALL_BYTES);
}

void _hex_dump(u8* data, size_t size) {

    // TODO: Maybe use this?
    static char* ASCII_CONTROL_CHARACTER_SYMBOLS[] = {
        "NUL",
        "SOH",
        "STX",
        "ETX",
        "EOT",
        "ENQ",
        "ACK",
        "BEL",
        "BS ",
        "HT ",
        "LF ",
        "VT ",
        "FF ",
        "CR ",
        "SO ",
        "SI ",
        "DLE",
        "DC1",
        "DC2",
        "DC3",
        "DC4",
        "NAK",
        "SYN",
        "ETB",
        "CAN",
        "EM ",
        "SUB",
        "ESC",
        "FS ",
        "GS ",
        "RS ",
        "US "
    };

    // TODO: improve this function with constexpr when it's finally added to by EDC 0_0
    char c = '\0';
    bool curr_matched = false;
    bool prev_matched = false;
    char curr[MEMORY_PRINT_CHUCK_SIZE] = { 0 };
    char prev[MEMORY_PRINT_CHUCK_SIZE] = { 0 };

    // For every 16 byte chunk
    for (size_t i = 0; i <= size - MEMORY_PRINT_CHUCK_SIZE; i += MEMORY_PRINT_CHUCK_SIZE) {

        // Get the next 16 bytes
        void* next_chunk = data + i;
        memcpy(curr, next_chunk, MEMORY_PRINT_CHUCK_SIZE);

        // Compare with the previous 16 bytes
        curr_matched = (memcmp(curr, prev, MEMORY_PRINT_CHUCK_SIZE) == 0);

        // TODO: Fix this.
        // If they are equal, then print a star and move on
        if (curr_matched) {
            if (!prev_matched) {
                printf("*\n");
            }
        } else {
            printf("0x%04X:", (unsigned int)(i & 0xFF));

            for (u8 j = 0; j < MEMORY_PRINT_CHUCK_SIZE; ++j) {
                c = curr[j];
                printf(" %02X", c & 0xFF);
            }

            printf(" |");

            for (u8 j = 0; j < MEMORY_PRINT_CHUCK_SIZE; ++j) {
                c = curr[j];

                // Only print the printable set! I don't want to deal with the control characters.
                if (c >= 32) {
                    printf(" %c", c);
                }

            }

            printf("\n");
        }

        // Update the previous chuck
        memcpy(prev, curr, MEMORY_PRINT_CHUCK_SIZE);
        prev_matched = curr_matched;
    }

    ////////////////////////////////////////////////////////////////////////////////

    // char current_line[17];
    // size_t i, j;
    // current_line[16] = '\0';
    // for (i = 0; i < size; ++i) {
    //     printf("%02X ", ((unsigned char*)data)[i]);
    //     if (((unsigned char*)data)[i] >= ' ' && ((unsigned char*)data)[i] <= '~') {
    //         current_line[i % 16] = ((char*)data)[i];
    //     } else {
    //         current_line[i % 16] = '.';
    //     }
    //     if ((i + 1) % 8 == 0 || i + 1 == size) {
    //         printf(" ");
    //         if ((i + 1) % 16 == 0) {
    //             printf("|  %s \n", current_line);
    //         } else if (i + 1 == size) {
    //             current_line[(i + 1) % 16] = '\0';
    //             if ((i + 1) % 16 <= 8) {
    //                 printf(" ");
    //             }
    //             for (j = (i + 1) % 16; j < 16; ++j) {
    //                 printf("   ");
    //             }
    //             printf("|  %s \n", current_line);
    //         }
    //     }
    // }
}
