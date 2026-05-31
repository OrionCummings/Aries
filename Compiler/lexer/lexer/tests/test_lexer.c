#include "test_lexer.h"

// TODO: Lots of duplicated code for checking test cases. Maybe consolidate into
// ~4 functions?

#define UNKNOWN (false)

void test_sym_new_success_1(void) {
    const char* cstr = "0";
    const TokenType expected_token = LIT_I32;
    str* s = str_new(cstr);
    Symbol* sym = sym_new(s);

    TEST_ASSERT_EQUAL(expected_token, sym->t);

    sym_free(sym);
    str_free(s);
}

void test_sym_new_success_from_str_view(void) {
    const char* cstr = "def i32 float";
    size_t start_index = 4;
    size_t end_index = 7;
    size_t len = end_index - start_index;
    const TokenType expected_token = KW_I32;
    str* s = str_new(cstr);
    str view = str_view(s, start_index, end_index);
    Symbol* sym = sym_new(&view);

    TEST_ASSERT_EQUAL(expected_token, sym->t);

    for (size_t i = 0; i < len; i++) {
        TEST_ASSERT_EQUAL(s->data[i + start_index], sym->s->data[i]);
    }

    sym_free(sym);
    str_free(s);
}

void test_lexer_lex_success_1() {

    const size_t num_symbols = 24;

    str* filename = str_new("/home/orion/Projects/Aries/Compiler/C "
                            "Rewrite/lexer/lexer_tests/example1.ari"); // TODO: Make this rely on a
                                                                       // hard-coded string so there
                                                                       // are no file dependencies!
    symlist* symlist = lex(filename);

    TEST_ASSERT_NOT_NULL(symlist);
    TEST_ASSERT_EQUAL(num_symbols, symlist->length);

    Symbol* symbols = calloc(num_symbols, sizeof(*symbols));

    symbols[0] = DEREF_SYMBOL(sym_new(str_new("def")));
    symbols[1] = DEREF_SYMBOL(sym_new(str_new(" ")));
    symbols[2] = DEREF_SYMBOL(sym_new(str_new("main")));
    symbols[3] = DEREF_SYMBOL(sym_new(str_new("(")));
    symbols[4] = DEREF_SYMBOL(sym_new(str_new("void")));
    symbols[5] = DEREF_SYMBOL(sym_new(str_new(")")));
    symbols[6] = DEREF_SYMBOL(sym_new(str_new(" ")));
    symbols[7] = DEREF_SYMBOL(sym_new(str_new("-")));
    symbols[8] = DEREF_SYMBOL(sym_new(str_new(">")));
    symbols[9] = DEREF_SYMBOL(sym_new(str_new(" ")));
    symbols[10] = DEREF_SYMBOL(sym_new(str_new("{")));
    symbols[11] = DEREF_SYMBOL(sym_new(str_new("\n")));
    symbols[12] = DEREF_SYMBOL(sym_new(str_new(" ")));
    symbols[13] = DEREF_SYMBOL(sym_new(str_new(" ")));
    symbols[14] = DEREF_SYMBOL(sym_new(str_new(" ")));
    symbols[15] = DEREF_SYMBOL(sym_new(str_new(" ")));
    symbols[16] = DEREF_SYMBOL(sym_new(str_new("return")));
    symbols[17] = DEREF_SYMBOL(sym_new(str_new(" ")));
    symbols[18] = DEREF_SYMBOL(sym_new(str_new("0")));
    symbols[19] = DEREF_SYMBOL(sym_new(str_new(";")));
    symbols[20] = DEREF_SYMBOL(sym_new(str_new("\n")));
    symbols[21] = DEREF_SYMBOL(sym_new(str_new("}")));

    for (size_t index = 0; index < num_symbols; index++) {
        TEST_ASSERT(sym_cmp(symbols[index], symlist->symbols[index]));
    }

    free(symbols);
}

