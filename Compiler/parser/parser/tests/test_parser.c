#include "test_parser.h"

static arena* scratchpad;

void init_suite(void) {
    LOG_PUSH(LOG_ALL);
    scratchpad = arena_new(4096);
}

void deinit_suite(void) {
    arena_free(scratchpad);
    LOG_POP();
}

void setUp() {
    arena_reset(scratchpad);
}

void tearDown() {}


void test_single_expression_assignment_u8(void) {

    str* s1 = str_new("1u8");
    str* s2 = str_new("12u8");
    str* s3 = str_new("123u8");

    SymbolList* sl1 = lex(s1);
    SymbolList* sl2 = lex(s2);
    SymbolList* sl3 = lex(s3);

    if (!sl1) { TEST_FAIL_MESSAGE("failed to allocate symbol list 1"); }
    if (!sl2) { TEST_FAIL_MESSAGE("failed to allocate symbol list 2"); }
    if (!sl3) { TEST_FAIL_MESSAGE("failed to allocate symbol list 3"); }

    symlist_print(*sl1);
    symlist_print(*sl2);
    symlist_print(*sl3);

    Expression* e1 = expression_parse(scratchpad, sl1);
    Expression* e2 = expression_parse(scratchpad, sl2);
    Expression* e3 = expression_parse(scratchpad, sl3);

    if (!e1) { TEST_FAIL_MESSAGE("failed to allocate expression 1"); }
    if (!e2) { TEST_FAIL_MESSAGE("failed to allocate expression 2"); }
    if (!e3) { TEST_FAIL_MESSAGE("failed to allocate expression 3"); }

    // TODO/NOTE: This doesn't check the other fields of Expression. Maybe that's a problem?
    if (e1->int_value != 1) { TEST_FAIL_MESSAGE("bad value in expression 1"); }
    if (e2->int_value != 12) { TEST_FAIL_MESSAGE("bad value in expression 2"); }
    if (e3->int_value != 123) { TEST_FAIL_MESSAGE("bad value in expression 3"); }

    symlist_free(sl1);
    symlist_free(sl2);
    symlist_free(sl3);

    str_free(s1);
    str_free(s2);
    str_free(s3);

}

void test_single_expression_assignment_u16(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_single_expression_assignment_u32(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_single_expression_assignment_u64(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_single_expression_assignment_i8(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_single_expression_assignment_i16(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_single_expression_assignment_i32(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_single_expression_assignment_i64(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_single_expression_assignment_f32(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_single_expression_assignment_f64(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_single_expression_assignment_str(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

int main(void) {
    init_suite();
    UNITY_BEGIN();

    RUN_TEST(test_single_expression_assignment_u8);
    // RUN_TEST(test_single_expression_assignment_u16);
    // RUN_TEST(test_single_expression_assignment_u32);
    // RUN_TEST(test_single_expression_assignment_u64);

    // RUN_TEST(test_single_expression_assignment_i8);
    // RUN_TEST(test_single_expression_assignment_i16);
    // RUN_TEST(test_single_expression_assignment_i32);
    // RUN_TEST(test_single_expression_assignment_i64);

    // RUN_TEST(test_single_expression_assignment_f32);
    // RUN_TEST(test_single_expression_assignment_f64);

    // RUN_TEST(test_single_expression_assignment_str);

    int ue = UNITY_END();
    deinit_suite();
    return ue;
}