#include "debug.h"

LogLevel current_log_level = LOG_ALL;
LogLevel previous_log_level = LOG_ALL;

void __error(const char* message, const char* file, const char* func, const uint64_t line, ...) {
#ifdef __ENABLE_ERROR

    if (current_log_level < LOG_ERROR) return;

    va_list args;
    va_start(args, line);

    char buffer[__DEBUG_MESSAGE_BUFFER_SIZE] = { 0 };
    int res = snprintf(buffer, __DEBUG_MESSAGE_BUFFER_SIZE, "[ERROR] %s:%s():%" PRIu64 ": \"%s\"\n", file, func, line, message);
    if (res > __DEBUG_MESSAGE_BUFFER_SIZE) {
        printf("META: The following error message was longer than %d characters and has been truncated.\n", __DEBUG_MESSAGE_BUFFER_SIZE);
    } else if (res == -1) {
        printf("META: The following error message contains an encoding error.\n");
    }
    vprintf(buffer, args);

    va_end(args);

#endif
}

void __warning(const char* message, const char* file, const char* func, const uint64_t line, ...) {
#ifdef __ENABLE_WARNING

    if (current_log_level < LOG_WARNING) return;

    va_list args;
    va_start(args, line);

    char buffer[__DEBUG_MESSAGE_BUFFER_SIZE] = { 0 };
    int res = snprintf(buffer, __DEBUG_MESSAGE_BUFFER_SIZE, "[WARNING] %s:%s():%" PRIu64 ": \"%s\"\n", file, func, line, message);
    if (res > __DEBUG_MESSAGE_BUFFER_SIZE) {
        printf("META: The following warning message was longer than %d characters and has been truncated.\n", __DEBUG_MESSAGE_BUFFER_SIZE);
    } else if (res == -1) {
        printf("META: The following warning message contains an encoding error.\n");
    }
    vprintf(buffer, args);

    va_end(args);
#endif
}

void __info(const char* message, const char* file, const char* func, const uint64_t line, ...) {
#ifdef __ENABLE_INFO

    if (current_log_level < LOG_INFO) return;

    va_list args;
    va_start(args, line);

    char buffer[__DEBUG_MESSAGE_BUFFER_SIZE] = { 0 };
    int res = snprintf(buffer, __DEBUG_MESSAGE_BUFFER_SIZE, "[INFO] %s:%s():%" PRIu64 ": \"%s\"\n", file, func, line, message);
    if (res > __DEBUG_MESSAGE_BUFFER_SIZE) {
        printf("META: The following info message was longer than %d characters and has been truncated.\n", __DEBUG_MESSAGE_BUFFER_SIZE);
    } else if (res == -1) {
        printf("META: The following info message contains an encoding error.\n");
    }
    vprintf(buffer, args);

    va_end(args);
#endif
}

void __trace(const char* file, const char* func, const uint64_t line) {
#ifdef __ENABLE_TRACE

    if (current_log_level < LOG_TRACE) return;

    char buffer[__DEBUG_MESSAGE_BUFFER_SIZE] = { 0 };
    int res = snprintf(buffer, __DEBUG_MESSAGE_BUFFER_SIZE, "[TRACE] %s:%s():%" PRIu64 "\n", file, func, line);
    if (res > __DEBUG_MESSAGE_BUFFER_SIZE) {
        printf("META: The following error message was longer than %d characters and has been truncated.\n", __DEBUG_MESSAGE_BUFFER_SIZE);
    } else if (res == -1) {
        printf("META: The following error message contains an encoding error.\n");
    }

    printf("%s", buffer);

#endif
}

void print_byte(uint8_t byte) {

}

void print_bytes(uint8_t* bytes, size_t n) {

}

void print_word(uint16_t hword) {

}

void print_words(uint16_t* hwords, size_t n) {

}

void print_dword(uint32_t word) {

}

void print_dwords(uint32_t* words, size_t n) {

}

void print_qword(uint64_t dword) {

}

void print_qwords(uint64_t* dwords, size_t n) {

}


