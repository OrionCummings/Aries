add_executable(bfilter_test
    ../bfilter.c
    
    test_bfilter.c
)

target_include_directories(bfilter_test PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
    ${CMAKE_CURRENT_LIST_DIR}/..
)

target_link_libraries(bfilter_test
    unity_lib
    arena_lib
    debug_lib
    hash_lib
)

target_compile_options(bfilter_test PRIVATE
    -Wall
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
