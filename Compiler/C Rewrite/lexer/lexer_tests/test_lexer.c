#include "unity.h"
#include "lexer.h"

void setUp() {
}

void tearDown() {
}

void test_lexer_new_success(void) {

}

void test_lexer_as_symbol_success_keyword_def(void) {

    const char* text = "def";
    str* s = str_new(text);

    Symbol* sym = as_symbol(s);

    TEST_ASSERT(sym != NULL);
    TEST_ASSERT(sym->s == NULL); // the symbol should NOT have text; it's a keyword so the text is invariant
    TEST_ASSERT_EQUAL(KEYWORD_DEF, sym->t);

    str_free(s);
    sym_free(sym);
}

void test_lexer_as_symbol_success_keyword_void(void) {

    const char* text = "void";
    str* s = str_new(text);

    Symbol* sym = as_symbol(s);

    TEST_ASSERT(sym != NULL);
    TEST_ASSERT(sym->s == NULL); // the symbol should NOT have text; it's a keyword so the text is invariant
    TEST_ASSERT_EQUAL(KEYWORD_VOID, sym->t);

    str_free(s);
    sym_free(sym);
}

void test_lexer_as_symbol_success_keyword_u32(void) {

    const char* text = "u32";
    str* s = str_new(text);

    Symbol* sym = as_symbol(s);

    TEST_ASSERT(sym != NULL);
    TEST_ASSERT(sym->s == NULL); // the symbol should NOT have text; it's a keyword so the text is invariant
    TEST_ASSERT_EQUAL(KEYWORD_U32, sym->t);

    str_free(s);
    sym_free(sym);
}

void test_lexer_as_symbol_success_symbol_fslash(void) {

    const char* text = "/";
    str* s = str_new(text);

    Symbol* sym = as_symbol(s);

    TEST_ASSERT(sym != NULL);
    TEST_ASSERT(sym->s == NULL); // the symbol should NOT have text; it's a keyword so the text is invariant
    TEST_ASSERT_EQUAL(SYM_FSLASH, sym->t);

    str_free(s);
    sym_free(sym);
}

void test_lexer_as_symbol_success_imperfect_symbol(void) {

    const char* text = " def ";
    str* s = str_new(text);

    Symbol* sym = as_symbol(s);

    TEST_ASSERT(sym != NULL);
    TEST_ASSERT(sym->s == NULL); // the symbol should NOT have text; it's a keyword so the text is invariant
    TEST_ASSERT_EQUAL(KEYWORD_DEF, sym->t);

    str_free(s);
    sym_free(sym);
}

int main(void) {
    UNITY_BEGIN();
    // RUN_TEST(test_lexer_new_success);
    RUN_TEST(test_lexer_as_symbol_success_keyword_def);
    RUN_TEST(test_lexer_as_symbol_success_keyword_void);
    RUN_TEST(test_lexer_as_symbol_success_keyword_u32);
    RUN_TEST(test_lexer_as_symbol_success_symbol_fslash);
    RUN_TEST(test_lexer_as_symbol_success_imperfect_symbol);
    return UNITY_END();
}