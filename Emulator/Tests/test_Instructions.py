from typing import Tuple
import unittest

from option import Err, Ok, Result

from Assembler import Assembler, AssemblerSettings, AssemblerSettingsSource
from CPU import CPU, CPUArchitecture, CPUSettings
from Constants import CONSTANT_REGISTER_MAP
from PrettyPrinting import PrintMode
from Transformations import decode
from Utilities import get_current_function_name

class InstructionTests(unittest.TestCase):

    test_file_directory = ""
    file_extension = ".aria"

    def create_assembler_and_cpu(self, file_name: str, instruction_memory_size_in_bytes: int, data_memory_size_in_bytes: int, program: str = None) -> Result[(Assembler, CPU), str]:

        assembler_settings = AssemblerSettings()

        if program is None:
            assembler_settings.source = AssemblerSettingsSource.File
        else:
            assembler_settings.source = AssemblerSettingsSource.String

        assembler_settings.file_name = file_name
        assembler_settings.print_mode = PrintMode.Hex
        assembler = Assembler(assembler_settings)
        r_run = assembler.run(program)
        if r_run.is_err:
            return Err(r_run.unwrap_err())

        cpu_settings = CPUSettings()
        cpu_settings.architecture = CPUArchitecture.Harvard
        cpu_settings.data_memory_information = (data_memory_size_in_bytes, 0)
        cpu_settings.instruction_memory_information = (instruction_memory_size_in_bytes, 0)
        cpu_settings.video_memory_information = (16, 0)
        cpu_settings.stack_information = (16, 0)
        cpu = CPU(cpu_settings)

        if program is None:
            r_load = cpu.load_program(assembler.file_contents, assembler.file_name)
        else:
            r_load = cpu.load_program(program, assembler.file_name)

        if r_load.is_err:
            return Err(r_load.unwrap_err())
        
        return Ok((assembler, cpu))

    def test_label_success(self):
        """Tests if labels work correctly. The expected behavior of this program is to
        jump past any loads to A, B, and C and straight to a halt. If the jump falls short,
        then A, B, or C will have a non-zero value and the test will fail. If the jump
        exceeds the expected address, this test will fail.
        """

        program = """
            j test
            ldi 255 A
            hlt
            test:
            hlt
        """

        instruction_memory_size_in_bytes = 32
        data_memory_size_in_bytes = 8
        r_combo = self.create_assembler_and_cpu(get_current_function_name(), instruction_memory_size_in_bytes, data_memory_size_in_bytes, program)
        if r_combo.is_err:
            self.fail(r_combo.unwrap_err())

        (assembler, cpu) = r_combo.unwrap() # type: ignore

        # Check if the jump address is correct
        instruction = cpu.get_current_instruction()
        r_decoded_instruction = decode(instruction)
        if r_decoded_instruction.is_err:
            self.fail(r_decoded_instruction.unwrap_err())
        decoded_instruction = r_decoded_instruction.unwrap()
        decoded_instruction_vector = decoded_instruction.split(" ")

        # There should be two elements in this vector: ['j', '4']
        self.assertEqual(len(decoded_instruction_vector), 2)

        # The second element should be '3'
        self.assertEqual(decoded_instruction_vector[1], '3')

        clock = cpu.clock() # j test
        self.assertTrue(clock, "CPU stopped prematurely")

        clock = cpu.clock() # hlt
        self.assertFalse(clock, "CPU failed to halt")

        # A, B, and C should be zero; if not, fail!
        self.assertEqual(cpu.register_file.get_reg('A').unwrap(), 0, "Register A was non-zero!")
        self.assertEqual(cpu.register_file.get_reg('B').unwrap(), 0, "Register B was non-zero!")
        self.assertEqual(cpu.register_file.get_reg('C').unwrap(), 0, "Register C was non-zero!")

        # The CPU should be halted
        self.assertTrue(cpu.halted, "CPU not halted!")

        # The PC should be 4 * 3 = 12 + an extra 4 because hlt also increments the pc
        self.assertEqual(cpu.register_file.get_pc(), 16, "Incorrect program counter!")

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

    def test_nop(self):
        """Tests the 'nop' instruction.
        """
        
        program = """
        nop
        hlt
        """
        instruction_memory_size_in_bytes = 8
        data_memory_size_in_bytes = 8
        r_combo = self.create_assembler_and_cpu(get_current_function_name(), instruction_memory_size_in_bytes, data_memory_size_in_bytes, program)
        if r_combo.is_err:
            self.fail(r_combo.unwrap_err())

        (assembler, cpu) = r_combo.unwrap() # type: ignore

        # Ensure all registers are zero
        for reg in CONSTANT_REGISTER_MAP.keys():
            r_reg_value = cpu.register_file.get_reg(reg)
            if r_reg_value.is_err:
                self.fail(r_reg_value.unwrap_err())
            reg_value = r_reg_value.unwrap()

            self.assertEqual(reg_value, 0)

        # Ensure all data memory is zero
        for (index, b) in enumerate(cpu.data_memory.bytes):
            self.assertEqual(b, 0, f"Data memory byte {index} is non-zero!")

        # Ensure all instruction memory is zero (except for the program)
        for (index, b) in enumerate(cpu.instruction_memory.bytes):
            if index in [0, 1]: # Ignore the first two instructions (nop & hlt)
                self.assertEqual(b, 0, f"Instruction memory byte {index} is non-zero!")

        # Execute one instruction
        cpu.clock() # nop

        # Ensure all registers are still zero (except for the program counter, which must be 4)
        for reg in CONSTANT_REGISTER_MAP.keys():
            r_reg_value = cpu.register_file.get_reg(reg)
            if r_reg_value.is_err:
                self.fail(r_reg_value.unwrap_err())
            reg_value = r_reg_value.unwrap()

            if reg == 'PC':
                self.assertEqual(reg_value, 4, "Unexpected program counter value!")
            else:
                self.assertEqual(reg_value, 0, "Unexpected register value!")

        # Ensure all data memory is still zero
        for (index, b) in enumerate(cpu.data_memory.bytes):
            self.assertEqual(b, 0, f"Data memory byte {index} is non-zero!")

        # Ensure all instruction memory is still zero (except for the program)
        for (index, b) in enumerate(cpu.data_memory.bytes):
            if index in [0, 1]: # Ignore the first two instructions (nop & hlt)
                self.assertEqual(b, 0, f"Instruction memory byte {index} is non-zero!")

        self.assertFalse(cpu.halted, "CPU halted on 'nop' instruction!")

    def test_hlt(self):
        """Tests the 'hlt' instruction.
        """
        
        program = """
        hlt
        """
        instruction_memory_size_in_bytes = 8
        data_memory_size_in_bytes = 8
        r_combo = self.create_assembler_and_cpu(get_current_function_name(), instruction_memory_size_in_bytes, data_memory_size_in_bytes, program)
        if r_combo.is_err:
            self.fail(r_combo.unwrap_err())

        (assembler, cpu) = r_combo.unwrap() # type: ignore

        # Ensure all registers are zero
        for reg in CONSTANT_REGISTER_MAP.keys():
            r_reg_value = cpu.register_file.get_reg(reg)
            if r_reg_value.is_err:
                self.fail(r_reg_value.unwrap_err())
            reg_value = r_reg_value.unwrap()

            self.assertEqual(reg_value, 0)

        # Ensure all data memory is zero
        for (index, b) in enumerate(cpu.data_memory.bytes):
            self.assertEqual(b, 0, f"Data memory byte {index} is non-zero!")

        # Ensure all instruction memory is zero (except for the program)
        for (index, b) in enumerate(cpu.instruction_memory.bytes):
            if index in [0, 1]: # Ignore the first two instructions (nop & hlt)
                self.assertEqual(b, 0, f"Instruction memory byte {index} is non-zero!")

        # Execute one instruction
        cpu.clock() # hlt

        # Ensure all registers are still zero (except for the program counter, which must be 4)
        for reg in CONSTANT_REGISTER_MAP.keys():
            r_reg_value = cpu.register_file.get_reg(reg)
            if r_reg_value.is_err:
                self.fail(r_reg_value.unwrap_err())
            reg_value = r_reg_value.unwrap()

            if reg == 'PC':
                self.assertEqual(reg_value, 4, "Unexpected program counter value!")
            else:
                self.assertEqual(reg_value, 0, "Unexpected register value!")

        # Ensure all data memory is still zero
        for (index, b) in enumerate(cpu.data_memory.bytes):
            self.assertEqual(b, 0, f"Data memory byte {index} is non-zero!")

        # Ensure all instruction memory is still zero (except for the program)
        for (index, b) in enumerate(cpu.data_memory.bytes):
            if index in [0, 1]: # Ignore the first two instructions (nop & hlt)
                self.assertEqual(b, 0, f"Instruction memory byte {index} is non-zero!")

        self.assertTrue(cpu.halted, "CPU not halted on 'hlt' instruction!")
    
    # def test_add(self):
    #     pass
    
    # def test_addi(self):
    #     pass
    
    # def test_ldi(self):
    #     pass
