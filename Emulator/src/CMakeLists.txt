add_executable(AriesEmulator
    main.c
    alu.c
    control_unit.c
    cpu.c
    decoder.c
    instruction.c
    register_file.c
)

# target_link_libraries(AriesEmulator PUBLIC
#     debug_lib
#     arena_lib
#     str_lib
# )

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
