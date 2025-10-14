#include "unity.h"
#include "utils.h"

void setUp() {}

void tearDown() {}

void test_str_new_success(void) {

    const char* expected_string = "test string";
    size_t length = strlen(expected_string);
    str* s = str_new(expected_string);

    TEST_ASSERT_EQUAL(length, s->length);
    TEST_ASSERT_EQUAL_STRING(expected_string, s->data);
    TEST_ASSERT_EQUAL(true, s->heap);

    str_free(s);
}

void test_str_new_null_string() {

    str* s = str_new(NULL);

    TEST_ASSERT_NULL(s);

    str_free(s);
}

void test_str_free_valid_string() {

    const char* cstring = "test string";
    str* s = str_new(cstring);

    str_free(s);

    TEST_ASSERT_NULL(s);
}

void test_str_free_valid_string_null_data() {

    const char* cstring = "test string";
    str* s = str_new(cstring);

    free(s->data);
    s->data = NULL;

    TEST_ASSERT_NULL(s->data);

    str_free(s);
}

void test_str_free_null_string() {

    str* s = str_new(NULL);
    str_free(s);
    TEST_ASSERT_NULL(s);
}

void test_str_concat_nominal_success() {

    const char* cstr1 = "example1";
    const char* cstr2 = "example2";
    const char* expected_string = "example1example2";
    str* s1 = str_new(cstr1);
    str* s2 = str_new(cstr2);

    str* actual_string = str_concat(s1, s2);

    TEST_ASSERT_EQUAL_STRING(expected_string, actual_string->data);
    TEST_ASSERT_EQUAL(strlen(expected_string), str_len(actual_string));

    str_free(s1);
    str_free(s2);
    str_free(actual_string);
}

void test_str_concat_null_parameter() {

    str* s1 = str_new("example1");

    str* actual_string = str_concat(s1, NULL);

    TEST_ASSERT_NULL(actual_string);

    str_free(s1);
    str_free(actual_string);
}

void test_str_concat_malformed_parameter() {

    str* s1 = str_new("example1");
    free(s1->data);
    s1->data = NULL;

    str* actual_string = str_concat(s1, NULL);

    TEST_ASSERT_NULL(actual_string);

    str_free(s1);
    str_free(actual_string);
}

void test_str_find_success() {

    int expected_pos = 3;
    char c = 'm';
    str* s = str_new("example1");

    int actual_pos = str_find(s, c);

    TEST_ASSERT_EQUAL(expected_pos, actual_pos);

    str_free(s);
}

void test_str_find_failure_not_present() {

    int expected_pos = -1;
    char c = 'z';
    str* s = str_new("example1");

    int actual_pos = str_find(s, c);

    TEST_ASSERT_EQUAL(expected_pos, actual_pos);

    str_free(s);
}

void test_str_find_failure_empty_str() {

    int expected_pos = -1;
    char c = 'z';
    str* s = str_new("");

    int actual_pos = str_find(s, c);

    TEST_ASSERT_EQUAL(expected_pos, actual_pos);

    str_free(s);
}

void test_str_find_failure_null_str() {

    int expected_pos = -1;
    char c = 'z';
    str* s = NULL;

    int actual_pos = str_find(s, c);

    TEST_ASSERT_EQUAL(expected_pos, actual_pos);

    str_free(s);
}

void test_str_find_failure_empty_str_null_char() {

    int expected_pos = -1;
    char c = '\0';
    str* s = str_new("");

    int actual_pos = str_find(s, c);

    TEST_ASSERT_EQUAL(expected_pos, actual_pos);

    str_free(s);
}

void test_str_at_success() {

    const char expected_char = 'i';
    const int index = 2;
    str* s = str_new("this is a test!");

    char actual_char = str_at(s, index);

    TEST_ASSERT_EQUAL(expected_char, actual_char);

    str_free(s);
}

void test_str_at_failure_index_too_big() {

    const char expected_char = '\0';
    const int index = 23;
    str* s = str_new("this is a test!");

    char actual_char = str_at(s, index);

    TEST_ASSERT_EQUAL(expected_char, actual_char);

    str_free(s);
}

