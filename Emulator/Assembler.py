from dataclasses import dataclass
from typing import List
from option import Err, Ok, Result
from Constants import ASM_COMMENT_CHARACTER, ASM_TEST_PREFIX_CHARACTER
from Transformations import encode, instruction_string
from PrettyPrinting import PrintMode, print_red, print_green, print_blue

@dataclass
class AssemblerSettings:
    file_name       = None
    print_mode      = PrintMode.NoOutput

class Assembler():
    
    # TODO: Refactor this function: it's quite messy.
    def __init__(self, settings: AssemblerSettings) -> None:
        """Assembles an Aires program from an Aries assembly (.aria) file."""
        
        # Assembler settings
        self.settings: AssemblerSettings = settings
        
        # Directory containing all test programs
        self.program_directory = "Programs"
        
        # The name of the Aires assembly file (.aria) 
        self.file_name: str = settings.file_name
        
        # The raw .aria file contents
        self.file_contents: List[str] = []
        
        # The contents of the file as a list of integers
        self.instructions: List[int] = []
        
        # The current line in the .aria file
        self.current_line: int = 0
        
        # TODO: Make this better with generators/yields
        # Read the file
        print_blue(f"Reading file '{self.file_name}'...")
        r_contents: Result[bool, str] = self.read(settings)
        if r_contents.is_err:
            print_red(f"Failed to read file {self.file_name}: {r_contents.unwrap_err()}")
            exit()

        print_green(f"Read file '{self.file_name}' into assembler buffer.")
        
        # Assemble the file
        print_blue(f"Assembling file '{self.file_name}'...")
        r_instructions = self.assemble(settings)
        if r_instructions.is_err:
            print_red(f"Failed to assemble file '{self.file_name}': {r_instructions.unwrap_err()}")
            exit()
            
        print_green(f"Assembled file '{self.file_name}'.")

        # Capture parsed instructions
        self.instructions = r_instructions.unwrap()
        
        # Update metadata post assembly
        self.update_metadata()
        
    def __str__(self) -> str:
        
        if self.settings.print_mode == PrintMode.NoOutput:
            return ""
        
        if len(self.instructions) < 1:
            builder += "No File Contents"
            return builder
        
        builder: str = ""
        builder += "[" + self.file_name + " - " + str(self.size) + " Bytes]\n"
        
        index = 0
        for instruction in self.instructions:
            
            # TODO: Get a better constant; 1 is a temporary number!
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
        self.size = len(self.instructions * 4) # BUG: This may conflict with the memory rework!!!!
        
        # Other metadata
        # ...
    
    def assemble(self, settings: AssemblerSettings) -> Result[List[int], str]:
        """Assembles the santized file into Aries machine code.
        """
        
        if len(self.file_contents) == 0:
            return Ok(True)
        
        instructions: List[int] = []
        
        # For every line of assembly code
        for line in self.file_contents:
            
            # Check if there is any content in this line
            stripped_line = line.strip()
            if stripped_line == '' or stripped_line[0] == ASM_COMMENT_CHARACTER:

                # TODO: This will offset all line numbers in error messages,
                # so this should be refactored eventually!

                # There is no content, so move on
                continue

            # Check if the first character indicates that this line should be ignored
            elif stripped_line[0] == ASM_TEST_PREFIX_CHARACTER:

                # TODO: Capture the line to be checked later
                pass

            else:

                # Encode the line as an instruction
                r_instruction = encode(line)

                # If parsing fails, propagate the error
                if r_instruction.is_err: return Err(r_instruction.unwrap_err())
                
                # Append the machine code instruction to the program
                instructions.append(r_instruction.unwrap())
        
        return Ok(instructions)
    
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
    settings.print_mode = PrintMode.Hex
    
    a: Assembler = Assembler("infinite_loop.aria", settings=settings)
    print(a)
