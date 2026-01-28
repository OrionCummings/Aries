import unittest
import itertools
from Operation import Operation, Operations, OperationType

class OperationTests(unittest.TestCase):
    
    no_operation_expected_truth_table = {
        #   (  a,     b,    cin ): (  s,   cout )
            (False, False, False): (False, False),
            (False, False, True):  (False, False),
            (False, True,  False): (False, False),
            (False, True,  True):  (False, False),
            (True,  False, False): (False, False),
            (True,  False, True):  (False, False),
            (True,  True,  False): (False, False),
            (True,  True,  True):  (False, False),
        }
    not_expected_truth_table = {
        #   (  a,     b,    cin ): (  s,   cout )
            (False, False, False): (True,  False),
            (False, False, True):  (True,  False),
            (False, True,  False): (True,  False),
            (False, True,  True):  (True,  False),
            (True,  False, False): (False, False),
            (True,  False, True):  (False, False),
            (True,  True,  False): (False, False),
            (True,  True,  True):  (False, False),
        }
    and_expected_truth_table = {
        #   (  a,     b,    cin ): (  s,   cout )
            (False, False, False): (False, False),
            (False, False, True):  (False, False),
            (False, True,  False): (False, False),
            (False, True,  True):  (False, False),
            (True,  False, False): (False, False),
            (True,  False, True):  (False, False),
            (True,  True,  False): (True,  False),
            (True,  True,  True):  (True,  False),
        }
    nand_expected_truth_table = {
        #   (  a,     b,    cin ): (  s,   cout )
            (False, False, False): (True,  False),
            (False, False, True):  (True,  False),
            (False, True,  False): (True,  False),
            (False, True,  True):  (True,  False),
            (True,  False, False): (True,  False),
            (True,  False, True):  (True,  False),
            (True,  True,  False): (False, False),
            (True,  True,  True):  (False, False),
        }
    or_expected_truth_table = {
        #   (  a,     b,    cin ): (  s,   cout )
            (False, False, False): (False, False),
            (False, False, True):  (False, False),
            (False, True,  False): (True,  False),
            (False, True,  True):  (True,  False),
            (True,  False, False): (True,  False),
            (True,  False, True):  (True,  False),
            (True,  True,  False): (True,  False),
            (True,  True,  True):  (True,  False),
        }
    xor_expected_truth_table = {
        #   (  a,     b,    cin ): (  s,   cout )
            (False, False, False): (False, False),
            (False, False, True):  (False, False),
            (False, True,  False): (True,  False),
            (False, True,  True):  (True,  False),
            (True,  False, False): (True,  False),
            (True,  False, True):  (True,  False),
            (True,  True,  False): (False, False),
            (True,  True,  True):  (False, False),
        }
    nor_expected_truth_table = {
        #   (  a,     b,    cin ): (  s,   cout )
            (False, False, False): (True,  False),
            (False, False, True):  (True,  False),
            (False, True,  False): (False, False),
            (False, True,  True):  (False, False),
            (True,  False, False): (False, False),
            (True,  False, True):  (False, False),
            (True,  True,  False): (False, False),
            (True,  True,  True):  (False, False),
        }
    xnor_expected_truth_table = {
        #   (  a,     b,    cin ): (  s,   cout )
            (False, False, False): (True,  False),
            (False, False, True):  (True,  False),
            (False, True,  False): (False, False),
            (False, True,  True):  (False, False),
            (True,  False, False): (False, False),
            (True,  False, True):  (False, False),
            (True,  True,  False): (True,  False),
            (True,  True,  True):  (True,  False),
        }
    add_expected_truth_table = {
        #   (  a,     b,    cin ): (  s,   cout )
            (False, False, False): (False, False),
            (False, False, True):  (True,  False),
            (False, True,  False): (True,  False),
            (False, True,  True):  (False, True),
            (True,  False, False): (True,  False),
            (True,  False, True):  (False, True),
            (True,  True,  False): (False, True),
            (True,  True,  True):  (True,  True),
        }

    @staticmethod
    def product() -> list[tuple]:
        return list(itertools.product([False, True], repeat=3))

    def test_op_no_operation(self):

        actual_truth_table = {}
        p = OperationTests.product()

        for (a, b, cin) in p:
            (s, cout) = Operations.op_no_operation(a, b, cin)
            actual_truth_table[(a, b, cin)] = (s, cout)
            self.assertEqual(OperationTests.no_operation_expected_truth_table[(a, b, cin)], actual_truth_table[(a, b, cin)])

    def test_op_not(self):
        
        actual_truth_table = {}
        p = OperationTests.product()

        for (a, b, cin) in p:
            (s, cout) = Operations.op_not(a, b, cin)
            actual_truth_table[(a, b, cin)] = (s, cout)
            self.assertEqual(OperationTests.not_expected_truth_table[(a, b, cin)], actual_truth_table[(a, b, cin)])

    def test_op_and(self):
        
        actual_truth_table = {}
        p = OperationTests.product()

        for (a, b, cin) in p:
            (s, cout) = Operations.op_and(a, b, cin)
            actual_truth_table[(a, b, cin)] = (s, cout)
            self.assertEqual(OperationTests.and_expected_truth_table[(a, b, cin)], actual_truth_table[(a, b, cin)])

    def test_op_nand(self):
        
        actual_truth_table = {}
        p = OperationTests.product()

        for (a, b, cin) in p:
            (s, cout) = Operations.op_nand(a, b, cin)
            actual_truth_table[(a, b, cin)] = (s, cout)
            self.assertEqual(OperationTests.nand_expected_truth_table[(a, b, cin)], actual_truth_table[(a, b, cin)])

    def test_op_or(self):
        
        actual_truth_table = {}
        p = OperationTests.product()

        for (a, b, cin) in p:
            (s, cout) = Operations.op_or(a, b, cin)
            actual_truth_table[(a, b, cin)] = (s, cout)
            self.assertEqual(OperationTests.or_expected_truth_table[(a, b, cin)], actual_truth_table[(a, b, cin)])

    def test_op_xor(self):
        
        actual_truth_table = {}
        p = OperationTests.product()

        for (a, b, cin) in p:
            (s, cout) = Operations.op_xor(a, b, cin)
            actual_truth_table[(a, b, cin)] = (s, cout)
            self.assertEqual(OperationTests.xor_expected_truth_table[(a, b, cin)], actual_truth_table[(a, b, cin)])

    def test_op_nor(self):
        
        actual_truth_table = {}
        p = OperationTests.product()

        for (a, b, cin) in p:
            (s, cout) = Operations.op_nor(a, b, cin)
            actual_truth_table[(a, b, cin)] = (s, cout)
            self.assertEqual(OperationTests.nor_expected_truth_table[(a, b, cin)], actual_truth_table[(a, b, cin)])

    def test_op_xnor(self):

        actual_truth_table = {}
        p = OperationTests.product()

        for (a, b, cin) in p:
            (s, cout) = Operations.op_xnor(a, b, cin)
            actual_truth_table[(a, b, cin)] = (s, cout)
            self.assertEqual(OperationTests.xnor_expected_truth_table[(a, b, cin)], actual_truth_table[(a, b, cin)])

    def test_op_add(self):
        
        actual_truth_table = {}
        p = OperationTests.product()

        for (a, b, cin) in p:
            (s, cout) = Operations.op_add(a, b, cin)
            actual_truth_table[(a, b, cin)] = (s, cout)
            self.assertEqual(OperationTests.add_expected_truth_table[(a, b, cin)], actual_truth_table[(a, b, cin)])

    def test_operation_constructor(self):

        for op_type in OperationType:
            op = Operation(op_type)
            self.assertTrue(isinstance(op, Operation))

    def test_eval_op_no_operation(self):

        op = Operation(OperationType.NoOperation)
        for (a, b, cin) in OperationTests.product():
            (s, cout) = Operations.op_no_operation(a, b, cin)
            self.assertEqual(op.eval(a, b, cin), (s, cout))

    def test_eval_op_not(self):

        op = Operation(OperationType.Not)
        for (a, b, cin) in OperationTests.product():
            (s, cout) = Operations.op_not(a, b, cin)
            self.assertEqual(op.eval(a, b, cin), (s, cout))

    def test_eval_op_and(self):

        op = Operation(OperationType.And)
        for (a, b, cin) in OperationTests.product():
            (s, cout) = Operations.op_and(a, b, cin)
            self.assertEqual(op.eval(a, b, cin), (s, cout))

    def test_eval_op_nand(self):

        op = Operation(OperationType.Nand)
        for (a, b, cin) in OperationTests.product():
            (s, cout) = Operations.op_nand(a, b, cin)
            self.assertEqual(op.eval(a, b, cin), (s, cout))

    def test_eval_op_or(self):

        op = Operation(OperationType.Or)
        for (a, b, cin) in OperationTests.product():
            (s, cout) = Operations.op_or(a, b, cin)
            self.assertEqual(op.eval(a, b, cin), (s, cout))

    def test_eval_op_xor(self):

        op = Operation(OperationType.Xor)
        for (a, b, cin) in OperationTests.product():
            (s, cout) = Operations.op_xor(a, b, cin)
            self.assertEqual(op.eval(a, b, cin), (s, cout))

    def test_eval_op_nor(self):

        op = Operation(OperationType.Nor)
        for (a, b, cin) in OperationTests.product():
            (s, cout) = Operations.op_nor(a, b, cin)
            self.assertEqual(op.eval(a, b, cin), (s, cout))

    def test_eval_op_xnor(self):

        op = Operation(OperationType.Xnor)
        for (a, b, cin) in OperationTests.product():
            (s, cout) = Operations.op_xnor(a, b, cin)
            self.assertEqual(op.eval(a, b, cin), (s, cout))

    def test_eval_op_add(self):

        op = Operation(OperationType.Add)
        for (a, b, cin) in OperationTests.product():
            (s, cout) = Operations.op_add(a, b, cin)
            (actual_s, actual_cout) = op.eval(a, b, cin)
            self.assertEqual((actual_s, actual_cout), (s, cout))