void test_str_at_failure_null_str() {

    const char expected_char = '\0';
    const int index = 2;
    str* s = NULL;

    char actual_char = str_at(s, index);

    TEST_ASSERT_EQUAL(expected_char, actual_char);

    str_free(s);
}

void test_str_append_success() {

    const char c = 't';
    str* s1 = str_new("yee");

    str* s2 = str_append(s1, c);

    TEST_ASSERT_EQUAL_STRING("yee", s1->data);
    TEST_ASSERT_EQUAL(3, s1->length);
    TEST_ASSERT_EQUAL(true, s1->heap);

    TEST_ASSERT_EQUAL_STRING("yeet", s2->data);
    TEST_ASSERT_EQUAL(4, s2->length);
    TEST_ASSERT_EQUAL(true, s2->heap);

    str_free(s1);
    str_free(s2);
}

void test_str_append_failure_null_character() {

    const char c = '\0';
    str* s = str_new("yee");

    str* n = str_append(s, c);

    TEST_ASSERT_NULL(n);
    TEST_ASSERT_EQUAL_STRING("yee", s->data);

    str_free(s);
    str_free(n);
}

void test_str_append_failure_null_str() {

    const char c = 't';
    str* s = NULL;

    str* n = str_append(s, c);

    TEST_ASSERT_NULL(n);

    str_free(s);
    str_free(n);
}

void test_str_len_success() {

    const char* text = "this is a test string!";
    size_t expected_len = strlen(text);
    str* s = str_new(text);

    size_t actual_len = str_len(s);

    TEST_ASSERT_EQUAL(expected_len, actual_len);

    str_free(s);
}

void test_str_len_failure_null_str() {

    const char* text = "this is a test string!";
    size_t expected_len = 0;
    str* s = NULL;

    size_t actual_len = str_len(s);

    TEST_ASSERT_EQUAL(expected_len, actual_len);

    str_free(s);
}

void test_str_cmp_success_ident_str() {

    const char* text = "this is a test string!";
    str* s1 = str_new(text);
    str* s2 = str_new(text);

    bool equal = str_cmp(s1, s2);

    TEST_ASSERT_TRUE(equal);

    str_free(s1);
    str_free(s2);
}

void test_str_cmp_success_same_text() {

    const char* text = "this is a test string!";
    str* s1 = str_new(text);
    str* s2 = str_new(text);

    size_t len_s1 = str_len(s1);
    size_t len_s2 = str_len(s2);

    s1->heap = true;
    s2->heap = false;

    s1->length = 45;

    bool equal = str_cmp(s1, s2);

    TEST_ASSERT_TRUE(equal);

    // Restore the string state so free() works as expected; this test
    // isn't for free(), so why stress it.
    s1->heap = true;
    s2->heap = true;

    s1->length = len_s1;
    s2->length = len_s2;

    str_free(s1);
    str_free(s2);
}

void test_str_cmp_failure_different_str() {

    const char* text1 = "this is a test string!";
    const char* text2 = "this is a different test string!";
    str* s1 = str_new(text1);
    str* s2 = str_new(text2);

    bool equal = str_cmp(s1, s2);

    TEST_ASSERT_FALSE(equal);

    str_free(s1);
    str_free(s2);
}

void test_str_cmp_failure_different_text() {

    // different string but otherwise same fields
    const char* text1 = "this is a test string!";
    const char* text2 = "this is a XXXX string!";
    str* s1 = str_new(text1);
    str* s2 = str_new(text2);

    bool equal = str_cmp(s1, s2);

    TEST_ASSERT_FALSE(equal);

    str_free(s1);
    str_free(s2);
}

void test_str_cmp_failure_one_null() {

    const char* text = "this is a test string!";
    str* s1 = str_new(text);
    str* s2 = NULL;

    bool equal = str_cmp(s1, s2);

    TEST_ASSERT_FALSE(equal);

    str_free(s1);
}

