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

void test_single_expression_u8(void) {
    typedef struct {
        const char* input;
        const char* output;
        bool valid;
        bool success;
    } TestCase;

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

    size_t ncases = sizeof(cases) / sizeof(*cases);
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
}

void test_single_expression_u16(void) {
    typedef struct {
        const char* input;
        const char* output;
        bool valid;
        bool success;
    } TestCase;

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

    size_t ncases = sizeof(cases) / sizeof(*cases);
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

void test_single_expression_type_inference(void) {

    typedef struct { // TODO: Change test case contents for this test!
        const char* input;
        const char* output;
        bool valid;
        bool success;
    } TestCase;

    TestCase cases[] = {
        (TestCase){"0u8", "u8", true},
        (TestCase){"0u16", "u16", true},
        (TestCase){"0u32", "u32", true},
        (TestCase){"0u64", "u64", true},

        (TestCase){"1u8", "u8", true},
        (TestCase){"255u8", "u8", true},
        (TestCase){"256u8", "", false}, // Too big to fit in u8

        (TestCase){"256u16", "u16", true},
        (TestCase){"65535u16", "u16", true},
        (TestCase){"65536u16", "", false}, // Too big to fit in u16

        (TestCase){"65536u32", "u32", true},
        (TestCase){"4294967295u32", "u32", true},
        (TestCase){"4294967296u32", "", false}, // Too big to fit in u32

        (TestCase){"4294967296u64", "u64", true},
        (TestCase){"18446744073709551615u64", "u64", true},
        (TestCase){"18446744073709551616u64", "", false}, // Too big to fit in u64

        // No suffixes; infer the type based on value
        (TestCase){"0", "u8", true},
        (TestCase){"255", "u8", true},
        (TestCase){"256", "u16", true},
        (TestCase){"65535", "u16", true},
        (TestCase){"65536", "u32", true},
        (TestCase){"4294967295", "u32", true},
        (TestCase){"4294967296", "u64", true},
        (TestCase){"18446744073709551615", "u64", true},
        
        (TestCase){"-0", "i8", true},
        (TestCase){"-1", "i8", true},
        (TestCase){"-127", "i8", true},
        (TestCase){"-128", "i16", true},
        (TestCase){"-32767", "i16", true},
        (TestCase){"-32768", "i32", true},
        (TestCase){"-2147483647", "i32", true},
        (TestCase){"-2147483648", "i64", true},
        (TestCase){"-9223372036854775807", "i64", true},

    };

    size_t ncases = sizeof(cases) / sizeof(*cases);
    for (index_t i = 0; i < ncases; ++i) {

        str* input = str_new(cases[i].input);
        str* output = str_new(cases[i].output);
        SymbolList* sl = lex(input);

        Expression* e = expression_parse(scratchpad, sl);// TODO: Failing! null!!
        bool suffix_match = str_has_suffix(e->value, cases[i].output);
        if (e != nullptr && e->value != nullptr && suffix_match) {
            str_print("e->value: ", e->value);
            printf("cases[i].output: %s\n", cases[i].output);
            cases[i].success = true;
        }

        symlist_free(sl);
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
    if (failed) { TEST_FAIL(); }
}

int main(void) {
    init_suite();
    UNITY_BEGIN();

    RUN_TEST(test_single_expression_type_inference);

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