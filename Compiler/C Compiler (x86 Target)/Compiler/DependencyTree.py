
from genericpath import isfile
from ntpath import join
import os
from pathlib import Path
from typing import Iterable, List, Optional
from option import Result, Err, Ok
from TranslationUnit import TranslationUnit
from InsertableTextFile import InsertableTextFile

def get_included_files(file_path: Path) -> Result[List[Path], str]:

    """
    Given a file path, return a list of included file names
    """

    base_path = file_path.parents[0]
    included_file_paths: List[Path] = []

    # Read the file
    with open(file_path, "r") as file:

        # Read the file into a buffer
        lines = file.readlines()

        # For every line
        for line in lines:

            # Check if it contains '#include"
            if line.find("#include ") != -1:

                # Remove any leading or trailing whitespace
                line = line.strip()

                # Split the line by spaces
                line_vector = line.split(" ")

                if len(line_vector) != 2:
                    return Err(f"Ill-formed #include statement '{line}'")

                # If these are system headers, return an error; not supported!
                if line.find("<") != -1 and line.find(">") != -1:
                    system_header = line_vector[1]
                    if len(system_header) < 3:
                        return Err("Use of system headers is not supported yet")

                    system_header = system_header[1:-1]
                    return Err(f"Use of system headers is not supported yet. {system_header}")

                include_file_name_unsanitized = line_vector[1]
                include_file_name_unsanitized_len = len(include_file_name_unsanitized)
                if include_file_name_unsanitized_len < 3:
                    return Err(f"Invalid included file name '{include_file_name_unsanitized}'!")

                include_file_name = include_file_name_unsanitized[1:-1]

                include_file_path = Path.joinpath(base_path, include_file_name)

                included_file_paths.append(include_file_path)

    return Ok(included_file_paths)

def parse_file_from_include_statement(line: str) -> Result[str, str]:

    line_vector = line.split(" ")

    if len(line_vector) != 2:
        return Err("Invalid include statement format!")
    
    rhs = line_vector[1]

    if len(rhs) < 3:
        return Err("Invalid include statement format!")
    
    # Remove the quotes
    included_file_name = rhs[1:-1]

    return Ok(included_file_name)

class DependencyTreeNode:

    def __init__(self, file_path: Path):

        # The path of this file
        self.file_path: Path = file_path

        # Get the name 
        self.name = file_path.name
        
        # A line-by-line representation of this file
        self.itf = InsertableTextFile(file_path.name)

        # A tuple of the files included in this file and the line number
        # on which they are included 
        self.children: List[(DependencyTreeNode, int)] = []

    def __str__(self) -> str:
        builder = f"Path: {self.file_path}\nName: {self.name}:\nContents: {self.itf}\n"
        builder += self.recursive_to_string(0)
        return builder

    def __iter__(self):
        for c in self.children:
            for cc in c:
                yield cc
        yield self

    def recursive_to_string(self, depth) -> str:
        builder = str(" " * depth) + self.file_path.name + "\n"
        for c in self.children:
            builder += c.recursive_to_string(depth + 1)
        return builder
    
    def append(self, file_name: str | List[str]) -> None: 
        if isinstance(file_name, str):
            self.children.append(file_name)
        elif isinstance(file_name, List[str]):
            self.children.append(*file_name)

    def explore(self) -> Result[None, str]:

        included_files_r = get_included_files(self.file_path)

        if included_files_r.is_err:
            return Err(f"Failed to get included files from '{self.file_path}':\n{included_files_r.unwrap_err()}")

        included_files = included_files_r.unwrap()

        self.children = [DependencyTreeNode(path) for path in included_files]
        for c in self.children:
            exploration_r = c.explore()
            if exploration_r.is_err:
                return Err(f"Failed to explore node '{c.file_path.name}'\n{exploration_r.unwrap_err()}")

        return Ok(None)
    
    def resolve(self, include_paths: Iterable[Path] | None, definitions: dict[str, str] | None) -> Result[None, str]:

        print(f"Resolving '{self.name}'")

        # Read the contents of the set file path into the ITF
        itf_r = self.itf.read(self.file_path)
        if itf_r.is_err:
            return Err(f"Failed to read file '{self.file_path.name}':\n{itf_r.unwrap_err()}")

        # Iterate through every line
        for (line_number, line) in enumerate(self.itf.lines):
            
            if line.startswith("#include"):
                file_name_r = parse_file_from_include_statement(line)
                if file_name_r.is_err:
                    return Err(f"Failed to parse include statement from line '{line}':\n{file_name_r.unwrap_err()}")
                file_name = file_name_r.unwrap()

                found_included_file = False
                # For every include path...
                for p in include_paths:

                    # Create a full path
                    potential_included_file_path = Path.joinpath(p, file_name)

                    print(f"potential included file: {potential_included_file_path.resolve()}")

                    # Check if that file exists
                    if potential_included_file_path.exists():

                        # If it does, then note that it's been found
                        found_included_file = True

                        # Replace the current line with the contents of the file
                        replacement_r = self.itf.replace(potential_included_file_path, line_number)
                        if replacement_r.is_err:
                            return Err(f"Failed to replace line {line_number} with '{file_name}':\n{replacement_r.unwrap_err()}")

                        break

                if not found_included_file:
                    return Err(f"Failed to find file '{file_name}' in include directories!")
                
                ...


        return Ok(None)

