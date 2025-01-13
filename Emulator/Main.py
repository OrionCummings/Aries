from functools import partial
from pynput.keyboard import Key, Listener
from CPU import CPU
from Assembler import Assembler, AssemblerSettings, PrintMode
from PrettyPrinting import error, info, print_red, red_bold

# Create assembler settings 
settings = AssemblerSettings()
settings.print_mode = PrintMode.Hex
settings.file_name = "label.aria"

# Create the assembler
assembler = Assembler(settings)
r_run = assembler.run()
if r_run.is_err:
    print(r_run.unwrap_err())
    exit(2)
 
# Create the CPU
cpu = CPU(instruction_memory_size_in_bytes=64, data_memory_size_in_bytes=64)

# Load the assembler's program into the CPU
r_load = cpu.load_program(assembler.instructions, assembler.file_name, 0)
if r_load.is_err:
    error(r_load.unwrap_err())
    exit(3)

def press(key) -> bool:
    """Runs one clock cycle if the space bar is pressed.
    Runs many clock cycles if the space bar is held.
    """

    if key == Key.space:
        
        # Clear the screen
        # print("\033c", end="")
        
        # Run one clock cycle of the CPU
        clock = cpu.clock()
        
        # Print the CPU state
        print(cpu)
         
        return clock #?
    else:
        return False 

def main():

    info("Press space to execute one clock cycle")
    print(cpu) 
    l = Listener(on_press=press)
    l.start()
    l.join()

    print(red_bold("CPU halted"))

if __name__ == "__main__":
    main()