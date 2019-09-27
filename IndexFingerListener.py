from impl import Leap
from misc import MousePositionSmoother, Debouncer


class IndexFingerListener(
    Leap.Listener
):
    def __init__(self, mouse, resolution, smooth_aggressiveness=8, smooth_falloff=1.3):
        super(IndexFingerListener, self).__init__()
        self.resolution = resolution
        self.cursor = mouse.AbsoluteCursor(resolution)
        self.smoother = MousePositionSmoother(
            smooth_aggressiveness,
            smooth_falloff
        )  # Keeps the cursor from fidgeting
        self.debouncer = Debouncer(5)  # A signal debouncer that ensures a reliable, non-jumpy click

    def on_init(self, arg0):
        print "Initialized"

    def on_connect(self, arg0):
        print "Connected"

    def on_disconnect(self, arg0):
        print "Disconnected"

    def on_exit(self, arg0):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()
        hands = frame.hands

        # we need at least one hand
        if hands.is_empty: return
        fingers = hands[0].fingers

        # we need at least one finger
        if fingers.is_empty: return
        index_finger = fingers.finger_type(Leap.Finger.TYPE_INDEX)[0]

        # if the index finger is not in the touch zone, exit
        if index_finger.touch_zone <= 0: return
        thumb = fingers.finger_type(Leap.Finger.TYPE_THUMB)[0]

        if self.angle_within(index_finger.direction, Leap.Vector.forward, 0.9):
            stabilized_position = index_finger.stabilized_tip_position
            interaction_box = frame.interaction_box
            normalized_position = interaction_box.normalize_point(stabilized_position)

            self.move(normalized_position)

        # when the thumb is aligned with the index finger,
        # we click the left mouse button.
        # otherwise, we release it
        self.debouncer.signal(
            self.distance_within(thumb.direction, index_finger.direction, .6)
        )

        # self.debug_angle(thumb, index_finger, self.debouncer.state)

        if self.cursor.left_button_pressed != self.debouncer.state:
            self.cursor.set_left_button_pressed(self.debouncer.state)

    # @staticmethod
    # def debug_angle(finger1, finger2, click):
    #     print "angle: %s, distance: %s, active: %s" % (
    #         finger1.direction.angle_to(finger2.direction),
    #         finger1.direction.distance_to(finger2.direction),
    #         "yes" if click else "no"
    #     )

    def move(self, position):
        # print "moving to: %s, %s" % (position.x, position.y)
        x, y = self.smoother.update((position.x, position.y))

        self.cursor.move(
            x * self.resolution.width,
            self.resolution.height - y * self.resolution.height,
        )

    @staticmethod
    def angle_within(vector1, vector2, angle):
        return angle > vector1.angle_to(vector2)

    @staticmethod
    def distance_within(vector1, vector2, distance):
        return distance > vector1.distance_to(vector2)