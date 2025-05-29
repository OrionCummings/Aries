
from pathlib import Path
from typing import List
from option import Result, Err, Ok

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
            if line.startswith("#include "):

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
