import unittest

from Assembler import Assembler, AssemblerSettings
from CPU import CPU
from PrettyPrinting import PrintMode
from Transformations import decode
from Utilities import get_current_function_name

class InstructionTests(unittest.TestCase):

    test_file_directory = ""
    file_extension = ".aria"

    def test_label_success(self):
        """Tests if labels work correctly. The expected behavior of this program is to
        jump past any loads to A, B, and C and straight to a halt. If the jump falls short,
        then A, B, or C will have a non-zero value and the test will fail. If the jump
        exceeds the expected address, this test will fail.
        """

        assembler_settings = AssemblerSettings()
        assembler_settings.file_name = get_current_function_name() + self.file_extension
        assembler_settings.print_mode = PrintMode.Hex
        assembler_settings.file_directory = 'Tests/Test Programs'
        assembler = Assembler(assembler_settings)
        r_run = assembler.run()
        if r_run.is_err:
            self.fail(r_run.unwrap_err())

        cpu = CPU(32, 32)
        r_load = cpu.load_program(assembler.instructions, assembler.file_name)
        if r_load.is_err:
            self.fail(f"{r_load.unwrap_err()}")

        # Check if the jump address is correct
        instruction = cpu.get_current_instruction()
        r_decoded_instruction = decode(instruction)
        if r_decoded_instruction.is_err:
            self.fail(r_decoded_instruction.unwrap_err())
        decoded_instruction = r_decoded_instruction.unwrap()
        decoded_instruction_vector = decoded_instruction.split(" ")

        # There should be two elements in this vector: ['j', '4']
        self.assertEqual(len(decoded_instruction_vector), 2)

        # The second element should be '4'
        self.assertEqual(decoded_instruction_vector[1], '4')

        clock = cpu.clock() # j target
        self.assertTrue(clock, "CPU stopped prematurely")

        clock = cpu.clock() # hlt
        self.assertFalse(clock, "CPU failed to halt")

        # A, B, and C should be zero; if not, fail!
        self.assertEqual(cpu.register_file.get_reg('A').unwrap(), 0, "Register A was non-zero!")
        self.assertEqual(cpu.register_file.get_reg('B').unwrap(), 0, "Register B was non-zero!")
        self.assertEqual(cpu.register_file.get_reg('C').unwrap(), 0, "Register C was non-zero!")

        # The CPU should be halted
        self.assertTrue(cpu.halted, "CPU not halted!")

        # The PC should be 4 * 4 = 16 + an extra 4 because hlt also increments the pc
        self.assertEqual(cpu.register_file.get_pc(), 20, "Incorrect program counter!")

    def test_label_failure_no_destination_label(self):
        """Tests if label resolution will throw an error if there is a label that is
        defined, but never used. This should be an invalid.
        """

        assembler_settings = AssemblerSettings()
        assembler_settings.file_name = get_current_function_name() + self.file_extension
        assembler_settings.print_mode = PrintMode.Hex
        assembler_settings.file_directory = 'Tests/Test Programs'
        assembler = Assembler(assembler_settings)

        r_run = assembler.run()

        self.assertTrue(r_run.is_err, "Assembly should have failed!")

    def test_label_failure_no_source_label(self):
        """Tests if label resolution will fail upon finding a label definition that is
        never called.
        """

        assembler_settings = AssemblerSettings()
        assembler_settings.file_name = get_current_function_name() + self.file_extension
        assembler_settings.print_mode = PrintMode.Hex
        assembler_settings.file_directory = 'Tests/Test Programs'
        assembler = Assembler(assembler_settings)

        r_run = assembler.run()

        self.assertTrue(r_run.is_err, "Assembly should have failed!")

    # def test_nop(self):
    #     pass

    # def test_hlt(self):
    #     pass
    
    # def test_add(self):
    #     pass
    
    # def test_addi(self):
    #     pass
    
    # def test_ldi(self):
    #     pass
