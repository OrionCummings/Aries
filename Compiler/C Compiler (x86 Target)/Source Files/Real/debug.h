#pragma once
#ifndef __DEBUG_H
#define __DEBUG_H

#define __STDC_FORMAT_MACROS
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>

#define __ENABLE_INFO
#define __ENABLE_ERROR
#define __ENABLE_BREAKPOINT

#define MESSAGE_BUFFER_SIZE 512

#define INFO(X, ...) \
	 __info__(X, __func__, __LINE__, __VA_ARGS__)

#define ERROR(X, ...) \
	__error__(X, __func__, __LINE__, __VA_ARGS__)

#define BKP(X, ...) \
	__breakpoint__(X, __func__, __LINE__, __VA_ARGS__)

#define TODO() \
	__todo__(__func__, __LINE__)

inline void __error__(const char* message, const char* func, const uint64_t line, ...) {
#if defined __ENABLE_ERROR
	va_list args;
	va_start(args, line);

	char buffer[MESSAGE_BUFFER_SIZE] = { 0 };
	int res = snprintf(buffer, MESSAGE_BUFFER_SIZE, "[ERROR] In function '%s' on line %" PRIu64 ": \"%s\"\n", func, line, message);
	if (res > MESSAGE_BUFFER_SIZE) {
		printf("[META] The following error message was longer than %d characters and has been truncated.\n", MESSAGE_BUFFER_SIZE);
	}
	else if (res == -1) {
		printf("[META] The following error message contains an encoding error.\n");
	}
	vprintf(buffer, args);

	va_end(args);

#endif
	exit(EXIT_FAILURE);
}

inline void __info__(const char* message, const char* func, const uint64_t line, ...) {
#if defined __ENABLE_INFO
	va_list args;
	va_start(args, line);

	char buffer[MESSAGE_BUFFER_SIZE] = { 0 };
	int res = snprintf(buffer, MESSAGE_BUFFER_SIZE, "[INFO] In function '%s' on line %" PRIu64 ": \"%s\"\n", func, line, message);
	if (res > MESSAGE_BUFFER_SIZE) {
		printf("[META] The following info message was longer than %d characters and has been truncated.\n", MESSAGE_BUFFER_SIZE);
	}
	else if (res == -1) {
		printf("[META] The following info message contains an encoding error.\n");
	}
	vprintf(buffer, args);

	va_end(args);
#endif
}

inline void __breakpoint__(const char* message, const char* func, const uint64_t line, ...) {
#if defined __ENABLE_BREAKPOINT
	va_list args;
	va_start(args, line);

	char buffer[MESSAGE_BUFFER_SIZE] = { 0 };
	int res = snprintf(buffer, MESSAGE_BUFFER_SIZE, "[BREAKPOINT] In function '%s' on line %" PRIu64 ": \"%s\"\n", func, line, message);
	if (res > MESSAGE_BUFFER_SIZE) {
		printf("[META] The following error message was longer than %d characters and has been truncated.\n", MESSAGE_BUFFER_SIZE);
	}
	else if (res == -1) {
		printf("[META] The following error message contains an encoding error.\n");
	}
	vprintf(buffer, args);

	va_end(args);

#endif
	exit(EXIT_FAILURE);
}

inline void __todo__(const char* func, const uint64_t line) {
	char buffer[MESSAGE_BUFFER_SIZE] = { 0 };
	int res = snprintf(buffer, MESSAGE_BUFFER_SIZE, "[TODO] Unimplemented features in function '%s' on line %" PRIu64 "\n", func, line);
	if (res > MESSAGE_BUFFER_SIZE) {
		printf("[META] The following info message was longer than %d characters and has been truncated.\n", MESSAGE_BUFFER_SIZE);
	}
	else if (res == -1) {
		printf("[META] The following info message contains an encoding error.\n");
	}

	printf("%s", buffer);

	exit(EXIT_FAILURE);
}

#endif