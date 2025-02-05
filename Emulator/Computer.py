from __future__ import annotations
from option import Ok, Err, Result
from CPU import CPU, CPUArchitecture, CPUSettings, MemoryLayout
from Constants import DEFAULT_DATA_MEMORY_SIZE_IN_BYTES, DEFAULT_INSTRUCTION_MEMORY_SIZE_IN_BYTES, DEFAULT_STACK_MEMORY_SIZE_IN_BYTES, DEFAULT_VIDEO_MEMORY_SIZE_IN_BYTES
from HarvardCPU import HCPU
from Utilities import panic, trace

class Computer():

    @staticmethod
    def create_cpu_settings(architecture: CPUArchitecture) -> Result[CPU, str]:

        r_settings = (CPUSettings()
                    .set_architecture(architecture)
                    .set_memory_layout(MemoryLayout.Sequential)
                    .set_instruction_memory_size(DEFAULT_INSTRUCTION_MEMORY_SIZE_IN_BYTES)
                    .set_data_memory_size(DEFAULT_DATA_MEMORY_SIZE_IN_BYTES)
                    .set_video_memory_size(DEFAULT_VIDEO_MEMORY_SIZE_IN_BYTES)
                    .set_stack_memory_size(DEFAULT_STACK_MEMORY_SIZE_IN_BYTES)
                    .validate()
        )

        if r_settings.is_err:
            return trace("failed to create default settings")

        return r_settings

    @staticmethod
    def create_cpu(settings: CPUSettings) -> Result[CPU, str]:

        match settings.architecture:
            case CPUArchitecture.Harvard:
                cpu = HCPU(settings)

            case _:
                return trace(f"unsupported cpu architecture '{settings.architecture}'")

        return Ok(cpu)

    def __init__(self, settings: CPUSettings):

        # Create default CPU settings
        r_cpu = Computer.create_cpu(settings)
        if r_cpu.is_err:
            panic("failed to create cpu")
        self.cpu = r_cpu.unwrap()

    def __str__(self) -> str:
        return str(self.cpu)

if __name__ == '__main__':

    r_settings = Computer.create_cpu_settings(CPUArchitecture.Harvard)
    if r_settings.is_err:
        panic("failed to create CPU settings", depth=1)
    settings = r_settings.unwrap()

    c = Computer(settings)

    print(c)