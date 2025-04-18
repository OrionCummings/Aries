from enum import Enum, auto
from typing import Optional, Self
from option import Ok, Result

class MacroType(Enum):
    NONE        = auto(),
    DEFINE      = auto(),
    INCLUDE     = auto(),
    CONDITIONAL = auto(),
    FUNCTION    = auto(),

class Macro():
    mtype: MacroType = MacroType.NONE
    data = []

class FileTreeNode():
    name: Optional[str] = None
    macros_used: Optional[list[Macro]] = None
    file_content_pre:  Optional[str] = None
    file_content_post: Optional[str] = None
    children: Optional[list[Self]] = None

    def __init__(self, name: str, file_content_pre: str):
        self.name = name
        self.file_content_pre = file_content_pre

class Preprocessor():

    def __init__(self, source_dir, main_file_name: str):
        self.source_dir: str = source_dir
        self.main_file_name: str = main_file_name
        self.main_file_path: str = source_dir + main_file_name
        self.file_tree: Optional[FileTreeNode] = None
        self.final_contents: str = ""

    def __str__(self):
        return self.to_string(self.main_file_name, 0)
    
    def to_string(self, file_name: str, depth: int) -> str:
        
        # A string builder
        builder: str = ""

        # Move to the right at every level
        builder +=  (" " * depth)

        # Append the file name
        builder += file_name + "\n"

        if self.file_tree is None: return ""
        if self.file_tree.children is None: return ""
        
        for children in self.file_tree.children:
            builder += children.to_string(children.name, depth+1)

        return builder

    def resolve(self) -> Result[None, str]:

        with open(self.main_file_path, 'r') as file:
            self.contents = file.readlines()

        macros_r = self.resolve_macros()
        if macros_r.is_err: return macros_r.unwrap_err()

        includes_r = self.resolve_includes()
        if includes_r.is_err: return includes_r.unwrap_err()

    def resolve_includes(self) -> Result[None, str]:
        return Ok(None)

    def resolve_macros(self) -> Result[None, str]:
        return Ok(None)

if __name__ == "__main__":

    source_dir = "C:\\Users\\Orion\\Stash\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Source Files\\Real\\"
    main_file_name = "main.c"

    p = Preprocessor(source_dir, main_file_name)
    p.resolve()

    print(p)

