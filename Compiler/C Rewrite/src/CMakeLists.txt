add_executable(AriesCompiler
    main.c
)

target_link_libraries(AriesCompiler PUBLIC
    utils_lib
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