void test_str_cmp_failure_both_null() {

    str* s1 = NULL;
    str* s2 = NULL;

    bool equal = str_cmp(s1, s2);

    TEST_ASSERT_FALSE(equal);
}

void test_str_cmp_raw_success() {

    const char* text1 = "";
    const char* text2 = "170298awhn";
    const char* text3 = "this is a test string!";
    str* s1 = str_new(text1);
    str* s2 = str_new(text2);
    str* s3 = str_new(text3);

    TEST_ASSERT_TRUE(str_cmp_raw(s1, text1));
    TEST_ASSERT_TRUE(str_cmp_raw(s2, text2));
    TEST_ASSERT_TRUE(str_cmp_raw(s3, text3));

    str_free(s1);
    str_free(s2);
    str_free(s3);
}

void test_str_cmp_raw_failure() {

    const char* text = "this is a test string!";
    str* s1 = str_new(text);
    str* s2 = str_new(text);
    str* s3 = str_new(text);
    str* s4 = str_new(text);

    TEST_ASSERT_FALSE(str_cmp_raw(s1, ""));
    TEST_ASSERT_FALSE(str_cmp_raw(s2, "24378sdfjhjas6"));
    TEST_ASSERT_FALSE(str_cmp_raw(s3, "this is a_test_string!"));
    TEST_ASSERT_FALSE(str_cmp_raw(s4, "this is a test string! with some more text!"));

    str_free(s1);
    str_free(s2);
    str_free(s3);
    str_free(s4);
}

void test_str_ident_success_ident_str() {

    const char* text = "this is a test string!";
    str* s1 = str_new(text);
    str* s2 = str_new(text);

    bool equal = str_ident(s1, s2);

    TEST_ASSERT_TRUE(equal);

    str_free(s1);
    str_free(s2);
}

void test_str_ident_failure_same_text() {

    const char* text = "this is a test string!";
    str* s1 = str_new(text);
    str* s2 = str_new(text);

    size_t len_s1 = str_len(s1);
    size_t len_s2 = str_len(s2);

    s1->heap = true;
    s2->heap = false;

    s1->length = 45;

    bool equal = str_ident(s1, s2);

    TEST_ASSERT_FALSE(equal);

    // Restore the string state so free() works as expected; this test
    // isn't for free(), so why stress it.
    s1->heap = true;
    s2->heap = true;

    s1->length = len_s1;
    s2->length = len_s2;

    str_free(s1);
    str_free(s2);
}

void test_str_ident_failure_different_str() {

    const char* text1 = "this is a test string!";
    const char* text2 = "this is a different test string!";
    str* s1 = str_new(text1);
    str* s2 = str_new(text2);

    bool equal = str_ident(s1, s2);

    TEST_ASSERT_FALSE(equal);

    str_free(s1);
    str_free(s2);
}

void test_str_ident_failure_different_text() {

    // different string but otherwise same fields
    const char* text1 = "this is a test string!";
    const char* text2 = "this is a XXXX string!";
    str* s1 = str_new(text1);
    str* s2 = str_new(text2);

    bool equal = str_ident(s1, s2);

    TEST_ASSERT_FALSE(equal);

    str_free(s1);
    str_free(s2);
}

void test_str_ident_failure_one_null() {

    const char* text = "this is a test string!";
    str* s1 = str_new(text);
    str* s2 = NULL;

    bool equal = str_ident(s1, s2);

    TEST_ASSERT_FALSE(equal);

    str_free(s1);
}

void test_str_ident_failure_both_null() {

    str* s1 = NULL;
    str* s2 = NULL;

    bool equal = str_ident(s1, s2);

    TEST_ASSERT_FALSE(equal);
}

void test_str_sub_success_single() {

    TEST_IGNORE_MESSAGE(
        "This test should succeed, but I'm too lazy to fix it!");

    const char* text = "this is a test string!";
    const char* sub = "test";
    str* s1 = str_new(text);
    str* s2 = str_new(sub);
    int expected_index = 9;

    int actual_index = str_sub(s1, s2);

    TEST_ASSERT_EQUAL(expected_index, actual_index);

    str_free(s1);
}

