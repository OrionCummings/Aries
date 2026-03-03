#include "register_file.h"

void register_file_print(const register_file_t reg_file, bool verbose) {

    printf("a  = 0x%08x b  = 0x%08x c  = 0x%08x d  = 0x%08x\n", reg_file.a, reg_file.b, reg_file.c, reg_file.d);
    printf("e  = 0x%08x f  = 0x%08x g  = 0x%08x h  = 0x%08x\n", reg_file.e, reg_file.f, reg_file.g, reg_file.h);
    printf("i  = 0x%08x j  = 0x%08x k  = 0x%08x l  = 0x%08x\n", reg_file.i, reg_file.j, reg_file.k, reg_file.l);

    if (verbose) {
        printf("sp = 0x%08x bp = 0x%08x pc = 0x%08x\n", reg_file.stack_pointer, reg_file.base_pointer, reg_file.program_counter);
        printf("z = %01d c = %01d p = %01d s = %01d o = %01d t = %01d r = %01d\n", reg_file.zero, reg_file.carry, reg_file.parity, reg_file.sign, reg_file.overflow, reg_file.trap, reg_file._reserved);
    } else {
        printf("sp = 0x%08x bp = 0x%08x pc = 0x%08x fl = 0b%08b\n",
            reg_file.stack_pointer, reg_file.base_pointer, reg_file.program_counter, reg_file.flags);
    }
}