from pathlib import Path
from typing import Iterable, List, Set
from option import Result, Err, Ok
from itertools import chain
from PrettyPrinting import blue
from Directives import DirectiveType, Definition

class InsertableTextFile:
    """
    An InsertableTextFile is a line-by-line representation of a text file. Added functionality to better support preprocessing functions like inline insertions required to support the include directive.
    """

    def __init__(self, name: str = "DEFAULT ITF"):
        self.name: str = name
        self.lines: List[str] = []

    def __str__(self):
        builder = f"{self.name}\n"
        for line in self.lines:
            builder += blue(line + "\n")
        return builder
    
    def to_file(self) -> str:
        return "\n".join(self.lines)

    def read(self, file_path: Path) -> Result[None, str]:
        try:
            with open(file_path, 'r') as file:
                self.lines = list(map(str.rstrip, file))
        except Exception as e:
            return Err(f"Failed to open file '{file_path}':\n{str(e)}")
        
        self.name = file_path.name
        return Ok(None)

    def replace(self, new_file: Path, line_number: int) -> Result[None, str]:
        """
        Replace the given line number with the contents of a new file
        """

        itf = InsertableTextFile()
        text_file_read_r = itf.read(new_file)
        if text_file_read_r.is_err:
            return Err(f"Failed to read file '{new_file}'")
        
        # TODO: Remove these debug statements!
        self.lines.insert(line_number-1, f"// Start of file {new_file.name}")
        self.lines.insert(line_number, f"// End of file {new_file.name}")

        self.lines = list(chain(self.lines[:line_number], itf.lines, self.lines[line_number:]))

        return Ok(None)
    
    def remove(self, start_line_number: int, end_line_number: int) -> Result[None, str]:
        """
        Removes the lines including both the start and end line numbers.
        """

        self.lines = list(chain(self.lines[:start_line_number], self.lines[end_line_number:]))

        return Ok(None)

    def resolve_directives(self) -> Result[None, str]:

        # TODO: General directive resolution cannot be done line-by-line!
        # There must be the ability to push/pop/peek to look ahead.

        self.new_lines: List[str] = []
        
        # TODO: Resolve include statements


if __name__ == "__main__":

    test_file1_path = Path("C:\\Users\\Orion\\Stash\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Source Files\\Tests\\test_file1.test")
    test_file2_path = Path("C:\\Users\\Orion\\Stash\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Source Files\\Tests\\test_file2.test")

    f = InsertableTextFile(test_file1_path.name)
    f.read(test_file1_path)
    print(f"File 1 before replacement:\n{f}\n")
    f.replace(test_file2_path, 2)
    print(f"File 1 after replacement:\n{f}\n")