#ifndef __TEST_BINT_NAND_H
#define __TEST_BINT_NAND_H

#include "unity.h"
#include "debug.h"
#include "bint.h"

void run_bint_nand_tests(void);

void test_bint_nand_equal_sizes(void);
void test_bint_nand_unequal_sizes(void);
void test_bint_nand_bad_parameters(void);

#endif