void test_str_to_token_success_1() {
    const char* cs1 = "def";
    const char* cs2 = "test";
    const char* cs3 = "f32";
    const char* cs4 = "struct";
    const char* cs5 = "void";
    const char* cs6 = "52u8";
    const char* cs7 = "2782u16";
    const char* cs8 = "6237823u32";
    const char* cs9 = "2367429836784u64";
    const char* cs10 = "-32i8";
    const char* cs11 = "-2361i16";
    const char* cs12 = "-2237823i32";
    const char* cs13 = "-167429836784i64";
    const char* cs14 = "0";
    const char* cs15 = "201";
    const TokenType expected_token1 = KW_DECL;
    const TokenType expected_token2 = TOKEN_IDENTIFIER;
    const TokenType expected_token3 = KW_F32;
    const TokenType expected_token4 = KW_STRUCT;
    const TokenType expected_token5 = KW_VOID;
    const TokenType expected_token6 = LIT_U8;
    const TokenType expected_token7 = LIT_U16;
    const TokenType expected_token8 = LIT_U32;
    const TokenType expected_token9 = LIT_U64;
    const TokenType expected_token10 = LIT_I8;
    const TokenType expected_token11 = LIT_I16;
    const TokenType expected_token12 = LIT_I32;
    const TokenType expected_token13 = LIT_I64;
    const TokenType expected_token14 = LIT_U32;
    const TokenType expected_token15 = LIT_U32;
    str* s1 = str_new(cs1);
    str* s2 = str_new(cs2);
    str* s3 = str_new(cs3);
    str* s4 = str_new(cs4);
    str* s5 = str_new(cs5);
    str* s6 = str_new(cs6);
    str* s7 = str_new(cs7);
    str* s8 = str_new(cs8);
    str* s9 = str_new(cs9);
    str* s10 = str_new(cs10);
    str* s11 = str_new(cs11);
    str* s12 = str_new(cs12);
    str* s13 = str_new(cs13);
    str* s14 = str_new(cs14);
    str* s15 = str_new(cs15);
    TokenType t1 = str_to_token(s1);
    TokenType t2 = str_to_token(s2);
    TokenType t3 = str_to_token(s3);
    TokenType t4 = str_to_token(s4);
    TokenType t5 = str_to_token(s5);
    TokenType t6 = str_to_token(s6);
    TokenType t7 = str_to_token(s7);
    TokenType t8 = str_to_token(s8);
    TokenType t9 = str_to_token(s9);
    TokenType t10 = str_to_token(s10);
    TokenType t11 = str_to_token(s11);
    TokenType t12 = str_to_token(s12);
    TokenType t13 = str_to_token(s13);
    TokenType t14 = str_to_token(s14);
    TokenType t15 = str_to_token(s15);

    TEST_ASSERT_EQUAL(expected_token1, t1);
    TEST_ASSERT_EQUAL(expected_token2, t2);
    TEST_ASSERT_EQUAL(expected_token3, t3);
    TEST_ASSERT_EQUAL(expected_token4, t4);
    TEST_ASSERT_EQUAL(expected_token5, t5);
    TEST_ASSERT_EQUAL(expected_token6, t6);
    TEST_ASSERT_EQUAL(expected_token7, t7);
    TEST_ASSERT_EQUAL(expected_token8, t8);
    TEST_ASSERT_EQUAL(expected_token9, t9);
    TEST_ASSERT_EQUAL(expected_token10, t10);
    TEST_ASSERT_EQUAL(expected_token11, t11);
    TEST_ASSERT_EQUAL(expected_token12, t12);
    TEST_ASSERT_EQUAL(expected_token13, t13);
    TEST_ASSERT_EQUAL(expected_token14, t14);
    TEST_ASSERT_EQUAL(expected_token15, t15);

    str_free(s1);
    str_free(s2);
    str_free(s3);
    str_free(s4);
    str_free(s5);
    str_free(s6);
    str_free(s7);
    str_free(s8);
    str_free(s9);
    str_free(s10);
    str_free(s11);
    str_free(s12);
    str_free(s13);
    str_free(s14);
    str_free(s15);
}

void test_str_get_alphanumeric_symbolic_boundaries_success_1() {
    const char* text = "a nice test";
    const size_t n = 6;
    index_t expected_boundaries[] = { 0, 1, 2, 6, 7, 11 };
    str* s = str_new(text);

    index_t* actual_boundaries = str_get_alphanumeric_symbolic_boundaries(s);

    for (size_t index = 0; index < n; index++) {
        // This doesn't check for buffer overruns, but it's probably not an
        // issue rn lol
        TEST_ASSERT_EQUAL(expected_boundaries[index], actual_boundaries[index]);
    }

    str_free(s);
    free(actual_boundaries);
}

