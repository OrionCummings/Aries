#include "unity.h"
#include "lexer.h"

void test_sym_list_add_symbol_1() {

    str file_content = STR_EMPTY;
    SymbolList* symlist = lex(&file_content);
    TEST_ASSERT_NOT_NULL(symlist);

    str* s1 = str_new("def");
    TEST_ASSERT_NOT_NULL(s1);

    Symbol* sym1 = sym_new(s1);
    TEST_ASSERT_NOT_NULL(sym1);

    sym_list_add(symlist, *sym1);

    TEST_ASSERT_NOT_NULL(symlist);
    TEST_ASSERT_NOT_NULL(symlist->symbols);
    TEST_ASSERT_EQUAL(1, symlist->length);

    for (size_t index = 0; index < symlist->length; index++) {
        sym_print(symlist->symbols[index]);
        sym_print(*sym1);
        TEST_ASSERT_EQUAL(0, sym_cmp(symlist->symbols[index], *sym1));
    }

    str_free(s1);

    sym_free(sym1);

    sym_list_free(symlist);
}