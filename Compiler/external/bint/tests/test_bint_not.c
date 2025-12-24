#include "test_bint_not.h"

void run_bint_not_tests(void) {
    RUN_TEST(test_bint_not);
    RUN_TEST(test_bint_not_bad_parameters);
}

void test_bint_not(void) {

    const uint8_t size1 = 1;
    const uint8_t size2 = 6;
    const uint8_t size3 = 13;

    bint_t* b1 = bint_new(size1);
    bint_t* b2 = bint_new(size2);
    bint_t* b3 = bint_new(size3);
    bint_t* b1_expected = bint_new(size1);
    bint_t* b2_expected = bint_new(size2);
    bint_t* b3_expected = bint_new(size3);

    uint8_t b1_bytes[] = { 0x01 };
    uint8_t b2_bytes[] = { 0x02, 0xA5, 0xD5, 0x2D, 0x89, 0x15 };
    uint8_t b3_bytes[] = { 0x2B, 0xA1, 0x85, 0x85, 0xCD, 0xFC, 0xCA, 0xD0, 0x54, 0x11, 0xD5, 0xC6, 0x86, 0xA3 };
    uint8_t b1_expected_bytes[] = { 0xFE };
    uint8_t b2_expected_bytes[] = { 0xFD, 0x5A, 0x2A, 0xD2, 0x76, 0xEA };
    uint8_t b3_expected_bytes[] = { 0xD4, 0x5E, 0x7A, 0x7A, 0x32, 0x03, 0x35, 0x2F, 0xAB, 0xEE, 0x2A, 0x39, 0x79, 0x5C };

    bint_set_bytes(b1_expected, b1_expected_bytes, size1, 0); // ~1
    bint_set_bytes(b2_expected, b2_expected_bytes, size2, 0); // ~23678923678978
    bint_set_bytes(b3_expected, b3_expected_bytes, size3, 0); // ~3456799834576934586345786345123
    bint_set_bytes(b1, b1_bytes, size1, 0); // 1
    bint_set_bytes(b2, b2_bytes, size2, 0); // 23678923678978
    bint_set_bytes(b3, b3_bytes, size3, 0); // 3456799834576934586345786345123

    // Perform the NOT operations
    bint_t* result1 = NULL;
    bint_t* result2 = NULL;
    bint_t* result3 = NULL;
    bint_error_t err1 = bint_not(&result1, b1);
    bint_error_t err2 = bint_not(&result2, b2);
    bint_error_t err3 = bint_not(&result3, b3);

    TEST_ASSERT_EQUAL(BINTE_NONE, err1);
    TEST_ASSERT_EQUAL(BINTE_NONE, err2);
    TEST_ASSERT_EQUAL(BINTE_NONE, err3);

    TEST_ASSERT_EQUAL(b1_expected->n_bytes, result1->n_bytes);
    TEST_ASSERT_EQUAL(b2_expected->n_bytes, result2->n_bytes);
    TEST_ASSERT_EQUAL(b3_expected->n_bytes, result3->n_bytes);

    for (index_t i = 0; i < b1_expected->n_bytes; i++)
        TEST_ASSERT_EQUAL(b1_expected->bytes[i], result1->bytes[i]);

    for (index_t i = 0; i < b2_expected->n_bytes; i++)
        TEST_ASSERT_EQUAL(b2_expected->bytes[i], result2->bytes[i]);

    for (index_t i = 0; i < b3_expected->n_bytes; i++)
        TEST_ASSERT_EQUAL(b3_expected->bytes[i], result3->bytes[i]);

    bint_free(b1);
    bint_free(b2);
    bint_free(b3);
    bint_free(result1);
    bint_free(result2);
    bint_free(result3);
    bint_free(b1_expected);
    bint_free(b2_expected);
    bint_free(b3_expected);
}

void test_bint_not_bad_parameters(void) {

    bint_t* a;
    bint_t* r;
    bint_error_t err;

    // Null parameter
    a = NULL;
    r = NULL;
    err = bint_not(&r, a);

    TEST_ASSERT_EQUAL(BINTE_INVALID_PARAM, err);
    TEST_ASSERT_NULL(r);

    // Valid operand bints but invalid result bint
    a = bint_new(2);
    r = bint_new(2);
    err = bint_not(&r, a);

    TEST_ASSERT_EQUAL(BINTE_LOST_INFO, err);
    TEST_ASSERT_NOT_NULL(r);

    bint_free(a);
    bint_free(r);
}