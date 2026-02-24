#include "cpu.h"
#include "memory.h"
#include "user_input.h"
#include "backplane.h"

static cpu_t cpu;
static memory_t memory;
static backplane_t backplane;

void system_reset() {
    backplane_reset(&backplane);
}

void init(void) {

    // Set the SIGINT callback
    signal(SIGINT, sigint_handler);

    system_reset();

    cpu.regs.program_counter = MEMORY_PROGRAM_START;
}

void deinit(void) {
}

void loop(void) {
    set_non_canonical_mode();
    int c;
    while ((c = getchar()) != TERMINAL_KEY_ESC) {
        reset_canonical_mode();

        switch (c) {
            case (TERMINAL_KEY_SPACE): {
                cpu_step(&cpu, &memory);
                break;
            }

            case (TERMINAL_KEY_R): {
                register_file_print(cpu.regs, false);
                break;
            }

            case (TERMINAL_KEY_R_CAP): {
                register_file_print(cpu.regs, true);
                break;
            }

            case (TERMINAL_KEY_M): {
                memory_print(&memory);
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

            default: {
                // Not handled
            }
        };

        set_non_canonical_mode();
    }
    reset_canonical_mode();
}

int main(void) {

    init();

    // TODO: TEST CODE
    for (u32 i = 0; i <= 0xFF; ++i) {
        memory_write(&memory, i & 0xFF, (address_t)i);
    }

    memory_print(&memory);

    loop();
    deinit();

    return 0;
}