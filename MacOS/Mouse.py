# William Yager
# Leap Python mouse controller POC

# Mouse functions in OS X
from Quartz.CoreGraphics import (
    CGEventCreateMouseEvent,
    CGEventPost,
    CGEventCreateScrollWheelEvent,
    kCGScrollEventUnitPixel,
    kCGEventMouseMoved,
    kCGEventLeftMouseDragged,
    kCGEventLeftMouseDown,
    kCGEventLeftMouseUp,
    kCGHIDEventTap
)

# OS X specific: We use CGEventCreateMouseEvent(source, mouse[Event]Type, mouseCursorPosition, mouseButton)
# to make our events, and we post them with CGEventPost(tapLocation, event).
# We can usually/always set "source" to None (Null) and mouseButton to 0 (as the button is implied in the event type)
Event = CGEventCreateMouseEvent  # Easier to type. Alias "Event()" to "CGEventCreateMouseEvent()"


def Post(event):  # Posts the event. I don't want to type "CGEventPost(kCGHIDEventTap," every time.
    CGEventPost(kCGHIDEventTap, event)


def AbsoluteMouseMove(posx, posy):
    event = Event(None, kCGEventMouseMoved, (posx, posy), 0)
    Post(event)


def AbsoluteMouseClickDown(posx, posy):
    event = Event(None, kCGEventLeftMouseDown, (posx, posy), 0)
    Post(event)


def AbsoluteMouseClickUp(posx, posy):
    event = Event(None, kCGEventLeftMouseUp, (posx, posy), 0)
    Post(event)


def AbsoluteMouseDrag(posx, posy):  # A Drag is a Move where the mouse key is held down
    event = Event(None, kCGEventLeftMouseDragged, (posx, posy), 0)
    Post(event)


def RelativeMouseScroll(x_movement, y_movement):  # Movements should be no larger than +- 10
    scrollWheelEvent = CGEventCreateScrollWheelEvent(
        None,  # No source
        kCGScrollEventUnitPixel,  # We are using pixel units
        2,  # Number of wheels(dimensions)
        y_movement,
        x_movement)
    CGEventPost(kCGHIDEventTap, scrollWheelEvent)


# A cursor that does commands based on absolute position (good for finger pointing)
class AbsoluteCursor(object):
    def __init__(self, resolution):
        self.x_max = resolution.width - 1
        self.y_max = resolution.height - 1
        self.left_button_pressed = False
        self.x = 0
        self.y = 0

    def move(self, posx, posy):  # Move to coordinates
        self.x = posx
        self.y = posy
        if self.x > self.x_max:
            self.x = self.x_max
        if self.y > self.y_max:
            self.y = self.y_max
        if self.x < 0.0:
            self.x = 0.0
        if self.y < 0.0:
            self.y = 0.0
        if self.left_button_pressed:  # We are dragging
            AbsoluteMouseDrag(self.x, self.y)
        else:  # We are not dragging
            AbsoluteMouseMove(self.x, self.y)

    def set_left_button_pressed(self, boolean_button):  # Set the state of the left button
        if boolean_button:  # Pressed
            self.click_down()
        else:  # Not pressed
            self.click_up()

    def click_down(self, posx=None, posy=None):
        if posx is None:
            posx = self.x
        if posy is None:
            posy = self.y
        AbsoluteMouseClickDown(posx, posy)
        self.left_button_pressed = True

    def click_up(self, posx=None, posy=None):
        if posx is None:
            posx = self.x
        if posy is None:
            posy = self.y
        AbsoluteMouseClickUp(posx, posy)
        self.left_button_pressed = False

    def scroll(self, x_movement, y_movement):
        RelativeMouseScroll(x_movement, y_movement)