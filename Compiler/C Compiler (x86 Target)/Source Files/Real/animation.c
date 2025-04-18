#include "animation.h"

Animation new_animation(void* easing_function) {
	return (Animation) { .state = INACTIVE, .ticks = 0, .time = 0.0, .easing_function = easing_function };
}

void start_animation(Animation* animation, AnimationDirection dir) {
	animation->state = ACTIVE;
	animation->ticks = (dir) ? ANIMATION_TICKS : 0;
	animation->time = (dir) ? 1.0 : 0.0;
}

void step_animation(Animation* animation, AnimationDirection dir) {

	if (animation == NULL) {
		ERROR("Passed null animation");
		return;
	}

	if (animation->easing_function == NULL) {
		ERROR("Passed null easing function");
		return;
	}

	if (animation->state == ACTIVE) {
		switch (dir) {
		case(FORWARD): {
			if ((animation->ticks)++ < ANIMATION_TICKS) {
				animation->time = animation->easing_function((double)animation->ticks / ANIMATION_TICKS);
			}
			else {
				animation->state = INACTIVE;
				animation->time = 1.0;
				animation->ticks = ANIMATION_TICKS;
			}
			break;
		}
		case(BACKWARD): {
			if ((animation->ticks)-- > 0) {
				animation->time = animation->easing_function((double)animation->ticks / ANIMATION_TICKS);
			}
			else {
				animation->state = INACTIVE;
				animation->time = 0.0;
				animation->ticks = 0;
			}
			break;
		}
		}
	}
}

void set_easing_function(Animation* animation, void* easing_function) {
	if (easing_function == NULL) {
		ERROR("Null easing function");
		return;
	}

	animation->easing_function = easing_function;
}

void print_animation(const Animation animation) {
	printf("[ANIMATION] %s: %.4f (%lu/%lu)\n", animation_state_names[animation.state], animation.time, animation.ticks, ANIMATION_TICKS);
}