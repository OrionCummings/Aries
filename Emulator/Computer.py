from __future__ import annotations
from option import Ok, Result
from CPU import CPU, CPUArchitecture, CPUSettings
from HCPU import HCPU
from Utilities import panic, trace

class Computer():

    @staticmethod
    def create_default_cpu() -> Result[CPU, str]:

        r_settings = Computer.create_default_cpu_settings()

        if r_settings.is_err:
            return trace("failed to create default cpu settings", r_settings.unwrap_err())

        cpu = HCPU(r_settings.unwrap())



        return Ok(cpu)

    def create_cpu(self, settings: CPUSettings) -> Result[None, str]:

        match settings.architecture:
            case CPUArchitecture.Harvard:
                self.cpu = HCPU(settings)

            case _:
                return trace(f"unsupported cpu architecture '{settings.architecture}'")

        return Ok(None)

    def __init__(self, settings: CPUSettings = None):

        if settings is None:

            # Create default CPU settings
            r_cpu: Result[None, str] = Computer.create_default_cpu()
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