void test_str_get_alphanumeric_symbolic_boundaries_success_2() {
    const char* text = "def func(i32 param)";
    const size_t n = 9;
    index_t expected_boundaries[] = { 0, 3, 4, 8, 9, 12, 13, 18, 19 };
    str* s = str_new(text);

    index_t* actual_boundaries = str_get_alphanumeric_symbolic_boundaries(s);

    for (size_t index = 0; index < n; index++) {
        // This doesn't check for buffer overruns, but it's probably not an
        // issue rn lol
        TEST_ASSERT_EQUAL(expected_boundaries[index], actual_boundaries[index]);
    }

    str_free(s);
    free(actual_boundaries);
}

void test_str_get_alphanumeric_symbolic_boundaries_success_3() {
    const char* text = "bool c = (a == b) && func()";
    const size_t n = 20;
    index_t expected_boundaries[] = { 0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 25, 26, 27 };
    str* s = str_new(text);

    index_t* actual_boundaries = str_get_alphanumeric_symbolic_boundaries(s);

    for (size_t index = 0; index < n; index++) {
        // This doesn't check for buffer overruns, but it's probably not an
        // issue rn lol
        TEST_ASSERT_EQUAL(expected_boundaries[index], actual_boundaries[index]);
    }

    str_free(s);
    free(actual_boundaries);
}

void test_str_get_alphanumeric_symbolic_boundaries_success_4() {

    TEST_IGNORE_MESSAGE("This test is unfinished because I am lazy");

    const char* text = "def fact(i32 n) {"
                       "    if (n == 1) {"
                       "        return 1;"
                       "    }"
                       ""
                       "    return fact(n-1) * n;"
                       "};"
                       ""
                       "def main(void) -> int {"
                       "    i32 n = 12;"
                       "    if (fact(n) == 479_001_600) {"
                       "        return 0;"
                       "    } else {"
                       "        return -1;"
                       "    }"
                       "}";

    const size_t n = 9;
    index_t expected_boundaries[] = { 0 };
    str* s = str_new(text);

    index_t* actual_boundaries = str_get_alphanumeric_symbolic_boundaries(s);

    for (size_t index = 0; index < n; index++) {
        // This doesn't check for buffer overruns, but it's probably not an
        // issue rn lol
        TEST_ASSERT_EQUAL(expected_boundaries[index], actual_boundaries[index]);
    }

    str_free(s);
    free(actual_boundaries);
}

void test_str_get_alphanumeric_symbolic_boundaries_success_5() {
    const char* text = "-> i32 { return 123; }";

    const size_t n = 14;
    index_t expected_boundaries[] = { 0, 1, 2, 3, 6, 7, 8, 9, 15, 16, 19, 20, 21, 22 };
    str* s = str_new(text);

    index_t* actual_boundaries = str_get_alphanumeric_symbolic_boundaries(s);

    for (size_t index = 0; index < n; index++) {
        // This doesn't check for buffer overruns, but it's probably not an
        // issue rn lol
        TEST_ASSERT_EQUAL(expected_boundaries[index], actual_boundaries[index]);
    }

    str_free(s);
    free(actual_boundaries);
}

void test_str_is_identifier_success_1() {
    str* s = str_new("this_is_a_valid_identifier");
    TEST_ASSERT(str_is_identifier(s));
    str_free(s);
}

void test_str_is_identifier_success_2() {
    str* s = str_new("anotherVariableNameThatShouldBeGood178");
    TEST_ASSERT(str_is_identifier(s));
    str_free(s);
}

void test_str_is_identifier_success_3() {
    str* s = str_new("THIS_IS_PROBABLY_A_CONSTANT_OF_SOME_KIND2378");
    TEST_ASSERT(str_is_identifier(s));
    str_free(s);
}

void test_str_is_identifier_failure_1() {
    str* s = str_new("bad id");
    TEST_ASSERT_FALSE(str_is_identifier(s));
    str_free(s);
}

void test_str_is_identifier_failure_2() {
    str* s = str_new("this is not a valid identifier");
    TEST_ASSERT_FALSE(str_is_identifier(s));
    str_free(s);
}

