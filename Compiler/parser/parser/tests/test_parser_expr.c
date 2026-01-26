#include "test_parser_expr.h"

static arena* scratchpad;

void test_single_expr_assignment(void) {

    scratchpad = arena_new(4096);

    RUN_TEST(test_single_expr_assignment_u8);
    // RUN_TEST(test_single_expr_assignment_u16);
    // RUN_TEST(test_single_expr_assignment_u32);
    // RUN_TEST(test_single_expr_assignment_u64);

    // RUN_TEST(test_single_expr_assignment_i8);
    // RUN_TEST(test_single_expr_assignment_i16);
    // RUN_TEST(test_single_expr_assignment_i32);
    // RUN_TEST(test_single_expr_assignment_i64);

    // RUN_TEST(test_single_expr_assignment_f32);
    // RUN_TEST(test_single_expr_assignment_f64);

    // RUN_TEST(test_single_expr_assignment_str);

    arena_free(scratchpad);

}
