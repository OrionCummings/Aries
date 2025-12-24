#ifndef __TEST_BINT_MUL_H
#define __TEST_BINT_MUL_H

#include "unity.h"
#include "debug.h"
#include "bint.h"

void run_bint_mul_tests(void);

void test_bint_mul(void);

void test_bint_mul_increment_no_overflow(void);
void test_bint_mul_decrement_no_underflow(void);

void test_bint_mul_increment_overflow(void);
void test_bint_mul_decrement_underflow(void);

void test_bint_mul_overflow_first_byte(void);
void test_bint_mul_overflow_mid_byte(void);
void test_bint_mul_overflow_last_byte(void);

void test_bint_mul_underflow_first_byte(void);
void test_bint_mul_underflow_mid_byte(void);
void test_bint_mul_underflow_last_byte(void);

#endif