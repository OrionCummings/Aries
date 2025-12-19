add_executable(AriesCompiler
    main.c
    args.c
)

target_link_libraries(AriesCompiler PUBLIC
    debug_lib
    arena_lib
    str_lib
    lexer_lib
    parser_lib
)

target_compile_options(AriesCompiler PRIVATE
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
