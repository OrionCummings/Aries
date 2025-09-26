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
    TEST_ASSERT_EQUAL(expected_string, s->data);
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
}

void test_str_concat_null_parameter() {

    str* s1 = str_new("example1");

    str* actual_string = str_concat(s1, NULL);

    TEST_ASSERT_NULL(actual_string);
}

void test_str_concat_malformed_parameter() {

    str* s1 = str_new("example1");
    free(s1->data);
    s1->data = NULL;

    str* actual_string = str_concat(s1, NULL);

    TEST_ASSERT_NULL(actual_string);
}

void test_str_find_success() {

    int expected_pos = 3;
    char c = 'm';
    str* s = str_new("example1");

    int actual_pos = str_find(s, c);

    TEST_ASSERT_EQUAL(expected_pos, actual_pos);
}

void test_str_find_failure_not_present() {

    int expected_pos = -1;
    char c = 'z';
    str* s = str_new("example1");

    int actual_pos = str_find(s, c);

    TEST_ASSERT_EQUAL(expected_pos, actual_pos);
}

void test_str_find_failure_empty_str() {

    int expected_pos = -1;
    char c = 'z';
    str* s = str_new("");

    int actual_pos = str_find(s, c);

    TEST_ASSERT_EQUAL(expected_pos, actual_pos);
}

void test_str_find_failure_null_str() {

    int expected_pos = -1;
    char c = 'z';
    str* s = NULL;

    int actual_pos = str_find(s, c);

    TEST_ASSERT_EQUAL(expected_pos, actual_pos);
}

void test_str_find_failure_empty_str_null_char() {

    int expected_pos = -1;
    char c = '\0';
    str* s = str_new("");

    int actual_pos = str_find(s, c);

    TEST_ASSERT_EQUAL(expected_pos, actual_pos);
}

void test_str_at_success() {

    const char expected_char = 'i';
    const int index = 2;
    const str* s = str_new("this is a test!");

    char actual_char = str_at(s, index);

    TEST_ASSERT_EQUAL(expected_char, actual_char);
}

void test_str_at_failure_index_too_big() {

    const char expected_char = '\0';
    const int index = 23;
    const str* s = str_new("this is a test!");

    char actual_char = str_at(s, index);

    TEST_ASSERT_EQUAL(expected_char, actual_char);
}

void test_str_at_failure_null_str() {

    const char expected_char = '\0';
    const int index = 2;
    const str* s = NULL;

    char actual_char = str_at(s, index);

    TEST_ASSERT_EQUAL(expected_char, actual_char);
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_str_new_success);
    RUN_TEST(test_str_new_null_string);

    RUN_TEST(test_str_free_valid_string);
    RUN_TEST(test_str_free_valid_string_null_data);
    RUN_TEST(test_str_free_null_string);

    RUN_TEST(test_str_at_success);
    RUN_TEST(test_str_at_failure_index_too_big);
    RUN_TEST(test_str_at_failure_null_str);

    RUN_TEST(test_str_concat_nominal_success);
    RUN_TEST(test_str_concat_null_parameter);
    RUN_TEST(test_str_concat_malformed_parameter);

    RUN_TEST(test_str_find_success);
    RUN_TEST(test_str_find_failure_not_present);
    RUN_TEST(test_str_find_failure_empty_str);
    RUN_TEST(test_str_find_failure_null_str);
    RUN_TEST(test_str_find_failure_empty_str_null_char);

    

    return UNITY_END();
}