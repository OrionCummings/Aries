import unittest
from RegisterFile import RegisterFile

class RegisterFileTests(unittest.TestCase):
    
    def test_register_file_constructor(self):

        # Construct a register file
        register_file = RegisterFile()

        # Ensure all registers are set to zero on initialization
        self.assertFalse(any(reg != 0 for reg in register_file.registers.values()))


if __name__ == '__main__':
    unittest.main()
