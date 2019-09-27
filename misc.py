# Smooths the mouse's position
class MousePositionSmoother(object):
    def __init__(self, smooth_aggressiveness, smooth_falloff):
        # Input validation
        if smooth_aggressiveness < 1:
            raise Exception("Smooth aggressiveness must be greater than 1.")
        if smooth_falloff < 1:
            raise Exception("Smooth falloff must be greater than 1.0.")
        self.previous_positions = []
        self.smooth_falloff = smooth_falloff
        self.smooth_aggressiveness = int(smooth_aggressiveness)

    def update(self, (x, y)):
        self.previous_positions.append((x, y))
        if len(self.previous_positions) > self.smooth_aggressiveness:
            del self.previous_positions[0]
        return self.get_current_smooth_value()

    def get_current_smooth_value(self):
        smooth_x = 0
        smooth_y = 0
        total_weight = 0
        num_positions = len(self.previous_positions)
        for position in range(0, num_positions):
            weight = 1 / (self.smooth_falloff ** (num_positions - position))
            total_weight += weight
            smooth_x += self.previous_positions[position][0] * weight
            smooth_y += self.previous_positions[position][1] * weight
        smooth_x /= total_weight
        smooth_y /= total_weight
        return smooth_x, smooth_y


class Debouncer(object):  # Takes a binary "signal" and debounces it.
    def __init__(self, debounce_time):  # Takes as an argument the number of opposite samples it needs to debounce.
        self.opposite_counter = 0  # Number of contrary samples vs agreeing samples.
        self.state = False  # Default state.
        self.debounce_time = debounce_time  # Number of samples to change states (debouncing threshold).

    def signal(self, value):  # Update the signal.
        if value != self.state:  # We are receiving a different signal than what we have been.
            self.opposite_counter = self.opposite_counter + 1
        else:  # We are recieving the same signal that we have been
            self.opposite_counter = self.opposite_counter - 1

        if self.opposite_counter < 0: self.opposite_counter = 0
        if self.opposite_counter > self.debounce_time: self.opposite_counter = self.debounce_time
        # No sense building up negative or huge numbers of agreeing/contrary samples

        if self.opposite_counter >= self.debounce_time:  # We have seen a lot of evidence that our internal state is wrong
            self.state = not self.state  # Change internal state
            self.opposite_counter = 0  # We reset the number of contrary samples
        return self.state  # Return the debounced signal (may help keep code cleaner)


class Resolution:
    def __init__(self, width, height):
        self.width = width
        self.height = height