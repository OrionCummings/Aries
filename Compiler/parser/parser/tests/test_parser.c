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

void setUp() { arena_reset(scratchpad); }

void tearDown() {}

// Test Cases
typedef struct {
    const char* input;
    const char* output;
    bool valid;
    bool success; // TODO: I assume this is set to zero when it's not
                  // initialized but I don't KNOW that!
} TestCase;

bool exercise_test_cases(TestCase cases[], size_t ncases) {
    for (size_t i = 0; i < ncases; i++) {
        str* input = str_new(cases[i].input);
        str* output = str_new(cases[i].output);

        if (cases[i].valid) {
            SymbolList* sl = lex(input);

            Expression* e = expression_parse(scratchpad, sl);
            if (e != nullptr && e->value != nullptr &&
                str_cmp(output, e->value)) {
                cases[i].success = true;
            }

            symlist_free(sl);
        }

        str_free(input);
        str_free(output);
    }

    bool failed = false;
    for (size_t i = 0; i < ncases; i++) {
        if (cases[i].valid != cases[i].success) {

            char error_message[256] = {0};
            (void)snprintf(error_message, 256,
                           "Test case #%lu failed: '%s' != '%s'", i,
                           cases[i].input, cases[i].output);
            TEST_MESSAGE(error_message);
            failed = true;
        }
    }

    return failed;
}

void test_single_expression_u8(void) {
    TestCase cases[] = {
        (TestCase){"", "", false},
        (TestCase){" ", "", false},
        (TestCase){".", "", false},
        (TestCase){"asdiofuh", "", false},
        (TestCase){"1-", "", false},
        (TestCase){"23478A", "", false},
        (TestCase){"0", "0", true},
        (TestCase){"-0", "", false},
        (TestCase){"1", "1", true},
        (TestCase){"-1", "", false},
        (TestCase){"27", "27", true},
        (TestCase){"255", "255", true},
        (TestCase){"256", "", false},
        (TestCase){"79340283470928374234", "", false},
        (TestCase){"21", "21", true},
    };

    if (exercise_test_cases(cases, sizeof(cases) / sizeof(*cases))) {
        TEST_FAIL();
    }
}

void test_single_expression_u16(void) {
    TestCase cases[] = {
        (TestCase){"", "", false},
        (TestCase){" ", "", false},
        (TestCase){".", "", false},
        (TestCase){"---------------------------------", "", false},
        (TestCase){"23748293784", "", false},
        (TestCase){"0", "0", true},
        (TestCase){"1", "1", true},
        (TestCase){"-1", "", false},
        (TestCase){"65335", "65335", true},
        (TestCase){"65336", "", false},
        (TestCase){"1", "a", true},

    };

    if (exercise_test_cases(cases, sizeof(cases) / sizeof(*cases))) {
        TEST_FAIL();
    }
}

void test_single_expression_u32(void) {}

void test_single_expression_u64(void) {}

void test_single_expression_i8(void) {}

void test_single_expression_i16(void) {}

void test_single_expression_i32(void) {}

void test_single_expression_i64(void) {}

void test_single_expression_f32(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_single_expression_f64(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_single_expression_str(void) {
    TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

int main(void) {
    init_suite();
    UNITY_BEGIN();

    // RUN_TEST(test_single_expression_u8);
    // RUN_TEST(test_single_expression_u16);
    // RUN_TEST(test_single_expression_u32);
    // RUN_TEST(test_single_expression_u64);

    // RUN_TEST(test_single_expression_i8);
    // RUN_TEST(test_single_expression_i16);
    // RUN_TEST(test_single_expression_i32);
    // RUN_TEST(test_single_expression_i64);

    // RUN_TEST(test_single_expression_f32);
    // RUN_TEST(test_single_expression_f64);

    // RUN_TEST(test_single_expression_str);

    int ue = UNITY_END();
    deinit_suite();
    return ue;
}