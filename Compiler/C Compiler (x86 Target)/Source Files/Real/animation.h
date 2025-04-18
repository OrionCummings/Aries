#pragma once

#include <math.h>
#include "debug.h"

#define ANIMATION_TICKS 25

typedef enum AnimationDirection {
	FORWARD = 0,
	BACKWARD = 1,
} AnimationDirection;

static const char* animation_state_names[] = { "Inactive", "Active", "Done" };

typedef enum AnimationState{
	INACTIVE,
	ACTIVE,
	DONE
} AnimationState;

typedef struct Animation {
	AnimationState state;
	uint32_t ticks;
	double time;
	double (*easing_function)(double t);
} Animation;

Animation new_animation(void* easing_function);
void set_easing_function(Animation* animation, void* easing_function);
void start_animation(Animation* animation, AnimationDirection dir);
void step_animation(Animation* animation, AnimationDirection dir);
void print_animation(const Animation animation);

// Easing functions (EFs) are (generally) bijective in [0, 1] and undefined elsewhere.
// Most EFs have a codomain of [0, 1], but this is not a hard requirement!
inline double easing_linear(double t) {
	return t;
}

inline double easing_in_out_cubic(double t) {
	return (t < 0.5) ? (4 * t * t * t) : 1 - (((-2 * t + 2) * (-2 * t + 2) * (-2 * t + 2)) / 2);
}

inline double easing_out_back(double t) {

	const double c1 = 1.70158;
	const double c3 = c1 + 1;

	return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2);
}