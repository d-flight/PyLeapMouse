"""
    Daniel Leicht

    based on
    William Yagers
    Leap Python mouse controller POC
"""


import sys

from misc import Resolution
from impl import Leap, Mouse
import IndexFingerListener


def show_help():
    print "----------------------------------PyLeapMouse----------------------------------"
    print "Set the resolution of the screen with --width and --height.\n"
    print "Set smooth aggressiveness with \"--smooth-aggressiveness\""
    print "Set smooth falloff with \"--smooth-falloff [% per sample]\""
    print "Read README.md for even more info.\n"


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        show_help()
        return

    print "----------------------------------PyLeapMouse----------------------------------"
    print "Set the resolution of the screen with --width and --height."
    print "Use -h or --help for more info.\n"

    # Default
    smooth_aggressiveness = 8
    smooth_falloff = 1.3
    width = None
    height = None

    for i in range(0, len(sys.argv)):
        arg = sys.argv[i].lower()
        if "--smooth-falloff" in arg:
            smooth_falloff = float(sys.argv[i + 1])
        if "--smooth-aggressiveness" in arg:
            smooth_aggressiveness = int(sys.argv[i + 1])
        if "--width" in arg:
            width = int(sys.argv[i + 1])
        if "--height" in arg:
            height = int(sys.argv[i + 1])

    if width is None or height is None:
        print "--width and --height are required."
        exit(1)

    resolution = Resolution(width, height)

    print "Running on %sx%s. \n" % (resolution.width, resolution.height)

    listener = IndexFingerListener.IndexFingerListener(
        Mouse,
        resolution,
        smooth_aggressiveness,
        smooth_falloff
    )

    controller = Leap.Controller()  # Get a Leap controller
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    controller.add_listener(listener)  # Attach the listener

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()
    # Remove the listener when done
    controller.remove_listener(listener)

main()
