#include "test_bint_nor.h"

void run_bint_nor_tests(void) {
    RUN_TEST(test_bint_nor_equal_sizes);
    RUN_TEST(test_bint_nor_unequal_sizes);
    RUN_TEST(test_bint_nor_bad_parameters);
}

void test_bint_nor_equal_sizes(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_bint_nor_unequal_sizes(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_bint_nor_bad_parameters(void) {
    bint_t* a;
    bint_t* b;
    bint_t* r;
    bint_error_t err;

    // Null first parameter
    a = NULL;
    b = bint_new(2);
    r = NULL;
    err = bint_nor(&r, a, b);

    TEST_ASSERT_EQUAL(BINTE_INVALID_PARAM, err);
    TEST_ASSERT_NULL(r);

    bint_free(b);

    // Null second parameter
    a = NULL;
    b = bint_new(2);
    r = NULL;
    err = bint_nor(&r, b, a);

    TEST_ASSERT_EQUAL(BINTE_INVALID_PARAM, err);
    TEST_ASSERT_NULL(r);

    bint_free(b);

    // Both null parameters
    a = NULL;
    b = NULL;
    r = NULL;
    err = bint_nor(&r, b, a);

    TEST_ASSERT_EQUAL(BINTE_INVALID_PARAM, err);
    TEST_ASSERT_NULL(r);

    // Valid operand bints but invalid result bint
    a = bint_new(2);
    b = bint_new(2);
    r = bint_new(2);
    err = bint_nor(&r, b, a);

    TEST_ASSERT_EQUAL(BINTE_LOST_INFO, err);
    TEST_ASSERT_NOT_NULL(r);

    bint_free(a);
    bint_free(b);
    bint_free(r);
}
