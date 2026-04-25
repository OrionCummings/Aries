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
    test_case_header();

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
    test_case_header();

    str* s1 = str_new("1u16");
    str* s2 = str_new("12u16");
    str* s3 = str_new("123u16");

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

void test_single_expression_assignment_u32(void) {
    test_case_header();

    str* s1 = str_new("0u32");
    str* s2 = str_new("574037u32");
    str* s3 = str_new("75893437u32");

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

    if (e1->int_value != 0) { TEST_FAIL_MESSAGE("bad value in expression 1"); }
    if (e2->int_value != 574037) { TEST_FAIL_MESSAGE("bad value in expression 2"); }
    if (e3->int_value != 75893437) { TEST_FAIL_MESSAGE("bad value in expression 3"); }

    symlist_free(sl1);
    symlist_free(sl2);
    symlist_free(sl3);

    str_free(s1);
    str_free(s2);
    str_free(s3);
}

void test_single_expression_assignment_u64(void) {
    test_case_header();

    str* s1 = str_new("2345798u64");
    str* s2 = str_new("7389237489783423u64");
    str* s3 = str_new("18446744073709551615u64");

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

    if (e1->int_value != 2345798ull) { TEST_FAIL_MESSAGE("bad value in expression 1"); }
    if (e2->int_value != 7389237489783423ull) { TEST_FAIL_MESSAGE("bad value in expression 2"); }
    if (e3->int_value != 18446744073709551615ull) { TEST_FAIL_MESSAGE("bad value in expression 3"); }

    symlist_free(sl1);
    symlist_free(sl2);
    symlist_free(sl3);

    str_free(s1);
    str_free(s2);
    str_free(s3);
}

void test_single_expression_assignment_i8(void) {
    test_case_header();

    str* s1 = str_new("42i8");
    str* s2 = str_new("128i8");
    str* s3 = str_new("-127i8");

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

    if (e1->int_value != 42) { TEST_FAIL_MESSAGE("bad value in expression 1"); }
    if (e2->int_value != 128) { TEST_FAIL_MESSAGE("bad value in expression 2"); }
    if (e3->int_value != -127) { TEST_FAIL_MESSAGE("bad value in expression 3"); }

    symlist_free(sl1);
    symlist_free(sl2);
    symlist_free(sl3);

    str_free(s1);
    str_free(s2);
    str_free(s3);
}

void test_single_expression_assignment_i16(void) {
    test_case_header();

    str* s1 = str_new("-0i16");
    str* s2 = str_new("12903i16");
    str* s3 = str_new("-27348i16");

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

    if (e1->int_value != -0) { TEST_FAIL_MESSAGE("bad value in expression 1"); }
    if (e2->int_value != 12903) { TEST_FAIL_MESSAGE("bad value in expression 2"); }
    if (e3->int_value != -27348) { TEST_FAIL_MESSAGE("bad value in expression 3"); }

    symlist_free(sl1);
    symlist_free(sl2);
    symlist_free(sl3);

    str_free(s1);
    str_free(s2);
    str_free(s3);
}

void test_single_expression_assignment_i32(void) {
    test_case_header();

    str* s1 = str_new("289i32");
    str* s2 = str_new("2349203i32");
    str* s3 = str_new("347982734897i32");

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

    if (e1->int_value != 289) { TEST_FAIL_MESSAGE("bad value in expression 1"); }
    if (e2->int_value != 2349203) { TEST_FAIL_MESSAGE("bad value in expression 2"); }
    if (e3->int_value != 347982734897) { TEST_FAIL_MESSAGE("bad value in expression 3"); }

    symlist_free(sl1);
    symlist_free(sl2);
    symlist_free(sl3);

    str_free(s1);
    str_free(s2);
    str_free(s3);
}

void test_single_expression_assignment_i64(void) {
    test_case_header();

    str* s1 = str_new("273489274i64");
    str* s2 = str_new("237402937492837472i64");
    str* s3 = str_new("896i64");

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

    if (e1->int_value != 273489274) { TEST_FAIL_MESSAGE("bad value in expression 1"); }
    if (e2->int_value != 237402937492837472) { TEST_FAIL_MESSAGE("bad value in expression 2"); }
    if (e3->int_value != 896) { TEST_FAIL_MESSAGE("bad value in expression 3"); }

    symlist_free(sl1);
    symlist_free(sl2);
    symlist_free(sl3);

    str_free(s1);
    str_free(s2);
    str_free(s3);
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

    // RUN_TEST(test_single_expression_assignment_u8);
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