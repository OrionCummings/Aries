#ifndef __TEST_PARSER_EXPRESSION_H
#define __TEST_PARSER_EXPRESSION_H

#include "unity.h"
#include "parser.h"

void test_single_expression_assignment(void);

void test_single_expression_assignment_u8(void);
void test_single_expression_assignment_u16(void);
void test_single_expression_assignment_u32(void);
void test_single_expression_assignment_u64(void);

void test_single_expression_assignment_i8(void);
void test_single_expression_assignment_i16(void);
void test_single_expression_assignment_i32(void);
void test_single_expression_assignment_i64(void);

void test_single_expression_assignment_f32(void);
void test_single_expression_assignment_f64(void);

void test_single_expression_assignment_str(void);

#endif