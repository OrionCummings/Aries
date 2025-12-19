add_library(list_lib STATIC
    list.c
)

target_link_libraries(list_lib PUBLIC
    debug_lib
)

target_include_directories(list_lib PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
)