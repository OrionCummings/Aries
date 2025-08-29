add_executable(ACompiler
    main.c
    debug.c
)

target_include_directories(ACompiler PRIVATE "../inc")

target_compile_options(ACompiler PRIVATE
    -pedantic 
    -Wall 
    -Wextra 
    -Werror  
    -Wconversion 
    -Wundef 
    -Wno-unused-parameter
    -Wno-unused-variable
    -Wno-type-limits
    -g
)
