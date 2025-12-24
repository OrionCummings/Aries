#include "test_bint_nand.h"

void run_bint_nand_tests(void) {
    RUN_TEST(test_bint_nand_equal_sizes);
    RUN_TEST(test_bint_nand_unequal_sizes);
    RUN_TEST(test_bint_nand_bad_parameters);
}

void test_bint_nand_equal_sizes(void) {

    // Test equal size bints (|a| = |b| = |result|)
    const uint8_t size = 2;

    // Set up expectations
    bint_t* a = bint_new(size);
    bint_t* b = bint_new(size);
    bint_t* expected_bint = bint_new(size);
    bint_t* actual_bint = NULL;

    uint8_t a_bytes[] = { 0xFA, 0x5D };
    uint8_t b_bytes[] = { 0xD2, 0x52 };
    uint8_t expected_bytes[] = { 0x2D, 0xAF };

    bint_set_bytes(a, a_bytes, size, 0);
    bint_set_bytes(b, b_bytes, size, 0);
    bint_set_bytes(expected_bint, expected_bytes, size, 0);

    // Perform the NAND operation
    bint_error_t err1 = bint_nand(&actual_bint, a, b);

    TEST_ASSERT_EQUAL(BINTE_NONE, err1);
    TEST_ASSERT_EQUAL(size, actual_bint->n_bytes);

    for (index_t i = 0; i < size; i++)
        TEST_ASSERT_EQUAL(expected_bint->bytes[i], actual_bint->bytes[i]);

    bint_free(expected_bint);
    bint_free(actual_bint);
    bint_free(a);
    bint_free(b);
}

void test_bint_nand_unequal_sizes(void) {

    // Test unequal size bints (|a| != |b| == |result| because NAND cannot expand/carry!)
    const uint8_t size_a = 2;
    const uint8_t size_b = 4;
    const uint8_t size_expected = 4;

    bint_t* a = bint_new(size_a);
    bint_t* b = bint_new(size_b);
    bint_t* expected_bint = bint_new(size_expected);
    bint_t* actual_bint = NULL;

    uint8_t a_bytes[] = { 0x8F, 0xAD };
    uint8_t b_bytes[] = { 0xA0, 0xFF, 0xFF, 0x5A };
    uint8_t expected_bytes[] = { 0x7F, 0x52, 0xFF, 0xFF };

    bint_set_bytes(a, a_bytes, size_a, 0);
    bint_set_bytes(b, b_bytes, size_b, 0);
    bint_set_bytes(expected_bint, expected_bytes, size_expected, 0);

    // Perform the NAND operation
    bint_error_t err2 = bint_nand(&actual_bint, a, b);

    TEST_ASSERT_EQUAL(BINTE_NONE, err2);
    TEST_ASSERT_EQUAL(size_expected, actual_bint->n_bytes);

    for (index_t i = 0; i < size_expected; i++)
        TEST_ASSERT_EQUAL(expected_bint->bytes[i], actual_bint->bytes[i]);

    bint_free(a);
    bint_free(b);
    bint_free(expected_bint);
    bint_free(actual_bint);
}

void test_bint_nand_bad_parameters(void) {

    bint_t* a;
    bint_t* b;
    bint_t* r;
    bint_error_t err;

    // Null first parameter
    a = NULL;
    b = bint_new(2);
    r = NULL;
    err = bint_nand(&r, a, b);

    TEST_ASSERT_EQUAL(BINTE_INVALID_PARAM, err);
    TEST_ASSERT_NULL(r);

    bint_free(b);

    // Null second parameter
    a = NULL;
    b = bint_new(2);
    r = NULL;
    err = bint_nand(&r, b, a);

    TEST_ASSERT_EQUAL(BINTE_INVALID_PARAM, err);
    TEST_ASSERT_NULL(r);

    bint_free(b);

    // Both null parameters
    a = NULL;
    b = NULL;
    r = NULL;
    err = bint_nand(&r, b, a);

    TEST_ASSERT_EQUAL(BINTE_INVALID_PARAM, err);
    TEST_ASSERT_NULL(r);

    // Valid operand bints but invalid result bint
    a = bint_new(2);
    b = bint_new(2);
    r = bint_new(2);
    err = bint_nand(&r, b, a);

    TEST_ASSERT_EQUAL(BINTE_LOST_INFO, err);
    TEST_ASSERT_NOT_NULL(r);

    bint_free(a);
    bint_free(b);
    bint_free(r);
}