from dataclasses import dataclass
from enum import Enum
from typing import List
from option import Err, Ok, Result
from Instructions import Encode, InstructionString
from Constants import ASM_COMMENT_CHARACTER, ASM_TEST_PREFIX_CHARACTER, PExit
from PrettyPrinting import PrintMode

@dataclass
class AssemblerSettings:
    self_test: bool = False
    print_mode      = PrintMode.no_output

class Assembler():
    
    def __init__(self, file_name: str, settings: AssemblerSettings) -> None:
        """Assembles an Aires program from an Aries assembly (.aria) file."""
        
        # Assembler settings
        self.settings: AssemblerSettings = settings
        
        # Directory containing all test programs
        self.program_directory = "Programs"
        
        # The name of the Aires assembly file (.aria) 
        self.file_name: str = file_name
        
        # The raw .aria file contents
        self.file_contents: List[str] = []
        
        # The contents of the file as a list of integers
        self.instructions: List[int] = []
        
        # The current line in the .aria file
        self.current_line: int = 0
        
        # Read the file into FileContents
        print("Reading file '{}' into assembler buffer.".format(file_name))
        r_real: result[bool, str] = self.read(settings)
        if r_real.is_err:
            p_exit(r_real.Err(), -4)
        print("Read file '{}' into assembler buffer.".format(file_name))
        
        if settings.selfTest: print("Assembling file '{}' with self tests enabled.".format(file_name))
        else:        print("Assembling file '{}' with self tests enabled.".format(file_name))
            
        # Assemble the file
        r_instructions = self.assemble(settings)
        if r_instructions.is_err:
            if Settings.self_test: print("Failed to assemble file '{}' as a test file!".format(file_name))
            else:        print("Failed to assemble file '{}'!".format(file_name))
            print(r_instructions.Err)
        
        self.instructions = r_instructions.unwrap()
            
        if settings.self_test: print("Assembled file '{}' with self tests enabled.".format(file_name))
        else:        print("Assembled file '{}'.".format(file_name))
        
        # Update metadata post assembly
        self.update_metadata()
        
        if settings.print_mode != PrintMode.no_output:
            print()
            print(self)
        
    def __str__(self) -> str:
        
        if self.settings.print_mode == PrintMode.NoOutput:
            return ""
        
        builder: str = ""
        builder += "[" + self.file_name + " - " + str(self.size) + " Bytes]\n"
        
        if len(self.instructions) < 1:
            builder += "No File Contents"
            return builder
        
        index = 0
        for instruction in self.instructions:
            
            if index != 0 and index % 1 == 0:
                builder += "\n"

            r_instruction: Result[str, str] = instruction_string(instruction, self.settings.print_mode)
            if r_instruction.is_err:
                builder += "Failed to convert instruction '{}': {}".format(format(instruction, "032b"), r_instruction.unwrap_err()) # TODO: Inconsistent use of 'format()'
                return builder
            
            builder += r_instruction.unwrap()
            
            index += 1
            
        return builder
    
    def update_metadata(self):
        """Updates assembler metadata after a successful assembly."""
        
        # BUG: Magic number!
        # Program size in bytes
        self.size = len(self.instructions * 4)
        
        # Other metadata
        # ...
    
    def assemble(self, settings: AssemblerSettings) -> Result[List[int], str]:
        """Assembles the santized file into Aries machine code. Accepts a 
        boolean value to determine if the given file should be interpreted
        as a test file. Test files contain additional information such as
        manually compiled machine code prefixed by ASM_TEST_PREFIX_CHARACTER
        that will be tested against the actual resulting machine code. An 
        error will be thrown if these two do not match.
        """
        
        if len(self.file_contents) == 0:
            return Ok(True)
        
        instructions: List[int] = []
        test_instructions: List[int] = []
        
        # For every line of assembly code
        for line in self.file_contents:
            
            # Parse the instruction
            if r_instruction := encode(line):
                
                # If parsing fails, propagate the error
                if r_instruction.is_err: return Err(r_instruction.Err)
                
                # Append the machine code instruction to the program
                instructions.append(r_instruction.unwrap())
            
            # Check if the first non-whitespace character is a colon; if so,
            # this is a test file!
            # TODO: Could use decode here to add an additional check
            elif line.strip()[0] == ASM_TEST_PREFIX_CHARACTER:
                
                instruction_str = "".join(line.split())
                instruction_str = instruction_str.replace(ASM_TEST_PREFIX_CHARACTER, "")

                instruction: int = int(instruction_str, 2)

                test_instructions.append(instruction)
            
            else:
                p_exit("Invalid instruction '{}'".format(line))
        
        # If this is a test file, then compare the assembled
        # instructions and the test instructions
        if settings.self_test:
            if len(test_instructions) != len(instructions):
                return Err("Test instructions and assembled instructions differ in size ({} != {})".format(len(test_instructions), len(instructions)))
        
            for index in range(0, len(test_instructions)):
                if test_instructions[index] != instructions[index]:
                    return Err("Test instructions and assembled instructions differ at index {} ({} != {})".format(index, format(test_instructions[index], "032b"), format(Instructions[Index], "032b")))
        
        return Ok(Instructions)
    
    def read(self, settings: AssemblerSettings) -> Result[bool, str]:
        """Reads the file into an internal buffer."""
        
        full_file_name = self.program_directory + "/" + self.file_name
        
        try:
            with open(full_file_name, "r") as file:
                while line := file.readline():
                    
                    # BUG: Stripping out comments is good! But we lose
                    # line number information using this method!!!!!
                    # Error messages will never be good!!!!!!!!!!
                    # Idea: just stop adding to the FileContents
                    # if a comment character is found! Then, the index
                    # into the FileContents list will map to the line
                    # number of the source file!!!!!!!!!!!
                    content = line.partition(ASM_COMMENT_CHARACTER)[0].strip()
                    if content != "":
                        self.file_contents.append(content)
                        
        except FileNotFoundError:
            return Err("File '" + full_file_name + "' not found! Unable to parse program.")
        
        return Ok(True)

if __name__ == "__main__":
    
    settings = AssemblerSettings()
    settings.print_mode = PrintMode.Bytes
    settings.self_test = True
    
    a: Assembler = Assembler("Example.aria", settings=settings)
