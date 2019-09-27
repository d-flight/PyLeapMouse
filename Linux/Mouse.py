from pymouse import PyMouse

mouse = PyMouse()


def AbsoluteMouseMove(posx, posy):
    mouse.move(int(posx), int(posy))


def AbsoluteMouseClickDown(posx, posy):
    mouse.press(posx, posy)


def AbsoluteMouseClickUp(posx, posy):
    mouse.release(posx, posy)


def AbsoluteMouseDrag(posx, posy):  # Only relevant in OS X(?)
    mouse.move(posx, posy)


def AbsoluteMouseScroll(posx, posy, up=True):  # PyUserInput doesn't appear to support relative scrolling
    mouse.click(posx, posy, button=(4 if up else 5))


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
        posx = self.x
        posy = self.y
        up = y_movement < 0
        AbsoluteMouseScroll(posx, posy, up)
