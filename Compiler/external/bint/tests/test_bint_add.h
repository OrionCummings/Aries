#ifndef __TEST_BINT_ADD_H
#define __TEST_BINT_ADD_H

#include "unity.h"
#include "debug.h"
#include "bint.h"

void run_bint_add_tests(void);

void test_bint_add(void);

void test_bint_add_increment_no_overflow(void);
void test_bint_add_decrement_no_underflow(void);

void test_bint_add_increment_overflow(void);
void test_bint_add_decrement_underflow(void);

void test_bint_add_overflow_first_byte(void);
void test_bint_add_overflow_mid_byte(void);
void test_bint_add_overflow_last_byte(void);

void test_bint_add_underflow_first_byte(void);
void test_bint_add_underflow_mid_byte(void);
void test_bint_add_underflow_last_byte(void);

#endif