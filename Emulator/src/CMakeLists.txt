add_executable(AriesEmulator
    main.c
    cpu.c
    alu.c
    memory.c
    instruction.c
    register_file.c
    user_input.c
    backplane.c
)

target_link_libraries(AriesEmulator PUBLIC
    debug_lib
    # arena_lib
    # str_lib
)

target_compile_options(AriesEmulator PRIVATE
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
