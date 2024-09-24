# ♈ The Aries Project

The Aries Project encompasses four components: the Aries Programming Language, the Aries Assembly Language, the Aries Hardware Emulator, and the Aries Computer. All four components aim to be non-trivial explorations into the domains of programming language development and theory, electrical and computer engineering, and embedded software development and testing.

## Active Development
- :fire: Aries Programming Language
    - Aries Visual Studio Code Extension
        - :white_check_mark: Syntax highlighting
        - Improved user interface
            - :ice_cube: Run button
            - :ice_cube: Examples
    - Aries Compiler
        - :white_check_mark: Tokenization/Lexer
        - :fire: Parser
        - :ice_cube: Generator
            - :ice_cube: AAL support
            - :ice_cube: x86-64 support
            - :ice_cube: :ice_cube: :ice_cube: RISC V support

- :fire: Aries Assembly Language
    - :fire: Defining the Aires Instruction Set Architecture
        - :fire: Simple Aries Instruction Set Architecture
            - :fire: Parser
            - :fire: Assembler
        - :ice_cube: Basic Aries Instruction Set Architecture
        - :ice_cube: Full Aries Instruction Set Architecture

- :fire: Aries Hardware Emulator
    - :fire: Implements AISA instructions in Python test environment
        - :fire: Implements Simple AISA instructions in Python test environment
        - :ice_cube: Implements Basic AISA instructions in Python test environment
        - :ice_cube: Implements Full AISA instructions in Python test environment
    - :ice_cube: Connect Aries Compiler output to AHE input

## Planned Development

- :ice_cube: Aries Hardware Design Package

---

## The Aries Programming Language (APL)


---
## The Aries Assembly Language (AAL)


---
## The Aries Hardware Emulator (AHE)


---
## The Aries Computer (AC)
* 16-bit architecture
* Little endian
* Variable clock speed [1 - 10k Hz]
* 13 16-bit registers
    - 9 general purpose 16-bit Registers
        + 4 8-bit High/Low Split Registers
        + 4 16-bit registers
        + 1 bit-addressable register
    - 1 8-bit flag register
    - 16-bit stack pointer
    - 16-bit base pointer
    - 16-bit instruction pointer
* 9 flags (one 8-bit register)
    - ZF: Zero 
    - CF: Carry
    - PF: Parity
    - SF: Sign
    - OF: Overflow
    - IF: Interrupt
    - IDF: Interrupt disable
    - TF: Trap
    - HF: HPC
* 4-bit memory alignment
* 16-bit floating point number support

Here is the first draft of the real memory map:
<img src="https://github.com/OrionCummings/Aries/blob/main/Resources/GitHub/memory-map.PNG?raw=true" alt="The memory layout of the Aries CPU" width="300"/>