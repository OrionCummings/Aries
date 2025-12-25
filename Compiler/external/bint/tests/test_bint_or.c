#include "test_bint_or.h"

void run_bint_or_tests(void) {
    RUN_TEST(test_bint_or_equal_sizes);
    RUN_TEST(test_bint_or_unequal_sizes);
    RUN_TEST(test_bint_or_bad_parameters);
}

void test_bint_or_equal_sizes(void) {

    // Test equal size bints (|a| = |b| = |result|)
    const uint8_t size = 5;

    // Set up expectations
    bint_t* a = bint_new(size);
    bint_t* b = bint_new(size);
    bint_t* expected_bint = bint_new(size);

    uint8_t a_bytes[] = { 0xA2, 0x00, 0x82, 0x19, 0xFD };
    uint8_t b_bytes[] = { 0xD2, 0x18, 0x72, 0xAA, 0xDF };
    uint8_t expected_bytes[] = { 0xF2, 0x18, 0xF2, 0xBB, 0xFF };

    bint_set_bytes(a, a_bytes, size, 0);
    bint_set_bytes(b, b_bytes, size, 0);
    bint_set_bytes(expected_bint, expected_bytes, size, 0);

    // Perform the OR operation
    bint_t* actual_bint = NULL;
    bint_error_t err1 = bint_or(&actual_bint, a, b);

    TEST_ASSERT_EQUAL(BINTE_NONE, err1);
    TEST_ASSERT_EQUAL(expected_bint->n_bytes, actual_bint->n_bytes);

    for (index_t i = 0; i < size; i++)
        TEST_ASSERT_EQUAL(expected_bint->bytes[i], actual_bint->bytes[i]);

    bint_free(expected_bint);
    bint_free(actual_bint);
    bint_free(a);
    bint_free(b);
}

void test_bint_or_unequal_sizes(void) {

    // Test equal size bints (|a| != |b| = |result|)
    const uint8_t size_a = 1;
    const uint8_t size_b = 5;

    // Set up expectations
    bint_t* a = bint_new(size_a + 1);
    bint_t* b = bint_new(size_b);
    bint_t* expected_bint = bint_new(size_b);

    uint8_t a_bytes[] = { 0xA2, 0xFF };
    uint8_t b_bytes[] = { 0x78, 0x18, 0xD2, 0xBB, 0x10 };
    uint8_t expected_bytes[] = { 0xFA, 0x18, 0xD2, 0xBB, 0x10 };

    bint_set_bytes(a, a_bytes, size_a + 1, 0);
    bint_set_bytes(b, b_bytes, size_b, 0);
    bint_set_bytes(expected_bint, expected_bytes, size_b, 0);

    a->n_bytes = size_a;

    // Perform the OR operation
    bint_t* actual_bint = NULL;
    bint_error_t err1 = bint_or(&actual_bint, a, b);

    TEST_ASSERT_EQUAL(BINTE_NONE, err1);
    TEST_ASSERT_EQUAL(expected_bint->n_bytes, actual_bint->n_bytes);

    for (index_t i = 0; i < expected_bint->n_bytes; i++)
        TEST_ASSERT_EQUAL(expected_bint->bytes[i], actual_bint->bytes[i]);

    bint_free(expected_bint);
    bint_free(actual_bint);
    bint_free(a);
    bint_free(b);
}

void test_bint_or_bad_parameters(void) {
    bint_t* a;
    bint_t* b;
    bint_t* r;
    bint_error_t err;

    // Null first parameter
    a = NULL;
    b = bint_new(2);
    r = NULL;
    err = bint_or(&r, a, b);

    TEST_ASSERT_EQUAL(BINTE_INVALID_PARAM, err);
    TEST_ASSERT_NULL(r);

    bint_free(b);

    // Null second parameter
    a = NULL;
    b = bint_new(2);
    r = NULL;
    err = bint_or(&r, b, a);

    TEST_ASSERT_EQUAL(BINTE_INVALID_PARAM, err);
    TEST_ASSERT_NULL(r);

    bint_free(b);

    // Both null parameters
    a = NULL;
    b = NULL;
    r = NULL;
    err = bint_or(&r, b, a);

    TEST_ASSERT_EQUAL(BINTE_INVALID_PARAM, err);
    TEST_ASSERT_NULL(r);

    // Valid operand bints but invalid result bint
    a = bint_new(2);
    b = bint_new(2);
    r = bint_new(2);
    err = bint_or(&r, b, a);

    TEST_ASSERT_EQUAL(BINTE_LOST_INFO, err);
    TEST_ASSERT_NOT_NULL(r);

    bint_free(a);
    bint_free(b);
    bint_free(r);
}