import unittest

from Mux import Mux

class MuxTests(unittest.TestCase):

    def test_constructor(self):

        m = Mux()

        self.assertIsInstance(m, Mux)

    def test_explicit_constructor(self):

        n = 4
        m = Mux(n)

        self.assertIsInstance(m, Mux)
        self.assertEqual(m.num_inputs, n)

    def test_set_input(self):

        n = 4
        inputs = [True, True, True, True]
        m = Mux(n)

        for index in range(0, n):
            m.set_input(index, inputs[index])

        self.assertListEqual(m.inputs, inputs)

    def test_set_inputs(self):

        n = 5
        inputs = [True, True, True, False, True]
        m = Mux(n)

        m.set_inputs(inputs)

        self.assertListEqual(m.inputs, inputs)

    def test_get_value(self):

        n = 5
        selector_index = 1
        inputs = [True, True, True, False, True]
        m = Mux(n)
        m.set_inputs(inputs)
        m.set_selector(selector_index)

        actual_value = m.get_value()
        self.assertEqual(actual_value, inputs[selector_index])

    def test_set_selector(self):

        n = 3
        inputs = [True, False, False]
        m = Mux(n)
        m.set_inputs(inputs)
        
        for index in range(0, n):
            m.set_selector(index)
            actual_value = m.selector
            self.assertEqual(actual_value, index)


