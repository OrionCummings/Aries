#include "cpu.h"
#include "memory.h"
#include "user_input.h"
#include "backplane.h"

static backplane_t backplane;
static bus32_t address_bus;
static bus8_t data_bus;

void system_reset() {
    backplane_reset(&backplane);

    backplane.cpu.regs.program_counter = MEMORY_PROGRAM_START;
}

void init(void) {

    // Set the SIGINT callback
    signal(SIGINT, sigint_handler);

    backplane_init(&backplane, &address_bus, &data_bus);

    // Reset the system at the end of initialization
    system_reset();
}

void deinit(void) {
}

void loop(void) {

    // Disable stdin buffering
    set_non_canonical_mode();
    int c;
    while ((c = getchar()) != TERMINAL_KEY_ESC) {
        printf("key = %c (%i)\n", c, c);

        // Enable stdin buffering so characters can be polled from stdin without hitting enter
        reset_canonical_mode();

        switch (c) {
            case (TERMINAL_KEY_SPACE): {
                cpu_step(&backplane.cpu, &backplane.memory);
                break;
            }

            case (TERMINAL_KEY_R): {
                register_file_print(backplane.cpu.regs, false);
                break;
            }

            case (TERMINAL_KEY_R_CAP): {
                register_file_print(backplane.cpu.regs, true);
                break;
            }

            case (TERMINAL_KEY_M): {
                memory_print(&backplane.memory);
                break;
            }

            case (TERMINAL_KEY_E): {
                // cpu_exec(&cpu, &memory);
                break;
            }

            case (TERMINAL_KEY_H): {
                // cpu_halt(&cpu);
                break;
            }

            case (TERMINAL_KEY_BSLASH): {
                command_handle();
                break;
            }

            case (TERMINAL_KEY_X): { // eXperimental

                static uint8_t n = 0;
                backplane.address_bus->dword = n++;

                printf("backplane.address_bus.dword = 0x%X\n", backplane.address_bus->dword);
                printf("backplane.memory.address_bus.dword = 0x%X\n", backplane.memory.address_bus->dword);

                break;
            }

            default: {
                // Not handled
            }
        };
        // Disable stdin buffering for the next loop
        set_non_canonical_mode();
    }
    // Enable stdin buffering so the console behaves as expected after the program returns
    reset_canonical_mode();
}

int main(void) {

    init();
    loop();
    deinit();

    return 0;
}