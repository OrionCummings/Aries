#include "test_bint_obj.h"

void run_bint_obj_tests(void) {
    // RUN_TEST(test_bint_new);
    // RUN_TEST(test_bint_anew);
    RUN_TEST(test_bint_new_str);
    // RUN_TEST(test_bint_new_cstr);
    // RUN_TEST(test_bint_free);
    // RUN_TEST(test_bint_free_arena);
    // RUN_TEST(test_bint_to_str);
    // RUN_TEST(test_bint_to_astr);
}

void test_bint_new(void) {

    bint_t* b = bint_new(1);

    TEST_ASSERT_NOT_NULL(b);
    TEST_ASSERT_NOT_NULL(b->bytes);
    TEST_ASSERT_EQUAL(1, b->n_bytes);
    TEST_ASSERT_EQUAL(false, b->state.flowed);
    TEST_ASSERT_EQUAL(true, b->state.positive);
    TEST_ASSERT_EQUAL(false, b->state.managed);
    TEST_ASSERT_EQUAL(0, b->bytes[0]);

    bint_free(b);
}

void test_bint_anew(void) {

    arena* a = arena_new(64);
    bint_t* b = bint_anew(a, 1);

    TEST_ASSERT_NOT_NULL(b);
    TEST_ASSERT_NOT_NULL(b->bytes);
    TEST_ASSERT_EQUAL(1, b->n_bytes);
    TEST_ASSERT_EQUAL(false, b->state.flowed);
    TEST_ASSERT_EQUAL(true, b->state.positive);
    TEST_ASSERT_EQUAL(true, b->state.managed);

    arena_free(a);
}

void test_bint_new_str(void) {

    const char* cstr = "24786";
    str* s = str_new(cstr);
    bint_t* b = bint_new_str(s);

    TEST_ASSERT_NOT_NULL(b);
    for (size_t index = 0; index < s->length; index++) {
        char actual_byte = (char)b->bytes[index];
        char expected_byte = cstr[index];
        TEST_ASSERT_EQUAL_CHAR(expected_byte, actual_byte);
    }

    bint_free(b);
    str_free(s);
}

void test_bint_new_cstr(void) {

    const uint8_t len = 1;
    const char* cstr = "1";
    bint_t* b = bint_new_cstr(cstr);

    TEST_ASSERT_NOT_NULL(b);
    for (size_t index = 0; index < len; index++) {
        char actual_byte = (char)b->bytes[index];
        char expected_byte = cstr[index];
        TEST_ASSERT_EQUAL_CHAR(expected_byte, actual_byte);
    }

    bint_free(b);
}

void test_bint_free(void) {

    bint_t* b = bint_new(1);
    TEST_ASSERT_NOT_NULL(b);

    bint_free(b);

    TEST_ASSERT_NULL(b);
}

void test_bint_free_arena(void) {

    arena* a = arena_new(64);
    bint_t* b = bint_anew(a, 1);
    TEST_ASSERT_NOT_NULL(b);

    bint_free(b);

    // It should NOT be freed because this bint is managed by the arena!
    TEST_ASSERT_NOT_NULL(b);

    arena_free(a);
}

void test_bint_to_str(void) {
    TEST_FAIL_MESSAGE("NOT IMPLEMENTED");
}

void test_bint_to_astr(void) {
    TEST_FAIL_MESSAGE("NOT IMPLEMENTED");
}