from functools import partial
from pynput.keyboard import Key, Listener
from CPU import CPU, CPUArchitecture, CPUSettings
from Assembler import Assembler, AssemblerSettings, AssemblerSettingsSource, PrintMode
from PrettyPrinting import error, info, red_bold
from Utilities import debug, panic

# Create assembler settings 
assmbler_settings = AssemblerSettings()
assmbler_settings.print_mode = PrintMode.Hex
assmbler_settings.source = AssemblerSettingsSource.File
assmbler_settings.file_name = "example.aria"
assmbler_settings.file_directory = "Programs"

# Create the assembler
assembler = Assembler(assmbler_settings)
r_run = assembler.run()
if r_run.is_err:
    print(r_run.unwrap_err())
    exit(2)

# Create the CPU
cpu_settings = CPUSettings()
cpu_settings.architecture = CPUArchitecture.Harvard
cpu_settings.data_memory_information = (16, 0)
cpu_settings.instruction_memory_information = (32, 0)
cpu_settings.video_memory_information = (16, 0)
cpu_settings.stack_information = (16, 0)
r_memory_size_in_bytes = cpu_settings.calculate_memory_size()

if r_memory_size_in_bytes.is_err:
    panic(f"{debug()}: failed to calculate total memory size\n{r_memory_size_in_bytes.unwrap_err()}")
cpu_settings.memory_size_in_bytes = r_memory_size_in_bytes.unwrap()

cpu = CPU(cpu_settings)

# Load the assembler's program into the CPU
r_load = cpu.load_program(assembler.instructions, assembler.file_name, 0)
if r_load.is_err:
    panic(f"{debug()}: failed to load program\n{r_load.unwrap_err()}")

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