void test_str_is_identifier_failure_3() {
    str* s = str_new(" bad");
    TEST_ASSERT_FALSE(str_is_identifier(s));
    str_free(s);
}

void test_str_is_identifier_failure_4() {
    str* s = str_new("bad ");
    TEST_ASSERT_FALSE(str_is_identifier(s));
    str_free(s);
}

void test_str_is_identifier_failure_5() {
    str* s = str_new("123");
    TEST_ASSERT_FALSE(str_is_identifier(s));
    str_free(s);
}

void test_str_is_identifier_failure_6() {
    str* s = str_new("269test_var");
    TEST_ASSERT_FALSE(str_is_identifier(s));
    str_free(s);
}

void test_str_is_bool_literal_success_true() {
    str* s = str_new("true");
    TEST_ASSERT_FALSE(str_is_bool_literal(s));
    str_free(s);
}

void test_str_is_bool_literal_success_false() {
    str* s = str_new("false");
    TEST_ASSERT_FALSE(str_is_bool_literal(s));
    str_free(s);
}

void test_str_has_prefix_success() {
    const char* prefix1 = "abc132";
    str* s1 = str_new("abc132");
    str* s2 = str_new("abc132237489+1278");
    str* s3 = str_new("abc132__  this is a test!\n\t");
    TEST_ASSERT_TRUE(str_has_prefix(s1, prefix1));
    TEST_ASSERT_TRUE(str_has_prefix(s2, prefix1));
    TEST_ASSERT_TRUE(str_has_prefix(s3, prefix1));
    str_free(s1);
    str_free(s2);
    str_free(s3);
}

void test_str_has_prefix_failure() {
    const char* prefix1 = "abc132";
    str* s1 = str_new("  abc132");
    str* s2 = str_new("126102 3abc132237489+1278");
    str* s3 = str_new("this is a test!\n\t");
    str* s4 = str_new("");
    TEST_ASSERT_FALSE(str_has_prefix(s1, prefix1));
    TEST_ASSERT_FALSE(str_has_prefix(s2, prefix1));
    TEST_ASSERT_FALSE(str_has_prefix(s3, prefix1));
    TEST_ASSERT_FALSE(str_has_prefix(s3, ""));
    TEST_ASSERT_FALSE(str_has_prefix(s4, prefix1));
    TEST_ASSERT_FALSE(str_has_prefix(s4, ""));
    str_free(s1);
    str_free(s2);
    str_free(s3);
    str_free(s4);
}

void test_str_has_suffix_success() {
    const char* suffix1 = "abc132";
    str* s1 = str_new("  abc132");
    str* s2 = str_new("126102 3abc132237489+1278abc132");
    str* s3 = str_new("this is a test!\n\tabc132");
    str* s4 = str_new("abc132");
    TEST_ASSERT_TRUE(str_has_suffix(s1, suffix1));
    TEST_ASSERT_TRUE(str_has_suffix(s2, suffix1));
    TEST_ASSERT_TRUE(str_has_suffix(s3, suffix1));
    TEST_ASSERT_TRUE(str_has_suffix(s4, suffix1));
    str_free(s1);
    str_free(s2);
    str_free(s3);
    str_free(s4);
}

void test_str_has_suffix_failure() {
    const char* suffix1 = "abc132";
    str* s1 = str_new("  abc132!");
    str* s2 = str_new("1261032");
    str* s3 = str_new("\t2");
    str* s4 = str_new("");
    TEST_ASSERT_FALSE(str_has_suffix(s1, suffix1));
    TEST_ASSERT_FALSE(str_has_suffix(s2, suffix1));
    TEST_ASSERT_FALSE(str_has_suffix(s3, suffix1));
    TEST_ASSERT_FALSE(str_has_suffix(s4, suffix1));
    str_free(s1);
    str_free(s2);
    str_free(s3);
    str_free(s4);
}

