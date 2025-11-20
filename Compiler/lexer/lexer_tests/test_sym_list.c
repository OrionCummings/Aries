#include "unity.h"
#include "lexer.h"

void test_sym_list_add_symbol_1() {

    // TODO: Figure out a better way to mock lexers!
    Lexer* l = lex_new("");

    str* s1 = str_new("def");
    str* s2 = str_new("void");
    str* s3 = str_new("return");
    str* s4 = str_new("i32");
    str* s5 = str_new("opt");

    Symbol* sym1 = sym_new(s1);
    Symbol* sym2 = sym_new(s2);
    Symbol* sym3 = sym_new(s3);
    Symbol* sym4 = sym_new(s4);
    Symbol* sym5 = sym_new(s5);

    TEST_ASSERT_NOT_NULL(sym1);
    TEST_ASSERT_NOT_NULL(sym2);
    TEST_ASSERT_NOT_NULL(sym3);
    TEST_ASSERT_NOT_NULL(sym4);
    TEST_ASSERT_NOT_NULL(sym5);

    lex_add_symbol(l, *sym1);
    lex_add_symbol(l, *sym2);
    lex_add_symbol(l, *sym3);
    lex_add_symbol(l, *sym4);
    lex_add_symbol(l, *sym5);

    TEST_ASSERT_NOT_NULL(l);
    TEST_ASSERT_NOT_NULL(l->sym_list);
    TEST_ASSERT_EQUAL(5, l->sym_list->length);

    lex_free(l);

    str_free(s1);
    str_free(s2);
    str_free(s3);
    str_free(s4);
    str_free(s5);

    sym_free(sym1);
    sym_free(sym2);
    sym_free(sym3);
    sym_free(sym4);
    sym_free(sym5);
}
