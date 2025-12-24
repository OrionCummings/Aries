#ifndef __TEST_BINT_OBJ_H
#define __TEST_BINT_OBJ_H

#include "unity.h"
#include "debug.h"
#include "bint.h"

void run_bint_obj_tests(void);

void test_bint_new(void);

void test_bint_anew(void);
void test_bint_anew_null_arena(void);

void test_bint_new_str(void);
void test_bint_new_cstr(void);

void test_bint_set_bytes(void);
void test_bint_set_bytes_too_many(void);
void test_bint_set_bytes_would_overrun(void);
void test_bint_set_bytes_null_array(void);

void test_bint_free(void);
void test_bint_free_arena(void);
void test_bint_to_str(void);
void test_bint_to_astr(void);

#endif