void test_str_is_u8_literal() {

    typedef struct {
        const char* input;
        bool output[2]; // expected, actual
        bool success;
    } TestCase;

    static TestCase cases[] = {
        // 0 < x < 255 with "u8" suffix
        (TestCase){   "0u8",  { true, UNKNOWN }, true },
        (TestCase){ "127u8",  { true, UNKNOWN }, true },
        (TestCase){ "255u8",  { true, UNKNOWN }, true },

        // numeric literals must end in a suffix!
        (TestCase){     "0", { false, UNKNOWN }, true },
        (TestCase){     "1", { false, UNKNOWN }, true },
        (TestCase){   "255", { false, UNKNOWN }, true },

        // throw some bullshit; see what happens
        (TestCase){  "-0u8", { false, UNKNOWN }, true },
        (TestCase){      "", { false, UNKNOWN }, true },
        (TestCase){    "u8", { false, UNKNOWN }, true },
        (TestCase){ "256u8", { false, UNKNOWN }, true },
        (TestCase){   "256", { false, UNKNOWN }, true },
        (TestCase){ "-21u8", { false, UNKNOWN }, true },
        (TestCase){    "-1", { false, UNKNOWN }, true },
        (TestCase){  "-127", { false, UNKNOWN }, true },
        (TestCase){  "-255", { false, UNKNOWN }, true },
        (TestCase){  "-256", { false, UNKNOWN }, true },
    };

    size_t ncases = sizeof(cases) / sizeof(*cases);
    bool failed = false;

    for (index_t i = 0; i < ncases; ++i) {
        str* s = str_new(cases[i].input);
        cases[i].output[1] = str_is_u8_literal(s);
        if (cases[i].output[0] != cases[i].output[1]) {
            cases[i].success = false;
            failed = true;

            char error_message[256] = { 0 };
            (void)snprintf(error_message, 256, "Test case #%lu failed: expected %s but received %s", i,
                           cases[i].output[0] ? "true" : "false", cases[i].output[1] ? "true" : "false");
            TEST_MESSAGE(error_message);
        }
        str_free(s);
    }

    if (failed) {
        TEST_FAIL_MESSAGE("At least one test cases was incorrect");
    }
}

void test_str_is_u16_literal() {

    typedef struct {
        const char* input;
        bool output[2]; // expected, actual
        bool success;
    } TestCase;

    static TestCase cases[] = {
        (TestCase){     "0u16",  { true, UNKNOWN }, true },
        (TestCase){   "127u16",  { true, UNKNOWN }, true },
        (TestCase){ "65535u16",  { true, UNKNOWN }, true },

        (TestCase){        "0", { false, UNKNOWN }, true },
        (TestCase){        "1", { false, UNKNOWN }, true },
        (TestCase){      "255", { false, UNKNOWN }, true },

        (TestCase){         "", { false, UNKNOWN }, true },
        (TestCase){      "u16", { false, UNKNOWN }, true },
        (TestCase){    "-0u16", { false, UNKNOWN }, true },
        (TestCase){ "65536u16", { false, UNKNOWN }, true },
        (TestCase){    "256u8", { false, UNKNOWN }, true },
        (TestCase){        "8", { false, UNKNOWN }, true },
        (TestCase){      "-75", { false, UNKNOWN }, true },
        (TestCase){       "-1", { false, UNKNOWN }, true },
        (TestCase){     "-127", { false, UNKNOWN }, true },
        (TestCase){     "-255", { false, UNKNOWN }, true },
        (TestCase){     "-256", { false, UNKNOWN }, true },
    };
    size_t ncases = sizeof(cases) / sizeof(*cases);
    bool failed = false;

    for (index_t i = 0; i < ncases; ++i) {
        str* s = str_new(cases[i].input);
        cases[i].output[1] = str_is_u16_literal(s);
        if (cases[i].output[0] != cases[i].output[1]) {
            cases[i].success = false;
            failed = true;

            char error_message[256] = { 0 };
            (void)snprintf(error_message, 256, "Test case #%lu failed: expected %s but received %s", i,
                           cases[i].output[0] ? "true" : "false", cases[i].output[1] ? "true" : "false");
            TEST_MESSAGE(error_message);
        }
        str_free(s);
    }

    if (failed) {
        TEST_FAIL_MESSAGE("At least one test cases was incorrect");
    }
}

