add_library(utils_lib STATIC ipow.c)
target_include_directories(utils_lib PUBLIC ${CMAKE_CURRENT_LIST_DIR})