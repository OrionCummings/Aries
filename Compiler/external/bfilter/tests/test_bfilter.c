#include "unity.h"
#include "bfilter.h"
#include "arena.h"
#include "debug.h"
#include "test_bfilter.h"

#define TEST_ARENA_SIZE_BYTES (1024)

static arena* scratchpad;

void test_bfilter_anew(void) {
    // TODO: Complete and find a better location!
    // TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_bfilter_add(void) {
    // TODO: Complete and find a better location!
    // TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

void test_bfilter_in(void) {
    // TODO: Complete and find a better location!
    // TEST_IGNORE_MESSAGE("NOT IMPLEMENTED");
}

////////////////////////////////////////////////

void setUp() {
    arena_reset(scratchpad);
}

void tearDown() {
}

void init_suite() {
    LOG_PUSH(LOG_NONE);
    scratchpad = arena_new(TEST_ARENA_SIZE_BYTES);
}

void deinit_suite() {
    arena_free(scratchpad);
    LOG_POP();
}

int main(void) {
    init_suite();
    UNITY_BEGIN();

    test_bfilter_anew();
    test_bfilter_add();
    test_bfilter_in();

    int ue = UNITY_END();
    deinit_suite();
    return ue;
}