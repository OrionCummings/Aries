from enum import Enum, auto
from os import listdir
from os.path import isfile, join
from typing import Optional, Self
from option import Err, Ok, Result

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

    def __init__(self, dir: str):
        self.dir: str = dir

        self.file_tree: Optional[FileTreeNode] = None
        self.final_contents: Optional[str] = None
        self.file_with_entry_point: Optional[str] = None
        self.root_path: Optional[str] = None
        self.root_path_system: Optional[str] = None

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

    def find_entry_point(self) -> Result[None, str]:
        """Find a function with a signature of 'int main(int argc, char** argv)'. Fails if
        anything other than one function with that signature exists."""

        files_in_source_dir = [f for f in listdir(self.dir) if isfile(join(self.dir, f))]

        entry_point_file_name: Optional[str] = None

        for src_file_name in files_in_source_dir:
            with open(self.dir + src_file_name, 'r') as file:
                if "int main(int argc, char** argv)" in file.read():
                    if entry_point_file_name is None:
                        entry_point_file_name = src_file_name
                    else:
                        second_entry_point_file_path = src_file_name
                        return Err(f"Entry point 'int main(int argc, char** argv)' found in two files!\n1: {entry_point_file_name}\n2: {second_entry_point_file_path}")

        if entry_point_file_name is None:
            return Err("No function with signature of 'int main(int argc, char** argv)' found!")

        return Ok(entry_point_file_name)

    def resolve(self) -> Result[None, str]:

        print("Attempting to resolve")

        if self.file_with_entry_point is None:
            return Err("Unable to resolve with unknown entry point!\nCall find_entry_point() first!")

        with open(self.dir + self.file_with_entry_point, 'r') as file:
            self.contents = file.readlines()

        included_files_r = self.resolve_includes(self.dir, self.file_with_entry_point, [])
        if included_files_r.is_err: return included_files_r

        included_files = included_files_r.unwrap()

        print(f"Resolved {self.file_with_entry_point}")
        print(f"Files found:\n{included_files}")
        
        return Ok(None)

    def resolve_includes(self, root_path: str, file_name_to_resolve: str, included_file_names: list[str]) -> Result[list[str], str]:

        print("Attempting to resolve includes")

        file_path = root_path + file_name_to_resolve

        system_headers = False

        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("#include"):
                    line_vector = line.split(" ")

                    # If these are system headers, return an error; not supported!
                    if line.find("<"):
                        system_header = line_vector[1]
                        if len(system_header) < 3:
                            return Err("Use of system headers is not supported yet")

                        system_header = system_header[1:-1]
                        return Err(f"Use of system headers is not supported yet. {system_header}")

                    line_vector_len = len(line_vector)
                    if line_vector_len != 2:
                        return Err(f"Invalid number of arguments ({line_vector_len-1}) for an include directive! Expected 1.")
                    
                    include_file_name_unsanitized = line_vector[1]
                    include_file_name_unsanitized_len = len(include_file_name_unsanitized)
                    if include_file_name_unsanitized_len <= 3:
                        return Err(f"Invalid included file name length ({include_file_name_unsanitized_len-3})! Length must be non-zero!")

                    include_file_name = include_file_name_unsanitized[1:-2]

                    # Resolve recursively
                    if system_headers == True:
                        resolved_includes_r = self.resolve_includes(self.root_path_system, include_file_name, included_file_names)
                    else:
                        resolved_includes_r = self.resolve_includes(root_path, include_file_name, included_file_names)
                    if resolved_includes_r.is_err:
                        return Err(f"Failed to resolve includes:\n{resolved_includes_r.unwrap_err()}")

                    resolved_includes = resolved_includes_r.unwrap()
                    included_file_names.append(resolved_includes)
                    included_file_names.append(include_file_name)
                    print(f"Added '{include_file_name}'")

        print(f"Resolved includes in {file_name_to_resolve}")
        return Ok(included_file_names)

    def resolve_macros(self) -> Result[None, str]:
        return Ok(None)

if __name__ == "__main__":

    root_dir = "C:\\Users\\Orion\\Stash\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Source Files\\Real\\"

    p = Preprocessor(root_dir)

    ## Init
    file_with_entry_point_r = p.find_entry_point()
    if file_with_entry_point_r.is_err:
        print(f"Failed to find entry point:\n{file_with_entry_point_r.unwrap_err()}")
        exit(1)

    file_with_entry_point = file_with_entry_point_r.unwrap()

    print(f"Entry point found in '{file_with_entry_point}'")

    p.file_with_entry_point = file_with_entry_point

    # Resolve
    resolution_r = p.resolve()
    if resolution_r.is_err:
        print(f"Failed to resolve:\n {resolution_r.unwrap_err()}")

    resolution = resolution_r.unwrap()

    # print(p)

