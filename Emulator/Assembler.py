from dataclasses import dataclass
from typing import List, Optional
from option import Err, Ok, Result
from Constants import ASM_COMMENT_CHARACTER, ASM_TEST_PREFIX_CHARACTER, InstructionFormat
from Transformations import decode, encode, get_instruction_mode, instruction_string
from PrettyPrinting import PrintMode, error, info, print_red, print_green, print_blue, print_yellow, red_bold, success, warning
from Utilities import debug, trace

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

        # The disassembly of the file
        self.disassembly: str = Optional[str]

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
                formatted_instruction = format(instruction, "032b")
                instruction_err = r_instruction.unwrap_err()
                builder += f"Failed to convert instruction '{formatted_instruction}': {instruction_err}"
                return builder
            
            builder += r_instruction.unwrap()
            
            index += 1
            
        return builder

    def read(self) -> Result[bool, str]:
        """Reads the file into an internal buffer."""
        
        # TODO: Make this better with generators/yields

        # If the file name doesn't end with '.aria', then append it
        if not self.file_name.endswith(".aria"):
            warning(f"File name provided ('{self.file_name}') does not end with '.aria'. Appending file extension.")
            self.file_name += ".aria"

        info(f"Reading file '{self.file_name}'...")

        full_file_name = self.program_directory + "/" + self.file_name
        
        try:
            with open(full_file_name, "r") as file:
                real_line_number = 1
                filtered_line_number = 1
                while line := file.readline():
                    
                    # BUG: Stripping out comments is good! But we lose
                    # line number information using this method!!!!!
                    # Error messages will never be good!!!!!!!!!!
                    # Idea: just stop adding to the FileContents
                    # if a comment character is found! Then, the index
                    # into the FileContents list will map to the line
                    # number of the source file!!!!!!!!!!!

                    # Partition the line into three parts:
                    # 1) before 'ASM_COMMENT_CHARACTER'
                    # 2 'ASM_COMMENT_CHARACTER'
                    # 3) after 'ASM_COMMENT_CHARACTER'
                    partition = line.partition(ASM_COMMENT_CHARACTER)

                    # Only take the first part to allow comments to
                    # appear on the same line as code
                    content = partition[0]

                    # Remove any bordering whitespace
                    stripped_content = content.strip()

                    # If the stripped content is empty, then this line is not code: ignore it.
                    # Otherwise, save it.
                    if stripped_content != "":

                        # Increment the 'filtered' line number. Filtered meaning "just code" 
                        # and no comments or other non-essential parts of a program.
                        filtered_line_number += 1
                        
                        # Save this information
                        self.file_contents.append((real_line_number, filtered_line_number, stripped_content))

                    # Regardless of if this line was code or not, increment the line number
                    real_line_number += 1
                        
        except FileNotFoundError:
            return trace(f"unable to parse program: file '{full_file_name}' not found!")
        
        success(f"Read file '{self.file_name}' into assembler buffer.")

        return Ok(True)

    def validate(self) -> Result[bool, str]:

        # TODO: Label resolution is currently a double pass algorithm when it doesn't
        # actually have to be. Refactor this!

        info(f"Validating file '{self.file_name}'...")

        # Find all labels
        known_labels = {}
        for (line_number, line) in enumerate(self.file_contents):
            line_content = line[2]
            if ":" in line_content and line_content[0].isalpha():
                known_labels[line_content.strip()[:-1]] = line_number+1

        known_labels_count = len(known_labels)
        resolved_labels_count = 0

        # Substitute all labels for their addresses/line numbers
        for (file_content_index, (real_line_number, filtered_line_number, line)) in enumerate(self.file_contents):

            # If this line contains a colon, the it's the label line! Skip it.
            if line.find(":") != -1:
                continue

            # If this a jump instruction, then it COULD use a label
            r_mode = get_instruction_mode(line)
            if r_mode.is_err:
                return trace(f"failed to get instruction mode:\n{r_mode.unwrap_err()}")
            mode = r_mode.unwrap()

            if mode == InstructionFormat.Jump:

                # Split the line
                split_line = line.split(" ")

                # TODO: This is a big assumption that will not always be correct!
                # Get the label
                parsed_label = split_line[-1]

                # If this is a valid key, then get the corresponding value. Otherwise,
                # throw an error!
                if parsed_label in known_labels:

                    parsed_label_address = known_labels[parsed_label]

                    # Subsitute the label in the jump instruction for the parsed label address
                    current_instruction_tuple = self.file_contents[file_content_index]
                    (label_real_line_number, label_filtered_line_number, label_line) = current_instruction_tuple
                    subsituted_instruction = label_line.split(" ")[0] + " " + str(parsed_label_address)
                    self.file_contents[file_content_index] = (label_real_line_number, label_filtered_line_number, subsituted_instruction)

                    resolved_labels_count += 1

                else:

                    # BUG: This does not account for TRUE numeric address arguments to jump instructions.
                    # Add a check for str[0].alpha() to determine if this is a number (address) or
                    # a string (label).
                    return trace(f"{self.file_name}:{real_line_number} Undefined label '{parsed_label}'!")

        if known_labels_count != resolved_labels_count:
            label_diff = known_labels_count - resolved_labels_count
            return trace(f"Failed to resolve all labels: {label_diff} label(s) remaining!")
        
        success(f"Resolved {known_labels_count}/{resolved_labels_count} label(s).")
        success(f"Validated file '{self.file_name}'.")

        return Ok(True)

    def assemble(self) -> Result[List[int], str]:
        """Assembles the santized file into Aries machine code.
        """
        
        info(f"Assembling file '{self.file_name}'...")

        # Clear any existing disassemblies
        self.disassembly = None

        if len(self.file_contents) == 0:
            return Ok(True)
        
        instructions: List[int] = []
        
        # For every line of assembly code
        for (real_line_number, filtered_line_number, line) in self.file_contents:
            
            # Check if there is any content in this line
            stripped_line = line.strip()
            if stripped_line == '' or stripped_line[0] == ASM_COMMENT_CHARACTER:

                # There is no content, so move on. All information that enables good error messages
                # has already been captured, so there is no need to do additional work here.
                continue

            # Check if the first character indicates that this line should be ignored
            elif stripped_line[0] == ASM_TEST_PREFIX_CHARACTER:

                # TODO: Capture the line to be checked later
                pass

            # Check if this line is a label destination
            elif stripped_line.find(":") != -1:

                # TODO: Should (probably?) do something here
                continue

            else:

                # Encode the line as an instruction
                r_instruction = encode(line)

                # If parsing fails, propagate the error
                if r_instruction.is_err:
                    return trace(f"failed to encode instruction:\n{r_instruction.unwrap_err()}")
                
                # Append the machine code instruction to the program
                self.instructions.append(r_instruction.unwrap())
        
        success(f"Assembled file '{self.file_name}'.")

        return Ok(instructions)

    def update(self) -> Result[bool, str]:
        """Updates assembler metadata after a successful assembly."""
        
        # BUG: Magic number!
        # Program size in bytes
        self.size = len(self.instructions * 4) # BUG: This may conflict with the memory rework!!!!
        
        # Other metadata
        # ...

        return Ok(True)

    def run(self) -> Result[bool, str]:

        # Read the file
        r_contents = self.read()
        if r_contents.is_err:
            return trace(f"failed to read file {self.file_name}\n{r_contents.unwrap_err()}")

        # Validate the file
        r_validation = self.validate()
        if r_validation.is_err:
            return trace(f"failed to validate file {self.file_name}\n{r_validation.unwrap_err()}")

        # Assemble the file
        r_instructions = self.assemble()
        if r_instructions.is_err:
            return trace(f"failed to assemble file '{self.file_name}'\n{r_instructions.unwrap_err()}")

        # Update metadata post assembly
        r_update = self.update()
        if r_update.is_err:
            return trace(f"failed to update after assembling '{self.file_name}'\n{r_update.unwrap_err()}")

        return Ok(True)

    def disassemble(self) -> Result[str, str]:
        
        if self.disassembly is not None:
            return self.disassembly
        
        self.disassembly = ""
        for instruction in self.instructions:
            r_disassembled_line = decode(instruction)

            if r_disassembled_line.is_err:
                return Err(r_disassembled_line.unwrap_err())

            self.disassembly += r_disassembled_line.unwrap()
            self.disassembly += "\n"

        return Ok(self.disassembly)

if __name__ == "__main__":

    settings = AssemblerSettings()
    settings.file_name = "label"
    settings.print_mode = PrintMode.Hex
    assembler: Assembler = Assembler(settings)

    r_run = assembler.run()
    if r_run.is_err:
        error(r_run.unwrap_err())
        exit(-2)

    print(assembler.disassemble().unwrap())

