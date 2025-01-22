from __future__ import annotations
from dataclasses import dataclass
from typing import SupportsIndex
from option import Ok, Result

from Utilities import trace

@dataclass
class ByteBankSettings():

    def __eq__(self, other: ByteBankSettings) -> bool:
        return \
            self.capacity == other.capacity and \
            self.print_num_rows == other.print_num_rows

    capacity: int = 64
    print_num_rows: int = 16

class ByteBank():

    def __init__(self, settings: ByteBankSettings):
        self.settings = settings
        self.capacity = self.settings.capacity
        self.content = bytearray(self.settings.capacity)

    def __eq__(self, other: ByteBank) -> bool:
        return (self.settings == other.settings and self.content == other.content)

    def __str__(self) -> str:

        builder = ""
        for index in range(0, self.capacity):

            if index % self.settings.print_num_rows == 0 and index != 0:
                builder += '\n'

            builder += "{:02X}".format(self.content[index])
            builder += " "

        return builder

    def get_byte(self, index: SupportsIndex) -> Result[bytearray, str]:
        if index not in range(0, self.capacity): return trace("index out of range")
        return Ok(self.content[index])

    def get_bytes(self, source_range: range | list[SupportsIndex]) -> Result[bytearray, str]:

        if isinstance(source_range, range):
            source_range = list(source_range)

        array = bytearray()
        for index in source_range:
            r_byt = self.get_byte(index)

            if r_byt.is_err:
                return trace(f"failed to get byte:\n{r_byt.unwrap_err()}")

            byt = r_byt.unwrap()
            array.append(byt)

        return Ok(array)

    def set_byte(self, index: SupportsIndex, value: int) -> Result[None, str]:
        if index not in range(0, self.capacity): return trace("index out of range")
        if value not in range(0, 256): return trace(f"value '{value}' not a valid byte")

        self.content[index] = value
        
        return Ok(None)

    def set_bytes(self, dest_range: range | list[SupportsIndex], values: list[int] | int) -> Result[None, str]:

        if isinstance(dest_range, range):
            dest_range = list(dest_range)

        len_dest_range = len(dest_range)

        if isinstance(values, int):
            values = [values] * len_dest_range

        len_values = len(values)

        if len_dest_range != len_values:
            return trace(f"size of range ({len_dest_range}) and size of values ({len_values}) differ")

        for (vindex, index) in enumerate(dest_range):
            r_set_byte = self.set_byte(index, values[vindex])
            if r_set_byte.is_err:
                return trace(f"failed to set byte:\n{r_set_byte.unwrap_err()}")

        return Ok(None)
    

# if __name__ == '__main__':

#     bank = ByteBank(ByteBankSettings())

#     bank.set_bytes(range(0, 17), 255)

#     print(bank)

