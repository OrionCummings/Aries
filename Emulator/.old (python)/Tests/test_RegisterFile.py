import unittest
from Constants import BP_INC, CONSTANT_REGISTER_MAP, PC_INC, SP_INC
from RegisterFile import RegisterFile, is_register

class RegisterFileTests(unittest.TestCase):
    
    def get_demo_register_file(self) -> RegisterFile:
        
        register_file = RegisterFile()
        
        for r, i in zip(CONSTANT_REGISTER_MAP.keys(), range(0, len(CONSTANT_REGISTER_MAP))):
            register_file.registers[r] = i
        
        return register_file
    
    def test_constructor(self):

        # Construct a register file
        register_file = RegisterFile()

        # Ensure all registers are set to zero on initialization
        self.assertFalse(any(reg != 0 for reg in register_file.registers.values()), "At least one register was initialized to a non-zero value!")

    def test_constructor_equality(self):
        
        # Construct register files
        register_file_a = RegisterFile()
        register_file_b = RegisterFile()

        # Check if two identical constructors will be equal
        self.assertEqual(register_file_a, register_file_b, "Two register files failed comparison!")

    def test_to_string_returns_str(self):
        
        register_file = RegisterFile()
        
        self.assertIsInstance(str(register_file), str, "String representation of register file is not a string!")

    def test_get_and_set_regs(self):
        
        register_file = RegisterFile()
        
        regs = ['A','B','C','D','E','F','G','H','I','J','K','L','SP','BP','PC','FL']
        number = 1278128
        
        for reg in regs:
            register_file.set_reg(reg, number)
            
            self.assertEqual(register_file.get_reg(reg).unwrap(), number, "Register {} was not get/set properly!".format(reg))

    def test_increment_program_counter(self):
        
        # Construct register files
        register_file = RegisterFile()

        self.assertEqual(register_file.get_reg('PC').unwrap(), 0, "Default value of the program counter is non-zero!")
        
        register_file.increment_program_counter()
        
        self.assertEqual(register_file.get_reg('PC').unwrap(), PC_INC, "Program counter failed to increment by PC_INC!")

    def test_increment_base_pointer(self):
        
        # Construct register files
        register_file = RegisterFile()

        self.assertEqual(register_file.get_reg('BP').unwrap(), 0, "Default value of the base pointer is non-zero!")

        register_file.increment_base_pointer()

        self.assertEqual(register_file.get_reg('BP').unwrap(), BP_INC, "Base pointer failed to increment by BP_INC!")

    def test_increment_stack_pointer(self):
        
        # Construct register files
        register_file = RegisterFile()

        self.assertEqual(register_file.get_reg('SP').unwrap(), 0, "Default value of the stack pointer is non-zero!")

        register_file.increment_stack_pointer()

        self.assertEqual(register_file.get_reg('SP').unwrap(), SP_INC, "Stack pointer failed to increment by SP_INC!")
        
    def test_clear_flags(self):
        
        # Construct register files
        register_file = RegisterFile()

        register_file.set_reg('FL', 255)
        
        self.assertEqual(register_file.get_reg('FL').unwrap(), 255)
        
        register_file.clear_flags()

        self.assertEqual(register_file.get_reg('FL').unwrap(), 0)

    def test_is_register(self):
        real_registers = CONSTANT_REGISTER_MAP.keys()
        for reg in real_registers:
            self.assertTrue(is_register(reg))

        real_registers = CONSTANT_REGISTER_MAP.values()
        for reg in real_registers:
            self.assertTrue(is_register(reg))


