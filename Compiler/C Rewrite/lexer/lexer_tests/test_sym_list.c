#include "unity.h"
#include "lexer.h"

void test_sym_list_add_symbol_1() {

    str* content = str_new(""); // Not actually taking input!
    Lexer* l = lex_new(1, content);

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

    lex_add_symbol(l, sym1);
    lex_add_symbol(l, sym2);
    lex_add_symbol(l, sym3);
    lex_add_symbol(l, sym4);
    lex_add_symbol(l, sym5);

    TEST_ASSERT_NOT_NULL(l);
    TEST_ASSERT_NOT_NULL(l->sym_list);
    TEST_ASSERT_EQUAL(5, l->sym_list->length);

    lex_free(l);
    str_free(content);
    
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
