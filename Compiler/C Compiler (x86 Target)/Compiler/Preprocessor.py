from pathlib import Path
from typing import Iterable, List, Optional, Self
from option import Err, Ok, Result
from TranslationUnit import TranslationUnit
from DependencyTree import DependencyTree
from Directives import DirectiveType, Definition
from Utils import parse_file_from_include_statement

class Preprocessor:

    def __init__(self, path: Path, include_paths: Iterable[Path] = None):
        
        # TODO: Clarify this comment
        # The file path of this translation unit (?)
        self.path = path

        # A set of definitions
        self.definitions: dict[str, str] = {}

        # TODO: This may be better as another, more specific data structure because of the shared 'path prefix'
        # A set of paths that have been resolved
        self.resolved_paths = set()

        # Create a dependency tree
        self.tree = DependencyTree(path)

        # Create a translation unit from the dependency tree
        self.translation_unit = None

        # Create the include paths set
        self.include_paths = set()

        # If include paths are provided, add them
        if include_paths is not None:
            self.add_include_path(include_paths)

        # By default, add the directory in which this Preprocessor acts
        self.add_include_path(self.path)

    def __str__(self):
        builder = ""
        builder += f"path: {str(self.path)}\n"
        builder += "definitions:\n"
        builder += "\n".join([str(d) for d in self.definitions])
        builder += f"dependency tree:\n{str(self.tree)}"
        builder += "translation unit:\n"
        builder += f"{str(self.translation_unit)}"
        return builder

    def is_defined(self, definition: str) -> bool:
        """ Returns True if the given definition exists and False otherwise."""
        return definition in self.definitions
    
    def is_resolved(self, path: Path) -> bool:
        """ Returns True if the given path has been resolved and False otherwise. """
        return path in self.resolved_paths
    
    def add_include_path(self, path: Path) -> None:
        if isinstance(path, Path):
            self.include_paths.add(path)

    def resolve(self) -> Result[None, str]:

        # For every node in the tree
        for n in self.tree.root:

            path = n.file_path
            file_name = path.resolve()
            print(f"Attempting to resolve '{path.name}'")

            # If the path has already been resolved, then stop!
            if n.file_path in self.resolved_paths:
                print(f"File '{file_name}' is already resolved!")
                continue

            # Attempt to resolve the node!

            # Populate the ITF
            reading_r = n.itf.read(path)
            if reading_r.is_err:
                return Err(f"Failed to read file '{path}':\n{reading_r.unwrap_err()}")

            # Iterate through every line
            for (line_number, line) in enumerate(n.itf.lines):
                
                if not line.startswith("#include"):
                    continue

                file_name_r = parse_file_from_include_statement(line)
                if file_name_r.is_err:
                    return Err(f"Failed to parse include statement from line '{line}':\n{file_name_r.unwrap_err()}")
                file_name = file_name_r.unwrap()

                found_included_file = False

                # Search include paths for this file
                for p in self.include_paths:

                    # Create a full path
                    potential_included_file_path = Path.joinpath(p, file_name)
                    print(f"Potential included file: {potential_included_file_path.resolve()}")

                    # Check if that file exists
                    if potential_included_file_path.exists():

                        # If it does, then note that it's been found
                        found_included_file = True
                        print(f"Found appropriate include candidate '{potential_included_file_path.resolve()}'")

                        # Replace the current line with the contents of the file
                        print(f"Inserting '{potential_included_file_path}' on line {line_number}")
                        replacement_r = n.itf.insert(potential_included_file_path, line_number)
                        if replacement_r.is_err:
                            return Err(f"Failed to replace line {line_number} with '{file_name}':\n{replacement_r.unwrap_err()}")
                        
                        n.itf.to_file()

                # If, at the end of the loop, we have not found any files that match, return an error!
                if not found_included_file:
                    return Err(f"Failed to find file '{file_name}' in include directories!")


            # Add the file path to the list of resolved paths
            self.resolved_paths.add(path)

        return Ok(None)

if __name__ == "__main__":

    root_dir = Path("C:\\Users\\Orion\\Stash\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Source Files\\DependencyTreeTest\\")

    p = Preprocessor(root_dir)
    print(p.tree)
    resolution_r = p.resolve()
    if resolution_r.is_err:
        print(resolution_r.unwrap_err())


    # print(p)

