#ifndef __TEST_BINT_OBJ_H
#define __TEST_BINT_OBJ_H

#include "bint.h"
#include "unity.h"
#include "debug.h"

void run_bint_obj_tests(void);

void test_bint_new(void);
void test_bint_anew(void);
void test_bint_new_str(void);
void test_bint_new_cstr(void);
void test_bint_free(void);
void test_bint_free_arena(void);
void test_bint_to_str(void);
void test_bint_to_astr(void);

#endif