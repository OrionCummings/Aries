#include "test_bint_and.h"

void run_bint_and_tests(void) {
    RUN_TEST(test_bint_and_equal_sizes);
    RUN_TEST(test_bint_and_unequal_sizes);
    RUN_TEST(test_bint_and_bad_parameters);
}

void test_bint_and_equal_sizes(void) {

    // Test equal size bints (|a| = |b| = |result|)
    const uint8_t size = 1;

    // Set up expectations
    bint_t* a = bint_new(size);
    bint_t* b = bint_new(size);
    bint_t* expected_bint = bint_new(size);

    uint8_t a_bytes[] = { 0x5A };
    uint8_t b_bytes[] = { 0xD2 };
    uint8_t expected_bytes[] = { 0x52 };

    bint_set_bytes(a, a_bytes, size, 0);
    bint_set_bytes(b, b_bytes, size, 0);
    bint_set_bytes(expected_bint, expected_bytes, size, 0);

    // Perform the AND operation
    bint_t* actual_bint = NULL;
    bint_error_t err1 = bint_and(&actual_bint, a, b);

    TEST_ASSERT_EQUAL(BINTE_NONE, err1);
    TEST_ASSERT_EQUAL(expected_bint->n_bytes, actual_bint->n_bytes);

    for (index_t i = 0; i < size; i++)
        TEST_ASSERT_EQUAL(expected_bint->bytes[i], actual_bint->bytes[i]);

    bint_free(expected_bint);
    bint_free(actual_bint);
    bint_free(a);
    bint_free(b);
}

void test_bint_and_unequal_sizes(void) {

    // Test unequal size bints (|a| != |b| == |result| because AND cannot expand/carry!)
    const uint8_t size_a = 1;
    const uint8_t size_b = 3;
    const uint8_t size_expected = 3;

    bint_t* a = bint_new(size_a + 1); // NOTE: This will be undone in a later step!
    bint_t* b = bint_new(size_b);
    bint_t* expected_bint = bint_new(size_expected);
    bint_t* actual_bint = NULL;

    uint8_t a_bytes[] = { 0x8F, 0xFF }; // NOTE: The '0xFF' byte is a sentinel byte to detect if bint_and() properly handles unequal sizes!
    uint8_t b_bytes[] = { 0xA0, 0xFF, 0xFF };
    uint8_t expected_bytes[] = { 0x80, 0x00, 0x00 };

    bint_set_bytes(a, a_bytes, size_a + 1, 0); // NOTE: Add 1 so the '0xFF' byte is written!
    bint_set_bytes(b, b_bytes, size_b, 0);
    bint_set_bytes(expected_bint, expected_bytes, size_expected, 0);

    a->n_bytes = size_a; // Manual decrement the byte count to the intended value.

    // Perform the AND operation
    bint_error_t err2 = bint_and(&actual_bint, a, b);

    TEST_ASSERT_EQUAL(BINTE_NONE, err2);
    TEST_ASSERT_EQUAL(expected_bint->n_bytes, actual_bint->n_bytes);

    for (index_t i = 0; i < size_expected; i++)
        TEST_ASSERT_EQUAL(expected_bint->bytes[i], actual_bint->bytes[i]);

    bint_free(a);
    bint_free(b);
    bint_free(expected_bint);
    bint_free(actual_bint);
}

void test_bint_and_bad_parameters(void) {

    bint_t* a;
    bint_t* b;
    bint_t* r;
    bint_error_t err;

    // Null first parameter
    a = NULL;
    b = bint_new(2);
    r = NULL;
    err = bint_and(&r, a, b);

    TEST_ASSERT_EQUAL(BINTE_INVALID_PARAM, err);
    TEST_ASSERT_NULL(r);

    bint_free(b);

    // Null second parameter
    a = NULL;
    b = bint_new(2);
    r = NULL;
    err = bint_and(&r, b, a);

    TEST_ASSERT_EQUAL(BINTE_INVALID_PARAM, err);
    TEST_ASSERT_NULL(r);

    bint_free(b);

    // Both null parameters
    a = NULL;
    b = NULL;
    r = NULL;
    err = bint_and(&r, b, a);

    TEST_ASSERT_EQUAL(BINTE_INVALID_PARAM, err);
    TEST_ASSERT_NULL(r);

    // Valid operand bints but invalid result bint
    a = bint_new(2);
    b = bint_new(2);
    r = bint_new(2);
    err = bint_and(&r, b, a);

    TEST_ASSERT_EQUAL(BINTE_LOST_INFO, err);
    TEST_ASSERT_NOT_NULL(r);

    bint_free(a);
    bint_free(b);
    bint_free(r);
}
