from __future__ import annotations
from option import Ok, Result
from CPU import CPU, CPUSettings
from Utilities import panic, trace

class Computer():

    def __init__(self, settings: CPUSettings = None):

        if settings is None:

            # Create default CPU settings
            r_cpu: Result[None, str] = CPU.create_default_cpu()
            if r_cpu.is_err:
                panic("failed to create cpu")
            self.cpu = r_cpu.unwrap()

        else:
            panic("custom cpu settings are not currently supported")

    def __str__(self) -> str:

        builder: str = "Computer:\n"
        builder += "CPU:\n"
        builder += str(self.cpu)
        builder += "\n"

        return builder

if __name__ == '__main__':

    c = Computer()

    print(c)