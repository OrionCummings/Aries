import unittest
from ALU import ALU, ALU1Bit
from Operation import OperationType

class ALU1BitTests(unittest.TestCase):

    def test_constructor(self):

        alu = ALU1Bit()

        self.assertIsInstance(alu, ALU1Bit)

    def test_add(self):

        a = 1
        b = 1

        # a and b are binary!
        self.assertIn(a, [0, 1])
        self.assertIn(b, [0, 1])

        expected_s = 0
        expected_cout = 1

        alu = ALU1Bit()
        alu.set_operation(OperationType.Add)
        alu.set_a(a)
        alu.set_b(b)
        alu.set_cin(0)

        alu.eval()

        actual_s = alu.get_s()
        actual_cout = alu.get_cout()

        # Make sure that carrying actually works!
        self.assertEqual(expected_cout, actual_cout)

        # Check if the result is correct. No need to check
        # the carry!
        self.assertEqual(expected_s, actual_s)

class ALUTests(unittest.TestCase):

    def test_constructor(self):

        a = ALU()

        self.assertIsInstance(a, ALU)

    def test_int_to_boolean_list(self):

        n = 623478
        expected_bool_list = [False,False,False,False,
                              False,False,False,False,
                              False,False,False,False,
                              True,False,False,True,
                              True,False,False,False,
                              False,False,True,True,
                              False,True,True,True,
                              False,True,True,False,]

        actual_bool_list = ALU.int_to_boolean_list(n)

        self.assertListEqual(expected_bool_list, actual_bool_list)

    def test_boolean_list_to_int(self):

        expected_int = 623478
        bool_list = [False,False,False,False,
                     False,False,False,False,
                     False,False,False,False,
                      True,False,False, True,
                      True,False,False,False,
                     False,False, True, True,
                     False, True, True, True,
                     False, True, True,False,]

        actual_int = ALU.boolean_list_to_int(bool_list)

        self.assertEqual(expected_int, actual_int)
    
    def test_add(self):

        a = 12367
        b = 612378

        expected_s = a + b
        expected_cout = 0

        alu = ALU()
        alu.set_operation(OperationType.Add)
        alu.set_a(a)
        alu.set_b(b)
        alu.set_cin(0)

        alu.eval()

        actual_s = alu.get_s()
        actual_cout = alu.get_cout()

        # Make sure that carrying actually works!
        self.assertEqual(expected_cout, actual_cout)

        # Check if the result is correct. No need to check
        # the carry!
        self.assertEqual(expected_s, actual_s)


