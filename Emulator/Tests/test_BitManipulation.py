import unittest
from BitManipulation import bit_mask, reset_bit, set_bit, get_bit, toggle_bit

class BitManipulationTests(unittest.TestCase):
    
    def test_single_bit_mask(self):

        for i in range(0, 32):
            
            expected_bit_mask = 1 << i
            actual_bit_mask = bit_mask(i)

            self.assertEqual(expected_bit_mask, actual_bit_mask, "At least one actual bit mask did not match the expected bit mask!")
    
    def test_range_bit_mask(self):

        start_index = 5
        end_index = 16
        expected_bit_mask = 0b00000000_00000000_11111111_11100000
        actual_bit_mask = bit_mask(start_index, end_index)

        self.assertEqual(expected_bit_mask, actual_bit_mask, "Range bit mask did not match the expected range bit mask!")

    def test_set_bit(self):
        
        for i in range(0, 32):
            
            number = 28739472
            expected_set_bit = number | bit_mask(i)
            actual_set_bit = set_bit(number, i)

            self.assertEqual(expected_set_bit, actual_set_bit, "At least one actual set bit did not match the expected set bit!")
    
    def test_reset_bit(self):
        
        for i in range(0, 32):
            
            number = 28739472
            expected_set_bit = number & ~bit_mask(i)
            actual_set_bit = reset_bit(number, i)

            self.assertEqual(expected_set_bit, actual_set_bit, "At least one actual set bit did not match the expected set bit!")

    def test_get_bit(self):

        for i in range(0, 32):
            
            number = 28739472
            expected_get_bit = (number & bit_mask(i)) >> i
            actual_get_bit = get_bit(number, i)

            self.assertEqual(expected_get_bit, actual_get_bit, "At least one actual get bit did not match the expected get bit!")
    
    def test_toggle_bit(self):
        
        for i in range(0, 32):
            
            number = 28739472
            expected_toggle_bit = (number ^ (1 << (i)))
            actual_toggle_bit = toggle_bit(number, i)

            self.assertEqual(expected_toggle_bit, actual_toggle_bit, "At least one actual toggle bit did not match the expected toggle bit!")

