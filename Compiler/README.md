# The Aries Compiler

The Aries Compiler (AC) compiles the Aries Programming Language (APL) into the Aries Assembly Language (AAL). 


AC is organized into several stages:

### Preprocessing
*The AC does not currently support preprocessing as I have not fully assessed if it is necessary.*

### Lexing
The input source file (.ari) is split into `Symbols`. These are placed into a `SymbolList` and passed to the next stage.

### Parsing
The input `SymbolList` is parsed based on a context free grammar into a parse tree.

### Generating



# External Libraries

### Unity
The [Unity Test Project](https://github.com/ThrowTheSwitch/Unity) is used to write tests for the AC and any related libraries.

