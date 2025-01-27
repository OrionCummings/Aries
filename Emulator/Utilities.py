import inspect
import os
from option import Result, Ok, Err
from Constants import CONSTANT_OPCODE_MAP
from PrettyPrinting import bold, print_red, yellow

def get_current_filename() -> str:
    return str(inspect.stack()[1][1])

def get_current_line() -> str:
    return str(inspect.stack()[1][2])

def get_current_function_name() -> str:
    return str(inspect.stack()[1][3])

def debug(function_depth: int = 1) -> str:
    stack = inspect.stack()[function_depth]
    file_name = os.path.split(stack[1])[1]
    line_number = str(stack[2])
    function_name = str(stack[3])
    return str(yellow(file_name + ":" + line_number + ":" + function_name + "():"))

def trace(new_message: str, old_messages: str = None, depth: int = 2) -> Err:
    if old_messages is None:
        return Err(f"{debug(depth)} {new_message}")
    else:
        return Err(f"{debug(depth)} {new_message}:\n{old_messages}")

def panic(s: str, e: int = 0):
    """A function to print an error message and exit."""
    print_red(bold(s))
    exit(e)

def get_opcode_from_id(id: int) -> Result[str, str]:
    for item in CONSTANT_OPCODE_MAP.items():
        (item_key, item_value) = item
        item_id = item_value[0]
        if item_id == id:
            return Ok(item_key)

    return trace(f"parsed opcode with unknown id '{id}'")
