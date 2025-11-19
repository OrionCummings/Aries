#ifndef __TEST_LEXER_H
#define __TEST_LEXER_H

#include "unity.h"
#include "lexer.h"

void test_lexer_new_success_1(void);
void test_sym_new_success_1(void);
void test_lexer_lex_success_1(void);
void test_str_to_token_success_1(void);
void test_str_get_alphanumeric_symbolic_boundaries_success_1(void);
void test_str_get_alphanumeric_symbolic_boundaries_success_2(void);
void test_str_get_alphanumeric_symbolic_boundaries_success_3(void);
void test_str_get_alphanumeric_symbolic_boundaries_success_4(void);
void test_str_get_alphanumeric_symbolic_boundaries_success_5(void);
void test_str_is_identifier_success_1(void);
void test_str_is_identifier_success_2(void);
void test_str_is_identifier_success_3(void);
void test_str_is_identifier_failure_1(void);
void test_str_is_identifier_failure_2(void);
void test_str_is_identifier_failure_3(void);
void test_str_is_identifier_failure_4(void);
void test_str_is_identifier_failure_5(void);
void test_str_is_identifier_failure_6(void);
void test_str_is_bool_literal_success_true(void);
void test_str_is_bool_literal_success_false(void);
void test_str_has_prefix_success(void);
void test_str_has_prefix_failure(void);
void test_str_has_suffix_success(void);
void test_str_has_suffix_failure(void);
void test_str_is_u8_literal(void);
void test_str_is_u16_literal(void);
void test_str_is_u32_literal(void);
void test_str_is_u64_literal(void);
void test_str_is_char_literal(void);
void test_lexer_add_symbol_1(void);
void test_lexer_example1(void);

#endif