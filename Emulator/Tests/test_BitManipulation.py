import unittest
from BitManipulation import bit_mask, set_bit, get_bit, toggle_bit

class BitManipulationTests(unittest.TestCase):
    
    def test_bit_mask(self):

        for i in range(0, 32):
            
            expected_bit_mask = 1 << i
            actual_bit_mask = bit_mask(i)

            self.assertEqual(expected_bit_mask, actual_bit_mask)


if __name__ == '__main__':
    unittest.main()
