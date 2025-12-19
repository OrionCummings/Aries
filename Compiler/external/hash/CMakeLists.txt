add_library(hash_lib STATIC
    hash.c
)

target_link_libraries(hash_lib PUBLIC
)

target_include_directories(hash_lib PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
)