class DependencyTree:

    def __init__(self, source_path: Path, include_path: Path = None) -> None:

        # Set up the include paths
        self.include_paths: List[Path] = []
        self.include_paths.append(source_path)
        if include_path is not None:
            self.include_paths.append(include_path)

        # Set the source path
        self.source_path = source_path

        # Find the file that contains a unique entry point
        file_path_with_entry_point_r = self.find_entry_point()
        if file_path_with_entry_point_r.is_err: 
            print(f"Unable to find entry point:\n{file_path_with_entry_point_r.unwrap_err()}")
            return
        file_path_with_entry_point = file_path_with_entry_point_r.unwrap()

        # Create the root node from the entry point file and explore the tree
        self.root: DependencyTreeNode = DependencyTreeNode(file_path_with_entry_point)
        exploration_r = self.root.explore()
        if exploration_r.is_err:
            print(f"Failed to explore tree: {exploration_r.unwrap_err()}")
            return

        self.translation_unit: Optional[TranslationUnit] = None

    def __str__(self):
        builder = ""
        builder += (self.root.file_path.name + "\n")
        for c in self.root.children:
            builder += (c.recursive_to_string(1))
        return builder

    def __iter__(self):
        yield self.root

    def find_entry_point(self) -> Result[Path, str]:
        """Find a function with a signature of 'int main(int argc, char** argv)'. Fails if
        anything other than one function with that signature exists."""

        # Get every file in the source directory
        files_in_source_dir = [f for f in self.source_path.iterdir() if f.is_file()]

        entry_point_file_path = None
        for source_file_path in files_in_source_dir:

            # Open the file
            with open(source_file_path, 'r') as file:

                # TODO: Make this check more robust
                # If the file contains the correct text
                if "int main(int argc, char** argv)" in file.read():

                    # If no entry point has been found
                    if entry_point_file_path is None:

                        # Save it
                        entry_point_file_path = source_file_path
                    else:

                        # If an entry point has already been found,
                        # return an error
                        second_entry_point_file_path = source_file_path
                        return Err(f"Entry point 'int main(int argc, char** argv)' found in two files!\n1: {entry_point_file_path}\n2: {second_entry_point_file_path}")
        
        if entry_point_file_path is None:
            return Err("No function with signature of 'int main(int argc, char** argv)' found!")

        return Ok(entry_point_file_path)


if __name__ == "__main__":

    node_path = Path("C:\\Users\\Orion\\Stash\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Source Files\\DependencyTreeTest\\b.h")
    node = DependencyTreeNode(node_path)
    resolution_r = node.resolve(include_paths=[node_path.parent], definitions=None)
    if resolution_r.is_err:
        print(f"Failed to resolve node:\n{resolution_r.unwrap_err()}")

    resolution = resolution_r.unwrap()
    print(f"Resolved '{node.name}':\n{str(node)}")

    with open("_test.h", 'w') as f:
        f.writelines(node.itf.to_file())

    # Establish the source path
    # source_path = Path("C:\\Users\\Orion\\Stash\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Source Files\\DependencyTreeTest\\")

    # Create a dependency tree from the given source path. From this
    # information, we can figure out the entry point file automatically.
    # Once the entry point is found, then the tree can be built. This
    # constructor performs everything.
    # tree = DependencyTree(source_path)

    # for node in tree:
        # print(node)




