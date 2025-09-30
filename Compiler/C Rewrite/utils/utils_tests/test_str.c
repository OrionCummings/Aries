#include "unity.h"
#include "utils.h"

void setUp() {
}

void tearDown() {
}

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

int main(void) {
    UNITY_BEGIN();
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

    // str_sub()

    RUN_TEST(test_str_len_success);
    RUN_TEST(test_str_len_failure_null_str);

    RUN_TEST(test_str_at_success);
    RUN_TEST(test_str_at_failure_index_too_big);
    RUN_TEST(test_str_at_failure_null_str);

    RUN_TEST(test_str_append_success);
    RUN_TEST(test_str_append_failure_null_character);
    RUN_TEST(test_str_append_failure_null_str);

    // str_view()

    // RUN_TEST(test_str_split_success);
    // RUN_TEST(test_str_split_failure_null_char);
    // RUN_TEST(test_str_split_failure_null_str);

    return UNITY_END();
}