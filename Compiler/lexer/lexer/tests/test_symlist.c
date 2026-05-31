#include "lexer.h"
#include "unity.h"

void test_symlist_push_symbol_1() {

    str file_content = STR_EMPTY;
    symlist* symlist = lex(&file_content);
    TEST_ASSERT_NOT_NULL(symlist);

    str* s1 = str_new("decl");
    TEST_ASSERT_NOT_NULL(s1);

    Symbol* sym1 = sym_new(s1);
    TEST_ASSERT_NOT_NULL(sym1);

    symlist_push(symlist, *sym1);

    TEST_ASSERT_NOT_NULL(symlist);
    TEST_ASSERT_NOT_NULL(symlist->symbols);
    TEST_ASSERT_EQUAL(1, symlist->length);

    for (size_t index = 0; index < symlist->length; index++) {
        TEST_ASSERT_EQUAL(true, sym_cmp(symlist->symbols[index], *sym1));
    }

    str_free(s1);

    sym_free(sym1);

    symlist_free(symlist);
}