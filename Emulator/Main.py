from functools import partial
from pynput.keyboard import Key, Listener
from CPU import CPU
from Assembler import Assembler, AssemblerSettings, PrintMode
from PrettyPrinting import red_bold

# Create assembler settings 
settings = AssemblerSettings()
settings.print_mode = PrintMode.Hex
settings.file_name = "Instructions/bne.aria"

# Create the assembler
assembler = Assembler(settings)

# Create the CPU
cpu = CPU(instruction_memory_size_in_bytes=16, data_memory_size_in_bytes=8)

# Load the assembler's program into the CPU
cpu.load_program(assembler.instructions, assembler.file_name, 0)

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

    print("Press space to execute one clock cycle")
    print(cpu) 
    with Listener(on_press = press) as l: l.join()
    print(red_bold("CPU halted"))

if __name__ == "__main__":
    main()