void test_str_is_u32_literal() {

    typedef struct {
        const char* input;
        bool output[2]; // expected, actual
        bool success;
    } TestCase;

    static TestCase cases[] = {
        (TestCase){                       "0u32",  { true, UNKNOWN }, true },
        (TestCase){                   "47238u32",  { true, UNKNOWN }, true },
        (TestCase){                   "65535u32",  { true, UNKNOWN }, true },
        (TestCase){              "4294967295u32",  { true, UNKNOWN }, true },

        (TestCase){                          "0", { false, UNKNOWN }, true },
        (TestCase){                          "1", { false, UNKNOWN }, true },
        (TestCase){                     "436727", { false, UNKNOWN }, true },

        (TestCase){                           "", { false, UNKNOWN }, true },
        (TestCase){                         "u8", { false, UNKNOWN }, true },
        (TestCase){                        "u32", { false, UNKNOWN }, true },
        (TestCase){                   "65536u16", { false, UNKNOWN }, true },
        (TestCase){                      "-0u32", { false, UNKNOWN }, true },
        (TestCase){                      "256u8", { false, UNKNOWN }, true },
        (TestCase){                          "8", { false, UNKNOWN }, true },
        (TestCase){                        "-75", { false, UNKNOWN }, true },
        (TestCase){                         "-1", { false, UNKNOWN }, true },
        (TestCase){                       "-127", { false, UNKNOWN }, true },
        (TestCase){              "4294967296u32", { false, UNKNOWN }, true },
        (TestCase){             "-4294967296u32", { false, UNKNOWN }, true },
        (TestCase){ "-2367823632696732423978u32", { false, UNKNOWN }, true },
        (TestCase){                  "238940u64", { false, UNKNOWN }, true },
        (TestCase){              "-346728346u32", { false, UNKNOWN }, true },
        (TestCase){                     "-75f64", { false, UNKNOWN }, true },
        (TestCase){                     "-75f32", { false, UNKNOWN }, true },
        (TestCase){                       "-256", { false, UNKNOWN }, true },
    };
    size_t ncases = sizeof(cases) / sizeof(*cases);
    bool failed = false;

    for (index_t i = 0; i < ncases; ++i) {
        str* s = str_new(cases[i].input);
        cases[i].output[1] = str_is_u32_literal(s);
        if (cases[i].output[0] != cases[i].output[1]) {
            cases[i].success = false;
            failed = true;

            char error_message[256] = { 0 };
            (void)snprintf(error_message, 256, "Test case #%lu failed: expected %s but received %s", i,
                           cases[i].output[0] ? "true" : "false", cases[i].output[1] ? "true" : "false");
            TEST_MESSAGE(error_message);
        }
        str_free(s);
    }

    if (failed) {
        TEST_FAIL_MESSAGE("At least one test cases was incorrect");
    }
}

void test_str_is_u64_literal() {

    typedef struct {
        const char* input;
        bool output[2]; // expected, actual
        bool success;
    } TestCase;

    static TestCase cases[] = {
        (TestCase){                                    "0u64",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){                                "47238u64",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){                                "65535u64",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){                               "238940u64",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){                           "4294967295u64",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){                           "4294967295u64",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){                 "18446744073709551615u64",  { true, UNKNOWN }, UNKNOWN },

        (TestCase){                                       "0", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                       "1", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                  "436727", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                   "-0u64", { false, UNKNOWN }, UNKNOWN },

        (TestCase){                                        "", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                      "u8", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                "65536u16", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                   "256u8", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                     "u32", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                     "u64", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                   "256u8", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                       "8", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                     "-75", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                      "-1", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                    "-127", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                           "4294967296u32", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                          "-4294967296u32", { false, UNKNOWN }, UNKNOWN },
        (TestCase){              "-2367823632696732423978u32", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                           "-346728346u32", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                  "-75f64", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                  "-75f64", { false, UNKNOWN }, UNKNOWN },
        (TestCase){ "236782363269673242378220923789247978u64", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                       "17290827349827u32", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                            "732897928u16", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                   "75f32", { false, UNKNOWN }, UNKNOWN },
        (TestCase){                                    "-256", { false, UNKNOWN }, UNKNOWN },
    };
    size_t ncases = sizeof(cases) / sizeof(*cases);
    bool failed = false;

    for (index_t i = 0; i < ncases; ++i) {
        str* s = str_new(cases[i].input);
        cases[i].output[1] = str_is_u64_literal(s);
        if (cases[i].output[0] != cases[i].output[1]) {
            cases[i].success = false;
            failed = true;

            char error_message[256] = { 0 };
            (void)snprintf(error_message, 256, "Test case #%lu failed: expected %s but received %s", i,
                           cases[i].output[0] ? "true" : "false", cases[i].output[1] ? "true" : "false");
            TEST_MESSAGE(error_message);
        }
        str_free(s);
    }

    if (failed) {
        TEST_FAIL_MESSAGE("At least one test cases was incorrect");
    }
}

