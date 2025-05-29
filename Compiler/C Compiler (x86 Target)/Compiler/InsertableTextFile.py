from pathlib import Path
from typing import Iterable, List, Optional, Set
from option import Result, Err, Ok
from itertools import chain
from PrettyPrinting import blue
from Directives import DirectiveType, Definition, DirectiveInstance
from Utils import get_included_files, parse_file_from_include_statement

class InsertableTextFile:
    """
    An InsertableTextFile is a line-by-line representation of a text file. Added functionality to better support preprocessing functions like inline insertions required to support the include directive.
    """

    def __init__(self, name: Optional[str] = None):
        self.name: str = name
        self.lines: List[str] = []
        self.directives: List[DirectiveInstance] = []

    def __str__(self):
        builder = f"{self.name}\nContent:"
        for line in self.lines:
            builder += line + "\n"
        builder += "\nDirectives:\n"
        for directive in self.directives:
            builder += str(directive)
        return builder
    
    def to_strings(self) -> str:
        """
        Returns the contents of the ITF as a single newline seperated string.
        """
        return "\n".join(self.lines)
    
    def to_file(self, file_name: Optional[str] = None):
        """
        Writes the ITF to a file.
        """
        if file_name is None:
            with open(f"{self.name}.itftest", 'w') as file:
                file.writelines(self.to_strings())
        else:
            with open(f"{file_name}.itftest", 'w') as file:
                file.writelines(self.to_strings())

    def read(self, file_path: Path) -> Result[None, str]:
        """
        Reads the given file into the internal line buffer.
        """
        try:
            with open(file_path, 'r') as file:
                self.lines = list(map(str.rstrip, file))
        except Exception as e:
            return Err(f"Failed to open file '{file_path}':\n{str(e)}")
        
        self.name = file_path.name
        return Ok(None)
    
    def analyze(self) -> Result[None, str]:
        """
        Analyzes the file contents and marks where preprocessor directives exist by line number and type
        """

        for (line_number, line) in enumerate(self.lines):

            # If the line does not start with a '#', then it's not a directive
            if not line.startswith("#"):
                continue

            if line.startswith("#include"):
                parse_r = parse_file_from_include_statement(line)
                if parse_r.is_err:
                    return Err(f"Failed to parse file from include statement:\n{parse_r.unwrap_err()}")
                file_name = parse_r.unwrap()

                directive = DirectiveInstance(DirectiveType.INCLUDE, line_number, file_name, None)
                self.directives.append(directive)

            else:
                return Err(f"Non-include directives are not implemented yet; failed to parse line '{line}'")

    def insert(self, new_file: Path, line_number: int) -> Result[None, str]:
        """
        Insert the contents of a new file at the given line number
        """

        new_itf = InsertableTextFile()
        read_r = new_itf.read(new_file)
        if read_r.is_err:
            return Err(f"Failed to read:\n{read_r.unwrap_err()}")

        before = self.lines[0:max(line_number-1, 0)]
        after = self.lines[max(line_number, 1) - 1:]

        self.lines = list(chain(before, new_itf.lines[:-1], after))

        return Ok(None)

if __name__ == "__main__":

    test_file1_path = Path("C:\\Users\\Orion\\Stash\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Source Files\\Tests\\test_file1.test")
    test_file2_path = Path("C:\\Users\\Orion\\Stash\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Source Files\\Tests\\test_file2.test")

    f1 = InsertableTextFile(test_file1_path.name)
    f2 = InsertableTextFile(test_file2_path.name)
    f1.read(test_file1_path)
    f2.read(test_file2_path)

    f2.insert(test_file1_path, 3)

    f2.to_file()

    # f1.analyze()
    # f2.analyze()
    # print("--------------------------------------------------------------------------------------")
    # print(f1)
    # print("--------------------------------------------------------------------------------------")
    # print(f2)
    # print("--------------------------------------------------------------------------------------")