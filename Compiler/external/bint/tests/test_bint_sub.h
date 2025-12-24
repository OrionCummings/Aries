#ifndef __TEST_BINT_SUB_H
#define __TEST_BINT_SUB_H

#include "unity.h"
#include "debug.h"
#include "bint.h"

void run_bint_sub_tests(void);

void test_bint_sub(void);

void test_bint_sub_increment_no_overflow(void);
void test_bint_sub_decrement_no_underflow(void);

void test_bint_sub_increment_overflow(void);
void test_bint_sub_decrement_underflow(void);

void test_bint_sub_overflow_first_byte(void);
void test_bint_sub_overflow_mid_byte(void);
void test_bint_sub_overflow_last_byte(void);

void test_bint_sub_underflow_first_byte(void);
void test_bint_sub_underflow_mid_byte(void);
void test_bint_sub_underflow_last_byte(void);

#endif