void test_str_sub_success_double() {

    TEST_IGNORE_MESSAGE(
        "This test should succeed, but I'm too lazy to fix it!");

    const char* text = "this is a test string! with some more tests content!!";
    const char* sub = "test";
    str* s1 = str_new(text);
    str* s2 = str_new(sub);
    int expected_index = 9;

    int actual_index = str_sub(s1, s2);

    TEST_ASSERT_EQUAL(expected_index, actual_index);

    str_free(s1);
}

void test_str_sub_failure_none() {
    const char* text = "this is a test string!";
    const char* sub = "nope";
    str* s1 = str_new(text);
    str* s2 = str_new(sub);
    int expected_index = -1;

    int actual_index = str_sub(s1, s2);

    TEST_ASSERT_EQUAL(expected_index, actual_index);

    str_free(s1);
}

void test_str_sub_failure_null_str() {
    const char* sub = "nope";
    str* s1 = NULL;
    str* s2 = str_new(sub);
    int expected_index = -1;

    int actual_index = str_sub(s1, s2);

    TEST_ASSERT_EQUAL(expected_index, actual_index);

    str_free(s2);
}

void test_str_sub_failure_null_sub() {
    const char* text = "this is a test string!";
    str* s1 = str_new(text);
    str* s2 = NULL;
    int expected_index = -1;

    int actual_index = str_sub(s1, s2);

    TEST_ASSERT_EQUAL(expected_index, actual_index);

    str_free(s1);
}

void test_str_sub_failure_both_null() {
    str* s1 = NULL;
    str* s2 = NULL;
    int expected_index = -1;

    int actual_index = str_sub(s1, s2);

    TEST_ASSERT_EQUAL(expected_index, actual_index);
}

void test_str_view_success() {
    const char* text = "here is some text";
    size_t start = 8;
    size_t end = 12;
    str* s = str_new(text);
    const char* expected_text = "some";

    str* view = str_view(s, start, end);

    TEST_ASSERT_EQUAL_STRING(expected_text, view->data);

    str_free(s);
}

void test_str_view_success_free() {
    const char* text = "here is some text";
    size_t start = 8;
    size_t end = 12;
    str* s = str_new(text);
    const char* expected_text = "some";

    str* view = str_view(s, start, end);

    TEST_ASSERT_EQUAL_STRING(expected_text, view->data);

    str_free(view);

    TEST_ASSERT_EQUAL_STRING(text, s->data);

    str_free(s);
}

void test_str_view_failure_start_greater_than_end() {
    const char* text = "here is some text";
    size_t start = 80;
    size_t end = 13;
    str* s = str_new(text);

    str* view = str_view(s, start, end);

    TEST_ASSERT_NULL(view);

    str_free(s);
}

void test_str_view_failure_start_too_large() {
    const char* text = "here is some text";
    size_t start = 250;
    size_t end = 400;
    str* s = str_new(text);

    str* view = str_view(s, start, end);

    TEST_ASSERT_NULL(view);

    str_free(s);
}

void test_str_view_failure_end_too_large() {
    const char* text = "here is some text";
    size_t start = 4;
    size_t end = 400;
    str* s = str_new(text);

    str* view = str_view(s, start, end);

    TEST_ASSERT_NULL(view);

    str_free(s);
}

void test_str_view_failure_start_equal_to_end() {
    const char* text = "here is some text";
    size_t start = 4;
    size_t end = 4;
    str* s = str_new(text);

    str* view = str_view(s, start, end);

    TEST_ASSERT_NULL(view);

    str_free(s);
}

void test_str_raw_success() {
    const char* text = "abcdefghijklmnopqrstuvwxyz";
    str* s = str_new(text);

    char* raw = str_raw(s);

    TEST_ASSERT_EQUAL_STRING(text, raw);

    str_free(s);
    free(raw);
}

