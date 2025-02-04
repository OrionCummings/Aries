import unittest
from typing import Tuple
from option import Err, Ok, Result
from Assembler import Assembler, AssemblerSettings, AssemblerSettingsSource
from CPU import CPU, CPUArchitecture, CPUSettings, MemoryLayout
from Constants import CONSTANT_REGISTER_MAP
from Stack import Stack
from Memory import Memory
from HarvardCPU import HarvardCPU
from PrettyPrinting import PrintMode
from Transformations import decode
from Utilities import get_current_function_name, trace

class InstructionTests(unittest.TestCase):

    test_file_directory = ""
    file_extension = ".aria"

    @staticmethod
    def validate_harvard_memory(harvard_cpu: HarvardCPU, instruction_memory_exclusion_range: range, data_memory_exclusion_range: range, video_memory_exclusion_range: range, stack_memory_exclusion_range: range) -> Result[None, str]:

        # Check that instruction memory is valid
        r_instruction_memory_valid = InstructionTests.validate_memory_initalization(harvard_cpu.instruction_memory, instruction_memory_exclusion_range)
        if r_instruction_memory_valid.is_err:
            return trace("invalid instruction memory state", r_instruction_memory_valid.unwrap_err())

        # Check that instruction memory is valid
        r_data_memory_valid = InstructionTests.validate_memory_initalization(harvard_cpu.data_memory, data_memory_exclusion_range)
        if r_data_memory_valid.is_err:
            return trace("invalid data memory state", r_data_memory_valid.unwrap_err())

        # Check that video memory is valid
        r_video_memory_valid = InstructionTests.validate_memory_initalization(harvard_cpu.video_memory, video_memory_exclusion_range)
        if r_video_memory_valid.is_err:
            return trace("invalid video memory state", r_video_memory_valid.unwrap_err())

        # Check that stack memory is valid
        r_stack_memory_valid = InstructionTests.validate_memory_initalization(harvard_cpu.stack_memory, stack_memory_exclusion_range)
        if r_stack_memory_valid.is_err:
            return trace("invalid stack memory state", r_stack_memory_valid.unwrap_err())
        
        return Ok(None)

    @staticmethod
    def validate_memory_initalization(memory: Memory | Stack, exclusion_range: range = None) -> Result[None, str]:

        # Ensure the memory is actually memory (and not a stack or something else)
        if isinstance(memory, Stack):
            
            # TODO: Make this better with 'any()' or 'all()'
            # Ensure all memory outside of the exclusion range is zero
            for (index, b) in enumerate(memory.content):
                if b != 0 and index not in exclusion_range:
                    return trace(f"stack byte {index} is non-zero!")

        elif isinstance(memory, Memory):

            # TODO: Make this better with 'any()' or 'all()'
            # Ensure all memory outside of the exclusion range is zero
            for (index, b) in enumerate(memory.content):
                if b != 0 and index not in exclusion_range:
                    return trace(f"memory byte {index} is non-zero!")
            
        else:
            return trace(f"invalid object '{memory}'")

        return Ok(None)

    @staticmethod
    def create_assembler(program_str: str = None, file_name: str = None) -> Result[Assembler, str]:

        # Create an AssemblerSettings instance
        assembler_settings = AssemblerSettings()

        # If no program string is provided, then this assembler will act on a file. Otherwise
        # it will act on a string passed as `program`.
        if program_str is None:
            assembler_settings.source = AssemblerSettingsSource.File
        else:
            assembler_settings.source = AssemblerSettingsSource.String

        # Set up and run the assembler on the given source
        assembler_settings.file_name = file_name
        assembler_settings.print_mode = PrintMode.Hex
        assembler = Assembler(assembler_settings)
        r_run = assembler.run(program_str)
        if r_run.is_err: return trace("failed to run assembler", r_run.unwrap_err())

        return Ok(assembler)

    @staticmethod
    def create_harvard_cpu(instruction_memory_size: int, data_memory_size: int, video_memory_size: int, stack_memory_size: int) -> Result[HarvardCPU, str]:

        # Create Harvard CPU settings with default values
        r_cpu_settings = (CPUSettings()
            .set_architecture(CPUArchitecture.Harvard)
            .set_memory_layout(MemoryLayout.Sequential)
            .set_instruction_memory_size(instruction_memory_size)
            .set_data_memory_size(data_memory_size)
            .set_video_memory_size(video_memory_size)
            .set_stack_memory_size(stack_memory_size)
            .validate()
        )

        # If the cpu settings were invalid, return an error
        if r_cpu_settings.is_err: return trace("invalid cpu settings", r_cpu_settings.unwrap_err())
        
        return Ok(HarvardCPU(r_cpu_settings.unwrap()))

    @staticmethod
    def create_cpu(architecture: CPUArchitecture, instruction_memory_size: int, data_memory_size: int, video_memory_size: int, stack_memory_size: int) -> Result[CPU, str]:

        match architecture:
            case CPUArchitecture.Harvard:
                r_cpu = InstructionTests.create_harvard_cpu(instruction_memory_size, data_memory_size, video_memory_size, stack_memory_size)

            case CPUArchitecture.VonNeumann:
                return trace("create_cpu() does not support the VonNeumann architecture")

            case CPUArchitecture.OnlyMemory:
                return trace("create_cpu() does not support the OnlyMemory architecture")

            case _:
                return trace(f"unknown CPU architecture '{architecture}'")
        
        # If we failed to create a cpu, return an error
        if r_cpu.is_err:
            return trace("failed to create cpu", r_cpu.unwrap_err())

        cpu = r_cpu.unwrap()

        return Ok(cpu)

    def test_label_success(self):

        program = """
            j test
            ldi 255 A
            hlt
            test:
            hlt
        """

        program_name = get_current_function_name()
        instruction_memory_size = 16
        data_memory_size = 0
        video_memory_size = 0
        stack_memory_size = 0

        r_harvard_cpu = InstructionTests.create_cpu(CPUArchitecture.Harvard, instruction_memory_size, data_memory_size, video_memory_size, stack_memory_size)
        if r_harvard_cpu.is_err:
            self.fail(r_harvard_cpu.unwrap_err(), "failed to create harvard cpu")

        cpu: HarvardCPU = r_harvard_cpu.unwrap()
        r_load_program = cpu.load_program(program, program_name)
        if r_load_program.is_err:
            return self.fail(trace("failed to load program", r_load_program.unwrap_err()).unwrap_err())

        # Check if the jump address is correct
        r_instruction = cpu.get_current_instruction()
        if r_instruction.is_err:
            return self.fail(trace("failed to get current instruction", r_instruction.unwrap_err()))
        instruction = r_instruction.unwrap()

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
        self.assertEqual(cpu.register_file.get_reg('A').unwrap(), 0, "register A was non-zero!")
        self.assertEqual(cpu.register_file.get_reg('B').unwrap(), 0, "register B was non-zero!")
        self.assertEqual(cpu.register_file.get_reg('C').unwrap(), 0, "register C was non-zero!")

        # The CPU should be halted
        self.assertTrue(cpu.halted, "CPU not halted!")

        # The PC should be 4 * 3 = 12 + an extra 4 because hlt also increments the pc
        self.assertEqual(cpu.register_file.get_pc(), 16, "incorrect program counter!")

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
        program_name = get_current_function_name()
        instruction_memory_size = 8
        data_memory_size = 0
        video_memory_size = 0
        stack_memory_size = 0

        r_harvard_cpu = InstructionTests.create_cpu(CPUArchitecture.Harvard, instruction_memory_size, data_memory_size, video_memory_size, stack_memory_size)
        if r_harvard_cpu.is_err:
            self.fail(r_harvard_cpu.unwrap_err(), "failed to create harvard cpu")

        cpu: HarvardCPU = r_harvard_cpu.unwrap()
        r_load_program = cpu.load_program(program, program_name)
        if r_load_program.is_err:
            return self.fail(trace("failed to load program", r_load_program.unwrap_err()).unwrap_err())

        # Ensure all registers are zero
        for reg in CONSTANT_REGISTER_MAP.keys():
            r_reg_value = cpu.register_file.get_reg(reg)
            if r_reg_value.is_err:
                self.fail(r_reg_value.unwrap_err())
            reg_value = r_reg_value.unwrap()

            self.assertEqual(reg_value, 0)

        # TODO: Make this depend on the size of the input program!!
        # Exclude the instructions after program loading
        instruction_memory_exclusion_range = range(0, 2 * 4)

        # These should all be zero for this test
        data_memory_exclusion_range = range(0, 0)
        video_memory_exclusion_range = range(0, 0)
        stack_memory_exclusion_range = range(0, 0)

        # Ensure all* memory is still zero
        r_validate_harvard_memory = InstructionTests.validate_harvard_memory(cpu, instruction_memory_exclusion_range, data_memory_exclusion_range, video_memory_exclusion_range, stack_memory_exclusion_range)
        if r_validate_harvard_memory.is_err:
            return trace("invalid instruction harvard memory state", r_validate_harvard_memory.unwrap_err())

        # Execute one instruction
        cpu.clock() # nop

        # Ensure all registers are still zero (except for the program counter, which must be 4)
        for reg in CONSTANT_REGISTER_MAP.keys():
            r_reg_value = cpu.register_file.get_reg(reg)
            if r_reg_value.is_err:
                self.fail(r_reg_value.unwrap_err())
            reg_value = r_reg_value.unwrap()

            if reg == 'PC':
                self.assertEqual(reg_value, 4, "unexpected program counter value!")
            else:
                self.assertEqual(reg_value, 0, "unexpected register value!")

        # Ensure all* memory is still zero
        r_validate_harvard_memory = InstructionTests.validate_harvard_memory(cpu, instruction_memory_exclusion_range, data_memory_exclusion_range, video_memory_exclusion_range, stack_memory_exclusion_range)
        if r_validate_harvard_memory.is_err:
            return trace("invalid instruction harvard memory state", r_validate_harvard_memory.unwrap_err())

        self.assertFalse(cpu.halted, "CPU halted on 'nop' instruction!")

    def test_hlt(self):
        """Tests the 'hlt' instruction.
        """
        
        program = """
        hlt
        """
        program_name = get_current_function_name()
        instruction_memory_size = 4
        data_memory_size = 0
        video_memory_size = 0
        stack_memory_size = 0

        r_harvard_cpu = InstructionTests.create_cpu(CPUArchitecture.Harvard, instruction_memory_size, data_memory_size, video_memory_size, stack_memory_size)
        if r_harvard_cpu.is_err:
            self.fail(r_harvard_cpu.unwrap_err(), "failed to create harvard cpu")

        cpu: HarvardCPU = r_harvard_cpu.unwrap()
        r_load_program = cpu.load_program(program, program_name)
        if r_load_program.is_err:
            return self.fail(trace("failed to load program", r_load_program.unwrap_err()).unwrap_err())

        # Ensure all registers are zero
        for reg in CONSTANT_REGISTER_MAP.keys():
            r_reg_value = cpu.register_file.get_reg(reg)
            if r_reg_value.is_err:
                self.fail(r_reg_value.unwrap_err())
            reg_value = r_reg_value.unwrap()

            self.assertEqual(reg_value, 0)

        # TODO: Make this depend on the size of the input program!!
        # Exclude the instructions after program loading
        instruction_memory_exclusion_range = range(0, 1 * 4)

        # These should all be zero for this test
        data_memory_exclusion_range = range(0, 0)
        video_memory_exclusion_range = range(0, 0)
        stack_memory_exclusion_range = range(0, 0)

        # Ensure all* memory is still zero
        r_validate_harvard_memory = InstructionTests.validate_harvard_memory(cpu, instruction_memory_exclusion_range, data_memory_exclusion_range, video_memory_exclusion_range, stack_memory_exclusion_range)
        if r_validate_harvard_memory.is_err:
            return trace("invalid instruction harvard memory state", r_validate_harvard_memory.unwrap_err())

        # Execute one instruction
        cpu.clock() # nop

        # Ensure all registers are still zero (except for the program counter, which must be 4)
        for reg in CONSTANT_REGISTER_MAP.keys():
            r_reg_value = cpu.register_file.get_reg(reg)
            if r_reg_value.is_err:
                self.fail(r_reg_value.unwrap_err())
            reg_value = r_reg_value.unwrap()

            if reg == 'PC':
                self.assertEqual(reg_value, 4, "unexpected program counter value!")
            else:
                self.assertEqual(reg_value, 0, "unexpected register value!")

        # Ensure all* memory is still zero
        r_validate_harvard_memory = InstructionTests.validate_harvard_memory(cpu, instruction_memory_exclusion_range, data_memory_exclusion_range, video_memory_exclusion_range, stack_memory_exclusion_range)
        if r_validate_harvard_memory.is_err:
            return trace("invalid instruction harvard memory state", r_validate_harvard_memory.unwrap_err())

        self.assertTrue(cpu.halted, "CPU failed to halt on 'hlt' instruction!")
    
    # def test_add(self):
    #     pass
    
    # def test_addi(self):
    #     pass
    
    # def test_ldi(self):
    #     pass
