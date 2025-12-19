from pathlib import Path
from typing import Optional
from option import Err, Ok, Result
from InsertableTextFile import InsertableTextFile

class TranslationUnit:

    """
    A translation unit is *effectively* a file with
    ALL preprocessor directives resolved.
    """

    def __init__(self):

        # The file path of this translation unit
        self.path: Optional[Path] = None

        # The textual content of this translation unit
        self.content: InsertableTextFile = InsertableTextFile()

        # A list of unresolved symbols in this translation unit
        self.unresolved_symbols = []

    def write(self) -> Result[None, str]:

        if self.path is None:
            return Err("Path not specified")

        try:
            with open(self.path, 'w') as file:
                stringified_content = str(self.content)
                file.write(stringified_content)

        except Exception as e:
            return Err(f"Failed to open file {self.path}:\n{str(e)}")

        return Ok(None)
