#ifndef TIMER_H
#define TIMER_H

#include <stdint.h>
#include <time.h>
#include <stdbool.h>

typedef struct {
    uint64_t start;
    uint64_t end;
} timer_t;

timer_t timer_new(time_t duration);
void timer_start(timer_t* timer);
void timer_wait(timer_t* timer, time_t duration);
void timer_reset(timer_t* timer);
bool timer_is_active(timer_t* timer);
bool timer_is_expired(timer_t* timer);

#endif