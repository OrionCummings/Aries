#include "unity.h"
#include "utils.h"

void setUp() {
}

void tearDown() {
}

void test_trace(void) {
	TEST_ASSERT_EQUAL(1, 1);

	A_TRACE();
	
}

int main(void) {
	UNITY_BEGIN();
	RUN_TEST(test_trace);
	return UNITY_END();
}