void test_str_is_char_literal() {

    typedef struct {
        const char* input;
        bool output[2]; // expected, actual
        bool success;
    } TestCase;

    static TestCase cases[] = {
        (TestCase){             "'a'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'b'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'c'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'q'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'z'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'-'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'/'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'&'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'$'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'@'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'='",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'+'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'0'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'5'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "'9'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){            "'\n'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){            "'\t'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){            "'\r'",  { true, UNKNOWN }, UNKNOWN },
        (TestCase){             "' '",  { true, UNKNOWN }, UNKNOWN },
        // (TestCase){            "'\''",  { true, UNKNOWN }, UNKNOWN }, // Maybe this should be valid?

        (TestCase){            "'00'", { false, UNKNOWN }, UNKNOWN },
        (TestCase){            "'-='", { false, UNKNOWN }, UNKNOWN },
        (TestCase){            "'--'", { false, UNKNOWN }, UNKNOWN },
        (TestCase){            "'27'", { false, UNKNOWN }, UNKNOWN },
        (TestCase){ "'ashpdioha8s9d'", { false, UNKNOWN }, UNKNOWN },
        (TestCase){  "'834570892357'", { false, UNKNOWN }, UNKNOWN },
        (TestCase){            "'  '", { false, UNKNOWN }, UNKNOWN },
        (TestCase){           "' 2 '", { false, UNKNOWN }, UNKNOWN },
        (TestCase){          "'\0\0'", { false, UNKNOWN }, UNKNOWN },
        (TestCase){            "'l2'", { false, UNKNOWN }, UNKNOWN },
        (TestCase){            "';;'", { false, UNKNOWN }, UNKNOWN },
        (TestCase){              "''", { false, UNKNOWN }, UNKNOWN },
        (TestCase){            "'[]'", { false, UNKNOWN }, UNKNOWN },
        (TestCase){            "';''", { false, UNKNOWN }, UNKNOWN },
    };
    size_t ncases = sizeof(cases) / sizeof(*cases);
    bool failed = false;

    for (index_t i = 0; i < ncases; ++i) {
        str* s = str_new(cases[i].input);
        cases[i].output[1] = str_is_char_literal(s);
        if (cases[i].output[0] != cases[i].output[1]) {
            cases[i].success = false;
            failed = true;

            char error_message[256] = { 0 };
            (void)snprintf(error_message, 256, "Test case #%lu failed: expected %s but received %s", i,
                           cases[i].output[0] ? "true" : "false", cases[i].output[1] ? "true" : "false");
            TEST_MESSAGE(error_message);
        }
        str_free(s);
    }

    if (failed) {
        TEST_FAIL_MESSAGE("At least one test cases was incorrect");
    }

    ///////////////////////////
    ///////////////////////////
    ///////////////////////////

    str* s1 = str_new("'a'");
    str* s2 = str_new("'l'");
    str* s3 = str_new("'\n'");
    str* s4 = str_new("' '");
    TEST_ASSERT_TRUE(str_is_char_literal(s1));
    TEST_ASSERT_TRUE(str_is_char_literal(s2));
    TEST_ASSERT_TRUE(str_is_char_literal(s3));
    TEST_ASSERT_TRUE(str_is_char_literal(s4));
    str_free(s1);
    str_free(s2);
    str_free(s3);
    str_free(s4);

    str* x1 = str_new("''");
    str* x2 = str_new("'aa'");
    str* x3 = str_new("' _'");
    TEST_ASSERT_FALSE(str_is_char_literal(x1));
    TEST_ASSERT_FALSE(str_is_char_literal(x2));
    TEST_ASSERT_FALSE(str_is_char_literal(x3));
    str_free(x1);
    str_free(x2);
    str_free(x3);
}

#undef UNKNOWN
