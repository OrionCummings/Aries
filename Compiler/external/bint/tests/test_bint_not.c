#include "test_bint_not.h"

void run_bint_not_tests(void) {
    RUN_TEST(test_bint_not);
}

void test_bint_not(void) {

    LOG_PUSH(LOG_ALL);

    bint_t* b1 = bint_new(64);
    bint_t* b2 = bint_new(64);
    bint_t* b3 = bint_new(64);

    // Set b1 to 1
    b1->bytes[0] = 1;

    // Set b2 to 23678923678978


    // Set b3 to 3456799834576934586345786345123


    // Invert b1, b2, and b3


    // Compare with expected results
    bint_t* b1_expected = bint_new(64);
    bint_t* b2_expected = bint_new(64);
    bint_t* b3_expected = bint_new(64);

    uint8_t b1_expected_bytes[] = {};

    bint_set_bytes(b1_expected, b1_expected_bytes, 1);
    bint_set_bytes(b2_expected, b2_expected_bytes, 1);
    bint_set_bytes(b3_expected, b3_expected_bytes, 1);

    bint_free(b1);
    bint_free(b2);
    bint_free(b3);
    bint_free(b1_expected);
    bint_free(b2_expected);
    bint_free(b3_expected);

    LOG_POP();
}
