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

    TEST_IGNORE_MESSAGE("Unimplemented feature!");

    const char* text = " def ";
    str* s = str_new(text);

    Symbol* sym = as_symbol(s);

    TEST_ASSERT(sym != NULL);
    TEST_ASSERT(sym->s == NULL); // the symbol should NOT have text; it's a keyword so the text is invariant
    TEST_ASSERT_EQUAL(KEYWORD_DEF, sym->t);

    str_free(s);
    sym_free(sym);
}

void test_lexer_lex_success_1() {

    const size_t num_symbols = 24;
    const char* filename = "/home/orion/Projects/Aries/Compiler/C Rewrite/lexer/lexer_tests/example1.ari";
    Lexer* l = lex_new(8, filename);
    if (!lex(l)) { TEST_FAIL_MESSAGE("Call to lex() failed!"); }
    if (l == NULL) { TEST_FAIL_MESSAGE("Null lexer object!"); }
    if (l->symbols == NULL) { TEST_FAIL_MESSAGE("Null lexer symbols object!"); }

    TEST_ASSERT_EQUAL(num_symbols, l->symbol_length);

    Symbol* symbols = calloc(num_symbols, sizeof(*symbols));

    symbols[0] = DEREF_SYMBOL(sym_new(KEYWORD_DEF, str_new("def")));
    symbols[1] = DEREF_SYMBOL(sym_new(SYM_SPACE, str_new(" ")));
    symbols[2] = DEREF_SYMBOL(sym_new(IDENTIFIER, str_new("main")));
    symbols[3] = DEREF_SYMBOL(sym_new(SYM_PAREN_OPEN, str_new("(")));
    symbols[4] = DEREF_SYMBOL(sym_new(KEYWORD_VOID, str_new("void")));
    symbols[5] = DEREF_SYMBOL(sym_new(SYM_PAREN_CLOSE, str_new(")")));
    symbols[6] = DEREF_SYMBOL(sym_new(SYM_SPACE, str_new(" ")));
    symbols[7] = DEREF_SYMBOL(sym_new(SYM_DASH, str_new("-")));
    symbols[8] = DEREF_SYMBOL(sym_new(SYM_GT, str_new(">")));
    symbols[9] = DEREF_SYMBOL(sym_new(SYM_SPACE, str_new(" ")));
    symbols[10] = DEREF_SYMBOL(sym_new(SYM_BRACE_OPEN, str_new("{")));
    symbols[11] = DEREF_SYMBOL(sym_new(SYM_NEWLINE, str_new("\n")));
    symbols[12] = DEREF_SYMBOL(sym_new(SYM_SPACE, str_new(" ")));
    symbols[13] = DEREF_SYMBOL(sym_new(SYM_SPACE, str_new(" ")));
    symbols[14] = DEREF_SYMBOL(sym_new(SYM_SPACE, str_new(" ")));
    symbols[15] = DEREF_SYMBOL(sym_new(SYM_SPACE, str_new(" ")));
    symbols[16] = DEREF_SYMBOL(sym_new(KEYWORD_RETURN, str_new("return")));
    symbols[17] = DEREF_SYMBOL(sym_new(SYM_SPACE, str_new(" ")));
    symbols[18] = DEREF_SYMBOL(sym_new(LIT_I32, str_new("0")));
    symbols[19] = DEREF_SYMBOL(sym_new(SYM_SEMICOLON, str_new(";")));
    symbols[20] = DEREF_SYMBOL(sym_new(SYM_NEWLINE, str_new("\n")));
    symbols[21] = DEREF_SYMBOL(sym_new(SYM_BRACE_CLOSE, str_new("}")));

    for (size_t index = 0; index < num_symbols; index++) {
        TEST_ASSERT(sym_cmp(symbols[index], l->symbols[index]));
    }

    free(symbols);
    lex_free(l);
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_lexer_new_success);

    RUN_TEST(test_lexer_as_symbol_success_keyword_def);
    RUN_TEST(test_lexer_as_symbol_success_keyword_void);
    RUN_TEST(test_lexer_as_symbol_success_keyword_u32);
    RUN_TEST(test_lexer_as_symbol_success_symbol_fslash);
    RUN_TEST(test_lexer_as_symbol_success_imperfect_symbol);

    RUN_TEST(test_lexer_lex_success_1);

    return UNITY_END();
}