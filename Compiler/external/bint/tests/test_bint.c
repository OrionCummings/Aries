#include "unity.h"
#include "arena.h"
#include "debug.h"
#include "test_bint.h"

#define TEST_ARENA_SIZE_BYTES (1024)

static arena* scratchpad;

void setUp() {
    arena_reset(scratchpad);
}
void tearDown() {
}

void init_suite() {
    LOG_PUSH(LOG_NONE);
    scratchpad = arena_new(TEST_ARENA_SIZE_BYTES);
}

void deinit_suite() {
    arena_free(scratchpad);
    LOG_POP();
}

int main(void) {
    init_suite();
    UNITY_BEGIN();

    // Object management
    run_bint_obj_tests();

    // Bitwise operations
    run_bint_not_tests();
    run_bint_and_tests();
    run_bint_nand_tests();
    run_bint_or_tests();
    run_bint_nor_tests();
    run_bint_xor_tests();
    run_bint_xnor_tests();
    run_bint_shl_tests();
    run_bint_shr_tests();
    run_bint_rotl_tests();
    run_bint_rotr_tests();

    // Simple operations
    run_bint_add_tests();
    run_bint_sub_tests();
    run_bint_mul_tests();
    run_bint_div_tests();
    run_bint_mod_tests();

    // Complex operations
    run_bint_pow_tests();
    run_bint_sqrt_tests();
    run_bint_log_tests();
    run_bint_exp_tests();

    int ue = UNITY_END();
    deinit_suite();
    return ue;
}