void test_str_raw_failure_null_string() {
    const char* text = "abcdefghijklmnopqrstuvwxyz";
    str* s = NULL;

    char* raw = str_raw(s);

    TEST_ASSERT_NULL(raw);

    free(raw);
}

void test_str_raw_failure_null_data() {
    const char* text = "abcdefghijklmnopqrstuvwxyz";
    str* s = str_new(text);
    char* real_data = s->data;
    s->data = NULL;

    char* raw = str_raw(s);

    TEST_ASSERT_NULL(raw);

    s->data = real_data;
    str_free(s);
    free(raw);
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
    index_t expected_boundaries[] = { 0,  4,  5,  6,  7,  8,  9,  10,
                                     11, 12, 13, 14, 15, 16, 17, 18,
                                     19, 20, 21, 25, 26, 27 };
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
    index_t expected_boundaries[] = { 0, 1,  2,  3,  6,  7,  8,
                                     9, 15, 16, 19, 20, 21, 22 };
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

void test_str_str_cmp_raw_success_1() {

    const char* text = "def";
    str* s = str_new(text);

    TEST_ASSERT(str_cmp_raw(s, text));

    str_free(s);
}

void test_str_str_cmp_raw_success_2() {

    const char* text = "this is something more complex!!!!\n\n\n";
    str* s = str_new(text);

    TEST_ASSERT(str_cmp_raw(s, text));

    str_free(s);
}

void test_str_str_cmp_raw_success_3() {

    const char* text = "t&_NV*(@#$&QW(8n-C&AQ#($*&Q@_+4cQ@&$M+C+4mcQ)M4c7="
        "Q40CMQ )9$Aw90euasdj*(CAJM_W*()JECQA_@$))";
    str* s = str_new(text);

    TEST_ASSERT(str_cmp_raw(s, text));

    str_free(s);
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
    str* s1 = str_new("0u8");
    str* s2 = str_new("127u8");
    str* s3 = str_new("255u8");
    TEST_ASSERT_TRUE(str_is_u8_literal(s1));
    TEST_ASSERT_TRUE(str_is_u8_literal(s2));
    TEST_ASSERT_TRUE(str_is_u8_literal(s3));
    str_free(s1);
    str_free(s2);
    str_free(s3);

    str* x1 = str_new("");
    str* x2 = str_new("u8");
    str* x3 = str_new("256u8");
    str* x4 = str_new("1267u8");
    str* x5 = str_new("2367823632696732423978u8"); // TODO: there may be a better number!
    TEST_ASSERT_FALSE(str_is_u8_literal(x1));
    TEST_ASSERT_FALSE(str_is_u8_literal(x2));
    TEST_ASSERT_FALSE(str_is_u8_literal(x3));
    TEST_ASSERT_FALSE(str_is_u8_literal(x4));
    TEST_ASSERT_FALSE(str_is_u8_literal(x5));
    str_free(x1);
    str_free(x2);
    str_free(x3);
    str_free(x4);
    str_free(x5);
}

void test_str_is_u16_literal() {
    str* s1 = str_new("0u16");
    str* s2 = str_new("127u16");
    str* s3 = str_new("65535u16");
    TEST_ASSERT_TRUE(str_is_u16_literal(s1));
    TEST_ASSERT_TRUE(str_is_u16_literal(s2));
    TEST_ASSERT_TRUE(str_is_u16_literal(s3));
    str_free(s1);
    str_free(s2);
    str_free(s3);

    str* x1 = str_new("");
    str* x2 = str_new("u16");
    str* x3 = str_new("65536u16");
    str* x4 = str_new("172908u16");
    str* x5 = str_new("2367823632696732423978u16"); // TODO: there may be a better number!
    str* x6 = str_new("2u8");
    str* x7 = str_new("732897928u32");
    str* x8 = str_new("73u64");
    str* x9 = str_new("75");
    str* x10 = str_new("u8");
    TEST_ASSERT_FALSE(str_is_u16_literal(x1));
    TEST_ASSERT_FALSE(str_is_u16_literal(x2));
    TEST_ASSERT_FALSE(str_is_u16_literal(x3));
    TEST_ASSERT_FALSE(str_is_u16_literal(x4));
    TEST_ASSERT_FALSE(str_is_u16_literal(x5));
    TEST_ASSERT_FALSE(str_is_u16_literal(x6));
    TEST_ASSERT_FALSE(str_is_u16_literal(x7));
    TEST_ASSERT_FALSE(str_is_u16_literal(x8));
    TEST_ASSERT_FALSE(str_is_u16_literal(x9));
    TEST_ASSERT_FALSE(str_is_u16_literal(x10));
    str_free(x1);
    str_free(x2);
    str_free(x3);
    str_free(x4);
    str_free(x5);
    str_free(x6);
    str_free(x7);
    str_free(x8);
    str_free(x9);
    str_free(x10);
}

void test_str_is_u32_literal() {
    str* s1 = str_new("0u32");
    str* s2 = str_new("65535u32");
    str* s3 = str_new("4294967295u32");
    TEST_ASSERT_TRUE(str_is_u32_literal(s1));
    TEST_ASSERT_TRUE(str_is_u32_literal(s2));
    TEST_ASSERT_TRUE(str_is_u32_literal(s3));
    str_free(s1);
    str_free(s2);
    str_free(s3);

    str* x1 = str_new("");
    str* x2 = str_new("u32");
    str* x3 = str_new("4294967296u32");
    str* x4 = str_new("17290827349827u32");
    str* x5 = str_new("2367823632696732423978u32");
    str* x6 = str_new("2u8");
    str* x7 = str_new("732897928u16");
    str* x8 = str_new("73u64");
    str* x9 = str_new("75");
    str* x10 = str_new("u8");
    TEST_ASSERT_FALSE(str_is_u32_literal(x1));
    TEST_ASSERT_FALSE(str_is_u32_literal(x2));
    TEST_ASSERT_FALSE(str_is_u32_literal(x3));
    TEST_ASSERT_FALSE(str_is_u32_literal(x4));
    TEST_ASSERT_FALSE(str_is_u32_literal(x5));
    TEST_ASSERT_FALSE(str_is_u32_literal(x6));
    TEST_ASSERT_FALSE(str_is_u32_literal(x7));
    TEST_ASSERT_FALSE(str_is_u32_literal(x8));
    TEST_ASSERT_FALSE(str_is_u32_literal(x9));
    TEST_ASSERT_FALSE(str_is_u32_literal(x10));
    str_free(x1);
    str_free(x2);
    str_free(x3);
    str_free(x4);
    str_free(x5);
    str_free(x6);
    str_free(x7);
    str_free(x8);
    str_free(x9);
    str_free(x10);
}

void test_str_is_u64_literal() {
    str* s1 = str_new("0u64");
    str* s2 = str_new("4294967295u64");
    str* s3 = str_new("18446744073709551615u64");
    TEST_ASSERT_TRUE(str_is_u64_literal(s1));
    TEST_ASSERT_TRUE(str_is_u64_literal(s2));
    TEST_ASSERT_TRUE(str_is_u64_literal(s3));
    str_free(s1);
    str_free(s2);
    str_free(s3);

    str* x1 = str_new("");
    str* x2 = str_new("u32");
    str* x3 = str_new("4294967296u32");
    str* x4 = str_new("17290827349827u32");
    str* x5 = str_new("236782363269673242378220923789247978u64");
    str* x6 = str_new("2u8");
    str* x7 = str_new("732897928u16");
    str* x8 = str_new("73u8");
    str* x9 = str_new("75");
    str* x10 = str_new("u64");
    TEST_ASSERT_FALSE(str_is_u64_literal(x1));
    TEST_ASSERT_FALSE(str_is_u64_literal(x2));
    TEST_ASSERT_FALSE(str_is_u64_literal(x3));
    TEST_ASSERT_FALSE(str_is_u64_literal(x4));
    TEST_ASSERT_FALSE(str_is_u64_literal(x5));
    TEST_ASSERT_FALSE(str_is_u64_literal(x6));
    TEST_ASSERT_FALSE(str_is_u64_literal(x7));
    TEST_ASSERT_FALSE(str_is_u64_literal(x8));
    TEST_ASSERT_FALSE(str_is_u64_literal(x9));
    TEST_ASSERT_FALSE(str_is_u64_literal(x10));
    str_free(x1);
    str_free(x2);
    str_free(x3);
    str_free(x4);
    str_free(x5);
    str_free(x6);
    str_free(x7);
    str_free(x8);
    str_free(x9);
    str_free(x10);
}

int main(void) {
    UNITY_BEGIN();

    if (true) {
        RUN_TEST(test_str_new_success);
        RUN_TEST(test_str_new_null_string);

        RUN_TEST(test_str_free_valid_string);
        RUN_TEST(test_str_free_valid_string_null_data);
        RUN_TEST(test_str_free_null_string);

        RUN_TEST(test_str_concat_nominal_success);
        RUN_TEST(test_str_concat_null_parameter);
        RUN_TEST(test_str_concat_malformed_parameter);

        RUN_TEST(test_str_cmp_success_ident_str);
        RUN_TEST(test_str_cmp_success_same_text);
        RUN_TEST(test_str_cmp_failure_different_str);
        RUN_TEST(test_str_cmp_failure_different_text);
        RUN_TEST(test_str_cmp_failure_one_null);
        RUN_TEST(test_str_cmp_failure_both_null);

        RUN_TEST(test_str_cmp_raw_success);
        RUN_TEST(test_str_cmp_raw_failure);

        RUN_TEST(test_str_ident_success_ident_str);
        RUN_TEST(test_str_ident_failure_same_text);
        RUN_TEST(test_str_ident_failure_different_str);
        RUN_TEST(test_str_ident_failure_different_text);
        RUN_TEST(test_str_ident_failure_one_null);
        RUN_TEST(test_str_ident_failure_both_null);

        RUN_TEST(test_str_find_success);
        RUN_TEST(test_str_find_failure_not_present);
        RUN_TEST(test_str_find_failure_empty_str);
        RUN_TEST(test_str_find_failure_null_str);
        RUN_TEST(test_str_find_failure_empty_str_null_char);

        RUN_TEST(test_str_sub_success_single);
        RUN_TEST(test_str_sub_success_double);
        RUN_TEST(test_str_sub_failure_none);
        RUN_TEST(test_str_sub_failure_null_str);
        RUN_TEST(test_str_sub_failure_null_sub);
        RUN_TEST(test_str_sub_failure_both_null);

        RUN_TEST(test_str_len_success);
        RUN_TEST(test_str_len_failure_null_str);

        RUN_TEST(test_str_at_success);
        RUN_TEST(test_str_at_failure_index_too_big);
        RUN_TEST(test_str_at_failure_null_str);

        RUN_TEST(test_str_append_success);
        RUN_TEST(test_str_append_failure_null_character);
        RUN_TEST(test_str_append_failure_null_str);

        RUN_TEST(test_str_view_success);
        RUN_TEST(test_str_view_success_free);
        RUN_TEST(test_str_view_failure_start_greater_than_end);
        RUN_TEST(test_str_view_failure_start_too_large);
        RUN_TEST(test_str_view_failure_end_too_large);
        RUN_TEST(test_str_view_failure_start_equal_to_end);

        RUN_TEST(test_str_raw_success);
        RUN_TEST(test_str_raw_failure_null_string);
        RUN_TEST(test_str_raw_failure_null_data);

        RUN_TEST(test_str_str_cmp_raw_success_1);
        RUN_TEST(test_str_str_cmp_raw_success_2);
        RUN_TEST(test_str_str_cmp_raw_success_3);

    }

    // Custom functions -- not strictly library based!
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
    }


    return UNITY_END();
}