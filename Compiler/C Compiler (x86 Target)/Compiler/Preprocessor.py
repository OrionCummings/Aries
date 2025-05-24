from pathlib import Path
from typing import Iterable, List, Optional, Self
from option import Err, Ok, Result
from TranslationUnit import TranslationUnit
from DependencyTree import DependencyTree
from Directives import DirectiveType, Definition

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
        self.include_paths = set(include_paths)

        # If the no include path is given, default to the directory in which this Preprocessor acts
        if include_paths is None:
            self.add_include_path(self.path.parent)

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

    def resolve(self):

        # For every node in the tree
        for n in self.tree.root:
            file_name = n.file_path.resolve()
            print(file_name)

            if n.file_path in self.resolved_paths:
                print(f"File '{file_name}' is already resolved!")
                return Ok(None)
            
            resolution_r = n.resolve(self.include_paths, self.definitions)
            if resolution_r.is_err:
                return Err(f"Failed to resolve file '{n.name}'")

if __name__ == "__main__":

    root_dir = Path("C:\\Users\\Orion\\Stash\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Source Files\\DependencyTreeTest\\")

    p = Preprocessor(root_dir)
    p.resolve()
    # print(p)

