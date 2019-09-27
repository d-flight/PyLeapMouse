# PyLeapMouse
This project is based on code from wyager's Proof-of-concept code for a Leap Motion-based mouse controller, which can be found here: [github.com/openleap/pyleapmouse]()

## Important Notice
The `Leap`-Libraries in the OS-specific directories are copies from the current version `2.3.1+31549`. If you want to use a different version of the libraries, just copy the respective files to the target directory.

## Supported Operating Systems
Due to the lack of windows machines in the ant dev office, supported systems are
+ macOS (developed on Catalina Beta)
+ Linux

Windows support can be easily added, just copy the dependencies to `/Windows`, add a new switch in `leap.py` and implement a `Mouse` class with the required methods you can find in the implementation for the other OSes

## Install Dependencies
First, create a new virtual Python environment using python 2 and activate it.

Depending on your OS, install with pip:
+ macOS: `pip install -r ./MacOS/requirements.txt`
+ Linux: `pip install -r ./Linux/requirements.txt`

## Run it
+ Connect Leap, start Leap Software
+ Make sure background apps are permitted in Leap Settings
+ Install Dependencies, see the respective section for more info
+ Run the command with the current screen resolution:
> python ./PyLeapMouse.py --width [screen width] --height [screen height]

To get more information about which options are available check out the _Advanced Options_ section, or just run
> python ./PyLeapMouse.py --help

## Control the mouse with Leap
+ To move the cursor, point forward with your index finger and move your hand
+ To click / drag, move the thumb close to your palm. To release / drop, move it away

## Advanced Options
+ `--smooth-aggressiveness [value]` sets the number of samples to use for pointer finger mouse smoothing.
+ `--smooth-falloff [value]` sets the rate at which previous samples lose importance.

For every sample back in time, the previous location of the mouse is weighted with weight smooth_falloff^(-#sample).
So if smooth_falloff = 1.2, the current frame has weight 1/(1.2^0)=1, but the frame from 5 frames ago has weight 1/(1.2^5) = .4
By default, the smooth aggressiveness is 8 frames with a falloff of 1.3.
