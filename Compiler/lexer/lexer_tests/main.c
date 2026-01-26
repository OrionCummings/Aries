#include "unity.h"
#include "lexer.h"
#include "test_lexer.h"
#include "test_symlist.h"

void setUp() {
    LOG_PUSH(LOG_NONE);
}

void tearDown() {
    LOG_POP();
}

void suiteSetUp(void) {

}

int suiteTearDown(int num_failures) {

    return 0;
}

int main(void) {
    UNITY_BEGIN();

    /// Misc Tests
    if (true) {
        RUN_TEST(test_sym_new_success_from_str_view);
    }

    /// Symbol List Tests
    if (true) {
        RUN_TEST(test_symlist_add_symbol_1);
    }

    /// Lexer Tests
    if (true) {

        RUN_TEST(test_str_get_alphanumeric_symbolic_boundaries_success_1);
        RUN_TEST(test_str_get_alphanumeric_symbolic_boundaries_success_2);
        RUN_TEST(test_str_get_alphanumeric_symbolic_boundaries_success_3);
        RUN_TEST(test_str_get_alphanumeric_symbolic_boundaries_success_4);
        RUN_TEST(test_str_get_alphanumeric_symbolic_boundaries_success_5);

        RUN_TEST(test_str_is_identifier_success_1);
        RUN_TEST(test_str_is_identifier_success_2);
        RUN_TEST(test_str_is_identifier_success_3);
        RUN_TEST(test_str_is_identifier_failure_1);
        RUN_TEST(test_str_is_identifier_failure_2);
        RUN_TEST(test_str_is_identifier_failure_3);
        RUN_TEST(test_str_is_identifier_failure_4);
        RUN_TEST(test_str_is_identifier_failure_5);
        RUN_TEST(test_str_is_identifier_failure_6);

        RUN_TEST(test_str_is_bool_literal_success_true);
        RUN_TEST(test_str_is_bool_literal_success_false);

        RUN_TEST(test_str_has_prefix_success);
        RUN_TEST(test_str_has_prefix_failure);

        RUN_TEST(test_str_has_suffix_success);
        RUN_TEST(test_str_has_suffix_failure);

        RUN_TEST(test_str_is_u8_literal);
        RUN_TEST(test_str_is_u16_literal);
        RUN_TEST(test_str_is_u32_literal);
        RUN_TEST(test_str_is_u64_literal);

        RUN_TEST(test_str_is_char_literal);

        // RUN_TEST(test_lexer_new_success_1);

        // RUN_TEST(test_lexer_lex_success_1);

        // RUN_TEST(test_str_to_token_success_1);

        // RUN_TEST(test_sym_new_success_1);
        // sym_new with "0" passed fails!
    }

    return UNITY_END();
}