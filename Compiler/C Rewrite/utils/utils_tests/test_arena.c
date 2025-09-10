#include "unity.h"
#include "utils.h"

void setUp() {
}

void tearDown() {
}

void test_arena_new_success(void) {

    arena* a = arena_new(1024);

    TEST_ASSERT_EQUAL_size_t(a->capacity, 1024);
    TEST_ASSERT_EQUAL_size_t(a->size, 0);
    TEST_ASSERT_NOT_NULL(a->data);
    
    arena_free(a);
}

void test_arena_free_success(void) {

    arena* a = arena_new(1024);

    arena_free(a);

    TEST_ASSERT_NULL(a);
}

void test_arena_free_null_arena(void) {

    arena* a = NULL;

    arena_free(a);

    TEST_ASSERT_NULL(a);
}

void test_arena_alloc_success_single(void) {

    arena* a = arena_new(1024);
    size_t size = 128;

    void* ptr = arena_alloc(a, size);

    TEST_ASSERT_NOT_NULL(ptr);
    TEST_ASSERT_EQUAL(size, a->size);

    arena_free(a);
}

void test_arena_alloc_success_multi(void) {

    arena* a = arena_new(1024);

    size_t size1 = 128;
    size_t size2 = 278;
    size_t size3 = 15;

    void* ptr1 = arena_alloc(a, size1);
    TEST_ASSERT_NOT_NULL(ptr1);
    TEST_ASSERT_EQUAL(a->data + 0, ptr1);
    
    void* ptr2 = arena_alloc(a, size2);
    TEST_ASSERT_NOT_NULL(ptr2);
    TEST_ASSERT_EQUAL(a->data + size1, ptr2);
    
    void* ptr3 = arena_alloc(a, size3);
    TEST_ASSERT_NOT_NULL(ptr3);
    TEST_ASSERT_EQUAL(a->data + size1 + size2, ptr3);

    TEST_ASSERT_EQUAL(size1 + size2 + size3, a->size);

    arena_free(a);
}

void test_arena_alloc_success_full(void) {

    arena* a = arena_new(1024);
    size_t size = 1024;

    arena_alloc(a, size);

    TEST_ASSERT_EQUAL(size, a->size);

    arena_free(a);
}

void test_arena_alloc_failure_too_full(void) {

    arena* a = arena_new(1024);
    size_t size = 1025;

    void* ptr = arena_alloc(a, size);

    TEST_ASSERT_NULL(ptr);
    TEST_ASSERT_EQUAL(0, a->size);

    arena_free(a);
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_arena_new_success);
    RUN_TEST(test_arena_free_success);
    RUN_TEST(test_arena_free_null_arena);
    RUN_TEST(test_arena_alloc_success_single);
    RUN_TEST(test_arena_alloc_success_multi);
    RUN_TEST(test_arena_alloc_success_full);
    RUN_TEST(test_arena_alloc_failure_too_full);
    return UNITY_END();
}