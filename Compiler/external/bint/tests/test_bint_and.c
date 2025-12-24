#include "test_bint_and.h"

void run_bint_and_tests(void) {
    RUN_TEST(test_bint_and_equal_sizes);
    RUN_TEST(test_bint_and_unequal_sizes);
}

void test_bint_and_equal_sizes(void) {

    // Test equal size bints (|a| = |b| = |result|)
    const uint8_t size = 1;

    // Set up expectations
    bint_t* expected_bint = bint_new(size);
    uint8_t expected_bytes[] = { 0x52 };
    bint_set_bytes(expected_bint, expected_bytes, size, 0);

    // Create and populate bints under test
    bint_t* a = bint_new(size);
    bint_t* b = bint_new(size);
    uint8_t a_bytes[] = { 0x5A };
    uint8_t b_bytes[] = { 0xD2 };
    bint_set_bytes(a, a_bytes, size, 0);
    bint_set_bytes(b, b_bytes, size, 0);

    // Perform the AND operation
    bint_t* actual_bint = NULL;
    bint_error_t err1 = bint_and(&actual_bint, a, b);

    TEST_ASSERT_EQUAL(BINTE_NONE, err1);
    TEST_ASSERT_EQUAL(size, actual_bint->n_bytes);

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
    const uint8_t size_b = 2;
    const uint8_t size_expected = 2;

    bint_t* a = bint_new(size_a);
    bint_t* b = bint_new(size_b);
    bint_t* expected_bint = bint_new(size_expected);
    bint_t* actual_bint = NULL;

    // NOTE: This is wrong/misinformed because the bytes may need to be swapped!!!!!!! Consider the order in which bytes are stored and make a decision on how to store them going forward!!!!
    uint8_t a_bytes[] = { 0x8F };
    uint8_t b_bytes[] = { 0xA0, 0xFF };
    uint8_t expected_bytes[] = { 0x00, 0x80 };

    bint_set_bytes(a, a_bytes, size_a, 0);
    bint_set_bytes(b, b_bytes, size_b, 0);
    bint_set_bytes(expected_bint, expected_bytes, size_expected, 0);

    // Perform the AND operation
    bint_error_t err2 = bint_and(&actual_bint, a, b);

    TEST_ASSERT_EQUAL(BINTE_NONE, err2);
    TEST_ASSERT_EQUAL(size_expected, actual_bint->n_bytes);

    for (index_t i = 0; i < size_expected; i++)
        TEST_ASSERT_EQUAL(expected_bint->bytes[i], actual_bint->bytes[i]);

    bint_free(a);
    bint_free(b);
    bint_free(expected_bint);
    bint_free(actual_bint);
}
