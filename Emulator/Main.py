from functools import partial
from option import Err, Ok, Result
from pynput.keyboard import Key, Listener
from CPU import CPU, CPUArchitecture, CPUSettings
from HarvardCPU import HarvardCPU
from VonNeumannCPU import VonNeumannCPU
from Assembler import Assembler, AssemblerSettings, AssemblerSettingsSource, PrintMode
from Constants import EC_ASSEMBLER_FAILURE
from PrettyPrinting import info, red_bold
from Utilities import panic, trace

# Create assembler settings 
assmbler_settings = (AssemblerSettings()
    .set_file_name("st")
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
# cpu = HarvardCPU(cpu_settings)

# Load the assembler's program into the CPU
r_load = cpu.load_program(assembler.instructions, assembler.file_name)
if r_load.is_err: panic("failed to load program", r_load.unwrap_err())

def once(key) -> Result[bool, str]:

    if key == Key.space:
        
        # Clear the screen
        print("\033c", end="")
        
        # Run one clock cycle of the CPU
        r_clock = cpu.clock()
        if r_clock.is_err:
            return trace("failed to clock CPU", r_clock.unwrap_err())
        
        clock = r_clock.unwrap()
        
        # Print the CPU state
        print(cpu)
         
        return Ok(clock) #?
    else:
        return Err("non-space key hit")

def main():

    # cpu.run()
    # print(cpu)

    info("Press space to execute one clock cycle")
    print(cpu)

    # Block for user input
    input("")

    while not r_once_cycle.is_err:
        r_once_cycle = once(Key.space)
        one_cycle_err = r_once_cycle.unwrap()
        pass
    
    panic("CPU halted", r_once_cycle.unwrap_err())
    # print(red_bold("CPU halted"))



if __name__ == "__main__":
    main()