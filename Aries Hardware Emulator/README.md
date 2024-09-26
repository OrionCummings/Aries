# Aires Hardware Emulator



# Simple
The Simple Aries ISA (SAISA) is a tiny instruction set inspired by The University of Washington - Seattle CSE 378 page found [here](https://courses.cs.washington.edu/courses/cse378/02sp/slides/simple-isa.html). SAISA is a gentle introduction into ISA design. It has no registers and a fixed amount of memory, typically 65535 bytes. 

SAISA contains six instructions:

Opcode | Instruction | Meaning
--- |--- | ---
0x00 | ADD A, B, C | MEM[C] = MEM[A] + MEM[B]
0x01 | SUB A, B, C | MEM[C] = MEM[A] - MEM[B]
0x02 | MOVE A, B | MEM[B] = MEM[A]
0x03 | LOAD VALUE, A | VALUE = MEM[A]
0x04 | BNE A, B, LOCATION | If A != B, then PC = LOCATION
0x05 | EXIT | Exits the program

### Instruction Examples:
Instruction | Machine Code
--- |--- 
**ADD**,    0,  **1**,    2 | **00 00** 00 00 **00 01** 00 02
**SUB**,    2, **10**,   12 | **00 01** 00 02 **00 0A** 00 0C
**MOVE**,   5, **40**       | **00 02** 00 05 00 28 **?? ??**
**LOAD**, 255,  **4**       | **00 03** 00 FF 00 04 **?? ??**
**BNE**,    4,  **9**, 4095 | **00 04** 00 04 **00 09** 0F FF
**EXIT**    4               | **00 05** 00 04 **?? ??** ?? ??

# Basic


# Full

