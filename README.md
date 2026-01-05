# ♈ The Aries Project

The Aires Project aims to make complex topics in computer science, electrical & computer engineering, and systems engineering more accessible by exposing every aspect of a modern computing ecosystem. My hope is that anyone seeking to learn more about complex topics in these fields can learn from this project and create their own new and beautiful projects.

I understand that this effort is enormous. I do not expect this project to *ever* be 'finished'. Frankly, my goal is not to finish this project: it's to help myself and others understand technical topics that I find facinating. If you are looking to contribute to the project, start looking around for improvements to further this educational goal!

## Scope

The Aries Project encompasses four components: the Aries Programming Language (APL), the Aries Assembly Language (AAL), the Aries Hardware Emulator (AHE), and the Aries Hardware Package (AHP). All four components aim to be non-trivial explorations into the domains of programming language development and theory, electrical and computer engineering, embedded software development and testing, and systems engineering.

#### The Aries Programming Language (APL)

The Aires Programming Language (APL) is a statically typed, imperative programming language designed to compile down to the Aries Assembly Language (AAL). APL shares many similarities to C with some syntax changes and semantic simplifications. More information about APL can be found here.

---
#### The Aries Assembly Language (AAL)

The Aires Assembly Language (AAL) is an assembly language designed to target the Aires Hardware Package (AHP) and the Aires Hardware Emulator (AHE). AAL has a small number of instructions to ease understanding and usage. More information about AAL can be found here.

---
#### The Aries Hardware Emulator (AHE)

The Aires Hardware Emulator (AHE) is an application written in Python 3 to emulate the inner workings of the Aires Hardware Package (AHP). The AHE is designed to allow one to view the AHP as it is running. The AHE is also designed to support AHP development and AAL testing. More information about AHE can be found here.

---
#### The Aries Hardware Package (AHP)

The Aires Hardward Package (AHP) is a 32-bit central processing unit. More information about AHP can be found here.

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

