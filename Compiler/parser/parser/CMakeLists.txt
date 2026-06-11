add_library(parser_lib STATIC parser.c types.c regex.c)
target_link_libraries(parser_lib lexer_lib str_lib)
target_include_directories(parser_lib PUBLIC ${CMAKE_CURRENT_LIST_DIR})

target_compile_options(parser_lib PRIVATE
    -O0
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

add_subdirectory(tests)