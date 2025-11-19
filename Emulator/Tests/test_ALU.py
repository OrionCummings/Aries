import unittest

from ALU import ALU, OperationType

class ALUTests(unittest.TestCase):

    def test_constructor(self):

        a = ALU()

        self.assertIsInstance(a, ALU)

    def test_eval_and(self):

        a = 1
        b = 1
        alu = ALU()
        alu.set_a(a)
        alu.set_b(b)
        alu.set_op(OperationType.AND)
        expected = a & b

        r_evaluation = alu.eval()
        if r_evaluation.is_err:
            self.fail(r_evaluation.unwrap_err())

        (actual, _) = r_evaluation.unwrap()

        self.assertEqual(actual, expected)

    def test_eval_or(self):

        a = 1
        b = 1
        alu = ALU()
        alu.set_a(a)
        alu.set_b(b)
        alu.set_op(OperationType.OR)
        expected = a | b

        r_evaluation = alu.eval()
        if r_evaluation.is_err:
            self.fail(r_evaluation.unwrap_err())

        (actual, _) = r_evaluation.unwrap()

        self.assertEqual(actual, expected)

    def test_eval_add(self):

        a = 1
        b = 1
        cin = 1
        alu = ALU()
        alu.set_a(a)
        alu.set_b(b)
        alu.set_cin(cin)
        alu.set_op(OperationType.ADD)
        expected_s = 1
        expected_c = 1

        r_evaluation = alu.eval()
        if r_evaluation.is_err:
            self.fail(r_evaluation.unwrap_err())

        (actual_s, actual_c) = r_evaluation.unwrap()

        self.assertEqual(actual_s, expected_s)
        self.assertEqual(actual_c, expected_c)

