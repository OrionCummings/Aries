from functools import partial
from pynput.keyboard import Key, Listener
from CPU import CPU, CPUArchitecture, CPUSettings
from HarvardCPU import HarvardCPU
from VonNeumannCPU import VonNeumannCPU
from Assembler import Assembler, AssemblerSettings, AssemblerSettingsSource, PrintMode
from Constants import EC_ASSEMBLER_FAILURE
from PrettyPrinting import info, red_bold
from Utilities import panic

# Create assembler settings 
assmbler_settings = (AssemblerSettings()
    .set_file_name("load_string")
    .set_print_mode(PrintMode.Hex)
    .set_source(AssemblerSettingsSource.File)
)

# Create and run the assembler
assembler = Assembler(assmbler_settings)
r_run = assembler.run()
if r_run.is_err:
    panic("failed to run assembler", r_run.unwrap_err(), error_code=EC_ASSEMBLER_FAILURE)

# Create the CPU
r_cpu_settings = (CPUSettings()
    .set_instruction_memory_size(64)
    .set_data_memory_size(64)
    .set_video_memory_size(64)
    .set_stack_memory_size(64)
    .pack()
)

if r_cpu_settings.is_err: panic("invalid cpu settings", r_cpu_settings.unwrap_err())
cpu_settings = r_cpu_settings.unwrap()
cpu = VonNeumannCPU(cpu_settings)

# Load the assembler's program into the CPU
r_load = cpu.load_program(assembler.instructions, assembler.file_name)
if r_load.is_err: panic("failed to load program", r_load.unwrap_err())

def press(key) -> bool:
    """Runs one clock cycle if the space bar is pressed.
    Runs many clock cycles if the space bar is held.
    """

    if key == Key.space:
        
        # Clear the screen
        print("\033c", end="")
        
        # Run one clock cycle of the CPU
        clock = cpu.clock()
        
        # Print the CPU state
        print(cpu)
         
        return clock #?
    else:
        return False 

def main():

    # cpu.run()
    # print(cpu)

    info("Press space to execute one clock cycle")
    print(cpu) 
    l = Listener(on_press=press)
    l.start()
    l.join()

    print(red_bold("CPU halted"))

if __name__ == "__main__":
    main()