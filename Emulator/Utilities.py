import inspect
import os
from option import Result, Ok, Err
from Constants import CONSTANT_OPCODE_MAP
from PrettyPrinting import print_red, yellow

debug = lambda: str(yellow(os.path.split(inspect.stack()[1][1])[1] + ":" + str(inspect.stack()[1][2]) + ":" + str(inspect.stack()[1][3]) + "()"))

def p_exit(s: str, e: int = 0):
    """A function to print an error message and exit."""
    print_red(s)
    exit(e)

def get_opcode_from_id(id: int) -> Result[str, str]:
    for item in CONSTANT_OPCODE_MAP.items():
        (item_key, item_value) = item
        item_id = item_value[0]
        if item_id == id:
            return Ok(item_key)

    return Err(f"{debug()}: no opcode with id {id} found!")