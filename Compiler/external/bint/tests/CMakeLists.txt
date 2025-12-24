add_executable(bint_test
    ../bint.c
    
    test_bint.c

    test_bint_obj.c

    test_bint_add.c
    test_bint_sub.c
    test_bint_mul.c
    test_bint_div.c
    test_bint_mod.c

    test_bint_not.c
    test_bint_and.c
    test_bint_nand.c
    test_bint_or.c
    test_bint_nor.c
    test_bint_xor.c
    test_bint_xnor.c
    test_bint_shl.c
    test_bint_shr.c
    test_bint_rotl.c
    test_bint_rotr.c

    test_bint_pow.c
    test_bint_sqrt.c
    test_bint_log.c
    test_bint_exp.c
)

target_include_directories(bint_test PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
    ${CMAKE_CURRENT_LIST_DIR}/..
)

target_link_libraries(bint_test
    unity_lib
    arena_lib
    debug_lib
    str_lib
)

target_compile_options(bint_test PRIVATE
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
