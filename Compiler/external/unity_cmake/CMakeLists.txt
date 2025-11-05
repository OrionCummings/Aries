add_library(unity_lib STATIC
    Unity/src/unity.c
)

target_include_directories(unity_lib PUBLIC
    Unity/src
)