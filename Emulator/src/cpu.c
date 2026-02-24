#include "cpu.h"

void cpu_reset(cpu_t* cpu) {
    A_INFO("reset cpu");

}

void cpu_step(cpu_t* cpu, memory_t* mem) {

    printf("step\n");

    address_t pc = cpu->regs.program_counter;
    instruction_t instr = mem_get_byte(mem, pc);

}

instruction_t mem_get_byte(memory_t* mem, address_t addr) {
    return 0;
}
